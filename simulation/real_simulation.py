import math
import pygame
from threading import Thread
from modules.slam.position_tracker import PositionTracker
from utils.config import Config


class RealSimulation:
    def __init__(self):
        self.config = Config.get()
        self.size = self.config["simulation"]["size"]
        run = self.config["simulation"]["run"]
        self.robot_radius = self.config["dimensions"]["radius"]
        self.positionTracker = PositionTracker.get()

        if run:
            simulation_loop = Thread(target=self.run)
            simulation_loop.start()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.size * 3 // 2, self.size))  # Use integer division
        map_coupe = pygame.image.load("ressources/images/plateau_coupe.png")
        screen.blit(map_coupe, (0, 0))

        robot_surface = self.drawRobot()
        running = True

        while running:
            # Check for quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Get robot position and orientation from position tracker
            x, y, w = self.positionTracker.getCurrentPosition()

            # Rotate the robot surface according to the current orientation
            rotated_robot_surface = pygame.transform.rotate(robot_surface, w)

            # Calculate the position to center the robot
            robot_rect = rotated_robot_surface.get_rect(center=(x, y))

            # Redraw the background and the robot at the new position
            screen.blit(map_coupe, (0, 0))  # Redraw the map to avoid leftover images
            screen.blit(rotated_robot_surface, robot_rect.topleft)

            pygame.display.flip()  # Update the display
            pygame.time.Clock().tick(30)  # Limit the framerate to 30 FPS

        pygame.quit()

    def drawRobot(self):
        height = (math.sqrt(3) / 2) * self.robot_radius  # Use self.robot_radius here
        width = self.robot_radius * 2

        robot_surface = pygame.surface.Surface((width, int(height)))

        center_x = width / 2
        center_y = height / 3

        angle_offset = math.radians(30)

        points = []
        for i in range(3):
            angle = angle_offset + i * math.radians(120)
            x = center_x + self.robot_radius * math.cos(angle)
            y = center_y + self.robot_radius * math.sin(angle)
            points.append((x, y))

        pygame.draw.polygon(robot_surface, (255, 0, 0), points)

        return robot_surface
