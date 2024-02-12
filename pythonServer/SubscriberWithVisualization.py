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

# Global running flag
running = True

def init_window():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    return vis

# Function to process incoming data
def process_sonar_data(data):
    print("Test - In Process_sonar_data")
    global sonar_data_queue
    formatted_data_list = []  # Temporary list to hold formatted data strings
    
    # Process and format the sonar data
    for i in range(len(data.pointX)):
        formatted_data = f"Received sonar data: pointX={data.pointX[i]}, pointY={data.pointY[i]}, beamIdx={data.beamIdx[i]}, quality={data.quality[i]}, intensity={data.intensity[i]}"
        formatted_data_list.append(formatted_data)

    # Append the list of formatted data strings to the queue
    with lock:
        sonar_data_queue.append(formatted_data_list)



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
    camera_target = np.array([0, 0, 5])
    print("In visualize")

    while running:
        if sonar_data_queue:
            with lock:
                print("In lock")
                data_list = sonar_data_queue.pop(0)
                points = []
                for data_str in data_list:
                    # Assuming data_str format is "Received sonar data: pointX=..., pointY=..., beamIdx=..., quality=..., intensity=..."
                    # Extract pointX and pointY values from the string
                    try:
                        pointX = float(data_str.split("pointX=")[1].split(",")[0])
                        pointY = float(data_str.split("pointY=")[1].split(",")[0])
                        points.append([x_coordinate, pointX, pointY])
                    except Exception as e:
                        print(f"Error parsing data string: {e}")
                
                if points:
                    points_np = np.array(points)
                    first_run, camera_target = plot_points(vis, pcd, points_np, camera_target, first_run, x_coordinate, points_np[:, 2])
                    x_coordinate += 0.3
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
        # Ensure threads are joined
        receiver_thread.join()

