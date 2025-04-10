from modules.communication.i2c_communication import I2CCommunication
from utils.log import Log
import time
# Si bug I2C : sudo i2cdetect -y 1
# Permet de voir les adresses available

class SpeedCommunication(I2CCommunication):
    def __init__(self, detect_ser):
        super().__init__("esp_steppers")
        self.log = Log("SpeedCommunication")
        self.detect_ser = detect_ser


    def sendSpeedCart(self, x: float, y: float, rot: float, vit: float):
        """
          Envoie les vitesses du robot sous forme cartésienne.

          Args:
              x (float): Composante de la vitesse linéaire selon l'axe X.
              y (float): Composante de la vitesse linéaire selon l'axe Y.
              rot (float): Vitesse de rotation (vitesse angulaire autour de l'axe Z).

          Returns:
              None

          Notes:
              - Si un obstacle est détecté (`self.detect_ser.stop` est True), le robot est arrêté en envoyant des vitesses nulles.
              - Actuellement, seul le mouvement réel est stoppé ; le programme de suivi de chemin continue (à corriger).
              - Les vitesses sont exprimées dans des unités arbitraires. Une constante pourra être ajoutée plus tard pour convertir en m/s.
              - La précision est limitée à 3 décimales pour privilégier la fréquence d'envoi des commandes.
          """
        if self.detect_ser.stop: # Varibale qui permet de stopper le robot si obstacle
            self.write("x: 0.0, y: 0.0, r: 0.0") # , v: 0.0
            while self.detect_ser.stop:
                self.log.warning("STOP: obstacle détecté, en attente...")
                self.sendSpeedCart(0.0, 0.0, 0.0, 0.0)  # assure arrêt total
                time.sleep(0.1)  # légère pause avant de rechecker

        else:
            sendString = f"x: {x:.3f}, y: {y:.3f}, r: {rot:.3f}" #  , v : {vit:.3f} data cannot exeed 32 bytes
            self.write(sendString)
