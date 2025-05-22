import asyncio
from gpiozero import OutputDevice
from mavsdk import System
from mavsdk.offboard import VelocityNedYaw
from picamera2 import Picamera2
from ultralytics import YOLO
import cv2

# Setup Relay
relay = OutputDevice(27, active_high=False, initial_value=True)

def spray_start():
    print("? [Relay] Spraying Started!")
    relay.off()

def spray_stop():
    print("? [Relay] Spraying Stopped!")
    relay.on()

# Load YOLO model
model = YOLO("/home/dilraj0005/Downloads/best(1).pt")

# Setup PiCamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

async def detect_rose():
    frame = picam2.capture_array()
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    results = model(frame_bgr, conf=0.1)

    # Show annotated preview
    annotated = results[0].plot()
    cv2.imshow("Rose Detection", annotated)
    cv2.waitKey(1)

    return any(model.names[int(cls)].lower() == "Rose" for r in results for cls in r.boxes.cls)

async def handle_detection(drone, yaw):
    try:
        print("? Hovering before ascend...")
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0, 0, 0, yaw))
        await asyncio.sleep(1)

        print("? Ascending by 1 meter...")
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0, 0, -0.5, yaw))
        await asyncio.sleep(2)

        print("? Hovering to Spray...")
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0, 0, 0, yaw))
        spray_start()
        await asyncio.sleep(3)
        spray_stop()

        print("?? Descending back by 1 meter...")
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0, 0, 0.5, yaw))
        await asyncio.sleep(2)

        print("? Hovering before continue...")
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0, 0, 0, yaw))
        await asyncio.sleep(1)

    except Exception as e:
        print(f"?? Error during handle_detection: {e}")

async def fly():
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyACM0:921600")
    print("? Connecting to drone...")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("? Drone connected")
            break

    await drone.action.arm()
    await drone.action.set_takeoff_altitude(2.0)
    await drone.action.takeoff()
    await asyncio.sleep(5)

    print("Sending initial dummy setpoints...")
    for _ in range(10):
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0, 0, 0, 0))
        await asyncio.sleep(0.1)

    await drone.offboard.start()
    print("? Offboard started")

    # === Forward ===
    print("? Moving FORWARD 3m at 0.2 m/s")
    rose_detected_forward = False
    forward_steps = 0

    while forward_steps < 15:
        if not rose_detected_forward and await detect_rose():
            print("? Rose Detected (Forward) ? Pausing to Spray")
            rose_detected_forward = True
            await handle_detection(drone, yaw=0)
            print("?? Resuming forward after spraying...")

        await drone.offboard.set_velocity_ned(VelocityNedYaw(0.2, 0, 0, 0))
        await asyncio.sleep(1)
        forward_steps += 1

    # === Backward ===
    print("?? Moving BACKWARD 3m at 0.2 m/s")
    rose_detected_backward = False
    backward_steps = 0

    while backward_steps < 15:
        if not rose_detected_backward and await detect_rose():
            print("? Rose Detected (Backward) ? Pausing to Spray")
            rose_detected_backward = True
            await handle_detection(drone, yaw=180)
            print("?? Resuming backward after spraying...")

        await drone.offboard.set_velocity_ned(VelocityNedYaw(-0.2, 0, 0, 180))
        await asyncio.sleep(1)
        backward_steps += 1

    print("? Landing...")
    await drone.action.land()
    cv2.destroyAllWindows()

asyncio.run(fly())
