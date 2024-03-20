import open3d as o3d
import numpy as np

def visualize_all_rotations(rotations, spacing=1):
    mesh = mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()





    # """
    # Visualizes all rotations with automatic x-axis offsets in Open3D.

    # :param rotations: List of rotation matrices (R_BN).
    # :param spacing: Distance between consecutive rotations along the x-axis.
    # """
    # # Create an Open3D point cloud to visualize the axes points
    # pcd = o3d.geometry.PointCloud()

    # # Define axis points in their default orientation
    # axis_points = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])

    # # Create a list to hold all points for visualization
    # all_points = []

    # for i, R_BN in enumerate(rotations):
    #     # Generate offset based on index to separate each set of axes visually
    #     offset = np.array([i * spacing, 0, 0])

    #     # Apply rotation and add offset to each of the axis points
    #     rotated_points = np.dot(R_BN, axis_points.T).T + offset
    #     all_points.extend(rotated_points)

    # # Convert all points into a format suitable for Open3D
    # pcd.points = o3d.utility.Vector3dVector(all_points)

    # # Create lines to represent the axes
    # # Lines are defined by pairs of indices into the points list
    # lines = []
    # colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # Colors for the X, Y, Z axes
    # line_colors = []

    # for i in range(len(rotations)):
    #     base_index = i * 4  # Starting index for each set of axes points
    #     lines.append([base_index, base_index + 1])  # X-axis
    #     lines.append([base_index, base_index + 2])  # Y-axis
    #     lines.append([base_index, base_index + 3])  # Z-axis
    #     line_colors.extend(colors)

    # # Create an Open3D line set for the axes lines
    # line_set = o3d.geometry.LineSet(
    #     points=o3d.utility.Vector3dVector(all_points),
    #     lines=o3d.utility.Vector2iVector(lines),
    # )
    # line_set.colors = o3d.utility.Vector3dVector(line_colors)

    # # Initialize an Open3D visualizer
    # vis = o3d.visualization.Visualizer()
    # vis.create_window()
    # vis.add_geometry(pcd)
    # vis.add_geometry(line_set)
    # vis.run()
    # vis.destroy_window()
