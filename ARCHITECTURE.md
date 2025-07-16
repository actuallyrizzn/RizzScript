# Technical Architecture - RizzScript

This document provides a detailed technical overview of RizzScript's architecture, design patterns, and implementation details for developers and contributors.

## Table of Contents

- [Overview](#overview)
- [Architecture Patterns](#architecture-patterns)
- [Core Components](#core-components)
- [Data Flow](#data-flow)
- [API Integrations](#api-integrations)
- [Threading Model](#threading-model)
- [Error Handling Strategy](#error-handling-strategy)
- [Configuration Management](#configuration-management)
- [UI Architecture](#ui-architecture)
- [Build System](#build-system)

## Overview

RizzScript is built using a **Model-View-Controller (MVC)** pattern with **Qt's signal-slot mechanism** for event handling. The application follows **separation of concerns** principles with distinct layers for UI, business logic, and external service integrations.

### Key Design Principles

1. **Asynchronous Processing**: All long-running operations are performed in background threads
2. **Modular Design**: Clear separation between UI, API services, and business logic
3. **Error Resilience**: Comprehensive error handling with graceful degradation
4. **Extensibility**: Plugin-ready architecture for future enhancements
5. **Security First**: Secure handling of API keys and user data

## Architecture Patterns

### Model-View-Controller (MVC)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      VIEW       │    │   CONTROLLER    │    │      MODEL      │
│   (PyQt5 UI)   │◄──►│  (MainWindow)   │◄──►│ (Data Classes)  │
│                 │    │                 │    │                 │
│ - TextEdit      │    │ - Event Handler │    │ - Transcript    │
│ - Dialogs       │    │ - State Mgmt    │    │ - Config        │
│ - Menus         │    │ - Coordination  │    │ - Speaker Map   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Observer Pattern

Qt's signal-slot mechanism implements the observer pattern for loose coupling between components:

```python
# Publisher
class TranscriptionThread(QThread):
    transcription_finished = pyqtSignal(object)
    error_occurred = pyqtSignal(str)

# Subscriber
class MainWindow(QMainWindow):
    def __init__(self):
        # Connect signals to slots
        thread.transcription_finished.connect(self.on_transcription_finished)
        thread.error_occurred.connect(self.on_transcription_error)
```

### Strategy Pattern

Different AI processing strategies can be implemented using the strategy pattern:

```python
class SpeakerMappingStrategy:
    def map_speakers(self, transcript, candidates):
        raise NotImplementedError

class OpenAISpeakerMapper(SpeakerMappingStrategy):
    def map_speakers(self, transcript, candidates):
        # OpenAI-specific implementation
        pass

class LocalSpeakerMapper(SpeakerMappingStrategy):
    def map_speakers(self, transcript, candidates):
        # Local processing implementation
        pass
```

## Core Components

### 1. MainWindow Class

**File**: `app.py` (lines 257-581)  
**Role**: Primary application controller and UI coordinator

#### Responsibilities:
- **UI Management**: Controls main window, menus, and dialogs
- **Event Coordination**: Routes user interactions to appropriate handlers
- **State Management**: Maintains application state and user preferences
- **Progress Monitoring**: Provides real-time feedback to users

#### Key Methods:
```python
def open_audio_file(self):          # Initiates transcription workflow
def show_speaker_mapping_panel(self): # Displays speaker mapping UI
def handleAutopopulate(self):       # Triggers AI speaker identification
def handleApplyTimestamps(self):    # Toggles timestamp display
def apply_speaker_mapping(self):    # Updates transcript with speaker names
```

#### State Variables:
- `last_transcript`: Complete AssemblyAI transcript object
- `plain_transcript_text`: Text without timestamps
- `timestamps_applied`: Boolean flag for timestamp state
- `fake_progress_active`: Controls progress simulation

### 2. TranscriptionThread Class

**File**: `app.py` (lines 86-102)  
**Role**: Background audio processing

#### Architecture:
```python
class TranscriptionThread(QThread):
    # Signals for async communication
    transcription_finished = pyqtSignal(object)
    error_occurred = pyqtSignal(str)
    
    def run(self):
        # AssemblyAI API integration
        # Speaker diarization configuration
        # Error handling and result emission
```

#### Data Flow:
1. **Input**: Audio file path
2. **Processing**: AssemblyAI transcription with diarization
3. **Output**: Tuple of (text, transcript_object)
4. **Error Handling**: Exception capture and signal emission

### 3. MappingWorker Class

**File**: `app.py` (lines 104-122)  
**Role**: AI-powered speaker identification

#### AI Integration:
```python
class MappingWorker(QThread):
    def run(self):
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="o1",  # GPT-4 model
            messages=[
                {"role": "system", "content": "Speaker attribution expert"},
                {"role": "user", "content": self.prompt}
            ]
        )
```

#### Prompt Engineering:
The worker uses sophisticated prompts that include:
- **Full transcript context** for accurate analysis
- **Candidate name suggestions** when provided
- **Conversation pattern analysis** instructions
- **JSON output formatting** requirements

### 4. SpeakerMappingWidget Class

**File**: `app.py` (lines 164-240)  
**Role**: Interactive speaker assignment interface

#### UI Components:
- **Candidate Input**: Text field for user-provided names
- **Progress Log**: Real-time AI analysis feedback
- **Speaker Fields**: Dynamic input fields for each detected speaker
- **Control Buttons**: Autopopulate and timestamp toggle

#### Signal Flow:
```python
# Widget signals
mappingApplied = pyqtSignal(dict)
autopopulateRequested = pyqtSignal()
applyTimestampsRequested = pyqtSignal()

# Connected to MainWindow handlers
widget.autopopulateRequested.connect(self.handleAutopopulate)
widget.mappingApplied.connect(self.apply_speaker_mapping)
```

## Data Flow

### Complete Workflow Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   User      │    │  MainWindow  │    │   Thread    │
│   Action    │───►│  Controller  │───►│   Pool      │
└─────────────┘    └──────────────┘    └─────────────┘
                           │                     │
                           ▼                     ▼
                   ┌──────────────┐    ┌─────────────┐
                   │  UI Update   │    │   API Call  │
                   │   Progress   │    │ (Assembly/  │
                   │   Feedback   │    │   OpenAI)   │
                   └──────────────┘    └─────────────┘
                           ▲                     │
                           │                     ▼
                   ┌──────────────┐    ┌─────────────┐
                   │   Signal     │◄───│   Result    │
                   │  Emission    │    │ Processing  │
                   └──────────────┘    └─────────────┘
```

### Detailed Data Pipeline

#### 1. Audio Processing Pipeline
```
Audio File → AssemblyAI → Raw Transcript → Speaker Labels → Display
    ↓              ↓            ↓              ↓           ↓
File Path → API Upload → JSON Response → Parsing → UI Update
```

#### 2. Speaker Mapping Pipeline
```
Transcript + Names → OpenAI → AI Analysis → JSON Response → UI Update
       ↓               ↓          ↓            ↓           ↓
Context Building → API Call → Processing → Parsing → Field Population
```

#### 3. Timestamp Processing Pipeline
```
Raw Transcript → Utterance List → Time Conversion → Format → Display
      ↓              ↓               ↓              ↓         ↓
JSON Data → Iteration → Math Calc → String Format → UI Update
```

## API Integrations

### AssemblyAI Integration

#### Configuration:
```python
aai.settings.api_key = API_KEY
transcriber = aai.Transcriber()
config = aai.TranscriptionConfig(speaker_labels=True)
```

#### Error Handling:
- **Network Errors**: Connection timeouts and retries
- **Authentication**: Invalid API key detection
- **Quota Limits**: Usage limit exceeded handling
- **Format Errors**: Unsupported audio format detection

#### Response Processing:
```python
# Raw response structure
transcript.utterances = [
    {
        'speaker': 'A',
        'text': 'Hello world',
        'start': 1000,  # milliseconds
        'end': 2500
    }
    # ... more utterances
]
```

### OpenAI Integration

#### Model Configuration:
```python
response = openai.ChatCompletion.create(
    model="o1",  # GPT-4 model identifier
    messages=[...],
    temperature=0.7,  # Controlled creativity
    max_tokens=1000   # Response limit
)
```

#### Prompt Engineering Strategy:
1. **Context Provision**: Full transcript included
2. **Task Specification**: Clear speaker mapping instructions
3. **Format Requirements**: JSON output specification
4. **Quality Guidelines**: Accuracy and consistency requirements

#### JSON Response Parsing:
```python
def extract_json(text):
    try:
        return json.loads(text)
    except:
        # Fallback: Extract JSON from mixed content
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            return json.loads(text[start:end+1])
```

## Threading Model

### Thread Architecture

RizzScript uses **QThread** for all background operations to maintain UI responsiveness:

```python
Main Thread (UI)
    ├── TranscriptionThread (AssemblyAI calls)
    ├── MappingWorker (OpenAI calls)  
    └── Progress Timer (UI updates)
```

### Thread Communication

#### Signal-Slot Pattern:
```python
# Cross-thread communication via signals
worker_thread.finished.connect(main_thread.on_completion)
worker_thread.error.connect(main_thread.on_error)
worker_thread.progress.connect(main_thread.update_progress)
```

#### Thread Safety:
- **No Shared Mutable State**: Each thread owns its data
- **Signal-Based Communication**: Qt's thread-safe signal system
- **Immutable Data Passing**: Objects passed via signals are immutable
- **UI Thread Updates**: All UI updates happen on main thread

### Progress Management

#### Real Progress (AssemblyAI):
```python
def start_progress(self, message="Processing..."):
    self.status_bar.showMessage(message)
    self.progress.setRange(0, 0)  # Indeterminate progress
    self.progress.setVisible(True)
```

#### Simulated Progress (OpenAI):
```python
def start_fake_progress(self):
    self.fake_progress_active = True
    self.fake_progress_step_index = 0
    self.schedule_next_fake_progress()

def schedule_next_fake_progress(self):
    delay = random.randint(2000, 4000)  # 2-4 second intervals
    QTimer.singleShot(delay, self.update_fake_progress)
```

## Error Handling Strategy

### Multi-Level Error Handling

#### 1. API Level Errors:
```python
try:
    transcript = transcriber.transcribe(file_path, config=config)
except AssemblyAIError as e:
    self.error_occurred.emit(f"Transcription failed: {str(e)}")
except NetworkError as e:
    self.error_occurred.emit(f"Network error: {str(e)}")
```

#### 2. UI Level Errors:
```python
def on_transcription_error(self, error_message):
    self.stop_progress("Transcription failed.")
    self.set_ui_enabled(True)
    QMessageBox.critical(self, "Error", error_message)
```

#### 3. Application Level Errors:
```python
def show_settings_dialog(self):
    try:
        dialog = SettingsDialog(self)
        # ... dialog logic
    except Exception as e:
        QMessageBox.critical(self, "Settings Error", f"Could not open settings: {str(e)}")
```

### Error Recovery Strategies

1. **Graceful Degradation**: Core features work even if AI features fail
2. **User Guidance**: Clear error messages with suggested solutions
3. **State Recovery**: Application returns to stable state after errors
4. **Retry Mechanisms**: Automatic retries for transient network errors

## Configuration Management

### Configuration Architecture

```python
CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config({"assemblyai_api_key": "", "openai_api_key": ""})
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)
```

### Security Considerations

1. **Local Storage**: Configuration stored locally, not in cloud
2. **Git Exclusion**: `.gitignore` prevents accidental commits
3. **Permission Control**: File permissions restrict access
4. **No Hardcoding**: No API keys in source code

### Configuration Schema

```json
{
    "assemblyai_api_key": "string",    // Required for transcription
    "openai_api_key": "string",        // Optional for AI features
    "version": "2.0.0",                // Application version
    "last_updated": "2024-01-01"       // Configuration timestamp
}
```

## UI Architecture

### Qt Widget Hierarchy

```
QMainWindow (MainWindow)
├── QTextEdit (Central Widget)
├── QMenuBar
│   ├── File Menu (Open, Save, Settings, Exit)
│   ├── Edit Menu (Copy, Cut, Paste, Search/Replace)
│   └── View Menu (Word Wrap Toggle)
├── QStatusBar
│   └── QProgressBar (Hidden by default)
└── QDockWidget (Speaker Mapping)
    └── SpeakerMappingWidget
        ├── QLineEdit (Candidate Names)
        ├── QTextEdit (Progress Log)
        ├── QPushButton (Autopopulate)
        ├── QPushButton (Toggle Timestamps)
        └── Dynamic Speaker Fields
```

### Style and Theming

#### Font Configuration:
```python
font = QFont("Consolas", 14)  # Fixed-width font for readability
self.text_edit.setFont(font)
```

#### Window Management:
```python
self.setWindowTitle("RizzScript: Voice Studio")
self.resize(800, 600)  # Default window size
```

### Responsive Design

1. **Resizable Components**: All UI elements scale with window size
2. **Dockable Panels**: Speaker mapping panel can be moved/resized
3. **Text Wrapping**: Configurable word wrap for different screen sizes
4. **Status Feedback**: Progress indicators adapt to available space

## Build System

### PyInstaller Configuration

**File**: `RizzScript.spec`

```python
a = Analysis(
    ['app.py'],                 # Entry point
    pathex=[],                  # Additional paths
    binaries=[],                # Binary dependencies
    datas=[],                   # Data files
    hiddenimports=[],           # Hidden imports
    excludes=[],                # Excluded modules
    noarchive=False,
    optimize=0,
)

exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name='RizzScript',          # Executable name
    debug=False,                # Release mode
    console=False,              # Windowed application
    upx=True,                   # Compression enabled
)
```

### Build Process

#### Development Build:
```bash
python app.py  # Direct execution
```

#### Production Build:
```bash
pyinstaller RizzScript.spec  # Creates dist/RizzScript.exe
```

#### Build Optimizations:
- **UPX Compression**: Reduces executable size
- **No Console**: Windowed application without console
- **Single File**: All dependencies bundled
- **Optimized Imports**: Only necessary modules included

### Dependency Management

#### Runtime Dependencies:
```python
# Core Framework
PyQt5>=5.15.0,<6.0.0

# API Services  
assemblyai>=0.20.0
openai>=1.0.0
```

#### Build Dependencies:
```python
# Packaging
pyinstaller>=5.0.0

# Optional
pydub>=0.25.0  # Audio format conversion
```

## Performance Considerations

### Memory Management

1. **Efficient Object Lifecycle**: Proper cleanup of Qt objects
2. **Large File Handling**: Streaming for large audio files
3. **Memory Monitoring**: Track memory usage during processing
4. **Garbage Collection**: Explicit cleanup of temporary objects

### CPU Optimization

1. **Background Processing**: CPU-intensive tasks in worker threads
2. **Efficient Algorithms**: Optimized text processing algorithms
3. **Caching**: Cache frequently accessed data
4. **Lazy Loading**: Load resources only when needed

### Network Optimization

1. **Connection Pooling**: Reuse HTTP connections for API calls
2. **Timeout Management**: Appropriate timeouts for API calls
3. **Retry Logic**: Exponential backoff for failed requests
4. **Error Recovery**: Graceful handling of network failures

## Security Architecture

### API Key Security

1. **Local Storage**: Keys stored locally, never transmitted unnecessarily
2. **Environment Variables**: Support for environment-based configuration
3. **Access Control**: File permissions restrict key access
4. **No Logging**: API keys never logged or exposed in debug output

### Data Protection

1. **No Cloud Storage**: All processing happens locally or via secure APIs
2. **Secure Transmission**: HTTPS for all API communications
3. **Input Validation**: Sanitize all user inputs
4. **Error Sanitization**: Prevent sensitive data in error messages

### Privacy Considerations

1. **Local Processing**: Transcript editing happens locally
2. **User Control**: Users control what data is sent to APIs
3. **No Tracking**: No user behavior tracking or analytics
4. **Transparent Data Flow**: Clear documentation of data handling

---

This architecture document provides the foundation for understanding and contributing to RizzScript. For specific implementation details, refer to the inline code documentation and comments in `app.py`.