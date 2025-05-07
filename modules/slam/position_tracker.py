import sys
import time
import math
import qwiic_otos
from utils.config import Config
from utils.log import Log
from utils.position import Position
from utils.config import Config
import time
import sys
from typing import Optional

class PositionTracker:
    def __init__(self):
        self.log = Log("PositionTracker")
        self.config = Config("PositionTracker")

        self.myOtos = qwiic_otos.QwiicOTOS()

        # Check if it's connected
        if not self.myOtos.is_connected():
            self.log.info("The device isn't connected to the system. Please check your connection", file=sys.stderr)
            return

        self.myOtos.begin()

        self.log.info("Ensure the OTOS is flat and stationary during calibration!")
        for i in range(5, 0, -1):
            self.log.info("Calibrating in %d seconds..." % i)
            time.sleep(1)

        self.log.info("Calibrating IMU...")
        self.myOtos.calibrateImu()

        self.myOtos.setLinearUnit(self.myOtos.kLinearUnitMeters)
        self.myOtos.setAngularUnit(self.myOtos.kAngularUnitRadians)
        self.myOtos.resetTracking()

        # Ajout pour limiter la fréquence de mise à jour
        self._last_position: Optional[Position] = None
        self._last_update_time = 0
        self._update_interval = self.config["update_interval"]

    def getCurrentPosition(self) -> Position:
        now = time.time()
        if self._last_position is None or (now - self._last_update_time) > self._update_interval:
            p = self.myOtos.getPosition()
            self._last_position = Position(p.x, p.y, p.h)
            self._last_update_time = now
        return self._last_position

    def setCurrentPosition(self, position: Position):
        currentPosition = qwiic_otos.Pose2D(position.x, position.y, position.w)
        self.myOtos.setPosition(currentPosition)

    def getCurrentVelocity(self) -> Position:
        vel = self.myOtos.getVelocity()
        return Position(vel.x, vel.y, vel.h)