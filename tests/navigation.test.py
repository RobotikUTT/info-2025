from modules.navigation.position_controller import PositionControllerLinear
from modules.lidar.lidar import DetectionService, LidarService

# TODO : PositionControllerLinear.__init__() missing 1 required positional argument: 'detection_service'

def main():
    ld = LidarService()
    # ld.start()
    posController = PositionControllerLinear(ld, DetectionService())
    posController.start()

    def arrivedCallback():
        print("Arrived !")
        exit()

    posController.goTo(0.2, 0.0, 10, arrivedCallback)

if __name__ == "__main__":
    main()