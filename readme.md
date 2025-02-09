# RizzScript

RizzScript is a **PyQt5**‐based GUI application for transcribing audio files and mapping speaker labels to real names. It leverages **AssemblyAI** for speech‑to‑text with speaker diarization and can optionally integrate **OpenAI** to guess speaker identities. The interface includes a text editor, search/replace functionality, timestamps toggling, and a **fake chain‑of‑thought** progress log for a lively user experience.

## Features

- **Audio Transcription with Speaker Labels**  
  - Supports `.mp3`, `.wav`, and `.ogg` files.  
  - Uses **AssemblyAI** to produce transcripts with speaker diarization.  
- **Speaker Mapping & Name Guessing**  
  - A side panel allows you to **autopopulate** speaker names via OpenAI’s API.  
  - Displays a **fake chain-of-thought** progress log while waiting for the API response.  
- **Search & Replace**  
  - Easily replace text in the main editor.  
- **Timestamps Toggle**  
  - Apply or remove timestamps in the transcript at any time.  
- **File Operations**  
  - Open audio files for transcription.  
  - Open/save `.txt` files to preserve or edit transcript text.  
- **Word Wrap**  
  - Toggle line-wrapping in the text editor.  
- **Configurable**  
  - AssemblyAI and OpenAI API keys are read from `config.json`.  
  - Manage them through the “Settings” dialog.

## Prerequisites

- **Python 3.8+**  
- **PyQt5** for the GUI  
  ```bash
  pip install pyqt5
  ```
- **AssemblyAI Python SDK** for speech‑to‑text  
  ```bash
  pip install assemblyai
  ```
- **OpenAI Python Library** if you plan to use name auto‑mapping  
  ```bash
  pip install openai
  ```

## Getting Started

1. **Clone this repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install dependencies**:
   ```bash
   pip install pyqt5 assemblyai openai
   ```
   *(Adjust as needed for your environment.)*

3. **Run the application**:
   ```bash
   python rizzscript.py
   ```

4. **Update API Keys**  
   - Click **File > Settings** to enter your **AssemblyAI** and **OpenAI** API keys.  
   - They’ll be stored in `config.json`.

## File Structure

- `rizzscript.py`: Main application code.
- `config.json`: Stores API keys for AssemblyAI and OpenAI (generated on first run if missing).

## Usage

### 1. Transcribing Audio Files

1. **File > Open Audio File**  
2. Select an audio file (`.mp3`, `.wav`, `.ogg`).  
3. RizzScript spins up a background worker to transcribe the file via **AssemblyAI**.  
4. The transcribed text appears in the main editor; each **Speaker** label (like `Speaker A`, `Speaker B`) is diarized.

### 2. Speaker Mapping & Name Auto-populate

1. After transcription, a **Speaker Mapping Panel** appears on the right.  
2. (Optional) Enter **candidate names** in a comma-separated list.  
3. Click **“Attempt to Autopopulate.”**  
   - A **fake chain-of-thought** progress log updates every few seconds while **OpenAI** is working.  
   - When done, the panel is populated with best‑guess names.  
4. Click **“Apply Changes”** to replace `Speaker A`, `Speaker B`, etc. in the editor with the guessed names.

### 3. Timestamps Toggle

- In the side panel, click **“Apply Timestamps”** to show `[HH:MM:SS]` at the start of each utterance.  
- Click again to **“Remove Timestamps”** and revert to the plain transcript.

### 4. Search & Replace

1. **Edit > Search and Replace**  
2. Enter the text to search and replacement text.  
3. Click **OK** to replace all occurrences in the editor.

### 5. Save & Open Text Files

- **File > Save** to store the current transcript as a `.txt`.  
- **File > Open** (not to be confused with Open Audio File) to load an existing `.txt`.

## Shortcuts

| Action            | Shortcut   |
|-------------------|------------|
| **Save File**     | Ctrl + S   |
| **Copy**          | Ctrl + C   |
| **Cut**           | Ctrl + X   |
| **Paste**         | Ctrl + V   |

## Behind the Scenes

- **Threaded Transcription**  
  - Uses `TranscriptionThread` to avoid freezing the UI.
- **Fake Progress Log**  
  - A timer updates the side panel with randomized chain-of-thought messages while the name auto‑mapping request runs in a separate `MappingWorker` thread.
- **config.json**  
  - Stores your `assemblyai_api_key` and `openai_api_key`.  
  - Automatically generated if missing.

## Known Limitations

- **Text-Only Name Guessing**: Speaker auto‑mapping relies on text from the transcript. If the transcript lacks explicit clues, guesses may be incorrect.  
- **Fake Chain-of-Thought**: The progress log is purely for user feedback and does not represent the actual model’s internal reasoning.

## License

This project is licensed under the **MIT License**. See `LICENSE` for details.