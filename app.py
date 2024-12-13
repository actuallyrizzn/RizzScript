import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # For the progress bar
import os
import time
import requests
import threading

# AssemblyAI API key
API_KEY = 'cda2a47b8d0b4b8fa3aed6f717eb8ce2'

headers = {'authorization': API_KEY}

def upload_audio(file_path):
    try:
        with open(file_path, 'rb') as f:
            response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, files={'file': f})
        response.raise_for_status()
        return response.json()['upload_url']
    except Exception as e:
        messagebox.showerror("Upload Failed", f"An error occurred while uploading the file: {str(e)}")
        return None

def request_transcription(audio_url):
    try:
        data = {'audio_url': audio_url}
        response = requests.post('https://api.assemblyai.com/v2/transcript', json=data, headers=headers)
        response.raise_for_status()
        return response.json()['id']
    except Exception as e:
        messagebox.showerror("Transcription Request Failed", f"An error occurred while requesting transcription: {str(e)}")
        return None

def get_transcription_result(transcript_id):
    try:
        url = f'https://api.assemblyai.com/v2/transcript/{transcript_id}'
        while True:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            status = result['status']
            update_status(f"Transcription status: {status}")
            print(f"DEBUG: Status: {status}, Response: {result}")
            if status == 'completed':
                stop_progress()
                update_status("Transcription complete!")
                return result['text']
            elif status == 'failed':
                stop_progress()
                messagebox.showerror("Transcription Failed", "The transcription process failed.")
                update_status("Transcription failed.")
                return None
            time.sleep(3)
    except Exception as e:
        stop_progress()
        messagebox.showerror("Transcription Failed", f"An error occurred while checking transcription status: {str(e)}")
        return None

def transcribe_audio(file_path):
    update_status("Uploading audio file...")
    start_progress()
    audio_url = upload_audio(file_path)
    if audio_url:
        update_status("Requesting transcription...")
        transcript_id = request_transcription(audio_url)
        if transcript_id:
            update_status("Waiting for transcription to complete...")
            transcript_text = get_transcription_result(transcript_id)
            if transcript_text:
                text_area.insert(tk.END, transcript_text + "\n")
        else:
            stop_progress()
            update_status("Transcription request failed.")
    else:
        stop_progress()
        update_status("Audio upload failed.")

def open_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
    if file_path:
        threading.Thread(target=transcribe_audio, args=(file_path,)).start()

def save_file(event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get("1.0", tk.END))
        messagebox.showinfo("File Saved", f"File saved to {file_path}")

def toggle_wrap():
    if text_area.cget("wrap") == "none":
        text_area.config(wrap="word")
    else:
        text_area.config(wrap="none")

def update_status(message):
    status_label.config(text=message)

def start_progress():
    progress.start(10)

def stop_progress():
    progress.stop()

# Initialize the main window
root = tk.Tk()
root.title("RizzScript")
root.geometry("800x600")

# Create a frame to hold the text widget and scrollbar
frame = tk.Frame(root)
frame.pack(fill='both', expand=True)

# Text widget for showing results
text_area = tk.Text(frame)
text_area.pack(side='left', fill='both', expand=True)

# Add a scrollbar
scrollbar = tk.Scrollbar(frame, orient='vertical', command=text_area.yview)
scrollbar.pack(side='right', fill='y')
text_area['yscrollcommand'] = scrollbar.set

# Status bar
status_label = tk.Label(root, text="Welcome to RizzScript", anchor="w", bg="lightgrey")
status_label.pack(fill='x', side='bottom')

# Progress bar
progress = ttk.Progressbar(root, mode='indeterminate')
progress.pack(fill='x', side='bottom')

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open Audio File", command=open_audio_file)
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Exit", command=root.quit)

# Create "Edit" menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy", command=lambda: root.focus_get().event_generate('<<Copy>>'), accelerator="Ctrl+C")
edit_menu.add_command(label="Cut", command=lambda: root.focus_get().event_generate('<<Cut>>'), accelerator="Ctrl+X")
edit_menu.add_command(label="Paste", command=lambda: root.focus_get().event_generate('<<Paste>>'), accelerator="Ctrl+V")

# Create "View" menu
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Toggle Word Wrap", command=toggle_wrap)

# Bind hotkeys
root.bind("<Control-s>", save_file)
root.bind("<Control-c>", lambda event: root.focus_get().event_generate('<<Copy>>'))
root.bind("<Control-x>", lambda event: root.focus_get().event_generate('<<Cut>>'))
root.bind("<Control-v>", lambda event: root.focus_get().event_generate('<<Paste>>'))

# Run the main loop
root.mainloop()