Autonomous Spraying Drone for Rose Detection 🌹

An AI-powered agricultural drone system built for precision spraying. This drone autonomously detects target plants (e.g., Rose flowers) in real time using a YOLOv8 model, hovers over them, activates a GPIO-controlled pump, and resumes its flight — all while navigating a programmed path.


🚀 Overview

This project integrates computer vision with autonomous drone flight using Raspberry Pi 5 and Pixhawk 2.4.8. The Raspberry Pi runs a custom-trained YOLOv8 model on a PiCamera2 video feed. On detecting the "Rose" class with sufficient confidence, the drone hovers, ascends, sprays via a pump, and then resumes its mission using MAVSDK-based waypoint control.


🧠 Key Features

- Real-time object detection with YOLOv8
- Onboard processing with Raspberry Pi 5 (12 FPS)
- MAVSDK-based autonomous navigation
- GPIO-controlled relay spraying system (3-second trigger)
- Hover-align-spray-resume logic
- Modular and expandable to other crops or diseases



🧰 Technologies Used

| Component         | Description                                  |
|-------------------|----------------------------------------------|
| YOLOv8            | Custom-trained model for Rose detection      |
| Raspberry Pi 5    | Companion computer for detection + GPIO      |
| Pixhawk 2.4.8     | Flight controller (PX4 or ArduPilot)         |
| PiCamera2         | For real-time image capture                  |
| MAVSDK (Python)   | For drone mission control                    |
| gpiozero          | GPIO control for spraying system             |
| OpenCV + asyncio  | Detection, visualization, and timing         |



📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/ats-02/autonomous-spraying-drone.git
cd autonomous-spraying-drone
```

2. Install required Python libraries:
```bash
pip install -r requirements.txt
```

3. Place your `best.pt` YOLOv8 weights in the `/models` folder  
   

🛠️ How It Works

1. Drone takes off and moves forward using MAVSDK.
2. PiCamera2 continuously captures frames.
3. YOLOv8 detects "Rose" class with confidence > 0.1.
4. Drone hovers, ascends slightly, and sprays via GPIO relay.
5. After spraying for 3 seconds, it descends and resumes flight.
6. Once the path is completed, the drone lands automatically.


📁 Folder Structure


main.py               # Main script for detection + flight + spraying
models/best.pt        # YOLOv8 trained weights (optional to upload)
media/                # Output image and test video
requirements.txt      # List of Python libraries
README.md             # Project documentation


🌱 Future Scope

- Train model on crop diseases or weed detection
- Add multi-camera support or NDVI sensors
- Build a fleet deployment model for co-operative farming
- Cloud-based dataset updates and field tracking
- Enable real-time dashboard or app for farmers

👤 Contributor

Athul Suresh — Project Lead, Developer & Vision System Integration

Dushyant Panwar — Hardware Integration & Image Labeling

Aditya Nimeshkumar Dalsaniya — Image Processing & Detection Pipeline

Dilraj Singh — Image Processing & Detection Pipeline




