# drone_assistant.py
import os
import subprocess
from autogen import AssistantAgent, UserProxyAgent

from dotenv import load_dotenv
import openai 

load_dotenv() 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define the mapping of commands to scripts
function_map = {
    "takeoff": "takeoff.py",
    "land": "land.py",
    "go to coordinates": "fly_to_coordinates.py",
}

# System message to initialize the assistant
system_message = (
    "You are a drone assistant. You will use transcribed user voice commands to control the drone by calling the appropriate MavSDK python scripts, contained in the function_map."
    "Respond only with the commands in the correct order required to execute the task, separated by 'and'."
    "Do not include any explanations or additional text."
)

llm_config = {"model": "gpt-4", "api_key": OPENAI_API_KEY}
assistant = AssistantAgent("assistant", llm_config=llm_config)

# Create a user proxy agent to handle the user prompts
user_proxy = UserProxyAgent("user_proxy", code_execution_config=False)

# Function to execute the mapped skill script with parameters
def execute_drone_command(command, **params):
    if command in function_map:
        script_name = function_map[command]
        script_path = os.path.join(os.getcwd(), script_name)
        if os.path.exists(script_path):
            subprocess.run(["python3", script_path] + [str(value) for value in params.values()])
        else:
            print(f"Script '{script_path}' not found.")
    else:
        print(f"Command '{command}' not recognized.")

# Function to handle text input and execute commands
def handle_text_input(user_prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt}
    ]
    response = assistant.generate_reply(messages=messages).strip()
    commands = response.split(" and ")
    for command in commands:
        command = command.strip()
        execute_drone_command(command)

# Example of how to use the handle_text_input function
if __name__ == "__main__":
    example_prompt = "takeoff and fly to coordinates (10, 3, -10)"
    handle_text_input(example_prompt)
