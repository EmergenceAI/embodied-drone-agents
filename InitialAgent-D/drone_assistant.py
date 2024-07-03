import os
import subprocess
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent

load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Define the function map based on your individual skill scripts
function_map = {
    "takeoff": "takeoff.py",
    "land": "land.py",
    "circle around": "circle_a_point.py",
    "follow": "follow_me.py",
    "return": "return_to_launch.py",
    "rotate to yaw": "rotate_to_specific_yaw.py",
    "fly to": "fly_to_coordinates.py",
    "hover": "hover_at_location.py"
}

# Define the AutoGen assistant agent
system_message = (
    "Your task is to analyze the task specified in the natural language input and autonomously map it to the commands in the function map. "
    "Run the corresponding command scripts in the correct order and respond only with the commands in the correct order required to execute the task, separated by 'and'."
    "For example, if the user specifies 'go to the coordinates (10, 3, -10),' you should run the fly_to_coordinates.py script after first taking off, knowing to passing 10, 3, and -10 as parameters for the script, and respond with 'takeoff and fly to (10, 3, -10)'. "
    "You should also understand variations of commands. "
    "For example, 'go to coordinates (10, 3, -10)' is the same as 'go to (10, 3, -10)' or 'fly to (10, 3, -10)', or 'fly to coordinates (10, 3, -10)'"
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

# Start the chat and process the prompts
def start_chat():
    user_prompt = input("Enter drone command: ")  # Dynamic user input
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt}
    ]
    response = assistant.generate_reply(messages=messages).strip()
    commands = response.split(" and ")  # Split multiple commands by "and"
    for command in commands:
        command = command.strip()  # Trim whitespace from the command
        execute_drone_command(command)

# Run the function
start_chat()
