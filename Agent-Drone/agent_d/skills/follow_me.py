import asyncio
from typing import Annotated
from mavsdk import System
from mavsdk.follow_me import Config, FollowMe

async def follow_me(
    latitude: Annotated[float, "Latitude of the target location"] = 0.0,
    longitude: Annotated[float, "Longitude of the target location"] = 0.0,
    altitude: Annotated[float, "Altitude of the target location"] = 10.0,
    velocity: Annotated[float, "Velocity of the target"] = 1.0
):
    """
    Follows the specified target location with given latitude, longitude, altitude, and velocity.

    Parameters:
    latitude (float): Latitude of the target location. Default is 0.0.
    longitude (float): Longitude of the target location. Default is 0.0.
    altitude (float): Altitude of the target location. Default is 10.0 meters.
    velocity (float): Velocity of the target. Default is 1.0 m/s.

    Returns:
    bool: True if the operation is successful, False otherwise.
    """
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected():
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

    # Set default values
    latitude = 0.0
    longitude = 0.0
    altitude = 10.0
    velocity = 1.0

    # Override default values with provided arguments
    if len(sys.argv) > 1:
        try:
            latitude = float(sys.argv[1])
        except ValueError:
            print("Invalid latitude value. Using default latitude of 0.0.")
    if len(sys.argv) > 2:
        try:
            longitude = float(sys.argv[2])
        except ValueError:
            print("Invalid longitude value. Using default longitude of 0.0.")
    if len(sys.argv) > 3:
        try:
            altitude = float(sys.argv[3])
        except ValueError:
            print("Invalid altitude value. Using default altitude of 10.0 meters.")
    if len(sys.argv) > 4:
        try:
            velocity = float(sys.argv[4])
        except ValueError:
            print("Invalid velocity value. Using default velocity of 1.0 m/s.")

    asyncio.run(follow_me(latitude, longitude, altitude, velocity))
