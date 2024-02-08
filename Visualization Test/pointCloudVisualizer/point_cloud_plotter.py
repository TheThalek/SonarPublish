import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from point_cloud_generator import generate_point_cloud
from mpl_toolkits.mplot3d import Axes3D

# Initialize the figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Store all points in a list
all_points = np.array([[0, 0, 0]])

# Create a scatter plot object which will be updated with new data
scatter = ax.scatter(all_points[:, 0], all_points[:, 1], all_points[:, 2])

# Define the color map
color_map = plt.get_cmap('jet')

def update(frame):
    global all_points
    new_points = generate_point_cloud()
    all_points = np.vstack((all_points, new_points))

    # Update the scatter plot data
    scatter._offsets3d = (all_points[:, 0], all_points[:, 1], all_points[:, 2])
    scatter.set_array(all_points[:, 2])  # Color by z-value
    scatter.set_cmap(color_map)
    return scatter,

# Adjust the limits
ax.set_xlim([0, 255 * 100])  # Assuming we want to show 100 sets of points
ax.set_ylim([-50, 50])
ax.set_zlim([0, 5])

# Update the color bar
scatter.set_clim([0, 5])
plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)

# Start the animation
ani = FuncAnimation(fig, update, interval=10, blit=False)

# Show the plot
plt.show()
