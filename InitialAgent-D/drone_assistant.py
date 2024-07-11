import os
import subprocess
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv
import openai
import sys
import agentops

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")

if not AGENTOPS_API_KEY:
    raise ValueError("AGENTOPS_API_KEY not found in environment variables")

agentops.init(AGENTOPS_API_KEY)

# Define the mapping of commands to scripts
function_map = {
    "takeoff": "takeoff.py",
    "land": "land.py",
    "go to coordinates": "fly_to_coordinates.py",
    "circle a point": "circle_a_point.py",
    "follow me": "follow_me.py",
    "hover at location": "hover_at_location.py",
    "return to launch": "return_to_launch.py",
    "rotate to specific yaw": "rotate_to_specific_yaw.py",
}

# System message to initialize the assistant
system_message = (
    "You are a drone assistant. You will use transcribed user voice commands to control the drone by calling the appropriate MavSDK python scripts, contained in the function_map. "
    "Respond only with the commands in the correct order required to execute the task, separated by 'and'. "
    "Do not include any explanations or additional text."
)

llm_config = {"model": "gpt-4", "api_key": OPENAI_API_KEY}

@agentops.track_agent(name='drone_assistant')
class DroneAssistant:
    def __init__(self):
        self.assistant = AssistantAgent("assistant", llm_config=llm_config)
        self.user_proxy = UserProxyAgent("user_proxy", code_execution_config=False)

    @agentops.record_function('execute_drone_command')
    def execute_drone_command(self, command, *args):
        if command in function_map:
            script_name = function_map[command]
            script_path = os.path.join(os.getcwd(), script_name)
            if os.path.exists(script_path):
                subprocess.run(["python3", script_path] + list(args))
            else:
                print(f"Script '{script_path}' not found.")
        else:
            print(f"Command '{command}' not recognized.")

    @agentops.record_function('handle_text_input')
    def handle_text_input(self, user_prompt):
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ]
        response = self.assistant.generate_reply(messages=messages).strip()
        commands = response.split(" and ")
        for command in commands:
            command = command.strip()
            if '(' in command and ')' in command:
                cmd_name = command[:command.find('(')].strip()
                args = command[command.find('(') + 1:command.find(')')].split(',')
                args = [arg.strip() for arg in args]
                self.execute_drone_command(cmd_name, *args)
            else:
                self.execute_drone_command(command)

@agentops.record_function('main')
def main():
    drone_assistant = DroneAssistant()
    example_prompt = str(sys.argv[1])
    print(f"Inputting prompt ({example_prompt}) into autogen system.")
    drone_assistant.handle_text_input(example_prompt)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        agentops.log_error(str(e))
        raise
    finally:
        agentops.end_session('Success')