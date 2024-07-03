# filename: fly_to_coordinates.py
import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw

async def fly_to(x, y, z):
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
    if len(sys.argv) != 4:
        print("Usage: python3 fly_to_coordinates.py <x> <y> <z>")
        sys.exit(1)
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    z = float(sys.argv[3])
    asyncio.run(fly_to(x, y, z))
