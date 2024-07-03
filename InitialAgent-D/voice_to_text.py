# voice_to_text.py
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
transcription_text = None

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
    transcription = transcribe_audio(temp_file.name)
    os.remove(temp_file.name)
    transcription_text.set(transcription)

# Function to transcribe audio using Whisper AI
def transcribe_audio(temp_file):
    model = whisper.load_model("base")
    result = model.transcribe(temp_file)
    transcription = result["text"]
    return transcription

# Function to initialize and run the GUI
def run_voice_to_text_app():
    global transcription_text
    app = tk.Tk()
    app.title("Voice to Text with Whisper AI")

    start_button = tk.Button(app, text="Start Recording", command=start_recording)
    start_button.pack(pady=10)

    stop_button = tk.Button(app, text="Stop Recording", command=stop_recording)
    stop_button.pack(pady=10)

    transcription_label = tk.Label(app, text="Transcription:")
    transcription_label.pack(pady=10)

    transcription_text = tk.StringVar()
    transcription_entry = tk.Entry(app, textvariable=transcription_text, width=50)
    transcription_entry.pack(pady=10)

    app.mainloop()

    return transcription_text.get()

if __name__ == "__main__":
    run_voice_to_text_app()
