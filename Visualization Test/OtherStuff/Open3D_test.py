import open3d as o3d
import numpy as np
import time

def init_window():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    return vis

def generate_points(x_coordinate):
    new_y = np.random.uniform(-50, 50, size=(255,))
    new_z = np.random.uniform(0, 10, size=(255,))
    new_x = np.full((255,), x_coordinate)
    new_points = np.stack((new_x, new_y, new_z), axis=-1)
    return new_points

def plot_points(vis, pcd, points, camera_target, first_run, x_coordinate, new_z):
    temp_pcd = o3d.geometry.PointCloud()
    temp_pcd.points = o3d.utility.Vector3dVector(points)
    pcd += temp_pcd

    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

    if first_run:
        vis.reset_view_point(True)
        first_run = False
    else:
        target_x = x_coordinate + 20  
        smooth_factor = 0.1  
        camera_target = camera_target * (1 - smooth_factor) + np.array([target_x, 0, np.mean(new_z)]) * smooth_factor
        vis.get_view_control().set_lookat(camera_target)

    return first_run, camera_target

def main():
    # Initialize the window and point cloud object
    vis = init_window()
    pcd = o3d.geometry.PointCloud()
    vis.add_geometry(pcd)
    first_run = True
    x_coordinate = 0
    camera_target = np.array([0, 0, 5])

    while True:
        points = generate_points(x_coordinate)
        first_run, camera_target = plot_points(vis, pcd, points, camera_target, first_run, x_coordinate, points[:, 2])
        
        # Increment x_coordinate
        x_coordinate += 0.3

        # Wait a bit before adding the next set of points
        time.sleep(0.01)

if __name__ == "__main__":
    main()

