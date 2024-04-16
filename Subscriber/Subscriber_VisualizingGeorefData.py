
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
previous_position_ecef = np.array([0, 0, 0])  # Initialize the previous ECEF position
shift = [0,0,0]
first_scan = 1

def process_georef_data(data):
    global georef_data_queue, previous_position_ecef, shift, first_scan
    points = []

    # New: Include body position in ECEF
        
    body_position_ecef = np.array([data.x_body_position_ecef, data.y_body_position_ecef, data.z_body_position_ecef])

    # Calculate shift based on the previous position
    if first_scan:
        shift  = [0,0,0]
        first_scan = 0
        previous_position_ecef = body_position_ecef  # Update previous position for next iteration
    else:
        shift += (body_position_ecef - previous_position_ecef)
        previous_position_ecef = body_position_ecef  # Update previous position for next iteration


    print("Shift applied:", shift)

    for i in range(len(data.x_pointCld_body)):
        # Apply the shift to each point
        point = [data.x_pointCld_body[i] + shift[0], data.y_pointCld_body[i] + shift[1], data.z_pointCld_body[i] + shift[2]]
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
                Georef = sonarData_pb2.Georef()
                Georef.ParseFromString(multipart_message[2])
                process_georef_data(Georef)
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