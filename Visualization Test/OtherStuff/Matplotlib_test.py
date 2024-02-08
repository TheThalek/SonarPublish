import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
max_points = 10000  # Max number of points to display
points_per_set = 255
max_sets = max_points // points_per_set  # Calculate how many sets can be displayed
x_increment = 1
y_range = (-50, 50)
z_range = (0, 5)

# Initialize the figure for plotting
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_xlim([0, max_sets * x_increment])
ax.set_ylim(y_range)
ax.set_zlim(z_range)

# Initialize a list to hold the generated points
points = []

def update(frame):
    global points
    # Generate new set of points
    new_x = len(points) * x_increment
    new_y = np.random.uniform(*y_range, points_per_set)
    new_z = np.random.uniform(*z_range, points_per_set)
    new_points = np.vstack((new_x + np.zeros(points_per_set), new_y, new_z)).T
    
    # Add the new points
    points.append(new_points)
    
    # Keep only the latest points within the max_points limit
    points = points[-max_sets:]
    
    # Flatten the list of arrays into a single array for plotting
    all_points = np.vstack(points)
    
    # Clear the axes and plot all points
    ax.cla()
    ax.scatter(all_points[:, 0], all_points[:, 1], all_points[:, 2], s=1)
    ax.set_xlim([0, max_sets * x_increment])
    ax.set_ylim(y_range)
    ax.set_zlim(z_range)

# Create an animation
ani = FuncAnimation(fig, update, frames=np.arange(100), interval=100)

plt.show()
