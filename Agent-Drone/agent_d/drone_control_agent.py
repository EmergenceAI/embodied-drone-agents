from string import Template
import autogen  # type: ignore

from agent_d.skills import (
    takeoff, land, fly_to_coordinates, circle_a_point,
    follow_me, return_to_launch, rotate_to_specific_yaw, hover_at_location
)
from agent_d.utils.helper_functions import example_helper
from agent_d.utils.prompts import LLM_PROMPTS

class DroneControlAgent:
    def __init__(self, config_list, user_proxy_agent: autogen.UserProxyAgent): # type: ignore
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
                "config_list": config_list,
                "cache_seed": 2,
                "temperature": 0.0
            },
        )
        self.__register_skills()

    def __get_ltm(self):
        return None

    def __register_skills(self):
        self.user_proxy_agent.register_for_execution()(takeoff.run)
        self.agent.register_for_llm(description="Take off the drone.")(takeoff.run)

        self.user_proxy_agent.register_for_execution()(land.run)
        self.agent.register_for_llm(description="Land the drone.")(land.run)

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

        self.user_proxy_agent.register_for_execution()(example_helper)
        self.agent.register_for_llm(description="Example helper function.")(example_helper)

        self.user_proxy_agent.register_reply(
            [autogen.Agent, None],
            reply_func=self.print_message_from_user_proxy,
            config={"callback": None},
        )
        self.agent.register_reply(
            [autogen.Agent, None],
            reply_func=self.print_message_from_agent,
            config={"callback": None},
        )

    def print_message_from_user_proxy(self, *args, **kwargs):
        pass

    def print_message_from_agent(self, *args, **kwargs):
        pass
