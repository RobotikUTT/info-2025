import argparse
from modules.lidar.lidar import LidarService, DetectionService, PrinterService
from modules.navigation.path_following import PathFollower
from modules.strategy.deploy_strategy import Strategy
from modules.effectors.effectors_control import EffectorsControl
from modules.navigation.position_controller import PositionControllerLinear
import time

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Robot control program entry point.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--run', action='store_true', help='Run the main strategy')
    group.add_argument('--test', action='store_true', help='Run all tests')
    group.add_argument('--follow', action='store_true', help='Run path following mode')
    group.add_argument('--lidar', action='store_true', help='Run lidar mode detection')

    args = parser.parse_args()

    if args.run:
        runStrategy()
    elif args.test:
        runTests()
    elif args.follow:
        runPathFollowing()
    elif args.lidar:
        run_lidar_detection()
