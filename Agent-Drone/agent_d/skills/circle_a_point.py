import asyncio
import math
from typing import Annotated
from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw

async def circle_a_point(
    radius: Annotated[float, "Radius of the circle"] = 5,
    x_center: Annotated[float, "X coordinate of the center point"] = 0,
    y_center: Annotated[float, "Y coordinate of the center point"] = 0,
    altitude: Annotated[float, "Altitude to maintain during circling"] = 5
) ->  Annotated[str, "A message indicating the status"]:
    """
    Circles the drone around a specific point at a given radius and altitude.

    Parameters:
    radius (float): Radius of the circle. Default is 5 meters.
    x_center (float): X coordinate of the center point. Default is 0.
    y_center (float): Y coordinate of the center point. Default is 0.
    altitude (float): Altitude to maintain during circling. Default is 5 meters.

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

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -altitude, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print(f"-- Circling around point ({x_center}, {y_center}, {altitude}) with radius {radius}")

    # Circle logic: let's assume we want to make a full circle in 36 steps (10 degrees per step)
    steps = 36
    for i in range(steps + 1):  # +1 to make a full circle
        angle = (2 * math.pi / steps) * i
        offset_x = radius * math.cos(angle)
        offset_y = radius * math.sin(angle)
        await drone.offboard.set_position_ned(PositionNedYaw(x_center + offset_x, y_center + offset_y, -altitude, 0.0))
        await asyncio.sleep(1)  # Adjust sleep time for smoothness

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")

    print("-- Circle complete")
    return "Circle complete"

if __name__ == "__main__":
    import sys

    # Set default values
    radius = 5
    x_center = 0
    y_center = 0
    altitude = 5

    # Override default values with provided arguments
    if len(sys.argv) > 1:
        try:
            radius = float(sys.argv[1])
        except ValueError:
            print("Invalid radius value. Using default radius of 5 meters.")
    if len(sys.argv) > 2:
        try:
            x_center = float(sys.argv[2])
        except ValueError:
            print("Invalid x_center value. Using default x_center of 0.")
    if len(sys.argv) > 3:
        try:
            y_center = float(sys.argv[3])
        except ValueError:
            print("Invalid y_center value. Using default y_center of 0.")
    if len(sys.argv) > 4:
        try:
            altitude = float(sys.argv[4])
        except ValueError:
            print("Invalid altitude value. Using default altitude of 5 meters.")

    asyncio.run(circle_a_point(radius, x_center, y_center, altitude))
