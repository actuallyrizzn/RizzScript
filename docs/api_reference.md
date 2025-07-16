# API Reference

Below is a *human-written* reference for the public classes and helper functions found in `app.py`.

---

## Helper Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `load_config()` | `dict` | Reads `config.json`, creating it with empty keys if missing. |
| `save_config(config)` | `None` | Writes the given dict back to `config.json` with pretty JSON. |
| `extract_json(text)` | `dict` | Extracts the first valid JSON object embedded anywhere in a string. Robust to leading/trailing cruft. |
| `seconds_to_hhmmss(seconds)` | `str` | Converts float seconds to `HH:MM:SS` formatted string.

---

## Qt Dialogs & Widgets

### `SettingsDialog`
Modal dialog that lets users enter AssemblyAI and OpenAI API keys.

• **Signals:** *none*  
• **Key methods:** `get_values()` ➜ `(assemblyai_key, openai_key)`

### `SearchReplaceDialog`
`QDialog` that captures plain text *search* and *replace* strings.

• **Static method:** `getValues(parent)` ➜ `(search, replace, accepted: bool)`

### `SpeakerMappingWidget`
Side-panel widget for speaker name mapping and timestamp toggling.

| Signal | Emitted Value |
|--------|---------------|
| `mappingApplied` | `dict` from generic label to real name |
| `autopopulateRequested` | *None* — triggers OpenAI mapping flow |
| `applyTimestampsRequested` | *None* — asks `MainWindow` to toggle timestamps |

---

## Worker Threads

### `TranscriptionThread(file_path)`
Uploads the given audio file to AssemblyAI and emits **transcript text + rich object** upon completion.

| Signal | Payload |
|--------|---------|
| `transcription_finished` | `(str, aai.Transcript)` |
| `error_occurred` | `str` |

### `MappingWorker(prompt)`
Executes an OpenAI chat completion in the background.

| Signal | Payload |
|--------|---------|
| `mappingReady` | `str` raw JSON (may contain extra text) |
| `errorOccurred` | `str` |

---

## `MainWindow`
Central `QMainWindow` subclass orchestrating the entire application.

### Important Slots / Methods

| Method | Purpose |
|--------|---------|
| `open_audio_file()` | Opens file dialog and spins up `TranscriptionThread`. |
| `on_transcription_finished(result)` | Handles thread success, populates editor. |
| `handleAutopopulate()` | Builds an OpenAI prompt and spawns `MappingWorker`. |
| `handleApplyTimestamps()` | Adds or removes `[HH:MM:SS]` markers based on toggle state. |
| `apply_speaker_mapping(mapping)` | Performs string substitution in the editor. |

Refer to the source for additional convenience methods (`toggle_wrap`, `search_and_replace`, etc.).