import RPi.GPIO as GPIO
from time import time

LED_PIN = 13
GPIO.setup(LED_PIN, GPIO.OUT)

def start() -> bool:
    """
    Permet de lancer le robot lorsque la tirette est enlevée
    """
    # ========== Set up GPIO pin ==========
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
    last_change_time = time()
    GPIO.output(13, GPIO.LOW)

    try:
        current_state = GPIO.input(SWITCH_PIN)
        if current_state == GPIO.LOW:
            on_ready()

        else:
            print("TIRETTE: Veuillez armer la tirette")

        while True:
            current_state = GPIO.input(SWITCH_PIN)
            current_time = time()

            if current_state != prev_switch_state and (current_time - last_change_time) >= DEBOUNCE_TIME_S:
                if current_state == GPIO.HIGH:
                    print("TIRETTE: The limit switch: Tirette retirée")
                    GPIO.output(13, GPIO.LOW)
                    return True

                else:
                    on_ready()

                prev_switch_state = current_state
                last_change_time = current_time

            time.sleep(0.01)  # Small delay to avoid high CPU usage

    except KeyboardInterrupt:
        GPIO.cleanup()

def on_ready():
    # TODO : need to start a LED when the robot is ready to start
    print(f"TIRETTE: The limit switch: Tirette armée")
    print(f"========== READY TO ROCK ==========")
    GPIO.output(13, GPIO.HIGH)