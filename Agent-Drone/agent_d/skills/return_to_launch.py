import asyncio
from mavsdk import System

async def return_to_launch():
    """
    Returns the drone to its launch location.

    Returns:
    bool: True if the operation is successful, False otherwise.
    """
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected")
            break

    print("-- Returning to launch")
    await drone.action.return_to_launch()

    # Wait for the drone to return to the launch location and land
    await asyncio.sleep(30)

    p
