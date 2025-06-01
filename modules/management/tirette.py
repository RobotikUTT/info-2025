import RPi.GPIO as GPIO
from time import time, sleep
from utils.log import Log

LED_PIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
BLINK_DELAY = 0.1

SWITCH_PIN = 26            # GPIO du switch 2 positions
DEBOUNCE_TIME_S = 0.2      # Anti-rebond (en secondes)
GPIO.setmode(GPIO.BCM)
READY = False
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
log = Log("Tirette")

def choose_team():
    # Return True si Jaune False si bleu
    current_state = GPIO.input(SWITCH_PIN)
    if current_state == GPIO.HIGH:
        log.info("INTERRUPTEUR: Position HAUTE : team JAUNE")
        return True
    else:
        log.info("INTERRUPTEUR: Position BASSE : team BLEU")
        return False
from time import time, sleep


def start() -> bool:
    global READY
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

    try:
        current_state = GPIO.input(SWITCH_PIN)
        if current_state == GPIO.LOW:
            on_ready()

        else:
            log.info("TIRETTE: Veuillez armer la tirette")

        while True:
            if READY == False:
                # Blink in order to wait to be started
                GPIO.output(LED_PIN, GPIO.HIGH)  # LED ON
                sleep(BLINK_DELAY)
                GPIO.output(LED_PIN, GPIO.LOW)  # LED OFF
                sleep(BLINK_DELAY)
            else:
                sleep(DEBOUNCE_TIME_S) # just pour tempo un peu

            current_state = GPIO.input(SWITCH_PIN)
            current_time = time()

            if current_state != prev_switch_state and (current_time - last_change_time) >= DEBOUNCE_TIME_S:
                if current_state == GPIO.HIGH:
                    log.info("TIRETTE: The limit switch: Tirette retirée")
                    GPIO.output(LED_PIN, GPIO.LOW)
                    return True

                else:
                    on_ready()
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    READY = True

                prev_switch_state = current_state
                last_change_time = current_time

    except KeyboardInterrupt:
        GPIO.cleanup()

def on_ready():
    # TODO : need to start a LED when the robot is ready to start
    log.info(f"TIRETTE: The limit switch: Tirette armée")
    log.info(f"========== READY TO ROCK ==========")