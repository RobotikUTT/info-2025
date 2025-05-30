import RPi.GPIO as GPIO
from time import time, sleep

# ========== Configuration ==========
SWITCH_PIN = 26            # GPIO du switch 2 positions
DEBOUNCE_TIME_S = 0.2      # Anti-rebond (en secondes)

# Initialisation GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# État initial
prev_state = GPIO.input(SWITCH_PIN)
last_change_time = time()

print("INTERRUPTEUR: En attente de changement d'état...")

try:
    while True:
        current_state = GPIO.input(SWITCH_PIN)
        current_time = time()

        if current_state != prev_state and (current_time - last_change_time) >= DEBOUNCE_TIME_S:
            if current_state == GPIO.HIGH:
                print("INTERRUPTEUR: Position HAUTE")
            else:
                print("INTERRUPTEUR: Position BASSE")

            prev_state = current_state
            last_change_time = current_time

        sleep(0.01)  # Pour réduire l'utilisation CPU

except KeyboardInterrupt:
    print("\nArrêt du programme.")
finally:
    GPIO.cleanup()
