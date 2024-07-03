# filename: return_to_launch.py
import asyncio
from mavsdk import System

async def return_to_launch():
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

    print("-- Return to launch complete")

if __name__ == "__main__":
    asyncio.run(return_to_launch())
