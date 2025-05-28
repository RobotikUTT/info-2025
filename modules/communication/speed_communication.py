from modules.communication.i2c_communication import I2CCommunication
from utils.log import Log

# Si bug I2C : sudo i2cdetect -y 1
# Permet de voir les adresses available

class SpeedCommunication(I2CCommunication):
    def __init__(self):
        super().__init__("esp_steppers")
        self.log = Log("SpeedCommunication")


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

        sendString = f"x: {x:.2f}, y: {y:.2f}, r: {rot:.2f}" #  , v : {vit:.3f} data cannot exeed 32 bytes
        # TODO : PATCH in order to send less than 32 bytes, pass .3f to .2f but can be adjusted
        # The proper way is to do struct binary packing but it needs an unpacking on the ESP
        # Not the time to do it during the competition
        self.log.debug(f"Taille envoyé : {len(sendString.encode('utf-8'))} bytes")
        self.write(sendString)
