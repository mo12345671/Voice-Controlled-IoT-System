import os
import ssl
import json
import time

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

import RPi.GPIO as GPIO

import board
import adafruit_dht

from RPLCD.i2c import CharLCD


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
# GPIO SETTINGS
# =========================

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)


SERVO_PIN = 27

LED1 = 16
LED2 = 20
LED3 = 21

DHT_PIN = 22


GPIO.setup(
    SERVO_PIN,
    GPIO.OUT
)

GPIO.setup(
    LED1,
    GPIO.OUT
)

GPIO.setup(
    LED2,
    GPIO.OUT
)

GPIO.setup(
    LED3,
    GPIO.OUT
)


# Turn LEDs OFF

GPIO.output(
    LED1,
    GPIO.LOW
)

GPIO.output(
    LED2,
    GPIO.LOW
)

GPIO.output(
    LED3,
    GPIO.LOW
)


# =========================
# SERVO
# =========================

servo = GPIO.PWM(
    SERVO_PIN,
    50
)

servo.start(0)


# =========================
# DHT11
# =========================

DHT_SENSOR = adafruit_dht.DHT11(
    board.D22
)


# =========================
# LCD
# =========================

lcd = CharLCD(
    i2c_expander="PCF8574",
    address=0x27,
    port=1,
    cols=16,
    rows=2
)


# =========================
# STATUS
# =========================

door_status = "CLOSED"

led_status = "LEDs OFF"


# =========================
# UPDATE LCD
# =========================

def update_lcd():

    global door_status
    global led_status


    try:

        temperature = DHT_SENSOR.temperature

        humidity = DHT_SENSOR.humidity


        print(
            "Temperature:",
            temperature,
            "C"
        )

        print(
            "Humidity:",
            humidity,
            "%"
        )


        lcd.clear()


        # First line

        if door_status == "OPEN":

            lcd.write_string(
                "Door: OPEN"
            )

        else:

            lcd.write_string(
                led_status
            )


        # Second line

        lcd.cursor_pos = (1, 0)

        lcd.write_string(
            "T:{:.1f}C H:{:.0f}%".format(
                temperature,
                humidity
            )
        )


    except RuntimeError as e:

        print(
            "DHT11 Error:",
            e
        )


        lcd.clear()


        if door_status == "OPEN":

            lcd.write_string(
                "Door: OPEN"
            )

        else:

            lcd.write_string(
                led_status
            )


        lcd.cursor_pos = (1, 0)

        lcd.write_string(
            "DHT11 Error"
        )


# =========================
# SERVO OPEN
# =========================

def servo_open():

    global door_status


    print("Opening door...")


    door_status = "OPEN"


    servo.ChangeDutyCycle(7.5)

    time.sleep(1)

    servo.ChangeDutyCycle(0)


    update_lcd()


# =========================
# SERVO CLOSE
# =========================

def servo_close():

    global door_status


    print("Closing door...")


    servo.ChangeDutyCycle(2.5)

    time.sleep(1)

    servo.ChangeDutyCycle(0)


    door_status = "CLOSED"


    update_lcd()


# =========================
# ALL LEDs OFF
# =========================

def leds_off():

    global led_status


    GPIO.output(
        LED1,
        GPIO.LOW
    )

    GPIO.output(
        LED2,
        GPIO.LOW
    )

    GPIO.output(
        LED3,
        GPIO.LOW
    )


    led_status = "LEDs OFF"


    update_lcd()


# =========================
# GREEN
# =========================

def open_green():

    global led_status


    print("Green LED ON")


    GPIO.output(
        LED1,
        GPIO.HIGH
    )

    GPIO.output(
        LED2,
        GPIO.LOW
    )

    GPIO.output(
        LED3,
        GPIO.LOW
    )


    led_status = "Green OPEN"


    update_lcd()


# =========================
# BLUE
# =========================

