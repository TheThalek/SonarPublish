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

def process_georef_data(data):
    global georef_data_queue
    points = []

    print("New georef data received:")
    for i in range(len(data.pointX)):
        point = [data.pointX[i], data.pointY[i], data.pointZ[i]]
        # print(point)
        points.append(point)

    with lock:
        georef_data_queue.append(points)

def init_window():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    return vis

def plot_points(vis, pcd, points, camera_target, first_run):
    temp_pcd = o3d.geometry.PointCloud()
    temp_pcd.points = o3d.utility.Vector3dVector(points)
    if first_run:
        pcd.points = temp_pcd.points
        vis.add_geometry(pcd)
        vis.reset_view_point(True)
        first_run = False
    else:
        pcd.points = temp_pcd.points
        vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    return first_run

def visualize():
    global running, georef_data_queue
    vis = init_window()
    pcd = o3d.geometry.PointCloud()
    first_run = True
    camera_target = np.array([0, 0, 0])  # Initialize camera target

    while running:
        if georef_data_queue:
            points = []
            with lock:
                while georef_data_queue:
                    data_list = georef_data_queue.popleft()  # Use popleft() for deque
                    for point in data_list:
                        points.append(point)
            if points:
                points_np = np.array(points)
                first_run = plot_points(vis, pcd, points_np, camera_target, first_run)

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
