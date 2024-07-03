# filename: circle_a_point.py
import asyncio
import sys
import math
from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw

async def circle_a_point(radius, x_center, y_center, altitude):
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

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 circle_a_point.py <radius> <x> <y> <altitude>")
        sys.exit(1)
    radius = float(sys.argv[1])
    x_center = float(sys.argv[2])
    y_center = float(sys.argv[3])
    altitude = float(sys.argv[4])
    asyncio.run(circle_a_point(radius, x_center, y_center, altitude))
