import zmq
import sonarData_pb2
import json
import math
import numpy as np
import open3d as o3d
import threading

from Math import llh2ecef

sonar_data_queue = []  # This will hold processed data ready for visualization
lock = threading.Lock()  # Ensure thread-safe access to the sonar_data_queue
running = True  # Control flag for running threads

# Function to deserialize and process sonar and telemetry data
def process_data(data):
    result = {}

    if data.HasField("sonar"):
        result["sonar"] = {
            "pointX": list(data.sonar.pointX),
            "pointY": list(data.sonar.pointY),
            "beamIdx": list(data.sonar.beamIdx),
            "quality": list(data.sonar.quality),
            "intensity": list(data.sonar.intensity),
        }

    if data.HasField("position"):
        result["position"] = {
            "latitude": data.position.latitude,
            "longitude": data.position.longitude,
            "position_timestep": data.position.position_timestep,
        }

    if data.HasField("pose"):
        result["pose"] = {
            "roll": data.pose.roll,
            "pitch": data.pose.pitch,
            "pose_timestep": data.pose.pose_timestep,
        }

    if data.HasField("heading"):
        result["heading"] = {
            "heading": data.heading.heading,
            "heading_timestep": data.heading.heading_timestep,
        }

    if data.HasField("depth"):
        result["depth"] = {
            "depth": data.depth.depth,
            "depth_timestep": data.depth.depth_timestep,
        }

    if data.HasField("altitude"):
        result["altitude"] = {
            "altitude": data.altitude.altitude,
            "altitude_timestep": data.altitude.altitude_timestep,
        } 

    return result

def georeference(processed_data):
    if all(k in processed_data for k in ['sonar', 'position', 'pose', 'heading', 'depth']):
        sonar = processed_data["sonar"]
        position = processed_data["position"]
        pose = processed_data["pose"]
        heading = processed_data["heading"]
        depth = processed_data["depth"]

        P_S = np.vstack((np.zeros(len(sonar["pointX"])), sonar["pointX"], sonar["pointY"]))
        T_B = np.array([-0.6881, 0.007, -0.061]).reshape((3, 1))  # Sonar to Body transformation offset
        P_B = P_S + T_B  # Transform sonar points to Body Frame

        # Body to NED transformation using pose and heading
        roll, pitch, heading = map(math.radians, [pose["roll"], pose["pitch"], heading["heading"]])

        R_X = np.array([
            [1, 0, 0],
            [0, math.cos(roll), -math.sin(roll)],
            [0, math.sin(roll), math.cos(roll)]
        ])

        R_Y = np.array([
            [math.cos(pitch), 0, math.sin(pitch)],
            [0, 1, 0],
            [-math.sin(pitch), 0, math.cos(pitch)]
        ])

        R_Z = np.array([
            [math.cos(heading), -math.sin(heading), 0],
            [math.sin(heading), math.cos(heading), 0],
            [0, 0, 1]
        ])

        R_BN = R_Z @ R_Y @ R_X  # Rotation matrix from body to NED

        P_N_B = R_BN @ P_B  # Transform Body Frame points to NED Frame

        # Convert position to ECEF for absolute positioning
        longitude, latitude = map(math.radians, [position["longitude"], position["latitude"]])
        x_ecef, y_ecef, z_ecef = llh2ecef(longitude, latitude, -depth["depth"])

        # Add the ECEF offset onto the NED transformed points
        T_N = np.array([x_ecef, y_ecef, z_ecef]).reshape((3, 1))
        P_ECEF = T_N + P_N_B  # Convert NED points to ECEF Frame

        return P_ECEF.T  # Transpose to get points in the shape (N, 3)
    else:
        print("Data missing for georeferencing...")
        return np.array([])  # Return empty array if data is missing


def visualize(sonar_data_queue):
    global running
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    pcd = o3d.geometry.PointCloud()
    vis.add_geometry(pcd)
    first_run = True
    camera_target = np.array([0, 0, 0])  # Initialize camera target

    while running:
        if not sonar_data_queue:
            continue

        with lock:
            sonar_data = sonar_data_queue.pop(0)  # Retrieve the latest georeferenced points

        if len(sonar_data) > 0:
            pcd.points = o3d.utility.Vector3dVector(sonar_data)
            vis.update_geometry(pcd)

            if first_run:
                vis.reset_view_point(True)
                first_run = False
            else:
                # Adjust camera target based on the new points' centroid
                centroid = np.mean(sonar_data, axis=0)
                camera_target = centroid[:3]  # Assuming sonar_data includes z-coordinate
                vis.get_view_control().set_lookat(camera_target)

            vis.poll_events()
            vis.update_renderer()
        else:
            print("No points to visualize.")

    vis.destroy_window()

def data_receiver(context, sonar_data_queue):
    global running
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    while running:
        try:
            multipart_message = subscriber.recv_multipart()
            data_message = sonarData_pb2.Ungeoref_And_Telemetry()
            data_message.ParseFromString(multipart_message[0])

            processed_data = process_data(data_message)
            georeferenced_data = georeference(processed_data)  # Perform georeferencing

            with lock:
                sonar_data_queue.append(georeferenced_data)  # Queue georeferenced points for visualization

        except zmq.Again:
            print("Waiting for data...")
        except KeyboardInterrupt:
            running = False
        except Exception as e:
            print(f"Error in data_receiver: {e}")

    subscriber.close()


def main():
    global running
    context = zmq.Context()

    # Initialize and start threads
    receiver_thread = threading.Thread(target=data_receiver, args=(context, sonar_data_queue))
    visualization_thread = threading.Thread(target=visualize, args=(sonar_data_queue,))

    receiver_thread.start()
    visualization_thread.start()

    try:
        receiver_thread.join()
        visualization_thread.join()
    except KeyboardInterrupt:
        print("Interrupted by user, stopping...")
        running = False
    finally:
        context.term()
        print("Cleanup completed, exiting.")

if __name__ == "__main__":
    main()