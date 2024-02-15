import json
import numpy as np
import open3d as o3d



def read_data_from_file_and_collect_points(filename):
    data_points = []  # List to store all sonar data points
    x_coordinate = 0  # Initialize x coordinate
    
    try:
        with open(filename, "r") as file:
            data = json.load(file)  # Read the entire file as a single JSON object
            for entry in data:  # Assume `data` is a list of objects
                if "sonar" in entry:
                    sonar_data = entry["sonar"]
                    for pointX, pointY in zip(sonar_data["pointX"], sonar_data["pointY"]):
                        # Append x_coordinate, pointX, and pointY to data_points
                        data_points.append([x_coordinate, pointX, pointY])
                    x_coordinate += 0.05  # Increment x coordinate for each set
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    
    return np.array(data_points)  # Convert list to numpy array for visualization

def visualize(points):
    try:
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        pcd = o3d.geometry.PointCloud()
        
        pcd.points = o3d.utility.Vector3dVector(points)
        vis.add_geometry(pcd)
        vis.run()  # Run the visualizer
    except KeyboardInterrupt:
        print("Visualization interrupted by user.")
    finally:
        vis.destroy_window()  # Ensure the window is closed properly

if __name__ == "__main__":
    # filename = "sonar_telemetry_data_Nyhavna_firstXsecs.json"
    filename = "sonar_telemetry_data_Nyhavna_LongVersion.json"
    
    try:
        points = read_data_from_file_and_collect_points(filename)
        visualize(points)
    except KeyboardInterrupt:
        print("Program exited by user.")
