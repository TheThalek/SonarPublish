import json
import numpy as np
import open3d as o3d
import math
from pyproj import Proj, transform



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

def read_data_from_file_and_collect_points_and_poses(filename):
    data_points = []
    poses = []
    
    with open(filename, "r") as file:
        data = json.load(file)
        for entry in data:
            if "sonar" in entry:
                sonar_data = entry["sonar"]
                position = entry.get("position", {})  # Extract position data
                latitude = position.get("latitude", None)  # Get latitude
                longitude = position.get("longitude", None)  # Get longitude
                pose = entry.get("pose", {})  # Extract pose data
                roll = pose.get("roll", 0)  # Get roll
                pitch = pose.get("pitch", 0)  # Get pitch
                heading = entry.get("heading", {}).get("heading", 0)  # Get heading
                
                R_pose = euler_to_rotation_matrix(roll, pitch, heading)
                
                # Lever arm from body to sonar
                X_B = -688.1 / 1000  # Convert mm to meters
                Y_B = 7.0 / 1000
                Z_B = -61.0 / 1000
                
                for pointX, pointY in zip(sonar_data["pointX"], sonar_data["pointY"]):
                    # Adjust sonar point coordinates based on the lever arm
                    sonar_point = np.array([pointX, pointY, 0])
                    # Apply rotation matrix to the sonar point
                    sonar_point_rotated = R_pose.dot(sonar_point)
                    # Adjust the point by the lever arm offset
                    sonar_point_adjusted = sonar_point_rotated + np.array([X_B, Y_B, Z_B])
                    data_points.append(sonar_point_adjusted)

                # Append pose information (position and orientation) for visualization
                poses.append((latitude, longitude, R_pose))
    
    return np.array(data_points), poses


def visualize(points, poses):
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    vis.add_geometry(pcd)
    
    # Visualize poses
    for lat, lon, R in poses:
        # Set the position of the coordinate frame to the robot's latitude and longitude
        mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[lon, lat, 0])
        # Rotate the coordinate frame according to the robot's orientation
        vis.add_geometry(mesh_frame.rotate(R, center=[0, 0, 0]))
    
    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    filename = "sonar_telemetry_data_Nyhavna_firstXsecs.json"
    points, poses = read_data_from_file_and_collect_points_and_poses(filename)
    visualize(points, poses)
