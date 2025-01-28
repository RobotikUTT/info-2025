from .base import I2CCommunicationBase


class SpeedCommunication(I2CCommunicationBase):
    def send_speed_polar(self, r, angle, rot):
        self.write(f"R: {r:.6f}, w: {angle:.6f}, r: {rot:.6f}")

    def send_speed_cart(self, x, y, rot):
        self.write(f"x: {x:.6f}, y: {y:.6f}, r: {rot:.6f}")