def open_blue():

    global led_status


    print("Blue LED ON")


    GPIO.output(
        LED1,
        GPIO.LOW
    )

    GPIO.output(
        LED2,
        GPIO.HIGH
    )

    GPIO.output(
        LED3,
        GPIO.LOW
    )


    led_status = "Blue OPEN"


    update_lcd()


# =========================
# RED
# =========================

def open_red():

    global led_status


    print("Red LED ON")


    GPIO.output(
        LED1,
        GPIO.LOW
    )

    GPIO.output(
        LED2,
        GPIO.LOW
    )

    GPIO.output(
        LED3,
        GPIO.HIGH
    )


    led_status = "Red OPEN"


    update_lcd()


# =========================
# ENTER
# =========================

def entering():

    print("ENTER")


    # Open door

    servo_open()


    # All LEDs ON

    GPIO.output(
        LED1,
        GPIO.HIGH
    )

    GPIO.output(
        LED2,
        GPIO.HIGH
    )

    GPIO.output(
        LED3,
        GPIO.HIGH
    )


    # Show on LCD

    global led_status

    led_status = "ALL LEDs ON"

    update_lcd()


    # Wait 5 seconds

    time.sleep(5)


    # LEDs OFF

    leds_off()


    # Close door

    servo_close()


# =========================
# GETTING OUT
# =========================

def getting_out():

    print("GETTING OUT")


    # Open door

    servo_open()


    # Wait 5 seconds

    time.sleep(5)


    # Close door

    servo_close()


    # LEDs OFF

    leds_off()


# =========================
# MQTT MESSAGE
# =========================

def on_message(
    client,
    userdata,
    msg
):

    try:

        message = msg.payload.decode()

        print(
            "Received:",
            message
        )


        command = json.loads(message)

        action = command.get(
            "action"
        )


        # =========================
        # ENTER
        # =========================

        if action == "enter":

            entering()


        # =========================
        # AREA
        # =========================

        elif action == "area":

            number = command.get(
                "number"
            )


            if number == 1:

                open_green()


            elif number == 2:

                open_blue()


            elif number == 3:

                open_red()


            else:

                print(
                    "Unknown area"
                )


        # =========================
        # EXIT
        # =========================

        elif action == "exit":

            getting_out()


        else:

            print(
                "Unknown action"
            )


    except Exception as e:

        print(
            "Error:",
            e
        )


# =========================
# MQTT CLIENT
# =========================

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="raspberry-pi"
)


client.username_pw_set(
    MQTT_USERNAME,
    MQTT_PASSWORD
)


client.tls_set(
    cert_reqs=ssl.CERT_REQUIRED
)


client.on_message = on_message


# =========================
# CONNECT
# =========================

print(
    "Connecting to HiveMQ..."
)


client.connect(
    MQTT_HOST,
    MQTT_PORT,
    60
)


print(
    "Connected to HiveMQ!"
)


# Subscribe

client.subscribe(
    TOPIC
)


print(
    "Subscribed to:",
    TOPIC
)


print(
    "=============================="
)

print(
    "Receiver is ready!"
)

print(
    "=============================="
)


# =========================
# MAIN LOOP
# =========================

try:

    while True:

        # Update LCD

        update_lcd()


        # Receive MQTT messages

        client.loop(
            timeout=0.1
        )


        time.sleep(2)


except KeyboardInterrupt:

    print(
        "\nStopping receiver..."
    )


finally:

    # LEDs OFF

    GPIO.output(
        LED1,
        GPIO.LOW
    )

    GPIO.output(
        LED2,
        GPIO.LOW
    )

    GPIO.output(
        LED3,
        GPIO.LOW
    )


    # Stop servo

    servo.ChangeDutyCycle(0)

    servo.stop()


    # Clear LCD

    lcd.clear()


    # Close DHT

    DHT_SENSOR.exit()


    # GPIO cleanup

    GPIO.cleanup()


    # MQTT disconnect

    client.disconnect()


    print(
        "Receiver stopped."
    )