import tkinter as tk
from tkinter import messagebox
import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile
import os
import threading

recording = False
audio_data = []
fs = 44100  # Sampling rate

# Function to start recording
def start_recording():
    global recording
    global audio_data
    audio_data = []  # Reset audio data
    recording = True
    messagebox.showinfo("Recording", "Recording started. Click OK to start speaking.")
    threading.Thread(target=record_audio).start()

def record_audio():
    global recording
    global audio_data
    while recording:
        data = sd.rec(int(1 * fs), samplerate=fs, channels=1, dtype=np.int16)
        sd.wait()
        audio_data.extend(data)

# Function to stop recording
def stop_recording():
    global recording
    recording = False
    messagebox.showinfo("Recording", "Recording stopped.")
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    write(temp_file.name, fs, np.array(audio_data, dtype=np.int16))
    transcribe_audio(temp_file.name)
    os.remove(temp_file.name)

# Function to transcribe audio using Whisper AI
def transcribe_audio(temp_file):
    model = whisper.load_model("base")
    result = model.transcribe(temp_file)
    transcription = result["text"]
    print("Transcription:", transcription)  # Print transcription in the terminal
    transcription_text.set(transcription)

# Main application window
app = tk.Tk()
app.title("Voice to Text with Whisper AI")

# Create start and stop buttons
start_button = tk.Button(app, text="Start Recording", command=start_recording)
start_button.pack(pady=10)

stop_button = tk.Button(app, text="Stop Recording", command=stop_recording)
stop_button.pack(pady=10)

# Label and text box for transcription
transcription_label = tk.Label(app, text="Transcription:")
transcription_label.pack(pady=10)

transcription_text = tk.StringVar()
transcription_entry = tk.Entry(app, textvariable=transcription_text, width=50)
transcription_entry.pack(pady=10)

# Run the application
app.mainloop()
