LLM_PROMPTS = {
    "USER_AGENT_PROMPT": "A proxy for the user for executing the user commands.",

    "DRONE_AGENT_PROMPT": (
        "You will perform drone control tasks in a simulated environment. "
        "Use the provided commands to control the drone. Ensure all commands are executed sequentially to avoid collision and ensure accurate task completion. "
        "If you need additional user input, request it directly. "
        "Execute actions sequentially to avoid navigation timing issues. Once a task is completed, confirm completion with ##TERMINATE##. "
        "Do not solicit further user requests. If user response is lacking, terminate the conversation with ##TERMINATE##.$basic_user_information"
    ),

    "TAKEOFF_PROMPT": (
        "This skill takes off the drone. Ensure that the drone reaches a safe altitude and hovers stably before completing the task. "
        "Returns True if the takeoff is successful or an appropriate error message if it fails."
    ),

    "LAND_PROMPT": (
        "This skill lands the drone safely. Ensure the drone descends gradually and lands stably before completing the task. "
        "Returns True if the landing is successful or an appropriate error message if it fails."
    ),

    "FLY_TO_COORDINATES_PROMPT": (
        "This skill flies the drone to the specified coordinates (x, y, z). Ensure the drone reaches the exact coordinates and hovers stably before completing the task. "
        "Returns True if the flight is successful or an appropriate error message if it fails."
    ),

    "CIRCLE_A_POINT_PROMPT": (
        "This skill circles the drone around a specific point at a given radius. Ensure the drone maintains a stable altitude and follows a circular path accurately. "
        "Returns True if the circling is successful or an appropriate error message if it fails."
    ),

    "FOLLOW_ME_PROMPT": (
        "This skill makes the drone follow a moving object or person. Ensure the drone maintains a safe distance and follows the target smoothly. "
        "Returns True if the follow-me action is successful or an appropriate error message if it fails."
    ),

    "RETURN_TO_LAUNCH_PROMPT": (
        "This skill returns the drone to its launch point. Ensure the drone follows a safe path and lands accurately at the launch point. "
        "Returns True if the return to launch is successful or an appropriate error message if it fails."
    ),

    "ROTATE_TO_SPECIFIC_YAW_PROMPT": (
        "This skill rotates the drone to a specific yaw angle. Ensure the drone rotates smoothly and maintains its position after the rotation. "
        "Returns True if the rotation is successful or an appropriate error message if it fails."
    ),

    "HOVER_AT_LOCATION_PROMPT": (
        "This skill makes the drone hover at a specific location. Ensure the drone maintains a stable hover at the given coordinates. "
        "Returns True if the hover is successful or an appropriate error message if it fails."
    )
}
