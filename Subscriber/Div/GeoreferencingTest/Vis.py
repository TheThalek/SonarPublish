import json
import numpy as np
import open3d as o3d
import math

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
    x_coordinate = 0
    yaw = 0  # Initial yaw angle
    
    with open(filename, "r") as file:
        data = json.load(file)
        for entry in data:
            if "sonar" in entry:
                sonar_data = entry["sonar"]
                for pointX, pointY in zip(sonar_data["pointX"], sonar_data["pointY"]):
                    data_points.append([x_coordinate, pointX, pointY])
                
                # Generate rotation matrix for the current pose
                R = euler_to_rotation_matrix(0, 0, yaw)  # Assuming zero roll and pitch
                
                # Append pose information (position and orientation) for visualization
                poses.append((x_coordinate, R))
                
                # Increment yaw angle by 1 degree for the next iteration
                yaw += 1
                
                x_coordinate += 0.1
    
    return np.array(data_points), poses

def visualize(points, poses):
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    vis.add_geometry(pcd)
    
    # Visualize poses
    for x, R in poses:
        mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[x, 0, 0])
        mesh_frame.rotate(R, center=[x, 0, 0])
        vis.add_geometry(mesh_frame)
    
    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    filename = "sonar_telemetry_data_Nyhavna_firstXsecs.json"
    points, poses = read_data_from_file_and_collect_points_and_poses(filename)
    visualize(points, poses)
