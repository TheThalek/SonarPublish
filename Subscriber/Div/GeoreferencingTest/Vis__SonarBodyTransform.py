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
                # R = euler_to_rotation_matrix(0, 0, yaw)  # Assuming zero roll and pitch
                R = euler_to_rotation_matrix(0, 0, 0)  # Assuming zero roll and pitch
               

                # # Assuming pose and heading information is available in each entry
                # if "pose" in entry and "heading" in entry:
                #     pose = entry["pose"]
                #     heading = entry["heading"]["heading"]
                #     # print("roll", pose["roll"], "pitch", pose["pitch"], "heading", heading)
                #     # Use euler_to_rotation_matrix to compute rotation matrix
                #     R = euler_to_rotation_matrix(pose["roll"], pose["pitch"], heading)
                #     # Append pose information (position and orientation) for visualization
                #     poses.append((x_coordinate, R))
                
                # Append pose information (position and orientation) for visualization
                poses.append((x_coordinate, R))
                
                # Increment yaw angle by 1 degree for the next iteration
                # yaw += 1
                
                x_coordinate += 0.1

                data_points_Sonar = data_points
                poses_sonar = poses

                # Then transform the pose/frame(?) and the data points to body
                T_B = [-0.6881, 0.007, -0.061] # The sonar- to body-frame "offset"

                data_points_body = []
                for point in data_points_Sonar:
                    transformed_point = [point[0] + T_B[0], point[1] + T_B[1], point[2] + T_B[2]]
                    data_points_body.append(transformed_point)

                poses_body = [(pos[0] + T_B[0], pos[1]) for pos in poses_sonar]  # Applying offset to x-coordinate of pose
                

    return np.array(data_points_Sonar), poses_sonar, np.array(data_points_body), poses_body



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



# def visualize_check(points_sonar, points_body, poses_sonar, poses_body):
#     vis = o3d.visualization.Visualizer()
#     vis.create_window()

#     # SONAR points in red, BODY points in blue
#     pcd_sonar = o3d.geometry.PointCloud()
#     pcd_sonar.points = o3d.utility.Vector3dVector(points_sonar)
#     pcd_sonar.paint_uniform_color([1, 0, 0])
#     vis.add_geometry(pcd_sonar)

#     pcd_body = o3d.geometry.PointCloud()
#     pcd_body.points = o3d.utility.Vector3dVector(points_body)
#     pcd_body.paint_uniform_color([0, 0, 1])
#     vis.add_geometry(pcd_body)

#     # Visualize SONAR and BODY frames
#     T_B = [-0.6881, 0.007, -0.061]  # Re-use this for BODY frame origin
#     for (x_s, R_s), (x_b, R_b) in zip(poses_sonar, poses_body):
#         mesh_frame_sonar = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[x_s, 0, 0])
#         mesh_frame_sonar.rotate(R_s, center=[x_s, 0, 0])
#         vis.add_geometry(mesh_frame_sonar)

#         mesh_frame_body = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[x_b, T_B[1], T_B[2]])
#         # mesh_frame_body.rotate(R_b, center=[x_b, T_B[1], T_B[2]])
#         mesh_frame_body.rotate(R_b, center=[x_b, T_B[1], T_B[2]])

#         print("x_b", x_b, "T_B[1]", T_B[1], "T_B[2]", T_B[2])
#         vis.add_geometry(mesh_frame_body)

#     vis.run()
#     vis.destroy_window()
#     # In this code:
#     # Red points represent the SONAR data, and blue points represent the BODY data.
#     # Both the SONAR and BODY frames are visualized, with their origins and orientations represented by the coordinate frames.
#     # By visually inspecting the overlap or alignment of the red and blue points in the 3D visualization, you can determine if the transformation was applied correctly.




if __name__ == "__main__":
    filename = "sonar_telemetry_data_Nyhavna_firstXsecs.json"
    points_sonar, poses_sonar, points_body, poses_body = read_data_from_file_and_collect_points_and_poses(filename)
    # visualize(points_sonar, poses_sonar)
    visualize(points_body, poses_body)
    # visualize_check(points_sonar, points_body, poses_sonar, poses_body)

    