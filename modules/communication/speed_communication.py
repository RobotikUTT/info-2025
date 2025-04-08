from modules.communication.i2c_communication import I2CCommunication
from utils.log import Log

class SpeedCommunication(I2CCommunication):
    def __init__(self, detect_ser):
        super().__init__("esp_steppers")
        self.log = Log("SpeedCommunication")
        self.detect_ser = detect_ser

    def sendSpeedPolar(self, r: float, angle: float, rot: float):
        """
        Sends the speed command to the robot in polar coordinates format.
        Not used in its current form

        Args:
            r (float): Linear speed magnitude (radius component).
            angle (float): Direction of movement in radians.
            rot (float): Rotational speed (angular velocity).

        Returns:
            None
        """
        if self.detect_ser.stop:
            self.write("R: 0.0, w: 0.0, r: 0.0")
        else:
            sendString = f"R: {r:.6f}, w: {angle:.6f}, r: {rot:.6f}"
            self.write(sendString)

    def sendSpeedCart(self, x: float, y: float, rot: float):
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
            self.write("x: 0.0, y: 0.0, r: 0.0")
        else:
            sendString = f"x: {x:.3f}, y: {y:.3f}, r: {rot:.3f}"
            self.write(sendString)
