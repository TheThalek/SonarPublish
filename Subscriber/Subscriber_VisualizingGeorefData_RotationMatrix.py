import zmq
import sonarData_pb2
import numpy as np
import threading
from threading import Lock
from collections import deque
import open3d as o3d

georef_data_queue = deque()
lock = Lock()
running = True
rotation_matrices = []  # Store rotation matrices to visualize

def process_georef_data(data):
    global georef_data_queue, rotation_matrices
    rotation_matrix = np.array(data.rotationMatrix).reshape(3, 3)
    with lock:
        georef_data_queue.append(rotation_matrix)  # Append the new rotation matrix

def init_window():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    return vis

def visualize():
    global running, georef_data_queue, rotation_matrices
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.get_render_option().point_size = 10  # Increase point size for better visibility
    offset_increment = 0.5  # Set offset increment for each new matrix
    max_frames = 1  # Maximum number of frames to display now set to 10

    counter = 0  # Initialize counter

    # https://www.open3d.org/docs/release/python_api/open3d.geometry.TriangleMesh.html says:
    # X-axis: Red 
    # Y-axis: Green
    # Z-axis: Blue

    while running:
        if georef_data_queue:
            with lock:
                while georef_data_queue:
                    rotation_matrix = georef_data_queue.popleft()
                    rotation_matrices.append(rotation_matrix)  # Store rotation matrix
                    if len(rotation_matrices) > max_frames:
                        rotation_matrices.pop(0)  # Keep only the latest max_frames rotation matrices
                    counter += 1  # Increment counter each time a new matrix is processed
                    print(f"{counter}")

            # Clear old geometry and add new frames
            vis.clear_geometries()
            for i, rm in enumerate(rotation_matrices):
                # Create a coordinate frame for each rotation matrix
                offset = np.array([i * offset_increment, 0, 0])  # Incremental offset for each frame
                frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.2, origin=offset)
                frame.rotate(rm, center=offset)
                vis.add_geometry(frame)

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
