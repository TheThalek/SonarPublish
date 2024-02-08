import numpy as np
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtWidgets, QtCore


class MBESVisualizer:
    def __init__(self):
        # Initialize the app
        self.app = QtWidgets.QApplication([])
        self.win = gl.GLViewWidget()
        self.win.setWindowTitle('MBES Data Visualization')
        self.win.show()

        # Initialize scatter plot item
        self.scatter = gl.GLScatterPlotItem()
        self.win.addItem(self.scatter)

        # Data parameters
        self.max_points = 10000  # Maximum number of points to be visible
        self.n_points = 55  # Number of points per set
        self.x = 0  # Starting x value for the first set

        # Store points data
        self.data = np.empty((0, 3))  # Initial empty array to store points

        # Timer for real-time updating
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # Update every 50 ms
        
    def update(self):
        # Generate new set of points
        newY = np.random.uniform(-50, 50, size=(self.n_points,))
        newZ = np.random.uniform(0, 3, size=(self.n_points,))  # Simulate depth values
        newX = np.full((self.n_points,), self.x)

        # Append new points to the data array
        new_points = np.column_stack((newX, newY, newZ))
        self.data = np.vstack((self.data, new_points))

        # If we've exceeded the maximum number of points, remove the oldest ones
        if len(self.data) > self.max_points:
            self.data = self.data[-self.max_points:]

        # Generate colors for each point based on z value
        colors = self.get_colors(self.data[:, 2])

        # Update the scatter plot data
        self.scatter.setData(pos=self.data, color=colors)
        self.x += 1  # Increment x for the next scan

    def get_colors(self, z_vals):
        # Normalize z values to the range [0, 1]
        z_norm = (z_vals - np.min(z_vals)) / np.ptp(z_vals)
        # Create an array of colors transitioning from blue to red
        colors = np.zeros((len(z_vals), 4))  # Initialize RGBA color array
        colors[:, 0] = z_norm  # Red channel
        colors[:, 2] = 1 - z_norm  # Blue channel
        colors[:, 3] = 1  # Alpha channel
        return colors

    def run(self):
        # Run the application
        self.app.exec_()

# Create and run the visualizer
if __name__ == '__main__':
    visualizer = MBESVisualizer()
    visualizer.run()