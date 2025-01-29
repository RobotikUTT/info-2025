import time

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import cos, sin
from teddy_lidar_revisited import LidarService

class LidarVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-300, 300)
        self.ax.set_ylim(-300, 300)
        self.line, = self.ax.plot([], [], 'bo')
        self.latest_data = []  # Store the latest data for the animation

    def update(self, values):
        # Update the latest data
        self.latest_data += values

    def animate(self, frame):
        # Ensure that the data is consistent
        if self.latest_data:
            x_data = [cos(value.absolute_angle) * value.distance / 10 for value in self.latest_data]
            y_data = [sin(value.absolute_angle) * value.distance / 10 for value in self.latest_data]
            
            # Check for shape mismatch
            if len(x_data) == len(y_data):
                self.line.set_data(x_data, y_data)
            else:
                print("Data mismatch: x_data and y_data lengths do not match.")
                return self.line,  # Return the line without updating if there is a mismatch

        return self.line,  # Return the line object to update it in FuncAnimation

    def start(self):
        # Set up the animation function to periodically update the plot
        ani = FuncAnimation(self.fig, self.animate, blit=True, interval=100)
        plt.show()
        
class LidarPrinter:
    def update(self, points):
        for point in points:
            print(f"Point: {point.distance}")
            
class DetectionService:
    def __init__(self, threshold):
        self.threshold = threshold
        self.stop = False
        self.stop_time = 0
    def update(self, points):
        treat_dist = sum(1 for point in points if point.distance < self.threshold)

        if self.stop and time.time() - self.stop_time > 3:
            self.stop = False  # Resume movement after 4 seconds
        elif not self.stop and treat_dist > 1:
            self.stop_time = time.time()
            self.stop = True  # Stop if more than 1 point is too close
        
if __name__ == "__main__":
    lv = DetectionService(10)
    ls = LidarService()
    ls.observers.append(lv)
    
    # Start the Lidar service (data collection)
    ls.start()
