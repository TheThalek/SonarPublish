import threading
import zmq
import sonarData_pb2
import time
import open3d as o3d
import numpy as np

# Global variable for sharing data between threads
sonar_data_queue = []
lock = threading.Lock()

# Global running flag
running = True

# Initialize x_coordinate and x_increment_factor globally
x_coordinate = 0
x_increment_factor = 0.5  # This value can be adjusted based on expected data range or visualization needs


def process_sonar_data(data):
    print("Test - In Process_sonar_data")
    global sonar_data_queue
    formatted_data_list = []
    
    for i in range(len(data.pointX)):
        formatted_data = f"Received sonar data: pointX={data.pointX[i]}, pointY={data.pointY[i]}, beamIdx={data.beamIdx[i]}, quality={data.quality[i]}, intensity={data.intensity[i]}"
        formatted_data_list.append(formatted_data)

    with lock:
        print(f"Appending {len(formatted_data_list)} points to the queue")
        sonar_data_queue.append(formatted_data_list)

def data_receiver():
    print("Test - In Data receiver")
    global running
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    try:
        while running:
            if subscriber.poll(timeout=1000):
                message = subscriber.recv()
                main_data = sonarData_pb2.Data()
                main_data.ParseFromString(message)

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

def init_window():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.get_view_control().set_lookat([0, 0, 0])  # Set a known good starting point
    vis.get_view_control().set_zoom(0.5)  # Adjust zoom if necessary
    return vis

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
        # Keep the camera target fixed relative to the last x-coordinate
        # Adjust these values as necessary to keep the focus on the desired area
        target_x = x_coordinate - 10  # Adjust this value to keep the view centered as desired
        camera_target = np.array([target_x, 0, np.mean(new_z)])
        vis.get_view_control().set_lookat(camera_target)

    return first_run, camera_target


def visualize():
    global running, sonar_data_queue, y_range
    vis = init_window()
    pcd = o3d.geometry.PointCloud()
    vis.add_geometry(pcd)
    first_run = True
    x_coordinate = 0
    camera_target = np.array([0, 0, 5])

    while running:
        if sonar_data_queue:
            with lock:
                data_list = sonar_data_queue.pop(0)
                points = []
                for data_str in data_list:
                    try:
                        pointX = float(data_str.split("pointX=")[1].split(",")[0])
                        pointY = float(data_str.split("pointY=")[1].split(",")[0])
                        points.append([x_coordinate, pointX, pointY])
                    except Exception as e:
                        print(f"Error parsing data string: {e}")

                if points:
                    points_np = np.array(points)

                    # Calculate y_range based on the maximum absolute y-value in the current set of points
                    y_range = np.max(np.abs(points_np[:, 2]))

                    # Calculate x-increment factor based on y_range
                    x_increment_factor = abs(y_range) / 10  # Adjust divisor as needed

                    # Update x-coordinate using the x-increment factor
                    x_coordinate += x_increment_factor
                    print(f"x-coordinate: {x_coordinate}")  # Print the x-coordinate

                    # Plot points with updated x-coordinate
                    first_run, camera_target = plot_points(vis, pcd, points_np, camera_target, first_run, x_coordinate, points_np[:, 2])

                    # Adjust camera zoom based on maximum z-value
                    max_z = np.max(points_np[:, 2])
                    zoom_factor = 10 / max_z  # Adjust divisor as needed
                    vis.get_view_control().set_zoom(zoom_factor)

        time.sleep(0.1)


if __name__ == "__main__":
    receiver_thread = threading.Thread(target=data_receiver)
    receiver_thread.start()

    try:
        vis = visualize()
    except KeyboardInterrupt:
        running = False
        print("Program exiting...")
    finally:
        receiver_thread.join()
        if vis is not None:
            vis.destroy_window()