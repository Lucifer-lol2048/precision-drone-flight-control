#  PX4 PID Tuning & Autonomous Precision Landing

A complete PX4 SITL project demonstrating PID tuning, stable autonomous flight, and precision landing using MAVSDK in a custom Gazebo simulation environment.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PX4](https://img.shields.io/badge/PX4-Autopilot-005571?style=for-the-badge)
![Gazebo](https://img.shields.io/badge/Gazebo-Classic-orange?style=for-the-badge)
![MAVSDK](https://img.shields.io/badge/MAVSDK-Python-blue?style=for-the-badge)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

---

##  Overview

This project was completed as part of the **Precision Drone Flight Control and Landing** challenge conducted by the Aeromodelling Club, IIT Guwahati.

The provided PX4 drone was intentionally unstable. The objective was to:

* Tune the drone's PID parameters for stable flight
* Minimize oscillations and positional drift
* Develop an autonomous landing script using MAVSDK
* Successfully navigate to the designated landing pad and land safely

---

##  Objectives

* Stabilize an unstable PX4 multicopter
* Improve hover performance through PID tuning
* Implement autonomous navigation using Offboard control
* Execute a precise landing inside a cluttered simulation environment

---

##  Technologies Used

* PX4 Autopilot (SITL)
* Gazebo Classic
* MAVSDK-Python
* Python 3
* Ubuntu 22.04 (WSL2)

---

##  PID Tuning

The default controller parameters resulted in noticeable oscillations and unstable hover.

After iterative tuning, the following parameters produced significantly improved stability:

| Parameter       | Value |
| --------------- | ----: |
| MC_ROLL_P       |   6.5 |
| MC_PITCH_P      |   6.5 |
| MPC_Z_P         |  0.80 |
| MPC_Z_VEL_P_ACC |  0.80 |
| MPC_Z_VEL_I_ACC |  0.20 |
| MPC_Z_VEL_D_ACC |  0.00 |

### Improvements Achieved

* Reduced roll and pitch oscillations
* Stable hover
* Reduced positional drift
* Reliable Offboard mode transition
* Smooth autonomous landing

---

##  Autonomous Landing

The MAVSDK script performs the following sequence:

1. Connect to PX4 SITL
2. Wait for a stable connection
3. Arm the drone
4. Take off
5. Switch to Offboard mode
6. Fly to the landing zone
7. Continuously monitor position error
8. Land safely
9. Disarm automatically

The landing routine uses continuous position feedback to determine when the target has been reached before initiating landing.

---

##  Repository Structure

```text
.
├── README.md
├── report/
│   └── PID_Report.pdf
├── src/
│   └── landing_script.py
├── images/
│   ├── environment.png
│   ├── pid_gui.png
│   ├── hover.png
│   └── landing.png
└── docs/
    └── tuned_parameters.md
```

---

##  Getting Started

### Clone the repository

```bash
git clone https://github.com/<your-username>/px4-pid-autonomous-landing.git
cd px4-pid-autonomous-landing
```

### Prerequisites

* Ubuntu 22.04 (or WSL2)
* PX4 Autopilot
* Gazebo Classic
* MAVSDK-Python
* Python 3

### Launch PX4 SITL

```bash
cd PX4-Autopilot
PX4_SITL_WORLD=safe_landing make px4_sitl gazebo-classic
```

### Run the landing script

```bash
python3 src/landing_script.py
```

---

##  Results

The tuned controller successfully achieved:

* Stable hover
* Smooth position control
* Reliable autonomous navigation
* Accurate landing on the designated helipad

  



https://github.com/user-attachments/assets/73ee9b68-6e4f-4604-8ab2-fae5506213c0





---

##  Report

A detailed report describing the PID tuning process, parameter selection, implementation details, and experimental results is available in the `report/` directory.

---

##  Future Improvements

* Vision-based precision landing
* Obstacle avoidance
* Automatic PID optimization
* Mission planning using waypoints
* ROS 2 integration


