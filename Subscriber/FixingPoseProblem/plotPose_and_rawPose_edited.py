import json
import matplotlib.pyplot as plt
import numpy as np  # For mathematical constants and operations
import open3d as o3d  # For 3D visualization

from scipy.spatial.transform import Rotation

def rotation_x(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    Rx = np.array([[1, 0, 0],
                   [0, c, -s],
                   [0, s, c]])
    return Rx


def rotation_y(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    Ry = np.array([[c, 0, s],
                   [0, 1, 0],
                   [-s, 0, c]])
    return Ry


def rotation_z(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    Rz = np.array([[c, -s, 0],
                   [s, c, 0],
                   [0, 0, 1]])
    return Rz


def rotation_xyz(theta_x, theta_y, theta_z):
    Rx = rotation_x(theta_x)
    Ry = rotation_y(theta_y)
    Rz = rotation_z(theta_z)
    return Rz@Ry@Rx

    
def transform(theta_x, theta_y, theta_z, t_x, t_y, t_z):
    mat_t = np.eye(4)
    mat_t[:3, :3] = rotation_xyz(theta_x, theta_y, theta_z)
    mat_t[:3, 3] = np.array([t_x, t_y, t_z])
    return mat_t

def transform_from_rot(R, t_x, t_y, t_z):
    mat_t = np.eye(4)
    mat_t[:3, :3] = R
    mat_t[:3, 3] = np.array([t_x, t_y, t_z])
    return mat_t

def get_eular(C):
    # version 1: https://stackoverflow.com/questions/15022630/how-to-calculate-the-angle-from-rotation-matrix
    theta_x = np.arctan2(C[2, 1], C[2, 2])
    theta_y = np.arctan2(-1*C[2, 0], np.sqrt(C[2, 1]**2+C[2, 2]**2))
    theta_z = np.arctan2(C[1, 0], C[0, 0])
    # version 2: https://physics.stackexchange.com/questions/123522/a-simple-way-of-calculating-euler-angles-from-rotation-matrix-help
    # theta_x = np.arctan2(-C[1,2], C[2,2])
    # theta_y = np.arctan2(C[0,2], np.sqrt(C[1,2]**2+C[2,2]**2))
    # theta_z = np.arctan2(-C[0,1], C[0,0])
    return np.array([theta_x, theta_y, theta_z])

def read_data(filename):
    """
    Reads JSON data from a file.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    

def plot_data(data, attributes, title_suffix, total_duration):
    """
    Generic function to plot given telemetry data attributes.
    """
    if not data:
        print("No data to plot.")
        return
    
    num_plots = len(attributes) // 2
    fig, axs = plt.subplots(num_plots, 1, figsize=(10, 6 * num_plots))
    
    if num_plots == 1:
        axs = [axs]  # Make axs iterable if there's only one subplot
    
    timesteps = np.linspace(0, total_duration, len(data), endpoint=False)

    for i in range(num_plots):
        attr = attributes[i*2].split()
        raw_attr = attributes[i*2 + 1].split()
        
        # Ensure the key exists in the dictionary before trying to plot
        if attr[0] in data[0] and raw_attr[0] in data[0]:
            values = [entry[attr[0]][attr[1]] for entry in data if attr[0] in entry]
            raw_values = [entry[raw_attr[0]][raw_attr[1]] for entry in data if raw_attr[0] in entry]
            
            axs[i].plot(timesteps, values, label=f'{attr[1]} (Smoothed)', linestyle='-', marker='o', color='blue', alpha=0.5)
            axs[i].plot(timesteps, raw_values, label=f'{raw_attr[1]} (Raw)', linestyle='--', marker='o', color='red', alpha=0.5)
            axs[i].set_title(f"{attr[1]} and {raw_attr[1]} over Time {title_suffix}")
            axs[i].set_xlabel('Time (seconds)')
            axs[i].set_ylabel('Angle (Degrees)')
            axs[i].legend()
            axs[i].grid(True)
    
    plt.tight_layout()
    plt.show()

def get_data(data, attributes, title_suffix, total_duration):
    """
    Generic function to plot given telemetry data attributes.
    """
    if not data:
        print("No data to plot.")
        return
    
    num_plots = len(attributes) // 2
    fig, axs = plt.subplots(num_plots, 1, figsize=(10, 6 * num_plots))
    
    if num_plots == 1:
        axs = [axs]  # Make axs iterable if there's only one subplot
    
    timesteps = np.linspace(0, total_duration, len(data), endpoint=False)

    eel_collection_values = []
    raw_collection_values = []

    for i in range(num_plots):
        attr = attributes[i*2].split()
        raw_attr = attributes[i*2 + 1].split()
        
        # Ensure the key exists in the dictionary before trying to plot
        if attr[0] in data[0] and raw_attr[0] in data[0]:
            values = [entry[attr[0]][attr[1]] for entry in data if attr[0] in entry]
            raw_values = [entry[raw_attr[0]][raw_attr[1]] for entry in data if raw_attr[0] in entry]
            
            axs[i].plot(timesteps, values, label=f'{attr[1]} (Smoothed)', linestyle='-', marker='o', color='blue', alpha=0.5)
            axs[i].plot(timesteps, raw_values, label=f'{raw_attr[1]} (Raw)', linestyle='--', marker='o', color='red', alpha=0.5)
            axs[i].set_title(f"{attr[1]} and {raw_attr[1]} over Time {title_suffix}")
            axs[i].set_xlabel('Time (seconds)')
            axs[i].set_ylabel('Angle (Degrees)')
            axs[i].legend()
            axs[i].grid(True)
            eel_collection_values.append(np.pi/180*np.array(values))
            raw_collection_values.append(np.pi/180*np.array(raw_values))

    return eel_collection_values, raw_collection_values    

def plot_open3d(eel_values, raw_values):
    eel_values_roll = eel_values[0]
    eel_values_pitch = eel_values[1]
    eel_values_yaw = eel_values[2]

    raw_values_roll = raw_values[0]
    raw_values_pitch = raw_values[1]
    raw_values_yaw = raw_values[2]


    num_points = len(eel_values_roll)
    
    increment = 0.5
    eel_rots = []
    raw_rots = []
    poes = []

    coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0)
    poes.append(coord_frame)

    print("num_points: ", num_points)
    for i in range(num_points): 

        #C = Rotation.from_euler('zyx', [eel_values_yaw[i], eel_values_pitch[i], eel_values_roll[i]], degrees=True).as_matrix()

        #rot_eel = rotation_xyz(eel_values_roll[i], 0, 0)
        #rot_raw = rotation_xyz(raw_values_roll[i], 0, 0)

        #rot = rot_raw.T @ rot_eel
        
        mat_t = transform(eel_values_roll[i], eel_values_pitch[i], eel_values_yaw[i], increment*i, 3, 0)
        eel_rots.append(mat_t[:3, :3])
        
        #mat_t = transform_from_rot(rot, increment*i, 1, 0)
        # Create a coordinate frame (size=1 for visualization scale)
        #coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0)
        # Apply the transformation
        #poes.append(coord_frame.transform(mat_t))


        #C = Rotation.from_euler('zyx', [raw_values_yaw[i], raw_values_pitch[i], raw_values_roll[i]], degrees=True).as_matrix()
        mat_t = transform(raw_values_roll[i], raw_values_pitch[i], raw_values_yaw[i], increment*i, 6, 0)
        raw_rots.append(mat_t[:3, :3])
        # Create a coordinate frame (size=1 for visualization scale)
        #coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0)
        # Apply the transformation
        #poes.append(coord_frame.transform(mat_t))
    
    eel_angles = []
    raw_angles = []
    for eel_rot, raw_rot in zip(eel_rots, raw_rots):
        eel_angles.append(get_eular(eel_rot))
        raw_angles.append(get_eular(raw_rot))
    eel_angles = np.array(eel_angles)*180/np.pi 
    raw_angles = np.array(raw_angles)*180/np.pi


    timesteps = np.linspace(0, total_duration, len(data), endpoint=False)
    fig, axs = plt.subplots(3, 1, figsize=(10, 6 * 3))
    for i in range(3):
            
        axs[i].plot(timesteps, eel_angles[:, i], label=f'(Smoothed)', linestyle='-', marker='o', color='blue', alpha=0.5)
        axs[i].plot(timesteps, raw_angles[:, i], label=f'(Raw)', linestyle='--', marker='o', color='red', alpha=0.5)
        #axs[i].set_title(f"{attr[1]} and {raw_attr[1]} over Time {title_suffix}")
        axs[i].set_xlabel('Time (seconds)')
        axs[i].set_ylabel('Angle (Degrees)')
        axs[i].legend()
        axs[i].grid(True)
    
    plt.tight_layout()
    plt.show()
    


def plot_raw_data(data, total_duration):
    """
    Plots raw telemetry data.
    """
    attributes = ['rawPose rawRoll', 'rawPose rawPitch', 'rawHeading rawHeading']
    plot_data(data, attributes, "(RawData)", total_duration)


def plot_combined_data(data, total_duration):
    """
    Plots combined "smoothed" and raw telemetry data.
    """
    sanity_checkattributes = [
        'pose roll', 'rawPose rawRoll',
        'pose pitch', 'rawPose rawPitch',
        'heading heading', 'rawHeading rawHeading'
    ]
    plot_data(data, attributes, "(Combined Data)", total_duration)


def sanity_check(data, total_duration):
    """
    Plots combined "smoothed" and raw telemetry data.
    """
    attributes = [
        'pose roll', 'rawPose rawRoll',
        'pose pitch', 'rawPose rawPitch',
        'heading heading', 'rawHeading rawHeading'
    ]
    eel_values, raw_values = get_data(data, attributes, "(Combined Data)", total_duration)
    plot_open3d(eel_values, raw_values)


if __name__ == "__main__":
    filename = "pose_and_rawPose_data_Nyhavna2min.json"
    total_duration = 120  # Adjust based on your data

    # filename = "pose_and_rawPose_data_Airplane100sek.json"
    # total_duration = 100  # Adjust based on your data

    # filename = "pose_and_rawPose_data_Airplane30sek_HavingFixedPosesInPublisherByAddingOnPiAndRemovingAfterinterpolation.json"
    # total_duration = 30  # Adjust based on your data

    # filename = "pose_and_rawPose_data.json"
    # total_duration = 250  # Adjust based on your data

    data = read_data(filename)

    # Uncomment the function you wish to use
    # plot_raw_data(data, total_duration)
    #plot_combined_data(data, total_duration)  # This should plot both interpolated/smoothed data and raw data

    sanity_check(data, total_duration)
    
