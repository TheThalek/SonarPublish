import open3d as o3d
import numpy as np
import time

# Create a point cloud object
pcd = o3d.geometry.PointCloud()

# Create a visualizer object
vis = o3d.visualization.Visualizer()
vis.create_window()
vis.add_geometry(pcd)

# Initialize the x coordinate
x_coordinate = 0

# Set an initial camera target, which will be updated smoothly
camera_target = np.array([0, 0, 5])  # Example initial target

# Initialize a flag for resetting the view
first_run = True

while True:
    # Generate new points
    new_y = np.random.uniform(-50, 50, size=(255,))
    new_z = np.random.uniform(0, 10, size=(255,))
    new_x = np.full((255,), x_coordinate)
    new_points = np.stack((new_x, new_y, new_z), axis=-1)
    
    # Convert new points to Open3D point cloud and append
    temp_pcd = o3d.geometry.PointCloud()
    temp_pcd.points = o3d.utility.Vector3dVector(new_points)
    pcd += temp_pcd

    # Update the visualization
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

    # Automatically adjust the view
    if first_run:
        vis.reset_view_point(True)
        first_run = False
    else:
        # Calculate a new target position that's a bit ahead of the latest x_coordinate
        # Adjust this value to shift the focus more to the right
        target_x = x_coordinate + 20  # Look ahead by 20 units; adjust as needed
        
        # Smoothly update the camera target to reduce shaking
        smooth_factor = 0.1  # Adjust this for smoother transitions
        camera_target = camera_target * (1 - smooth_factor) + np.array([target_x, 0, np.mean(new_z)]) * smooth_factor
        
        vis.get_view_control().set_lookat(camera_target)

    # Increment x_coordinate
    x_coordinate += 0.3

    # Wait a bit before adding the next set of points
    time.sleep(0.01)