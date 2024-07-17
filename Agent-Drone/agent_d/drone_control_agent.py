from string import Template
import autogen  # type: ignore
from dotenv import load_dotenv
import os


from agent_d.skills import (
    takeoff, land, fly_to_coordinates, circle_a_point,
    follow_me, return_to_launch, rotate_to_specific_yaw, hover_at_location
)
from agent_d.utils.helper_functions import example_helper
from agent_d.utils.prompts import LLM_PROMPTS

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class DroneControlAgent:
    def __init__(self, config_list, user_proxy_agent): # type: ignore
        self.user_proxy_agent = user_proxy_agent
        user_ltm = self.__get_ltm()
        system_message = LLM_PROMPTS["DRONE_AGENT_PROMPT"]

        if user_ltm:
            user_ltm = "\n" + user_ltm
            system_message = Template(system_message).substitute(basic_user_information=user_ltm)
        
        self.agent = autogen.AssistantAgent(
            name="drone_control_agent",
            system_message=system_message,
            
            llm_config={
                "config_list": [{"model": "gpt-4", "api_key": OPENAI_API_KEY}],
                "cache_seed": 2,
                "temperature": 0.0
            },
        )

        self.user_proxy_agent = autogen.UserProxyAgent(
            name="user_proxy_agent",
            is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("##TERMINATE##"),
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            code_execution_config={
                "work_dir": "coding",
                "use_docker": False,
            },
        )

        self.__register_skills()


    def __get_ltm(self):
        return None

    def __register_skills(self):
        self.user_proxy_agent.register_for_execution()(takeoff.takeoff)
        self.agent.register_for_llm(description="Take off the drone.")(takeoff.takeoff)

        self.user_proxy_agent.register_for_execution()(land.land)
        self.agent.register_for_llm(description="Land the drone.")(land.land)

        self.user_proxy_agent.register_for_execution()(fly_to_coordinates.fly_to)
        self.agent.register_for_llm(description="Fly the drone to specified coordinates.")(fly_to_coordinates.fly_to)

        self.user_proxy_agent.register_for_execution()(circle_a_point.circle_a_point)
        self.agent.register_for_llm(description="Circle the drone around a specific point.")(circle_a_point.circle_a_point)

        self.user_proxy_agent.register_for_execution()(follow_me.follow_me)
        self.agent.register_for_llm(description="Follow a moving object.")(follow_me.follow_me)

        self.user_proxy_agent.register_for_execution()(return_to_launch.return_to_launch)
        self.agent.register_for_llm(description="Return the drone to the launch point.")(return_to_launch.return_to_launch)

        self.user_proxy_agent.register_for_execution()(rotate_to_specific_yaw.rotate_to_yaw)
        self.agent.register_for_llm(description="Rotate the drone to a specific yaw angle.")(rotate_to_specific_yaw.rotate_to_yaw)

        self.user_proxy_agent.register_for_execution()(hover_at_location.hover_at_location)
        self.agent.register_for_llm(description="Hover the drone at a specific location.")(hover_at_location.hover_at_location)

        # self.user_proxy_agent.register_reply(
        #     [autogen.Agent, None],
        #     # reply_func=self.print_message_from_user_proxy,
        #     config={"callback": None},
        # )
        # self.agent.register_reply(
        #     [autogen.Agent, None],
        #     # reply_func=self.print_message_from_agent,
        #     config={"callback": None},
        # )

    def print_message_from_user_proxy(self, *args, **kwargs):
        pass

    def print_message_from_agent(self, *args, **kwargs):
        pass

    async def run_conversation(self):
        while True:
            user_input = input("Enter your command: ")
            if user_input.lower() == "exit":
                break
            # response = await self.agent.chat({"content": user_input})

            result=await self.user_proxy_agent.a_initiate_chat(  # noqa: F704
            self.agent,
            message=user_input,
            cache=None)

            summary = result.summary
            response = { 'type':'answer', 'content': summary }
            print(f"Agent response: {response}")
