#LANDING SCRIPT (AUTONOMOUS)

import asyncio
import math
import threading

from mavsdk import System
from mavsdk.offboard import PositionNedYaw, OffboardError

class DroneController:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.drone = System()

        self.thread = threading.Thread(
            target=self.start_loop,
            daemon=True
        )
        self.thread.start()

    def start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def connect_drone(self):
        await self.drone.connect(system_address="udpin://0.0.0.0:14540")

        print("Waiting for drone connection...")

        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print("Drone connected!")
                return

    def connect(self):
        future = asyncio.run_coroutine_threadsafe(
            self.connect_drone(),
            self.loop
        )
        return future.result()

    async def arm_async(self):
        print("Arming...")
        await self.drone.action.arm()

    def arm(self):
        future = asyncio.run_coroutine_threadsafe(
            self.arm_async(),
            self.loop
        )
        return future.result()

    async def takeoff_async(self):
        print("Taking off...")
        await self.drone.action.takeoff()

    def takeoff(self):
        future = asyncio.run_coroutine_threadsafe(
            self.takeoff_async(),
            self.loop
        )
        return future.result()

    async def land_async(self):
        print("Landing...")
        await self.drone.action.land()

    def land(self):
        future = asyncio.run_coroutine_threadsafe(
            self.land_async(),
            self.loop
        )
        return future.result()

    async def wait_until_takeoff_async(self, target_altitude=1.21):

        print("Waiting to reach takeoff altitude...")

        async for pos in self.drone.telemetry.position_velocity_ned():

            altitude = -pos.position.down_m

            print(f"Altitude: {altitude:.2f} ", end="\r")

            if altitude >= target_altitude:
                print(f"\nReached altitude ({altitude:.2f} m)")
                return


    def wait_until_takeoff(self):
        future = asyncio.run_coroutine_threadsafe(
            self.wait_until_takeoff_async(),
            self.loop
        )
        return future.result()

    async def wait_until_landed_async(self):

        async for in_air in self.drone.telemetry.in_air():

            if not in_air:
                print("Landing complete.")
                return

            await asyncio.sleep(0.2)

    def wait_until_landed(self):
        future = asyncio.run_coroutine_threadsafe(
            self.wait_until_landed_async(),
            self.loop
        )
        return future.result()

    async def hover_offboard_async(self):

        print("Sending initial setpoint...")

        async for pos in self.drone.telemetry.position_velocity_ned():
            north = pos.position.north_m
            east = pos.position.east_m
            down = pos.position.down_m
            break

        print(f"Current position: {north:.2f}, {east:.2f}, {down:.2f}")

        await self.drone.offboard.set_position_ned(
            PositionNedYaw(
                north,
                east,
                down,
                0.0
            )
        )

        print("Starting Offboard...")

        try:
            await self.drone.offboard.start()

        except OffboardError as error:
            print(f"Offboard failed: {error}")
            return

        TARGET_NORTH = 2.0
        TARGET_EAST = 4.0
        #2,4 lands it at the intended helipad at 5,3
        
        
        TOLERANCE = 0.05
        #can be further decreased

        print("Flying to helipad...")

        await self.drone.offboard.set_position_ned(
            PositionNedYaw(
                TARGET_NORTH,
                TARGET_EAST,
                down,
                0.0
            )
        )

        while True:

            async for pos in self.drone.telemetry.position_velocity_ned():
                north = pos.position.north_m
                east = pos.position.east_m
                break

            error = math.sqrt(
                (TARGET_NORTH - north) ** 2 +
                (TARGET_EAST - east) ** 2
            )

            print(f"Distance to target: {error:.2f} m", end="\r")

            if error < TOLERANCE:
                print("\nReached helipad.")
                break

            await asyncio.sleep(0.1)

    def hover_offboard(self):
        future = asyncio.run_coroutine_threadsafe(
            self.hover_offboard_async(),
            self.loop
        )
        return future.result()


controller = DroneController()

print("Connecting...")
controller.connect()

asyncio.run(asyncio.sleep(1))
controller.arm()

asyncio.run(asyncio.sleep(1))
controller.takeoff()
controller.wait_until_takeoff()

print("Starting Hover Offboard...")
controller.hover_offboard()

controller.land()
controller.wait_until_landed()

print("Mission Complete.")