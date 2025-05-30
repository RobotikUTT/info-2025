import RPi.GPIO as GPIO
from time import sleep

# ========== Configuration ==========
LED_PIN = 13       # GPIO où la LED est connectée
BLINK_DELAY = 0.5  # Durée entre ON et OFF en secondes

# Initialisation GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

print("BLINK: LED clignote sur GPIO 13. Ctrl+C pour arrêter.")

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED ON
        sleep(BLINK_DELAY)
        GPIO.output(LED_PIN, GPIO.LOW)   # LED OFF
        sleep(BLINK_DELAY)

except KeyboardInterrupt:
    print("\nArrêt du clignotement.")
finally:
    GPIO.output(LED_PIN, GPIO.LOW)  # Éteindre la LED par sécurité
    GPIO.cleanup()
