import zmq
import sonarData_pb2
import time
import open3d as o3d
import numpy as np
import threading
from threading import Lock
from collections import deque  # Import deque

georef_data_queue = deque()  # Initialize as deque
lock = Lock()
running = True
fake_shift = 0

def process_georef_data(data):
    global georef_data_queue, fake_shift
    points = []

    # Convert the flattened rotation matrix to a 3x3 matrix
    rotation_matrix = np.array(data.rotationMatrix_NED).reshape(3, 3)
    # Define a constant jump distance
    jump_distance = 0.01
    # Calculate the "fake" shift as a move in the direction of the chosen axis by the jump distance
    direction_vector = rotation_matrix[:, 0]  # Extracting the first column, to get the direction of the x axis from the rotation matrix, e.g. the direction of the 
    fake_shift += direction_vector * jump_distance

    # print("New georef data received:")
    for i in range(len(data.x_pointCld_body_NED)):
        # Apply the shift to each point
        point = [data.x_pointCld_body_NED[i] + fake_shift[0], data.y_pointCld_body_NED[i] + fake_shift[1], data.z_pointCld_body_NED[i] + fake_shift[2]]
        points.append(point)

    with lock:
        georef_data_queue.append(points)


def init_window():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    return vis


def visualize():
    global running, georef_data_queue
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    pcd = o3d.geometry.PointCloud()
    first_run = True
    all_points = []  # Initialize outside the while loop to accumulate points

    while running:
        if georef_data_queue:
            with lock:
                while georef_data_queue:
                    data_list = georef_data_queue.popleft()
                    all_points.extend(data_list)  # Extend the all_points list with new data
            if all_points:
                points_np = np.array(all_points)
                # Update camera target to the mean of the latest points
                camera_target = np.mean(points_np, axis=0)
                temp_pcd = o3d.geometry.PointCloud()
                temp_pcd.points = o3d.utility.Vector3dVector(points_np)
                if first_run:
                    pcd.points = temp_pcd.points
                    vis.add_geometry(pcd)
                    vis.reset_view_point(True)
                    first_run = False
                else:
                    pcd.points = temp_pcd.points
                    vis.update_geometry(pcd)
                # Set camera to look at the mean of the latest points
                vis.get_view_control().set_lookat(camera_target)
                vis.poll_events()
                vis.update_renderer()

                
def data_receiver():
    global running
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
    try:
        while running:
            try:
                multipart_message = subscriber.recv_multipart()
                Georef_NED = sonarData_pb2.Georef_NED()
                Georef_NED.ParseFromString(multipart_message[2])
                process_georef_data(Georef_NED)
            except zmq.Again:
                continue
    except KeyboardInterrupt:
        running = False
        print("Data receiver stopped.")
    except Exception as e:
        running = False
        print(f"An error occurred in the data receiver thread: {e}")
    finally:
        subscriber.close()
        context.term()

if __name__ == "__main__":
    receiver_thread = threading.Thread(target=data_receiver)
    receiver_thread.start()

    try:
        visualize()
    except KeyboardInterrupt:
        running = False
        print("Program exiting...")
    finally:
        receiver_thread.join()