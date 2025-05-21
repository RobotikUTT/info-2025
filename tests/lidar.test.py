from modules.lidar.lidar import LidarService, PrinterService


def main():
    lidar_service = LidarService()
    lidar_service.observers += [PrinterService]
    lidar_service.start()
    lidar_service.join()


if __name__ == "__main__":
    main()
