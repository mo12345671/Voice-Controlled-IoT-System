import os
import ssl
import json
import time

import paho.mqtt.client as mqtt
import speech_recognition as sr
from dotenv import load_dotenv


# =========================
# MQTT SETTINGS
# =========================

load_dotenv()

MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

TOPIC = "voice/commands"


# =========================
# MQTT CLIENT
# =========================

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="voice-publisher"
)

client.username_pw_set(
    MQTT_USERNAME,
    MQTT_PASSWORD
)

client.tls_set(
    cert_reqs=ssl.CERT_REQUIRED
)


print("Connecting to HiveMQ...")

client.connect(
    MQTT_HOST,
    MQTT_PORT,
    60
)

client.loop_start()

print("Connected to HiveMQ!")
print()


# =========================
# SPEECH RECOGNITION
# =========================

recognizer = sr.Recognizer()

recognizer.pause_threshold = 0.8


# =========================
# MICROPHONE
# =========================

with sr.Microphone(device_index=1) as source:

    print("Adjusting microphone...")

    recognizer.adjust_for_ambient_noise(
        source,
        duration=2
    )

    print()
    print("==============================")
    print("Voice System Ready!")
    print("==============================")

    print("Say:")
    print("Open Door")
    print("Open Green")
    print("Open Blue")
    print("Open Red")
    print("Getting out")
    print("Exit")

    print("==============================")
    print()


    # =========================
    # MAIN LOOP
    # =========================

    while True:

        try:

            print("Listening...")

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=5
            )


            # Convert voice to text

            text = recognizer.recognize_google(
                audio,
                language="en-US"
            )

            print("You said:", text)


            # Normalize text

            text = text.lower().strip()


            # =========================
            # EXIT PROGRAM
            # =========================

            if text in ["exit", "quit", "stop"]:

                print("Stopping...")

                break


            # =========================
            # OPEN DOOR
            # =========================

            if text == "open door":

                command = {
                    "action": "open_door"
                }


            # =========================
            # GREEN
            # =========================

            elif "open green" in text:

                command = {
                    "action": "area",
                    "number": 1
                }


            # =========================
            # BLUE
            # =========================

            elif "open blue" in text:

                command = {
                    "action": "area",
                    "number": 2
                }


            # =========================
            # RED
            # =========================

            elif "open red" in text:

                command = {
                    "action": "area",
                    "number": 3
                }


            # =========================
            # GETTING OUT
            # =========================

            elif text == "getting out":

                command = {
                    "action": "exit"
                }


            # =========================
            # UNKNOWN COMMAND
            # =========================

            else:

                print("Unknown command")
                print()

                continue


            # =========================
            # JSON
            # =========================

            message = json.dumps(command)

            print("Sending:", message)


            # =========================
            # PUBLISH
            # =========================

            info = client.publish(
                TOPIC,
                message
            )

            info.wait_for_publish()

            print("Command sent!")
            print()


            time.sleep(0.5)


        except sr.WaitTimeoutError:

            print("No command detected.")
            print()


        except sr.UnknownValueError:

            print("I couldn't understand you.")
            print()


        except sr.RequestError as e:

            print(
                "Speech recognition error:",
                e
            )

            print()


# =========================
# DISCONNECT
# =========================

client.loop_stop()

client.disconnect()

print("Publisher stopped.")