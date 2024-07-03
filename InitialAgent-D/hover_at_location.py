# filename: hover_at_location.py
import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw

async def hover_at_location(x, y, z):
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

    # Indefinite hover, awaiting the next command
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python3 hover_at_location.py <x> <y> <z>")
        sys.exit(1)
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    z = float(sys.argv[3])
    asyncio.run(hover_at_location(x, y, z))
