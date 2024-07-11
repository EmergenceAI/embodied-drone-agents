import os
import asyncio
from dotenv import load_dotenv
import openai
import agentops
from agent_d.drone_control_agent import DroneControlAgent

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key and AgentOps API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")

if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

if AGENTOPS_API_KEY is None:
    raise ValueError("AgentOps API key not found. Please set it in the .env file.")

# Initialize AgentOps
agentops.init(AGENTOPS_API_KEY)

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

@agentops.track_agent(name='drone-control-agent')
class TrackedDroneControlAgent(DroneControlAgent):
    @agentops.record_function('run')
    async def run(self):
        return await super().run()

@agentops.record_function('main')
def main():
    # Initialize the TrackedDroneControlAgent
    agent = TrackedDroneControlAgent(config_list=[], user_proxy_agent=None)
    
    # Run the agent
    asyncio.run(agent.run())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        agentops.log_error(str(e))
        raise
    finally:
        agentops.end_session('Success')