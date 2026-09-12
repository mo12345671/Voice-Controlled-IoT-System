Voice-Controlled IoT System

A voice-controlled IoT system built using Python, MQTT, HiveMQ Cloud, and Raspberry Pi 3. The system allows users to control a door and different areas using voice commands while monitoring temperature and humidity through a DHT11 sensor.

📌 Project Overview

This project connects a computer-based voice recognition system with a Raspberry Pi through MQTT.

The user speaks a command through a microphone. The publisher.py program recognizes the command, converts it into a JSON message, and publishes it to HiveMQ Cloud.

The Raspberry Pi runs receiver.py, which subscribes to the MQTT topic and performs the requested action using GPIO-controlled hardware.

System Architecture
✨ Features
🎙️ Voice-controlled operation
📡 MQTT communication using HiveMQ Cloud
🔐 Secure MQTT connection using TLS
🚪 Servo-controlled door
🟢 Green LED control
🔵 Blue LED control
🔴 Red LED control
🌡️ DHT11 temperature monitoring
💧 DHT11 humidity monitoring
🖥️ 16×2 I2C LCD display
🔄 Real-time communication between publisher and Raspberry Pi
🎤 Voice Commands
Voice Command	Action
Open Door	Opens the door and turns on all LEDs for 5 seconds
Open Green	Turns on Green LED only
Open Blue	Turns on Blue LED only
Open Red	Turns on Red LED only
Getting out	Opens the door for 5 seconds, then closes it
Exit	Stops the publisher
Example

When the user says:

The publisher sends:

The Raspberry Pi receives the message and turns on the Green LED.

🛠️ Hardware Components
Raspberry Pi 3
Servo Motor
DHT11 Temperature & Humidity Sensor
Green LED
Blue LED
Red LED
220Ω–330Ω resistors
16×2 I2C LCD
Jumper wires
Breadboard
Suitable power supply for the servo
🔌 GPIO Connections

The project uses BCM GPIO numbering.

Component	Raspberry Pi GPIO
Servo Signal	GPIO 27
Green LED	GPIO 16
Blue LED	GPIO 20
Red LED	GPIO 21
DHT11 DATA	GPIO 22
LCD SDA	GPIO 2
LCD SCL	GPIO 3
LCD I2C Address	0x27
DHT11
LCD
Servo

Make sure the servo has a suitable power source and shares a common ground with the Raspberry Pi.

💻 Software
Technologies
Python 3
MQTT
HiveMQ Cloud
Paho MQTT
SpeechRecognition
Raspberry Pi GPIO
Adafruit CircuitPython DHT
RPLCD
I2C
TLS
📁 Project Structure
publisher.py

The publisher runs on the computer and is responsible for:

Listening to the microphone
Converting speech to text
Detecting the requested command
Creating a JSON message
Publishing the command to HiveMQ
receiver.py

The receiver runs on the Raspberry Pi and is responsible for:

Connecting to HiveMQ
Subscribing to the MQTT topic
Receiving commands
Controlling the servo
Controlling the LEDs
Reading DHT11 data
Updating the LCD
📦 Installation
Publisher PC

Install the required packages:

If you're using a virtual environment:

Activate it on Windows:

Then:

🍓 Raspberry Pi Installation

Create/activate your virtual environment:

Install the required libraries:

🔐 Environment Variables

Create a .env file:

Do not upload the .env file to GitHub.

Use .env.example instead:

🚫 .gitignore

Create a .gitignore file:

This prevents your virtual environment and MQTT credentials from being uploaded.

☁️ MQTT Configuration

The project uses HiveMQ Cloud as the MQTT broker.

The main topic is:

Publisher

Publishes commands to:

Receiver

Subscribes to:

Communication uses:

📩 MQTT Message Examples
Open Door
Green Area
Blue Area
Red Area
Getting Out
🚪 Door Operation

When the user says:

The following sequence happens:

For:

the sequence is:

💡 LED Control

Each area is controlled independently.

Green
Blue
Red
🌡️ DHT11 + LCD

The DHT11 is connected to:

The LCD displays the current system status.

Green Area
Blue Area
Red Area
Door
▶️ How to Run
Step 1 — Start the Receiver

On the Raspberry Pi:

You should see:

Step 2 — Start the Publisher

On the computer:

You should see:

Then say one of the supported commands.

🧪 Example Workflow
🔒 Security

The MQTT connection uses TLS on port 8883.

Credentials are stored in .env and should never be committed to GitHub.

Never publish:

🚀 Future Improvements

Possible improvements for future versions:

Add more voice commands
Add a web dashboard
Add remote monitoring
Store temperature and humidity data
Add motion detection
Add authentication for commands
Add multiple Raspberry Pi nodes
Add mobile application control
Improve MQTT error handling
Add asynchronous command processing
🎓 Project Context

This project was developed as part of the Samsung Innovation Campus learning experience, applying concepts related to Industrial IoT, MQTT communication, embedded systems, sensors, and actuators.

👥 Team

Built as a team project with a focus on practical IoT communication and hardware control.
