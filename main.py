import argparse
from modules.lidar.lidar import LidarService, DetectionService, PrinterService
from modules.navigation.path_following import PathFollower
from modules.strategy.deploy_strategy import Strategy
from modules.effectors.effectors_control import EffectorsControl
from modules.navigation.position_controller import PositionControllerLinear
import RPi.GPIO as GPIO
import time
import pygame
import threading

def show_score(score):
    pygame.init()
    screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption('Score')
    font = pygame.font.Font(None, 200)
    running = True
    while running:
        screen.fill((0, 0, 0))

        # Rendre le texte sur une surface
        text_surface = font.render(str(score), True, (255, 255, 255))
        # Rotation à 90 degrés
        rotated_surface = pygame.transform.rotate(text_surface, 270)  # angle en degrés, sens horaire

        # Position pour centrer le texte tourné sur l'écran
        rect = rotated_surface.get_rect(center=(150, 100))  # centre écran 300x200

        screen.blit(rotated_surface, rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

def run_lidar_detection():
    lidar_service = LidarService()
    detection_service = DetectionService()

    lidar_service.observers.append(detection_service)
    lidar_service.start()

    print("LIDAR et détection démarrés. En attente d'obstacles...")

    while True:
        if detection_service.stop:
            print("### Obstacle détecté ! ###")
        else:
            print("Pas d'obstacle.")
        time.sleep(0.5)

def runPathFollowing():
    lidar_service = LidarService()

    detection_service = DetectionService()

    lidar_service.observers += [detection_service]
    lidar_service.start()

    pathFollower = PathFollower(detection_service)
    pathFollower.follow_path()


def runStrategy():
    lidar_service = LidarService()
    lidar_service.start()

    detection_service = DetectionService()

    lidar_service.observers += [detection_service]

    effector_controller = EffectorsControl()

    position_controller = PositionControllerLinear(detection_service)

    strategy = Strategy(position_controller, effector_controller)
    strategy.start()


def runTests():
    # i2c.test.main()
    # effector.test.main()
    # lidar.test.main()
    # navigation.test.main()
    # strategy.test.main()
    pass

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
    last_change_time = time.time()

    try:
        current_state = GPIO.input(SWITCH_PIN)
        if current_state == GPIO.LOW:
            print(f"TIRETTE: The limit switch: Tirette armée")
            print(f"========== READY TO ROCK ==========")
        else:
            print("TIRETTE: Veuillez armer la tirette")

        while True:
            current_state = GPIO.input(SWITCH_PIN)
            current_time = time.time()

            if current_state != prev_switch_state and (current_time - last_change_time) >= DEBOUNCE_TIME_S:
                if current_state == GPIO.HIGH:
                    print("TIRETTE: The limit switch: Tirette retirée")
                    time.sleep(2) # to avoid detection
                    return True

                else:
                    print("TIRETTE: The limit switch: Tirette armée")
                    print(f"========== READY TO ROCK ==========")

                prev_switch_state = current_state
                last_change_time = current_time

            time.sleep(0.01)  # Small delay to avoid high CPU usage

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Robot control program entry point.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--run', action='store_true', help='Run the main strategy')
    group.add_argument('--test', action='store_true', help='Run all tests')
    group.add_argument('--follow', action='store_true', help='Run path following mode')
    group.add_argument('--lidar', action='store_true', help='Run lidar mode detection')

    # Ajouté en dehors du groupe exclusif
    parser.add_argument('--score', type=int, help='Score à afficher dans la GUI')
    args = parser.parse_args()


    s = start()
    if s:
        # Si --score est fourni, on lance la fenêtre Tkinter dans un thread séparé
        if args.score is not None:
            threading.Thread(target=show_score, args=(args.score,), daemon=True).start()

        if args.run:
            runStrategy()
        elif args.test:
            runTests()
        elif args.follow:
            runPathFollowing()
        elif args.lidar:
            run_lidar_detection()
