from pyqtgraph.Qt import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np

class RealTime3DPlotter:
    def __init__(self, max_points=1000):
        # Create the application window
        self.app = QtWidgets.QApplication([])
        self.win = pg.GraphicsLayoutWidget(show=True, title="3D Point Cloud Visualization")
        self.win.resize(800, 600)
        
        # Create 3D plot widget
        self.plot = self.win.addPlot(title="3D Scatter Plot", projection='3d')
        self.scatter = pg.ScatterPlotItem(size=5, pen=pg.mkPen(None))
        self.plot.addItem(self.scatter)

        # Data storage
        self.x = 0
        self.data = np.empty((max_points, 3))

        # Timer to update the plot
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # milliseconds

    def update(self):
        # Generate a new set of points and add them to the plot
        y = np.random.normal(size=50)
        z = np.random.normal(size=50)
        points = np.vstack([np.full(50, self.x), y, z]).T
        self.scatter.addPoints(pos=points)
        self.x += 1

    def start(self):
        # Start the application loop
        self.app.exec_()

# Run the plotter
if __name__ == '__main__':
    plotter = RealTime3DPlotter()
    plotter.start()
