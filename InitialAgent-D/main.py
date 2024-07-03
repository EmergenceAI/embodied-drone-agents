# main.py
import voice_to_text
import drone_assistant

def main():
    print("Please record your voice command:")
    transcription = voice_to_text.run_voice_to_text_app()
    print(f"Transcription received: {transcription}")
    drone_assistant.handle_text_input(transcription)

if __name__ == "__main__":
    main()
