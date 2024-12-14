import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk  # For the progress bar
import os
import json
import assemblyai as aai
import threading

# Default config file path
CONFIG_FILE = "config.json"

# Load or create configuration
# This function checks if the configuration file exists.
# If not, it creates a default configuration file with an empty API key.
def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config({"api_key": ""})  # Create default config if missing
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# Save the configuration to the config file.
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# Fetch API key from the configuration file.
# If the API key is missing, show an error message.
config = load_config()
API_KEY = config.get("api_key", "")
if not API_KEY:
    messagebox.showerror("Configuration Error", "API key is missing! Please update your settings.")
aai.settings.api_key = API_KEY

# Update the AssemblyAI API key through a dialog box.
def update_api_key():
    global API_KEY
    # Prompt the user for a new API key.
    new_key = simpledialog.askstring("AssemblyAI API Key", "Enter your AssemblyAI API Key:")
    if new_key:
        config["api_key"] = new_key  # Update the key in the config.
        save_config(config)  # Save the updated configuration.
        API_KEY = new_key
        aai.settings.api_key = API_KEY  # Apply the new key.
        messagebox.showinfo("Success", "API key updated successfully!")

# Search and replace functionality for the text area.
def search_and_replace():
    # Prompt the user for the search term.
    search_text = simpledialog.askstring("Search and Replace", "Enter the text to search:")
    if not search_text:
        return
    # Prompt the user for the replacement text.
    replace_text = simpledialog.askstring("Replace", "Enter the replacement text:")
    if replace_text is None:  # Allow cancel for replace
        return

    # Replace all occurrences of the search text with the replacement text in the text area.
    content = text_area.get("1.0", tk.END)
    replaced_content = content.replace(search_text, replace_text)
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", replaced_content)
    messagebox.showinfo("Success", f"Replaced all occurrences of '{search_text}' with '{replace_text}'.")

# Transcription logic using AssemblyAI.
def transcribe_audio(file_path):
    update_status("Uploading and transcribing file...")  # Update the status label.
    start_progress()  # Start the progress bar.
    try:
        transcriber = aai.Transcriber()
        # Configure transcription to include speaker labels.
        config = aai.TranscriptionConfig(speaker_labels=True)
        transcript = transcriber.transcribe(file_path, config=config)  # Perform transcription.
        stop_progress()  # Stop the progress bar.
        update_status("Transcription complete!")
        # Insert the transcription results into the text area.
        for utterance in transcript.utterances:
            text_area.insert(tk.END, f"Speaker {utterance.speaker}: {utterance.text}\n")
    except Exception as e:
        stop_progress()
        messagebox.showerror("Transcription Failed", f"An error occurred: {str(e)}")
        update_status("Transcription failed.")

# Open an audio file and start transcription in a separate thread.
def open_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
    if file_path:
        threading.Thread(target=transcribe_audio, args=(file_path,)).start()

# Save the current content of the text area to a file.
def save_file(event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get("1.0", tk.END))
        messagebox.showinfo("File Saved", f"File saved to {file_path}")

# Toggle word wrap in the text area.
def toggle_wrap():
    if text_area.cget("wrap") == "none":
        text_area.config(wrap="word")
    else:
        text_area.config(wrap="none")

# Update the status label with a message.
def update_status(message):
    status_label.config(text=message)

# Start the progress bar animation.
def start_progress():
    progress.start(10)  # Increment every 10ms.

# Stop the progress bar animation.
def stop_progress():
    progress.stop()

# Main GUI setup.
root = tk.Tk()
root.title("RizzScript")
root.geometry("800x600")  # Set the initial window size.

frame = tk.Frame(root)
frame.pack(fill='both', expand=True)  # Make the frame resizable.

# Text area for displaying and editing text.
text_area = tk.Text(frame)
text_area.pack(side='left', fill='both', expand=True)

# Vertical scrollbar for the text area.
scrollbar = tk.Scrollbar(frame, orient='vertical', command=text_area.yview)
scrollbar.pack(side='right', fill='y')
text_area['yscrollcommand'] = scrollbar.set

# Status label at the bottom of the window.
status_label = tk.Label(root, text="Welcome to RizzScript", anchor="w", bg="lightgrey")
status_label.pack(fill='x', side='bottom')

# Progress bar at the bottom of the window.
progress = ttk.Progressbar(root, mode='indeterminate')
progress.pack(fill='x', side='bottom')

# Menu bar setup.
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu with options to open, save, and update API key.
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open Audio File", command=open_audio_file)
file_menu.add_command(label="AssemblyAI API Key", command=update_api_key)
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Exit", command=root.quit)

# Edit menu with copy, cut, paste, and search/replace functionality.
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy", command=lambda: root.focus_get().event_generate('<<Copy>>'), accelerator="Ctrl+C")
edit_menu.add_command(label="Cut", command=lambda: root.focus_get().event_generate('<<Cut>>'), accelerator="Ctrl+X")
edit_menu.add_command(label="Paste", command=lambda: root.focus_get().event_generate('<<Paste>>'), accelerator="Ctrl+V")
edit_menu.add_command(label="Search and Replace", command=search_and_replace)

# View menu with word wrap toggle.
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Toggle Word Wrap", command=toggle_wrap)

# Keyboard shortcuts for common operations.
root.bind("<Control-s>", save_file)
root.bind("<Control-c>", lambda event: root.focus_get().event_generate('<<Copy>>'))
root.bind("<Control-x>", lambda event: root.focus_get().event_generate('<<Cut>>'))
root.bind("<Control-v>", lambda event: root.focus_get().event_generate('<<Paste>>'))

# Start the main event loop.
root.mainloop()
