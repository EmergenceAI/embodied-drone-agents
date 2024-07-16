import asyncio
from mavsdk import System

async def run():
    """
    Lands the drone at its current location.

    Returns:
    bool: True if landing is successful, False otherwise.
    """
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected")
            break

    print("-- Landing")
    await drone.action.land()

    # Optionally, wait for a few seconds to ensure landing is complete
    await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(run())
