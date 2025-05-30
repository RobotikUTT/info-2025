from __future__ import annotations
from dataclasses import dataclass
import math

from dataclasses import dataclass
import math

@dataclass
class Position:
    x: float
    y: float
    w: float

    def __post_init__(self):
        self.w = self.normalize_angle(self.w)

    def normalize_angle(self, w):
        return (w + math.pi) % (2 * math.pi) - math.pi

    def normalize(self) -> 'Position':
        d = math.hypot(self.x, self.y)
        norm_x, norm_y = (0.0, 0.0) if d == 0 else (self.x / d, self.y / d)
        return Position(norm_x, norm_y, self.w)

    def norm(self) -> float:
        """Retourne la norme du vecteur (x, y)."""
        return math.hypot(self.x, self.y)

    def minus(self, other: 'Position') -> 'Position':
        return Position(
            self.x - other.x,
            self.y - other.y,
            self.w - other.w
        )

    def add(self, other: 'Position') -> 'Position':
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

    def equal(self, other: 'Position', error_pos=0.0, error_angle=0.0) -> bool:
        reached_x = abs(self.x - other.x) <= error_pos
        reached_y = abs(self.y - other.y) <= error_pos

        delta_w = self.normalize_angle(self.w - other.w)
        reached_w = abs(delta_w) <= error_angle

        return reached_x and reached_y and reached_w

    def get(self) -> tuple[float, float, float]:
        return self.x, self.y, self.w

    def copy(self) -> 'Position':
        return Position(self.x, self.y, self.w)

    def rotate(self, omega: float) -> 'Position':
        """Retourne une nouvelle Position avec (x, y) tournés de omega radians."""
        cos_o = math.cos(omega)
        sin_o = math.sin(omega)
        x_rot = self.x * cos_o - self.y * sin_o
        y_rot = self.x * sin_o + self.y * cos_o
        return Position(x_rot, y_rot, self.w)
