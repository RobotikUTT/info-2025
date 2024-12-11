import math
import pygame
from threading import Thread
from modules.slam.position_tracker import PositionTracker
from utils.config import Config

class RealSimulation:
    def __init__(self):
        self.config = Config().get()
        self.size = self.config["simulation"]["size"]
        run = self.config["simulation"]["run"]
        self.robot_radius = self.config["dimension"]['robot']["radius"]
        self.positionTracker = PositionTracker()

        if run:
            simulation_loop = Thread(target=self.run)
            simulation_loop.start()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.size * 3 // 2, self.size))  # Use integer division
        map_coupe = pygame.image.load("../ressources/images/plateau_coupe.png")
        screen.blit(map_coupe, (0, 0))

        robot_surface = self.drawRobot()
        running = True

        while running:
            # Check for quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            x, y, w = (100, 100, 2) # self.positionTracker.getCurrentPosition()
            rotated_robot_surface = pygame.transform.rotate(robot_surface, w)

            robot_rect = rotated_robot_surface.get_rect(center=(x, y))

            screen.blit(map_coupe, (0, 0))
            screen.blit(rotated_robot_surface, robot_rect.topleft)

            pygame.display.flip()
            pygame.time.Clock().tick(30)

        pygame.quit()

    def drawRobot(self):
        height = (math.sqrt(3)) * self.robot_radius
        width = self.robot_radius * 2

        # Create a surface with transparency support
        robot_surface = pygame.Surface((width, int(height)), pygame.SRCALPHA)

        # Transparent background is already set by default (RGBA = (0, 0, 0, 0))
        center_x = width / 2
        center_y = height / 2

        angle_offset = math.radians(30)

        points = []
        for i in range(3):
            angle = angle_offset + i * math.radians(120)
            x = center_x + self.robot_radius * math.cos(angle)
            y = center_y + self.robot_radius * math.sin(angle)
            points.append((x, y))

        # Draw a filled polygon on the transparent surface
        pygame.draw.polygon(robot_surface, (255, 0, 0, 255), points)  # RGBA format (255 = opaque red)

        return robot_surface


rs = RealSimulation()