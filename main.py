from modules.lidar.lidar import LidarService, DetectionService, PrinterService
from modules.navigation.path_following import PathFollower

def main():
    lidar_service = LidarService()
    lidar_service.start()
    detection_service = DetectionService(200)
    printer_service = PrinterService()
    lidar_service.observers += [detection_service, printer_service]
    path_follower = PathFollower(detection_service)
    path_follower.start()

if __name__ == "__main__":
    main()
