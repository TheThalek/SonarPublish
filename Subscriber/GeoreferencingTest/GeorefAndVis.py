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
    
    with open(filename, "r") as file:
        data = json.load(file)
        for entry in data:
            if "sonar" in entry:
                sonar_data = entry["sonar"]
                for pointX, pointY in zip(sonar_data["pointX"], sonar_data["pointY"]):
                    data_points.append([x_coordinate, pointX, pointY])
                
                # Assuming pose and heading information is available in each entry
                if "pose" in entry and "heading" in entry:
                    pose = entry["pose"]
                    heading = entry["heading"]["heading"]
                    # print("roll", pose["roll"], "pitch", pose["pitch"], "heading", heading)
                    # Use euler_to_rotation_matrix to compute rotation matrix
                    R = euler_to_rotation_matrix(pose["roll"], pose["pitch"], heading)
                    # Append pose information (position and orientation) for visualization
                    poses.append((x_coordinate, R))
                
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
