from modules.navigation.position_controller import PositionControllerLinear
from modules.lidar.lidar import DetectionService, LidarService

def main():
    ld = LidarService()
    ld.start()
    detection = DetectionService()
    posController = PositionControllerLinear(ld, detection)
    posController.start()

    positions = [(0, 0, 0), (0.5, 0, 0), (0.5, 0.5, 0), (0, 0.5, 0)]

    def arrivedCallback1():
        print("Arrivé à position 1")
        posController.goTo(*positions[1], arrivedCallback2)

    def arrivedCallback2():
        print("Arrivé à position 2")
        posController.goTo(*positions[2], arrivedCallback3)

    def arrivedCallback3():
        print("Arrivé à position 3")
        posController.goTo(*positions[3], arrivedCallback4)

    def arrivedCallback4():
        print("Arrivé à la dernière position.")
        posController.goTo(*positions[0], arrivedCallback1)

    # Démarrer à la première position
    arrivedCallback1()

    # Attendre que le thread se termine (s’il y en a un)
    posController.join()

if __name__ == "__main__":
    main()
