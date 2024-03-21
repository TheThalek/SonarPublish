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


def euler_to_rotation_matrix(roll, pitch, yaw):
    # Convert degrees to radians
    roll, pitch, yaw = np.radians([roll, pitch, yaw])
    
    # Create individual rotation matrices
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]])
    
    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])
    
    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])
    
    # Combined rotation matrix
    R = np.dot(R_z, np.dot(R_y, R_x))
    return R


def init_window():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    return vis


def process_sonar_data(data, pose):
    global sonar_data_queue
    points = []  # Prepare to store processed points directly
    
    for i in range(len(data.pointX)):
        point = [data.pointX[i], data.pointY[i]]  # Adjust based on actual data structure
        points.append(point)

    with lock:
        # Append both points and pose as a tuple
        sonar_data_queue.append((points, pose))


def process_telemetry_pose(data):
    # This function should return the pose data (roll, pitch, yaw) for now.
    # Adjust these field names based on your actual protobuf definitions.
    roll = data.roll
    pitch = data.pitch
    heading = data.heading  # Assuming 'heading' is used for yaw
    return (roll, pitch, heading)


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
    global running, sonar_data_queue
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    try:
        while running:
            multipart_message = subscriber.recv_multipart()  # Receiving serialized data
            Ungeoref_And_Telemetry = sonarData_pb2.Ungeoref_And_Telemetry()
            Ungeoref_And_Telemetry.ParseFromString(multipart_message[0])

            pose = None
            if Ungeoref_And_Telemetry.HasField("pose"):
                pose = process_telemetry_pose(Ungeoref_And_Telemetry.pose)

            if Ungeoref_And_Telemetry.HasField("sonar"):
                # Now we pass along the pose with the sonar data
                process_sonar_data(Ungeoref_And_Telemetry.sonar, pose)

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
    global running, sonar_data_queue  # Consider including a pose queue if necessary
    vis = init_window()
    pcd = o3d.geometry.PointCloud()
    vis.add_geometry(pcd)
    first_run = True
    x_coordinate = 0
    camera_target = np.array([0, 0, 0])  # Start camera target at origin

    while running:
        if sonar_data_queue:
            points = []
            poses = []  # Assuming you have pose data alongside sonar points
            with lock:
                while sonar_data_queue:
                    # Process all available data batches in the queue
                    data_list, pose_list = sonar_data_queue.pop(0)  # Adjust based on your data structure
                    for point in data_list:
                        points.append([x_coordinate, point[0], point[1]])  # Adjust based on structure
                    poses.extend(pose_list)  # Collect poses for current batch

            if points:
                points_np = np.array(points)

                # Visualize points
                first_run, camera_target = plot_points(vis, pcd, points_np, camera_target, first_run, x_coordinate)

                # Visualize poses
                for pose in poses:
                    roll, pitch, yaw = pose  # Unpack your pose data
                    R = euler_to_rotation_matrix(roll, pitch, yaw)
                    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[x_coordinate, 0, 0])
                    mesh_frame.rotate(R, center=[x_coordinate, 0, 0])  # Apply rotation
                    vis.add_geometry(mesh_frame)

                # Adjust x_coordinate based on the processed data
                y_range = np.max(points_np[:, 1]) - np.min(points_np[:, 1])
                x_coordinate += y_range / 100

    vis.run()
    vis.destroy_window()



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