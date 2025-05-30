import argparse
from modules.lidar.lidar import LidarService, DetectionService
from modules.navigation.path_following import PathFollower
from modules.strategy.deploy_strategy import Strategy
from modules.effectors.effectors_control import EffectorsControl
from modules.navigation.position_controller import PositionControllerLinear
from modules.management.tirette import start
from modules.management.scoring import show_score
import time
import threading


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
    ld = LidarService()
    ld.start()
    position_controller = PositionControllerLinear(ld, DetectionService())
    position_controller.start()

    effector_controller = EffectorsControl("esp_effectors")

    strategy = Strategy(position_controller, effector_controller)
    strategy.start()
    strategy.join()


def runTests():
    # i2c.test.main()
    # effector.test.main()
    # lidar.test.main()
    # navigation.test.main()
    # strategy.test.main()
    pass


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

    if start():
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
