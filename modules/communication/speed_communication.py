from modules.communication.i2c_communication import I2CCommunication
from utils.log import Log

class SpeedCommunication(I2CCommunication):
    def __init__(self, detect_ser):
        super().__init__("esp_steppers")
        self.log = Log("SpeedCommunication")
        self.detect_ser = detect_ser

    def sendSpeedPolar(self, r, angle, rot):
        # forme polaire, pas utilisée actuellement
        if self.detect_ser.stop:
            self.write("R: 0.0, w: 0.0, r: 0.0")
        else:
            sendString = f"R: {r:.6f}, w: {angle:.6f}, r: {rot:.6f}"
            self.write(sendString)

    def sendSpeedCart(self, x, y, rot):
        # forme cartésienne
        if self.detect_ser.stop: # Varibale qui permet de stopper le robot si obstacle
            self.write("x: 0.0, y: 0.0, r: 0.0")
            # arreter lui, il faut aussi que le programme de suivi de ligne s'arrete
            # TODO : ce n'est pas le cas car position virtuelle suivi de chemin continue
        else:
            sendString = f"x: {x:.3f}, y: {y:.3f}, r: {rot:.3f}"
            # pas des positions mais des vitesses en unitées arbitraires
            # rajouter une constante pour être en m/s après les tests
            # précision à 3 nombres car à + ça prend un paquet en plus
            # choix entre précision et fréquence
            self.write(sendString)
