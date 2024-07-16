import asyncio
from typing import Annotated
from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw

async def fly_to(
    x: Annotated[float, "X coordinate to fly to"] = 0,
    y: Annotated[float, "Y coordinate to fly to"] = 0,
    z: Annotated[float, "Z coordinate (altitude) to fly to"] = 0
):
    """
    Flies the drone to the specified coordinates.

    Parameters:
    x (float): X coordinate to fly to. Default is 0.
    y (float): Y coordinate to fly to. Default is 0.
    z (float): Z coordinate (altitude) to fly to. Default is 0.

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

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print(f"-- Flying to ({x}, {y}, {z})")
    await drone.offboard.set_position_ned(PositionNedYaw(float(x), float(y), -float(z), 0.0))

    # Wait for the drone to reach the target position
    await asyncio.sleep(10)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")

    print("-- Fly to complete")

if __name__ == "__main__":
    import sys

    # Set default values
    x = 0
    y = 0
    z = 0

    # Override default values with provided arguments
    if len(sys.argv) > 1:
        try:
            x = float(sys.argv[1])
        except ValueError:
            print("Invalid x value. Using default x of 0.")
    if len(sys.argv) > 2:
        try:
            y = float(sys.argv[2])
        except ValueError:
            print("Invalid y value. Using default y of 0.")
    if len(sys.argv) > 3:
        try:
            z = float(sys.argv[3])
        except ValueError:
            print("Invalid z value. Using default z of 0.")

    asyncio.run(fly_to(x, y, z))
