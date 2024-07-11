from string import Template
import autogen  # type: ignore
import agentops

from agent_d.skills import (
    takeoff, land, fly_to_coordinates, circle_a_point,
    follow_me, return_to_launch, rotate_to_specific_yaw, hover_at_location
)
from agent_d.utils.helper_functions import example_helper
from agent_d.utils.prompts import LLM_PROMPTS

@agentops.track_agent(name='drone_control_agent')
class DroneControlAgent:
    @agentops.record_function('initialize_drone_control_agent')
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
                "config_list": config_list,
                "cache_seed": 2,
                "temperature": 0.0
            },
        )
        self.__register_skills()

    @agentops.record_function('get_ltm')
    def __get_ltm(self):
        return None

    @agentops.record_function('register_skills')
    def __register_skills(self):
        self.__register_skill(takeoff.run, "Take off the drone.")
        self.__register_skill(land.run, "Land the drone.")
        self.__register_skill(fly_to_coordinates.fly_to, "Fly the drone to specified coordinates.")
        self.__register_skill(circle_a_point.circle_a_point, "Circle the drone around a specific point.")
        self.__register_skill(follow_me.follow_me, "Follow a moving object.")
        self.__register_skill(return_to_launch.return_to_launch, "Return the drone to the launch point.")
        self.__register_skill(rotate_to_specific_yaw.rotate_to_yaw, "Rotate the drone to a specific yaw angle.")
        self.__register_skill(hover_at_location.hover_at_location, "Hover the drone at a specific location.")
        self.__register_skill(example_helper, "Example helper function.")

        self.__register_reply_for_user_proxy()
        self.__register_reply_for_agent()

    @agentops.record_function('register_skill')
    def __register_skill(self, skill, description):
        self.user_proxy_agent.register_for_execution()(skill)
        self.agent.register_for_llm(description=description)(skill)

    @agentops.record_function('register_reply_for_user_proxy')
    def __register_reply_for_user_proxy(self):
        self.user_proxy_agent.register_reply(
            [autogen.Agent, None],
            reply_func=self.print_message_from_user_proxy,
            config={"callback": None},
        )

    @agentops.record_function('register_reply_for_agent')
    def __register_reply_for_agent(self):
        self.agent.register_reply(
            [autogen.Agent, None],
            reply_func=self.print_message_from_agent,
            config={"callback": None},
        )

    @agentops.record_function('print_message_from_user_proxy')
    def print_message_from_user_proxy(self, *args, **kwargs):
        pass

    @agentops.record_function('print_message_from_agent')
    def print_message_from_agent(self, *args, **kwargs):
        pass