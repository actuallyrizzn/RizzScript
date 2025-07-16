# Architecture Overview

RizzScript is intentionally kept to a **single file (`app.py`)** to reduce friction for new contributors, yet its internal structure follows clear separations of concern.

```
┌────────────┐   audio file    ┌─────────────────┐
|   UI /     | ─────────────▶ |  Transcription   |
| MainWindow |                 |   Thread        |
└─────┬──────┘                 └─────────────────┘
      │  transcript + meta                 │ OpenAI prompt
      │                                     ▼
      │                          ┌──────────────────┐
      │                          |  MappingWorker   |
      │                          └──────────────────┘
      │                                     │ mapping dict
      ▼                                     ▼
┌────────────────┐                 ┌──────────────────┐
| SpeakerMapping |  ◀──────────────│  MainWindow      |
|   Widget       |   signal/slot   └──────────────────┘
```

---

## 1. Data Flow

1. **User selects an audio file** ➜ `MainWindow.open_audio_file` starts a `TranscriptionThread`.
2. `assemblyai.Transcriber` performs speech-to-text & diarisation in a *background thread*.
3. When finished, the thread emits `transcription_finished`, returning the raw text **and** the rich `Transcript` object.
4. `MainWindow` populates the editor and opens a `SpeakerMappingWidget` dock.
5. The widget can create a prompt for *MappingWorker* which calls **OpenAI ChatCompletion** to infer real names.
6. The mapping is applied back to the transcript via Qt *signals and slots*.

---

## 2. Concurrency Model

• **Qt Threads** (`QThread`) isolate long-running API calls from the GUI.  
• Communication happens through **pyqtSignal** objects to keep the GUI thread safe.  
• A *fake* progress log is generated on the GUI thread using `QTimer.singleShot`, so no extra threads are required.

---

## 3. Key Modules & Responsibilities

| Section | Responsibility |
|---------|----------------|
| Helper Functions | Config management, JSON parsing, time conversion. |
| `SettingsDialog` | Enter & persist API keys. |
| `TranscriptionThread` | Upload & transcribe audio using AssemblyAI. |
| `MappingWorker` | Send a prompt to OpenAI and return a JSON mapping. |
| `SearchReplaceDialog` | Simple find/replace UI. |
| `SpeakerMappingWidget` | UI for renaming speakers and toggling timestamps. |
| `MainWindow` | Orchestrates all components and owns the central editor. |

---

## 4. File & Directory Layout

Although most logic lives in `app.py`, the repo also contains:

• `dist/` — packaged executables and artefacts  
• `build/` — PyInstaller temp files  
• `old/` — archived versions for posterity  
• `RizzScript.spec` — PyInstaller configuration  

---

## 5. Why a Single-File GUI?

Keeping everything in `app.py` reduces barriers for new contributors and suits small desktop utilities.  If the codebase grows, it can be modularised into `rizzscript/` package with sub-modules (`ui`, `workers`, `services`, etc.).

---

## 6. Future Improvements

• Unit tests for helper functions  
• Logging to file for easier debugging  
• Plugin interface for alternative STT providers  
• Migrate to **asyncio + Qt** (via *qasync*) for finer-grained concurrency