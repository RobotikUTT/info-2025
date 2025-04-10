import argparse
from modules.lidar.lidar import LidarService, DetectionService, PrinterService
from modules.navigation.path_checks import PathChecker
from modules.navigation.path_following import PathFollower
from modules.strategy.deploy_strategy import Strategy


def main(run_path_follower: bool):
    lidar_service = LidarService()
    lidar_service.start()
    strategy = Strategy

    detection_service = DetectionService()
    printer_service = PrinterService()

    lidar_service.observers += [detection_service]

    if run_path_follower:
        path_follower = PathFollower(detection_service) # PathFollower(detection_service)  # permet de faire le dessin en secours
        # PathChecker fonctionne toujours
        strategy.start(path_follower)
        # path_follower.start()  # faudrait le combiner avec le PID quand même, chemin dans un json

    print("No --run parameter set, doesn't use motors so")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the Lidar system.")
    parser.add_argument(
        '--run',
        action='store_true',
        help='Start the PathFollower after Lidar initialization'
    )
    args = parser.parse_args()

    main(run_path_follower=args.run)
