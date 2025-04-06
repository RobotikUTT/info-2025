import argparse
from modules.lidar.lidar import LidarService, DetectionService, PrinterService
from modules.navigation.path_following import PathFollower

def main(run_path_follower: bool):
    lidar_service = LidarService()
    lidar_service.start()

    detection_service = DetectionService()
    printer_service = PrinterService()

    lidar_service.observers += [detection_service]

    if run_path_follower:
        path_follower = PathFollower(detection_service)  # permet de faire le dessin en secours
        path_follower.start()  # faudrait le combiner avec le PID quand même, chemin dans un json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the Lidar system.")
    parser.add_argument(
        '--run',
        action='store_true',
        help='Start the PathFollower after Lidar initialization'
    )
    args = parser.parse_args()

    main(run_path_follower=args.run)
