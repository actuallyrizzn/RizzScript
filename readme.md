# **RizzScript**  

**RizzScript** is a **PyQt5-based GUI application** for **audio transcription, speaker mapping, and timestamp management**. It leverages **AssemblyAI** for transcription and diarization, with **OpenAI-powered speaker attribution**. The UI includes **search/replace, a toggleable timestamp feature, and a fake chain-of-thought progress log** for a smooth UX.

---

## **🔹 Features**
✔ **Audio Transcription with Speaker Labels**  
   - Supports **`.mp3`, `.wav`, `.ogg`** formats.  
   - Uses **AssemblyAI** for **speech-to-text with diarization**.  

✔ **Speaker Mapping & Auto-Guessing**  
   - Maps `Speaker A`, `Speaker B`, etc. to real names.  
   - **OpenAI integration** provides name suggestions.  

✔ **Timestamps Toggle**  
   - Apply or remove timestamps dynamically (`[HH:MM:SS]`).  

✔ **Text Editor with Search & Replace**  
   - Standard **find/replace** functionality.  

✔ **File Operations**  
   - **Open** and **save** `.txt` files to edit transcripts.  

✔ **Fully Threaded for Performance**  
   - **Transcription & Speaker Mapping** run in the background.  
   - **No UI freezing!**  

✔ **Configuration Management**  
   - API keys stored in **`config.json`** for easy access.  

---

## **📥 Prerequisites**
**Install dependencies:**
```bash
pip install pyqt5 assemblyai openai
```
- **Python 3.8+**  
- **PyQt5** (for GUI)  
- **AssemblyAI** (for transcription)  
- **OpenAI API** *(if using name guessing)*  

---

## **🚀 Getting Started**
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd RizzScript
   ```
2. **Run the application:**
   ```bash
   python app.py
   ```
3. **Enter API Keys:**  
   - Click **File > Settings**  
   - Enter your **AssemblyAI** and **OpenAI** API keys.  
   - Keys are stored in `config.json`.  

---

## **📂 File Structure**
| Directory/File          | Description |
|-------------------------|------------|
| **`app.py`**            | Main application file. |
| **`config.json`**       | Stores API keys for AssemblyAI & OpenAI. |
| **`dist/`**             | Contains compiled `.exe` (Windows builds). |
| **`build/`**            | Temporary build files (can be ignored). |
| **`old/`**              | Backup of older versions. |
| **`RizzScript.spec`**   | PyInstaller spec file for packaging. |
| **`.git/`**             | Git repository metadata (ignore). |

---

## **🎯 Usage Guide**
### **1️⃣ Transcribing Audio Files**
1. Click **File > Open Audio File**  
2. Select an **audio file** (`.mp3`, `.wav`, `.ogg`).  
3. **Transcription runs in the background.**  
4. **Diarized transcript appears** in the text editor.  

### **2️⃣ Speaker Mapping**
1. The **Speaker Mapping Panel** opens after transcription.  
2. **Optional**: Enter **candidate names** in a comma-separated list.  
3. Click **"Attempt to Autopopulate"**   
   - When complete, suggested names appear.  
4. Click **"Apply Changes"** to update the transcript.  

### **3️⃣ Toggling Timestamps**
- Click **"Apply Timestamps"** to add `[HH:MM:SS]` at the start of each utterance.  
- Click again to **remove timestamps**.  

### **4️⃣ Editing & Saving Transcripts**
- **Edit text freely.**  
- **Search & Replace:** `Edit > Search and Replace`  
- **Save transcript:** `File > Save` (`.txt` format).  

---

## **🖥 Compiling for Windows**
1. **Install PyInstaller:**  
   ```bash
   pip install pyinstaller
   ```
2. **Build the executable:**
   ```bash
   pyinstaller --onefile --windowed --name "RizzScript" app.py
   ```
3. **Find the `.exe` in `dist/`**

---

## **🎯 Keyboard Shortcuts**
| Action                 | Shortcut |
|------------------------|---------|
| **Save File**          | `Ctrl + S` |
| **Copy**               | `Ctrl + C` |
| **Cut**                | `Ctrl + X` |
| **Paste**              | `Ctrl + V` |

---

## **🛠 Known Limitations**
- **Text-Only Name Guessing**: Speaker auto‑mapping is based on **text from the transcript**.  
- **Fake Chain-of-Thought Log**: The UI progress log **does not reflect real AI reasoning.** It exists purely for UX feedback.  

---

## **📜 License**
This project is licensed under the **MIT License**. See `LICENSE` for details.  

---

**🎉 Congrats! You’re ready to use RizzScript!** 🚀  
Need help? **Open an issue or submit a pull request!**  

---

### **🔹 Changes from the Original**
- **Clarified File Structure**: Highlighted **important** vs. **ignored** files.  
- **Expanded Usage Guide**: Made it **super clear** how to use **speaker mapping, timestamps, and editing.**  
- **Windows Build Instructions**: Added a PyInstaller guide.  
- **Known Limitations Section**: So users aren’t confused by what’s fake vs. real.  
