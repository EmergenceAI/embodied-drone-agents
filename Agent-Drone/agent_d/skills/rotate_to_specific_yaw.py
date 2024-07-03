# filename: rotate_to_specific_yaw.py
import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw

async def rotate_to_yaw(yaw):
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

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 rotate_to_specific_yaw.py <yaw>")
        sys.exit(1)
    yaw = float(sys.argv[1])
    asyncio.run(rotate_to_yaw(yaw))
