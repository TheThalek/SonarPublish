import threading
import zmq
import sonarData_pb2
import time
import open3d as o3d
import numpy as np
import os

# Global variables
sonar_data_queue = []
lock = threading.Lock()
running = True

def init_window():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    return vis

def process_sonar_data(data):
    global sonar_data_queue
    points = []  # Prepare to store processed points directly
    
    for i in range(len(data.pointX)):
        # Store points directly without intermediate string formatting
        point = [data.pointX[i], data.pointY[i]]  # Adjust based on actual data structure
        points.append(point)

    with lock:
        sonar_data_queue.append(points)

def plot_points(vis, pcd, points, camera_target, first_run, x_coordinate):
    temp_pcd = o3d.geometry.PointCloud()
    temp_pcd.points = o3d.utility.Vector3dVector(points)
    pcd += temp_pcd  # Efficiently combine new points with existing point cloud

    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

    if first_run:
        vis.reset_view_point(True)
        first_run = False
    else:
        # Dynamically adjust camera target based on new points
        new_target_x = np.mean(points[:, 0])
        camera_target[0] = new_target_x  # Update camera's X coordinate to focus on new points
        vis.get_view_control().set_lookat(camera_target)

    return first_run, camera_target


def data_receiver():
    print("Test - In Data receiver")
    global running
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    try:
        while running:
            # Use zmq's poll to wait for a message with a timeout, so it can exit gracefully
            if subscriber.poll(timeout=1000):  # Timeout in milliseconds
                message = subscriber.recv()  # Receiving serialized data
                main_data = sonarData_pb2.Data()
                main_data.ParseFromString(message)  # Deserialize using Protocol Buffers

                # Process incoming sonar data
                if main_data.HasField("sonar"):
                    process_sonar_data(main_data.sonar)
    except KeyboardInterrupt:
        running = False
        print("Data receiver stopped.")
    except Exception as e:
        running = False
        print(f"An error occurred in the data receiver thread: {e}")
    finally:
        subscriber.close()
        context.term()


def visualize():
    global running, sonar_data_queue
    vis = init_window()
    pcd = o3d.geometry.PointCloud()
    vis.add_geometry(pcd)
    first_run = True
    x_coordinate = 0
    camera_target = np.array([0, 0, 0])  # Start camera target at origin

    while running:
        if sonar_data_queue:
            points = []
            with lock:
                while sonar_data_queue:
                    # Process all available data batches in the queue
                    data_list = sonar_data_queue.pop(0)
                    for point in data_list:
                        # Convert direct point data to the required format
                        points.append([x_coordinate, point[0], point[1]])  # Adjust indexing based on structure
                        
            if points:
                points_np = np.array(points)
                first_run, camera_target = plot_points(vis, pcd, points_np, camera_target, first_run, x_coordinate)
                x_coordinate += 0.01  # Increment x_coordinate for the next batch of points
                
        time.sleep(0.01)

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