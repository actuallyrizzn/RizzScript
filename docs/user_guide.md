# User Guide

Welcome to the step-by-step guide for **every feature** inside RizzScript.

---

## 1. Launching the App

Run `python app.py` or double-click `RizzScript.exe` (Windows build).  The main window contains:

• **Menu Bar** (File, Edit, View)  
• **Central Editor** where the transcript appears  
• **Status Bar** with a progress spinner  

---

## 2. Transcribing Audio

1. Click **File → Open Audio File**.  
2. Select an `.mp3`, `.wav`, or `.ogg`.  
3. A spinner shows *Uploading file …* followed by *Transcribing file …*.  
4. Once complete, the text appears in the editor.

*Tip:* You can keep working in other applications; transcription happens in a background thread.

---

## 3. Speaker Mapping

If more than one speaker is detected, a **Speaker Mapping** panel slides in.

| Control | Purpose |
|---------|---------|
| Candidate Names | Comma-separated list of names you *expect* to appear. |
| Attempt to Autopopulate | Uses OpenAI to guess who is who. |
| Apply Changes | Replaces `Speaker A`, `Speaker B`, … in the transcript. |

The panel also shows a *fake* chain-of-thought log — purely cosmetic so the UI feels alive.

---

## 4. Timestamp Toggle

Click **Apply Timestamps** to prepend `[HH:MM:SS]` to every utterance. Click again to remove them.

---

## 5. Editing Text

• Standard clipboard shortcuts (Ctrl-C/Ctrl-X/Ctrl-V) work.  
• Word-wrap can be toggled via **View → Toggle Word Wrap**.  
• Find & Replace is under **Edit → Search and Replace**.

---

## 6. Saving & Loading

• **File → Save** stores the current editor buffer as `.txt`.  
• Opening existing `.txt` files is supported via **File → Open**.

---

## 7. Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Save | `Ctrl + S` |
| Copy | `Ctrl + C` |
| Cut  | `Ctrl + X` |
| Paste| `Ctrl + V` |

---

## 8. Tips & Tricks

• Press **Esc** to cancel an open dialog.  
• You can drag the Speaker Mapping dock to the left side if you prefer.  
• Large files (>2 h) take longer; monitor your AssemblyAI quota.  

Happy transcribing! 🎉