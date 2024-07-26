# Embodied Drone Agents

Welcome to the Embodied Drone Agents project! This repository contains code for creating embodied AI-driven drone agents using the AutoGen framework and MavSDK. Our goal is to enable the conversion of language prompts into parameterized function calls to control drone behavior programmatically.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#example-prompts)
- [Contributing](#contributing)
- [To-Do](#to-do)
- [Acknowledgements](#acknowledgements)

## Introduction

Embodied Drone Agents is a project focused on developing embodied AI agents in drones that can understand and execute complex tasks based on natural language instructions. By leveraging AutoGen for language processing and MavSDK for drone control, we aim to create a seamless interface for drone operation.

## Features

- **Language to Action**: Convert natural language prompts into parameterized function calls.
- **Hierarchial Agent Structure**: Use of high-level planner LLM and executor agent that communicate with each other in order to achieve desired complex behavior.
- **Drone Control**: Utilize MavSDK to control various aspects of drone behavior.
- **Extensibility**: Easily add new commands and behaviors through modular design.
- **Voice capability**: Users can input either voice or text queries into the agent system.

## Installation

To get started with the Embodied Drone Agents project, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/EmergenceAI/embodied-drone-agents.git
   cd embodied-drone-agents
   ```

2. **Install dependencies:**
   Ensure you have Python 3.8+ installed. Then, install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MavSDK:**
   Follow the [MavSDK installation guide](https://mavsdk.mavlink.io/main/en/getting_started/installation.html) to install MavSDK.

## Usage

To use the Embodied Drone Agents, you can run the main script and provide language prompts to control the drone:

```bash
python main.py
```

You can customize the behavior by modifying the configuration files and scripts provided in the `config` and `scripts` directories.

## Example Prompts

Here are a few examples to get you started:

1. **Takeoff and Land:**
   Take off to a height of 10m, and then come back down

2. **Fly to a Specific Location:**
   Fly to coordinates 10, 8, 6. Then, fly to the origin.

3. **Complex Multi-Step Tasks:**
   Fly up, to the left, to the right, and then in a circle

## Contributing

We welcome contributions to the Embodied Drone Agents project! If you have any improvements or new features to add, please follow these steps:

1. **Fork the repository.**
2. **Create a new branch:** `git checkout -b feature-branch`
3. **Commit your changes:** `git commit -m 'Add new feature'`
4. **Push to the branch:** `git push origin feature-branch`
5. **Create a pull request.**

Please ensure your code follows the project's coding standards and includes appropriate tests.

## To-Do

Still need to improve the voice -> text -> query -> autogen -> MavSDK pipeline. Also, find a way to add Gazebo state as recurring input into the high-level planner LLM agent, so that more complex tasks can be achieved.

## Acknowledgements

We would like to thank the following individuals and organizations for their invaluable contributions as we developed this project.
- **Aniketh Arvind** & **Mihir Kulshreshtha**, developers
- **Ashish Jagmohan**, primary supervisor
- **Tamer Abuelsaad**, technical advisor
- **Aditya Vempaty**, technical advisor
- **Deepak Akkil**, technical advisor
- **Ravi Kokku**, technical advisor
- **Emergence AI**, AI agent company
