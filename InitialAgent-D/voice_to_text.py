# voice_to_text.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
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
def start_recording(event):
    global recording
    global audio_data
    audio_data = []  # Reset audio data
    recording = True
    record_button.config(bg='red')
    threading.Thread(target=record_audio).start()

def record_audio():
    global recording
    global audio_data
    while recording:
        data = sd.rec(int(1 * fs), samplerate=fs, channels=1, dtype=np.int16)
        sd.wait()
        audio_data.extend(data)

# Function to stop recording
def stop_recording(event):
    global recording
    recording = False
    record_button.config(bg='white')
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
    global transcription_text, record_button
    app = tk.Tk()
    app.title("Voice to Text with Whisper AI")

    # Load mic icon image
    mic_image = Image.open("mic_icon.png").resize((50, 50), Image.ANTIALIAS)
    mic_photo = ImageTk.PhotoImage(mic_image)

    record_button = tk.Button(app, image=mic_photo, bg='white', bd=0, highlightthickness=0)
    record_button.bind('<ButtonPress>', start_recording)
    record_button.bind('<ButtonRelease>', stop_recording)
    record_button.pack(pady=20)

    transcription_label = tk.Label(app, text="Transcription:")
    transcription_label.pack(pady=10)

    transcription_text = tk.StringVar()
    transcription_entry = tk.Entry(app, textvariable=transcription_text, width=50)
    transcription_entry.pack(pady=10)

    app.mainloop()

    return transcription_text.get()

if __name__ == "__main__":
    run_voice_to_text_app()
