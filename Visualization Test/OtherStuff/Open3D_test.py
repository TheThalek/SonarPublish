import threading
import numpy as np
import open3d as o3d
import time
import random

# Global variable for sharing data between threads
point_queue = []
lock = threading.Lock()

# Global running flag
running = True

# Generate random ranges for y and z that will be constant for the whole run
z_upper = random.uniform(0.01, 0.1)
y_range = random.uniform(0, 3)

def generate_and_process_points():
    global running, point_queue
    x_coordinate = 0
    # Calculate the step size for x based on the range of y values
    x_increment_factor = y_range / 150  # Adjust the division factor as needed (happens only once)
    while running:
        print("Generating points")
        new_y = np.random.uniform(-y_range, y_range, size=(255,))
        new_z = np.random.uniform(0, z_upper, size=(255,))
        new_x = np.full((255,), x_coordinate)
        points = np.stack((new_x, new_y, new_z), axis=-1)
        
        with lock:
            point_queue.append(points)
        
        # Increment x_coordinate by a factor of the range of y values
        x_coordinate += x_increment_factor
        time.sleep(0.01)  # Adjust timing as needed


def visualize():
    global running, point_queue
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    pcd = o3d.geometry.PointCloud()
    vis.add_geometry(pcd)

    first_run = True

    while running:
        if point_queue:
            points = None
            with lock:
                if point_queue:
                    points = point_queue.pop(0)

            if points is not None:
                temp_pcd = o3d.geometry.PointCloud()
                temp_pcd.points = o3d.utility.Vector3dVector(points)
                pcd += temp_pcd
                vis.update_geometry(pcd)
                vis.poll_events()
                vis.update_renderer()

                x_coordinate = points[0, 0]  # Update to the latest x_coordinate of new points

                if first_run:
                    vis.reset_view_point(True)
                    first_run = False
                else:
                    # Set the camera to look at the new points, effectively pushing old points to the right
                    camera_target = np.array([x_coordinate, 0, np.mean(points[:, 2])])
                    vis.get_view_control().set_lookat(camera_target)
                    # Optionally, adjust the zoom and up direction as needed

        time.sleep(0.005)

    vis.destroy_window()

if __name__ == "__main__":
    point_generation_thread = threading.Thread(target=generate_and_process_points)
    point_generation_thread.start()

    try:
        visualize()
    except KeyboardInterrupt:
        running = False
        print("Shutting down...")
        point_generation_thread.join()
