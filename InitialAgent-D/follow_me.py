# filename: follow_me.py
import asyncio
from mavsdk import System
from mavsdk.follow_me import Config, FollowMe

async def follow_me(latitude, longitude, altitude, velocity):
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    follow_me_config = Config(
        min_height_m=10.0,
        follow_distance_m=8.0,
        responsiveness=0.2,
        altitude_mode=Config.AltitudeMode.BEHIND
    )

    await drone.follow_me.set_config(follow_me_config)

    print("-- Arming")
    await drone.action.arm()

    print("-- Starting Follow Me mode")
    await drone.follow_me.start()

    await drone.follow_me.set_target_location(FollowMe.TargetLocation(latitude, longitude, altitude, velocity))

    print("-- Following...")
    await asyncio.sleep(60)

    print("-- Stopping Follow Me mode")
    await drone.follow_me.stop()

    print("-- Follow Me complete")

if __name__ == "__main__":
    import sys
    latitude = float(sys.argv[1])
    longitude = float(sys.argv[2])
    altitude = float(sys.argv[3])
    velocity = float(sys.argv[4])
    asyncio.run(follow_me(latitude, longitude, altitude, velocity))
