import asyncio
from typing import Annotated
from mavsdk import System

async def takeoff(height: Annotated[float, "Altitude to reach after takeoff"] = 5) ->  Annotated[str, "A message indicating the status"]:
    """
    Takes off the drone to the specified height.

    Parameters:
    height (float): Altitude to reach after takeoff. Default is 5 meters.

    Returns:
    bool: True if takeoff is successful, False otherwise.
    """
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("Drone has a global position estimate")
            break

    print("-- Arming")
    await drone.action.arm()

    print(f"-- Taking off to {height} meters")
    await drone.action.set_takeoff_altitude(height)
    await drone.action.takeoff()

    # Wait for the drone to reach the takeoff altitude
    await asyncio.sleep(10)

    return "Took off"

if __name__ == "__main__":
    import sys

    height = 5  # default height
    if len(sys.argv) > 1:
        try:
            height = float(sys.argv[1])
        except ValueError:
            print("Invalid height value. Using default height of 5 meters.")

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(run(height))
