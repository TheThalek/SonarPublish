import threading
import zmq
import sonarData_pb2
import time
import open3d as o3d
import numpy as np
import os

# Global variable for sharing data between threads
sonar_data_queue = []
lock = threading.Lock()

def init_window():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    return vis

# Function to process incoming data
def process_sonar_data(data):
    # Access the data fields (which are repeated fields)
    pointX_list = data.pointX
    pointY_list = data.pointY
    beamIdx_list = data.beamIdx
    quality_list = data.quality
    intensity_list = data.intensity

    # Print the received sonar data
    for i in range(len(pointX_list)):
        pointX = pointX_list[i]
        pointY = pointY_list[i]
        beamIdx = beamIdx_list[i]
        quality = quality_list[i]
        intensity = intensity_list[i]

        print(f"Received sonar data: pointX={pointX}, pointY={pointY}, beamIdx={beamIdx}, quality={quality}, intensity={intensity}")


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

def data_receiver():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    try:
        while True:
            message = subscriber.recv()  # Receiving serialized data
            main_data = sonarData_pb2.Data()
            main_data.ParseFromString(message)  # Deserialize using Protocol Buffers

            # Process incoming sonar data
            if main_data.HasField("sonar"):
                process_sonar_data(main_data.sonar)
    except KeyboardInterrupt:
        print("Data receiver stopped.")
    except Exception as e:
        print(f"An error occurred in the data receiver thread: {e}")
    finally:
        subscriber.close()
        context.term()


def generate_points(x_coordinate):
    new_y = np.random.uniform(-50, 50, size=(255,))
    new_z = np.random.uniform(0, 10, size=(255,))
    new_x = np.full((255,), x_coordinate)
    new_points = np.stack((new_x, new_y, new_z), axis=-1)
    return new_points

def visualize():
    vis = init_window()
    pcd = o3d.geometry.PointCloud()
    vis.add_geometry(pcd)
    first_run = True
    x_coordinate = 0
    camera_target = np.array([0, 0, 5])

    while True:
        # Generate points directly instead of using sonar_data_queue
        points = generate_points(x_coordinate)
        first_run, camera_target = plot_points(vis, pcd, points, camera_target, first_run, x_coordinate, points[:, 2])
        
        # Increment x_coordinate for the next set of points
        x_coordinate += 0.3
        
        # Wait a bit before adding the next set of points
        time.sleep(0.01)


if __name__ == "__main__":
    # Start the data receiver thread
    receiver_thread = threading.Thread(target=data_receiver)
    receiver_thread.start()

    # Main thread for visualization
    visualize()
