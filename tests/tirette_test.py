import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for your button
SWITCH_PIN = 16

# Set the initial state and pull-up resistor for the button
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define debounce time in seconds (e.g., 0.2s = 200ms)
DEBOUNCE_TIME_S = 0.2

# Initialize previous state
prev_switch_state = GPIO.input(SWITCH_PIN)
last_change_time = time.time()

try:
    while True:
        current_state = GPIO.input(SWITCH_PIN)
        current_time = time.time()

        if current_state != prev_switch_state and (current_time - last_change_time) >= DEBOUNCE_TIME_S:
            if current_state == GPIO.HIGH:
                print("The limit switch: TOUCHED -> UNTOUCHED")
            else:
                print("The limit switch: UNTOUCHED -> TOUCHED")

            prev_switch_state = current_state
            last_change_time = current_time

        time.sleep(0.01)  # Small delay to avoid high CPU usage

except KeyboardInterrupt:
    GPIO.cleanup()
