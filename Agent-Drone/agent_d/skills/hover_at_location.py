import asyncio
from typing import Annotated
from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw

async def hover_at_location(
    x: Annotated[float, "X coordinate to hover at"] = 0,
    y: Annotated[float, "Y coordinate to hover at"] = 0,
    z: Annotated[float, "Z coordinate (altitude) to hover at"] = 0
) ->  Annotated[str, "A message indicating the status"]:
    """
    Hovers the drone at the specified coordinates.

    Parameters:
    x (float): X coordinate to hover at. Default is 0.
    y (float): Y coordinate to hover at. Default is 0.
    z (float): Z coordinate (altitude) to hover at. Default is 0.

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

    print("Checking if the drone is already in flight...")
    in_air = False
    async for in_air_state in drone.telemetry.in_air():
        in_air = in_air_state
        break

    if not in_air:
        print("-- Arming")
        await drone.action.arm()

        print("-- Taking off")
        await drone.action.takeoff()
        await asyncio.sleep(10)  # Wait for the drone to take off and reach a stable hover

    print(f"-- Setting initial setpoint to hover at ({x}, {y}, {z})")
    await drone.offboard.set_position_ned(PositionNedYaw(x, y, z, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        if not in_air:
            print("-- Disarming")
            await drone.action.disarm()
        return

    print(f"-- Hovering at ({x}, {y}, {z}) indefinitely")
    return f"-- Hovering at ({x}, {y}, {z}) indefinitely"

    # Indefinite hover, awaiting the next command
    while True:
        await asyncio.sleep(1)

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

    asyncio.run(hover_at_location(x, y, z))
