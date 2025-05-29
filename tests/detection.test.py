from modules.lidar.lidar import LidarService, DetectionService


def main():
    lidar_service = LidarService()
    lidar_service.observers += [DetectionService()]
    lidar_service.start()
    lidar_service.join()


if __name__ == "__main__":
    main()