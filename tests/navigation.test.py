from modules.navigation.position_controller import PositionControllerLinear


def main():
    posController = PositionControllerLinear()

    def arrivedCallback():
        print("Arrived !")

    posController.goTo(10, 10, 10, arrivedCallback)

if __name__ == "__main__":
    main()