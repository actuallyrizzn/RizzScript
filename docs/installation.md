# Installation Guide

This guide covers everything you need to **install, configure, and run RizzScript** on macOS, Windows, and Linux.

---

## 1. Requirements

• **Python 3.8 or newer**  
• Internet connection (for AssemblyAI / OpenAI calls)  
• OS-specific package manager (Homebrew, Chocolatey, apt, etc.) — optional but recommended

> RizzScript is 100 % Python and has no GPU/CUDA requirements.

---

## 2. Clone the Repository

```bash
# Pick a location you like
$ git clone https://github.com/<your-org>/RizzScript.git
$ cd RizzScript
```

---

## 3. Create a Virtual Environment (recommended)

```bash
$ python -m venv .venv
$ source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

---

## 4. Install Dependencies

Run the following command from the repo root:

```bash
$ pip install -r requirements.txt
```

If you do **not** have a `requirements.txt`, use:

```bash
$ pip install pyqt5 assemblyai openai
```

---

## 5. Configure API Keys

RizzScript requires **AssemblyAI** for speech-to-text and **OpenAI** (optional) for speaker name guessing.

1. Obtain keys from the respective dashboards.  
2. Launch the app once (`python app.py`) and open **File → Settings**.  
3. Paste your keys and click **OK**.  
4. Keys are saved locally in `config.json` (never committed).

---

## 6. Run the Application

```bash
$ python app.py
```

Upon first launch you should see the main editor window.

---

## 7. Packaging for Windows (optional)

Create a portable `.exe` with **PyInstaller**:

```bash
$ pip install pyinstaller
$ pyinstaller --onefile --windowed --name "RizzScript" app.py
```

The output binary appears in `dist/`.

---

## 8. Troubleshooting

| Symptom | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'PyQt5'` | Make sure you activated the virtual environment and re-run `pip install pyqt5`. |
| Window freezes during transcription | This should not happen; file an issue with OS, steps, and logs. |
| API quota errors | Verify you have enough quota for AssemblyAI / OpenAI accounts. |

*Still stuck?* Open an issue on GitHub and we will be happy to help.