import os
import asyncio
from dotenv import load_dotenv
import openai
from agent_d.drone_control_agent import DroneControlAgent

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

def main():
    # Initialize the DroneControlAgent
    agent = DroneControlAgent(config_list=[], user_proxy_agent=None)
    
    # Run the agent (assuming run is an asyncio coroutine)
    asyncio.run(agent.run())

if __name__ == "__main__":
    main()
