from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass
class Position:
    x: float
    y: float
    w: float

    def __post_init__(self):
        self.w = self.normalize_angle(self.w)

    def normalize_angle(self, w): # TODO refactor car self.w = self.normalize(self.w) 2 usages
        return (w + math.pi) % (2 * math.pi)

    def normalize(self) -> Position:
        d = math.hypot(self.x, self.y)
        norm_x, norm_y = (0.0, 0.0) if d == 0 else (self.x / d, self.y / d)
        norm_w = 1.0 if self.w > 0 else -1.0
        return Position(norm_x, norm_y, norm_w)

    def minus(self, other: Position) -> Position:
        return Position(
            self.x - other.x,
            self.y - other.y,
            self.w - other.w
        )

    def add(self, other: Position) -> Position:
        return Position(
            self.x + other.x,
            self.y + other.y,
            self.w + other.w
        )

    def multiplyPos(self, alpha: float) -> None:
        self.x *= alpha
        self.y *= alpha

    def multiplyAngle(self, alpha: float) -> None:
        self.w *= alpha
        self.w = self.normalize_angle(self.w)

    def equal(self, other, error_pos=0.0, error_angle=0.0):
        reached_x = abs(self.x - other.x) <= error_pos
        reached_y = abs(self.y - other.y) <= error_pos

        delta_w = self.normalize_angle(self.w - other.w)
        reached_w = abs(delta_w) <= error_angle

        return reached_x and reached_y and reached_w

    def get(self) -> tuple[float, float, float]:
        return self.x, self.y, self.w

    def angle_xy(self) -> float:
        """Renvoie l'angle du vecteur (x, y) par rapport à l'axe des x en radians, entre -π et π."""
        return math.atan2(self.y, self.x)