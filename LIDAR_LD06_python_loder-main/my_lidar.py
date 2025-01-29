from math import cos, sin
import pygame
from teddy_lidar_revisited import LidarService

class LidarVisualizer:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.size = 600
        self.screen = pygame.display.set_mode((self.size, self.size))
        self.origin = (self.size // 2, self.size // 2)

    def update(self, values):
        self.screen.fill((0, 0, 0))
        for value in values:
            end_x = self.origin[0] + cos(value.absolute_angle) * value.distance / 10
            end_y = self.origin[1] + sin(value.absolute_angle) * value.distance / 10
            pygame.draw.line(self.screen, (255, 255, 255), self.origin, (end_x, end_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)


lv = LidarVisualizer()
ld = LidarService()
ld.observers.append(lv)
ld.start()