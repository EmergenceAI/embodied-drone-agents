import os
from dotenv import load_dotenv
import agentops
import voice_to_text
import drone_assistant

# Load environment variables
load_dotenv()

# Initialize AgentOps
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
if not AGENTOPS_API_KEY:
    raise ValueError("AGENTOPS_API_KEY not found in environment variables")

agentops.init(AGENTOPS_API_KEY)

@agentops.record_function('voice_to_text_transcription')
def get_transcription():
    print("Please record your voice command:")
    return voice_to_text.run_voice_to_text_app()

@agentops.record_function('handle_drone_command')
def process_drone_command(transcription):
    print(f"Transcription received: {transcription}")
    drone_assistant.handle_text_input(transcription)

@agentops.record_function('main')
def main():
    try:
        transcription = get_transcription()
        process_drone_command(transcription)
    except Exception as e:
        agentops.log_error(str(e))
        raise

if __name__ == "__main__":
    try:
        main()
    finally:
        agentops.end_session('Success')