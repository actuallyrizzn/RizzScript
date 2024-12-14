# RizzScript

RizzScript is a Python-based GUI application designed to facilitate transcription of audio files using AssemblyAI's API. It features a text editor with search-and-replace functionality, file saving, and customizable options like word wrap.

## Features

- **Audio Transcription**: Supports transcription of audio files in `.mp3`, `.wav`, and `.ogg` formats with speaker labeling.
- **Configurable API Key**: Allows users to manage their AssemblyAI API key through the GUI.
- **Search and Replace**: Provides an easy way to search and replace text within the text editor.
- **File Operations**: Open, save, and edit text files.
- **Customizable Word Wrap**: Toggle word wrapping in the text editor.
- **Progress Indication**: Visual feedback for long-running operations like transcription.

## Prerequisites

- Python 3.8+
- AssemblyAI Python SDK

Install dependencies:
```bash
pip install assemblyai
```

## Getting Started

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Run the application:
   ```bash
   python rizzscript.py
   ```

3. Update your AssemblyAI API key through the `File > AssemblyAI API Key` menu option.

## File Structure

- `config.json`: Stores the AssemblyAI API key.
- `rizzscript.py`: Main application code.

## Usage

### Transcribing Audio Files
1. Click on `File > Open Audio File`.
2. Select an audio file from your system.
3. The transcription process will start, and results will appear in the text editor.

### Search and Replace
1. Go to `Edit > Search and Replace`.
2. Enter the text to search and the replacement text.
3. Click `OK` to replace all occurrences.

### Save and Open Text Files
- Save the text in the editor using `File > Save`.
- Open an existing text file via `File > Open`.

### Toggle Word Wrap
Enable or disable word wrapping in the editor from `View > Toggle Word Wrap`.

## Shortcuts

| Action           | Shortcut        |
|------------------|-----------------|
| Save File        | `Ctrl + S`      |
| Copy             | `Ctrl + C`      |
| Cut              | `Ctrl + X`      |
| Paste            | `Ctrl + V`      |

## Dependencies

- `tkinter`: For the GUI.
- `assemblyai`: For transcription services.
- `json`: For configuration management.
- `os`: For file path operations.
- `threading`: For running transcription in the background.

## Error Handling
- If the API key is missing, a configuration error dialog will appear.
- Transcription errors are displayed as message boxes.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
