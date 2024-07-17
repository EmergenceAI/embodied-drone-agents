import asyncio
from typing import Annotated
from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw

async def rotate_to_yaw(
    yaw: Annotated[float, "Yaw angle to rotate to"] = 0.0
) ->  Annotated[str, "A message indicating the status"]:
    """
    Rotates the drone to the specified yaw angle.

    Parameters:
    yaw (float): Yaw angle to rotate to. Default is 0.0 degrees.

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
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, 0.0))  # Set initial height (e.g., -5 meters)

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print(f"-- Rotating to yaw {yaw}")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, yaw))  # Maintain the same height during rotation

    # Wait for the drone to rotate to the specified yaw
    await asyncio.sleep(5)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")

    print("-- Rotate complete")
    return "-- Rotate complete"

if __name__ == "__main__":
    import sys

    # Set default value
    yaw = 0.0

    # Override default value with provided argument
    if len(sys.argv) > 1:
        try:
            yaw = float(sys.argv[1])
        except ValueError:
            print("Invalid yaw value. Using default yaw of 0.0 degrees.")

    asyncio.run(rotate_to_yaw(yaw))
