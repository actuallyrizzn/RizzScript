import sys
import os
import json
import re
import random
import assemblyai as aai
import openai  # Ensure the OpenAI library is installed

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction,
    QFileDialog, QMessageBox, QInputDialog, QProgressBar, QStatusBar,
    QDialog, QFormLayout, QDialogButtonBox, QLineEdit, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QWidget, QDockWidget, QCheckBox
)

# ----------------------------
# Helper Functions and Config
# ----------------------------

CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config({"assemblyai_api_key": "", "openai_api_key": ""})
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def extract_json(text):
    try:
        return json.loads(text)
    except Exception:
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            json_text = text[start:end+1]
            return json.loads(json_text)
        else:
            raise ValueError("No valid JSON found in text.")

def seconds_to_hhmmss(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

config = load_config()
API_KEY = config.get("assemblyai_api_key", "")
OPENAI_API_KEY = config.get("openai_api_key", "")

aai.settings.api_key = API_KEY  # Use AssemblyAI API key.
# For OpenAI, we'll set openai.api_key when needed.

# ----------------------------
# Settings Dialog
# ----------------------------
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout(self)
        self.assemblyai_edit = QLineEdit(self)
        self.assemblyai_edit.setPlaceholderText("Enter AssemblyAI API key")
        self.assemblyai_edit.setText(config.get("assemblyai_api_key", ""))
        
        self.openai_edit = QLineEdit(self)
        self.openai_edit.setPlaceholderText("Enter OpenAI API key")
        self.openai_edit.setText(config.get("openai_api_key", ""))
        
        layout.addRow("AssemblyAI API Key:", self.assemblyai_edit)
        layout.addRow("OpenAI API Key:", self.openai_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_values(self):
        return self.assemblyai_edit.text().strip(), self.openai_edit.text().strip()

# ----------------------------
# Transcription Thread
# ----------------------------
class TranscriptionThread(QThread):
    # Emits a tuple: (plain transcript text, full transcript object)
    transcription_finished = pyqtSignal(object)
    error_occurred = pyqtSignal(str)

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path

    def run(self):
        try:
            transcriber = aai.Transcriber()
            # Enable speaker diarization.
            config_trans = aai.TranscriptionConfig(
                speaker_labels=True
            )
            transcript = transcriber.transcribe(self.file_path, config=config_trans)
            result_text = ""
            for utterance in transcript.utterances:
                result_text += f"Speaker {utterance.speaker}: {utterance.text}\n"
            self.transcription_finished.emit((result_text, transcript))
        except Exception as e:
            self.error_occurred.emit(str(e))

# ----------------------------
# Mapping Worker (for OpenAI API call)
# ----------------------------
class MappingWorker(QThread):
    mappingReady = pyqtSignal(str)
    errorOccurred = pyqtSignal(str)

    def __init__(self, prompt, parent=None):
        super().__init__(parent)
        self.prompt = prompt

    def run(self):
        try:
            openai.api_key = OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="o1",
                messages=[
                    {"role": "system", "content": "You are an expert in speaker attribution."},
                    {"role": "user", "content": self.prompt},
                ]
            )
            result_text = response.choices[0].message.content.strip()
            self.mappingReady.emit(result_text)
        except Exception as e:
            self.errorOccurred.emit(str(e))

# ----------------------------
# Search & Replace Dialog
# ----------------------------
class SearchReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search and Replace")
        self.setModal(True)
        layout = QFormLayout(self)
        
        self.search_edit = QLineEdit(self)
        self.replace_edit = QLineEdit(self)
        layout.addRow("Search for:", self.search_edit)
        layout.addRow("Replace with:", self.replace_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    @staticmethod
    def getValues(parent=None):
        dialog = SearchReplaceDialog(parent)
        result = dialog.exec_()
        return (dialog.search_edit.text(), dialog.replace_edit.text(), result == QDialog.Accepted)

# ----------------------------
# Speaker Mapping Widget (Side Panel)
# ----------------------------
class SpeakerMappingWidget(QWidget):
    mappingApplied = pyqtSignal(dict)
    autopopulateRequested = pyqtSignal()      # For auto-populating speaker names.
    applyTimestampsRequested = pyqtSignal()   # For toggling timestamps.
    
    def __init__(self, speaker_list, parent=None):
        super().__init__(parent)
        self.speaker_list = speaker_list
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Candidate Names input.
        candidate_layout = QHBoxLayout()
        candidate_label = QLabel("Candidate Names (optional, comma-separated):")
        self.candidate_edit = QLineEdit(self)
        candidate_layout.addWidget(candidate_label)
        candidate_layout.addWidget(self.candidate_edit)
        layout.addLayout(candidate_layout)
        
        # Progress log area for fake chain-of-thought.
        self.progress_log = QTextEdit(self)
        self.progress_log.setReadOnly(True)
        self.progress_log.setFixedHeight(100)
        self.progress_log.setPlaceholderText("Progress log...")
        layout.addWidget(self.progress_log)
        
        # Buttons: Autopopulate and Toggle Timestamps.
        buttons_layout = QHBoxLayout()
        self.autopopulate_button = QPushButton("Attempt to Autopopulate", self)
        self.autopopulate_button.clicked.connect(lambda: self.autopopulateRequested.emit())
        buttons_layout.addWidget(self.autopopulate_button)
        self.apply_timestamps_button = QPushButton("Apply Timestamps", self)
        self.apply_timestamps_button.clicked.connect(lambda: self.applyTimestampsRequested.emit())
        buttons_layout.addWidget(self.apply_timestamps_button)
        layout.addLayout(buttons_layout)
        
        header = QLabel("Map Detected Speakers to Names:")
        layout.addWidget(header)

        self.entries = {}
        for speaker in sorted(self.speaker_list):
            h_layout = QHBoxLayout()
            label = QLabel(speaker)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Enter full name (or just a first name if that's all available)")
            self.entries[speaker] = line_edit
            h_layout.addWidget(label)
            h_layout.addWidget(line_edit)
            layout.addLayout(h_layout)
        
        # "Apply Changes" button.
        self.apply_button = QPushButton("Apply Changes", self)
        self.apply_button.clicked.connect(self.apply_mapping)
        layout.addWidget(self.apply_button)
        layout.addStretch()

    def getCandidateNames(self):
        text = self.candidate_edit.text().strip()
        if text:
            return [name.strip() for name in text.split(",") if name.strip()]
        return []

    def getSpeakers(self):
        return sorted(self.speaker_list)

    def populateFields(self, mapping):
        for speaker, name in mapping.items():
            if speaker in self.entries:
                self.entries[speaker].setText(name)

    def apply_mapping(self):
        mapping = {}
        for speaker, line_edit in self.entries.items():
            new_name = line_edit.text().strip()
            if new_name:
                mapping[speaker] = new_name
        self.mappingApplied.emit(mapping)

    def update_progress_log(self, message):
        self.progress_log.append(message)

    def clear_progress_log(self):
        self.progress_log.clear()

# ----------------------------
# Main Window
# ----------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RizzScript: Voice Studio")
        self.resize(800, 600)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)
        self.word_wrap_enabled = True

        # Set a larger, fixed-width font.
        font = QFont("Consolas", 14)
        self.text_edit.setFont(font)

        self.create_menus()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress)

        self.status_timer = QTimer(self)
        self.status_timer.setSingleShot(True)
        self.status_timer.timeout.connect(self.update_transcribing_status)

        if not API_KEY:
            QMessageBox.critical(self, "Configuration Error", "AssemblyAI API key is missing! Please set it in Settings.")

        self.transcription_thread = None
        self.last_transcript = None    # Full transcript object.
        self.plain_transcript_text = None  # Transcript text without timestamps.
        self.timestamps_applied = False  # Toggle state.
        # Fake progress using QTimer.singleShot with randomized delays.
        self.fake_progress_active = False
        self.fake_progress_steps = [
            ["Scanning transcript...", "Reviewing conversation structure...", "Initializing speaker analysis..."],
            ["Detecting distinct speech patterns...", "Tracking speaker contributions...", "Analyzing dialogue frequency..."],
            ["Identifying recurring phrases and unique vocabulary...", "Extracting key terms...", "Noticing distinct lexical patterns..."],
            ["Observing direct participant address...", "Detecting explicit name mentions...", "Noticing direct references in segments..."],
            ["Speaker A appears to lead the discussion...", "A primary speaker sets the conversation tone...", "Speaker A's dialogue indicates leadership..."],
            ["Speaker B responds but rarely initiates topics...", "A participant is mainly reactive...", "Speaker B builds on existing points..."],
            ["Noting that questions are often directed to Speaker A...", "Tracking the flow of inquiries...", "Observing frequent clarifications for Speaker A..."],
            ["Monitoring shifts in tone and formality...", "Observing subtle variations in speech tone...", "Noting differences in conversational style..."],
            ["Cross-checking explicit name mentions with speaker labels...", "Validating any detected names...", "Verifying clear name references..."],
            ["Observing patterns of acknowledgment between speakers...", "Tracking mutual references...", "Noticing consistent interactions..."],
            ["Speaker A frequently recalls past discussions...", "Continuity in Speaker A's dialogue is evident...", "Noting references to previous conversations..."],
            ["Aligning inferred speaker identities with conversation dynamics...", "Mapping roles based on dialogue cues...", "Determining speaker identities from context..."],
            ["Finalizing speaker mapping...", "Compiling final identity assignments...", "Consolidating findings into a structured mapping..."],
            ["Validating consistency across responses...", "Ensuring uniform speaker attribution...", "Cross-checking speaker roles for consistency..."],
            ["Mapping complete.", "Speaker mapping finalized.", "Attribution process complete."]
        ]
        self.fake_progress_step_index = 0
        self.fake_progress_active = False
        self.mapping_worker = None  # For the MappingWorker instance.
        self.speaker_mapping_dock = None

    def create_menus(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        self.open_audio_action = QAction("Open Audio File", self)
        self.open_audio_action.triggered.connect(self.open_audio_file)
        file_menu.addAction(self.open_audio_action)

        self.settings_action = QAction("Settings", self)
        self.settings_action.triggered.connect(self.show_settings_dialog)
        file_menu.addAction(self.settings_action)

        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_file)
        file_menu.addAction(self.save_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = self.menuBar().addMenu("Edit")
        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(self.copy_action)

        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(self.cut_action)

        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(self.paste_action)

        self.search_replace_action = QAction("Search and Replace", self)
        self.search_replace_action.triggered.connect(self.search_and_replace)
        edit_menu.addAction(self.search_replace_action)

        view_menu = self.menuBar().addMenu("View")
        self.toggle_wrap_action = QAction("Toggle Word Wrap", self)
        self.toggle_wrap_action.triggered.connect(self.toggle_wrap)
        view_menu.addAction(self.toggle_wrap_action)

    def set_ui_enabled(self, enabled: bool):
        self.open_audio_action.setEnabled(enabled)
        self.settings_action.setEnabled(enabled)
        self.save_action.setEnabled(enabled)
        self.search_replace_action.setEnabled(enabled)
        self.toggle_wrap_action.setEnabled(enabled)

    def show_settings_dialog(self):
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_assemblyai_key, new_openai_key = dialog.get_values()
            config["assemblyai_api_key"] = new_assemblyai_key
            config["openai_api_key"] = new_openai_key
            save_config(config)
            global API_KEY, OPENAI_API_KEY
            API_KEY = new_assemblyai_key
            OPENAI_API_KEY = new_openai_key
            aai.settings.api_key = API_KEY
            QMessageBox.information(self, "Settings Updated", "API keys have been updated successfully!")

    def search_and_replace(self):
        search_text, replace_text, ok = SearchReplaceDialog.getValues(self)
        if not ok:
            return
        if not search_text:
            QMessageBox.warning(self, "Input Error", "Search text cannot be empty.")
            return
        content = self.text_edit.toPlainText()
        self.text_edit.setPlainText(content.replace(search_text, replace_text))
        QMessageBox.information(self, "Success", f"Replaced all occurrences of '{search_text}' with '{replace_text}'.")

    def open_audio_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if file_path:
            self.set_ui_enabled(False)
            self.start_progress("Uploading file...")
            self.status_timer.start(2000)
            self.transcription_thread = TranscriptionThread(file_path)
            self.transcription_thread.transcription_finished.connect(self.on_transcription_finished)
            self.transcription_thread.error_occurred.connect(self.on_transcription_error)
            self.transcription_thread.start()

    def update_transcribing_status(self):
        if self.transcription_thread and self.transcription_thread.isRunning():
            self.status_bar.showMessage("Transcribing file...")

    def on_transcription_finished(self, result):
        # result is a tuple: (plain transcript text, transcript object)
        if self.status_timer.isActive():
            self.status_timer.stop()
        self.stop_progress("Transcription complete!")
        self.set_ui_enabled(True)
        transcript_text, transcript_obj = result
        self.last_transcript = transcript_obj
        self.plain_transcript_text = transcript_text
        self.timestamps_applied = False
        self.text_edit.setPlainText(transcript_text)
        speakers = set(re.findall(r"(Speaker\s+[A-Z0-9]+):", transcript_text))
        print("Detected Speakers:", speakers)
        if len(speakers) > 1:
            self.show_speaker_mapping_panel(sorted(speakers))

    def on_transcription_error(self, error_message):
        if self.status_timer.isActive():
            self.status_timer.stop()
        self.stop_progress("Transcription failed.")
        self.set_ui_enabled(True)
        QMessageBox.critical(self, "Transcription Failed", f"An error occurred: {error_message}")

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(self.text_edit.toPlainText())
                QMessageBox.information(self, "File Saved", f"File saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Could not save file: {str(e)}")

    def toggle_wrap(self):
        if self.word_wrap_enabled:
            self.text_edit.setLineWrapMode(QTextEdit.NoWrap)
        else:
            self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.word_wrap_enabled = not self.word_wrap_enabled

    def start_progress(self, status_message="Processing..."):
        self.status_bar.showMessage(status_message)
        self.progress.setRange(0, 0)
        self.progress.setVisible(True)

    def stop_progress(self, status_message=""):
        self.progress.setVisible(False)
        self.progress.setRange(0, 100)
        self.status_bar.showMessage(status_message, 5000)

    def show_speaker_mapping_panel(self, speaker_list):
        if self.speaker_mapping_dock:
            self.removeDockWidget(self.speaker_mapping_dock)
        self.speaker_mapping_dock = QDockWidget("Speaker Mapping", self)
        self.speaker_mapping_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.mapping_widget = SpeakerMappingWidget(speaker_list, self)
        self.mapping_widget.autopopulateRequested.connect(self.handleAutopopulate)
        self.mapping_widget.applyTimestampsRequested.connect(self.handleApplyTimestamps)
        self.mapping_widget.mappingApplied.connect(self.apply_speaker_mapping)
        self.speaker_mapping_dock.setWidget(self.mapping_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.speaker_mapping_dock)

    def start_fake_progress(self):
        self.fake_progress_active = True
        self.fake_progress_step_index = 0
        self.mapping_widget.clear_progress_log()
        self.schedule_next_fake_progress()

    def schedule_next_fake_progress(self):
        if not self.fake_progress_active:
            return
        # Randomized delay between 2000 and 4000 ms.
        delay = random.randint(2000, 4000)
        QTimer.singleShot(delay, self.update_fake_progress)

    def update_fake_progress(self):
        if not self.fake_progress_active:
            return
        if self.fake_progress_step_index < len(self.fake_progress_steps):
            step_variations = self.fake_progress_steps[self.fake_progress_step_index]
            message = random.choice(step_variations)
            self.mapping_widget.update_progress_log(message)
            self.fake_progress_step_index += 1
        else:
            # Continue cycling the final step.
            final_variations = self.fake_progress_steps[-1]
            message = random.choice(final_variations)
            self.mapping_widget.update_progress_log(message)
        self.schedule_next_fake_progress()

    def stop_fake_progress(self):
        self.fake_progress_active = False

    def handleAutopopulate(self):
        self.start_fake_progress()  # Start fake progress logging.
        candidates = self.mapping_widget.getCandidateNames()
        speakers = self.mapping_widget.getSpeakers()
        transcript_text = self.text_edit.toPlainText()  # Full transcript context.
        if candidates:
            prompt = (
                f"You are an expert in speaker attribution. Your task is to analyze the full transcript below and match each generic speaker label "
                f"to a realistic and distinct speaker name based solely on the full transcript context.\n\n"
                f"Full Transcript:\n{transcript_text}\n\n"
                f"Generic Speaker Labels: {', '.join(speakers)}\n\n"
                f"Candidate Names Provided: {', '.join(candidates)}\n\n"
                "Please provide speaker names as accurately as possible for every speaker label based solely on the full transcript context. "
                "Do not output any placeholder such as 'Unknown <X>' unless absolutely no contextual evidence is available. "
                "Even if candidate names are not provided, try to infer a plausible name from the transcript based on conversational context clues.\n\n"
                "Output the result as a valid JSON object only, with no extra text.\n"
                'Example output: {"Speaker A": "Shlomo", "Speaker B": "Mark"}'
            )
        else:
            prompt = (
                f"You are an expert in speaker attribution. Your task is to analyze the full transcript below and determine realistic and distinct speaker names "
                f"for each generic speaker label based solely on context.\n\n"
                f"Full Transcript:\n{transcript_text}\n\n"
                f"Generic Speaker Labels: {', '.join(speakers)}\n\n"
                "Please provide speaker names as accurately as possible for every speaker label based solely on the full transcript context. "
                "Do not output any placeholder such as 'Unknown <X>' unless absolutely no contextual evidence is available. "
                "Even if candidate names are not provided, try to infer a plausible name from the transcript based on conversational context clues.\n\n"
                "Output the result as a valid JSON object only, with no extra text.\n"
                'Example output: {"Speaker A": "Shlomo", "Speaker B": "Mark"}'
            )
        self.mapping_worker = MappingWorker(prompt)
        self.mapping_worker.mappingReady.connect(self.on_mapping_ready)
        self.mapping_worker.errorOccurred.connect(self.on_mapping_error)
        self.mapping_worker.start()

    def on_mapping_ready(self, result_text):
        self.stop_fake_progress()  # Stop fake progress updates.
        print("Auto Mapping Raw Response:", result_text)
        mapping = extract_json(result_text)
        self.mapping_widget.populateFields(mapping)
        self.mapping_widget.update_progress_log("Mapping complete.")
        self.mapping_worker = None

    def on_mapping_error(self, error_message):
        self.stop_fake_progress()
        QMessageBox.critical(self, "Auto Mapping Error", f"An error occurred: {error_message}")
        self.mapping_worker = None

    def handleApplyTimestamps(self):
        if not self.last_transcript:
            QMessageBox.warning(self, "Error", "No transcript data available.")
            return
        if not self.timestamps_applied:
            new_text = ""
            for utt in self.last_transcript.utterances:
                sec_time = utt.start / 1000.0  # Convert ms to s.
                ts = seconds_to_hhmmss(sec_time)
                new_text += f"[{ts}] Speaker {utt.speaker}: {utt.text}\n"
            self.text_edit.setPlainText(new_text)
            self.timestamps_applied = True
            self.mapping_widget.apply_timestamps_button.setText("Remove Timestamps")
        else:
            self.text_edit.setPlainText(self.plain_transcript_text)
            self.timestamps_applied = False
            self.mapping_widget.apply_timestamps_button.setText("Apply Timestamps")

    def apply_speaker_mapping(self, mapping):
        content = self.text_edit.toPlainText()
        for speaker_label, real_name in mapping.items():
            content = content.replace(speaker_label, real_name)
        self.text_edit.setPlainText(content)
        QMessageBox.information(self, "Speaker Mapping", "Speaker names have been updated.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
