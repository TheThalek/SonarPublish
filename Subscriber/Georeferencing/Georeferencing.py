import json
import math
import numpy as np


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.ticker import FuncFormatter


from Classes import SonarData, TelemetryDataPosition, TelemetryDataPose, TelemetryDataHeading, TelemetryDataDepth, TelemetryDataAltitude
from Visualization import visualize_all_rotations
from Math import llh2ecef

# Function to load data from JSON file
def load_data_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Function to format the axis labels
def format_func(value, tick_number):
    # Convert to a string and remove the leading '1e-6 +' or similar
    return f"{value:.6f}"


# Function to process and convert each "message" in the data to data classes
def process_message(message):
    sonar = SonarData(**message['sonar']) if 'sonar' in message else None
    position = TelemetryDataPosition(**message['position']) if 'position' in message else None
    pose = TelemetryDataPose(**message['pose']) if 'pose' in message else None
    heading = TelemetryDataHeading(**message['heading']) if 'heading' in message else None
    depth = TelemetryDataDepth(**message['depth']) if 'depth' in message else None
    altitude = TelemetryDataAltitude(**message['altitude']) if 'altitude' in message else None
    
    # Return a tuple or a structured object containing all these instances
    return sonar, position, pose, heading, depth, altitude



if __name__ == "__main__":
    # filename = "sonar_telemetry_data_Nyhavna30sek.json"  # Name of your JSON file
    # filename = "sonar_telemetry_data_Nyhavna10sek_MyInterpolation.json"  # Name of your JSON file
    filename = "sonar_telemetry_data_withBetterDepthInterpolation.json"  # Name of your JSON file


    data = load_data_from_json(filename)

    # Lists for saving data from loop 
    all_R_BN = []
    all_T_N = []
    all_P_N = []  # This will now accumulate P_N points from all scans
    # R_BN_first = 0
    # R_BN_second = 0
    robot_positions_ecef = []
    latitudes = []
    longitudes = []
    depths = []

    x_ecef_first = 0
    y_ecef_first = 0
    z_ecef_first = 0
    x_ecef_second = 0
    y_ecef_second = 0
    z_ecef_second = 0

    for message in data:
        sonar, position, pose, heading, depth, altitude = process_message(message)
        
        # Go from the raw sonar format to being a point cloud references in Sonar Frame
        P_S = np.vstack((np.zeros(len(sonar.pointX)), sonar.pointX, sonar.pointY))

        # Sonar to Body transformation
        T_B = np.array([-0.6881, 0.007, -0.061]).reshape((3, 1)) # Offset in [m] between sonar and body. No pose change
    
        P_B = P_S + T_B
            #  TO DO; Visualize these points, to see if P_S and P_B has a correct offset wrt. each other
        
        # Body to NED transformation
        roll = math.radians(pose.roll)
        pitch = math.radians(pose.pitch)
        heading = math.radians(heading.heading)
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

        R_BN = R_Z @ R_Y @ R_X # Rotation matrix from body to NED
            # TO DO; Visualize this rotation matrix, to see if the rotation makes sense
        all_R_BN.append(R_BN) # For visualization later

        # Calculate the transformed points
        P_N_B = R_BN @ P_B  # Assuming P_B is correctly shaped for matrix multiplication

        longitude = math.radians(position.longitude)
        latitude = math.radians(position.latitude)
        # print("long", longitude, "lat", latitude, "\n")
        x_ecef, y_ecef, z_ecef = llh2ecef(longitude, latitude, -depth.depth)
        print(-depth.depth)
        # print("x_ecef", x_ecef, "y_ecef", y_ecef, "z_ecef", z_ecef, "\n")
        robot_positions_ecef.append((x_ecef, y_ecef, z_ecef))
        latitudes.append(math.radians(position.latitude))
        longitudes.append(math.radians(position.longitude))
        depths.append(-depth.depth)  # Assuming depth is positive downwards



        T_N = [
            [x_ecef] * len(P_N_B[0]),  # Create a list where x_ecef is replicated to match the length of P_N[0]
            [y_ecef] * len(P_N_B[0]),  # Do the same for y_ecef
            [z_ecef] * len(P_N_B[0])   # And the same for z_ecef
        ]

        # Add the offset onto the transformed points
        P_N = T_N + P_N_B
        all_P_N.append(P_N) 
        # print(P_N)







    # # Unpack the ECEF positions
    # x_data, y_data, z_data = zip(*robot_positions_ecef)

    # # Set up time data, assuming each position corresponds to a regular time interval
    # time_data = range(len(x_data))

    # # Plot X_ecef over time
    # plt.figure(figsize=(10, 4))
    # plt.plot(time_data, x_data, label='X ECEF')
    # plt.xlabel('Time')
    # plt.ylabel('X ECEF Coordinate')
    # plt.title('X ECEF over Time')
    # plt.legend()
    # plt.show()

    # # Plot Y_ecef over time
    # plt.figure(figsize=(10, 4))
    # plt.plot(time_data, y_data, label='Y ECEF')
    # plt.xlabel('Time')
    # plt.ylabel('Y ECEF Coordinate')
    # plt.title('Y ECEF over Time')
    # plt.legend()
    # plt.show()

    # # Plot Z_ecef over time
    # plt.figure(figsize=(10, 4))
    # plt.plot(time_data, z_data, label='Z ECEF')
    # plt.xlabel('Time')
    # plt.ylabel('Z ECEF Coordinate')
    # plt.title('Z ECEF over Time')
    # plt.legend()
    # plt.show()







    # # # Now plot the robot's positions in ECEF coordinates
    # # x_data, y_data, z_data = zip(*robot_positions_ecef)
    # # fig = plt.figure()
    # # ax = fig.add_subplot(111, projection='3d')
    # # ax.plot(x_data, y_data, z_data, 'r')  # Use 'plot' to connect the points with a line
    # # ax.set_xlabel('X Label')
    # # ax.set_ylabel('Y Label')
    # # ax.set_zlabel('Z Label')
    # # plt.show()







    # Now plot the latitude, longitude, and depth data with formatted y-axis
    # Latitude over time
    plt.figure(figsize=(10, 4))
    plt.plot(latitudes, label='Latitude')
    plt.xlabel('Time')
    plt.ylabel('Latitude (radians)')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))  # Format y-axis
    plt.title('Latitude over Time')
    plt.legend()
    plt.show()

    # Longitude over time
    plt.figure(figsize=(10, 4))
    plt.plot(longitudes, label='Longitude')
    plt.xlabel('Time')
    plt.ylabel('Longitude (radians)')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))  # Format y-axis
    plt.title('Longitude over Time')
    plt.legend()
    plt.show()

    # Depth over time
    plt.figure(figsize=(10, 4))
    plt.plot(depths, label='Depth')
    plt.xlabel('Time')
    plt.ylabel('Depth (meters)')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))  # Format y-axis
    plt.title('Depth over Time')
    plt.legend()
    plt.show()






    # # Initialize lists for x, y, and z coordinates
    # x_data = []
    # y_data = []
    # z_data = []

    # # Iterate through the first 100 scans only
    # for scan in all_P_N[:100]:  # This slices the list to include only the first 100 scans
    #     x_data.extend(scan[0])
    #     y_data.extend(scan[1])
    #     z_data.extend(scan[2])

    # # Now x_data, y_data, and z_data contain points from the first 100 scans
    # # Proceed with plotting
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(x_data, y_data, z_data, c='r', marker='o')
    # ax.set_xlabel('X Label')
    # ax.set_ylabel('Y Label')
    # ax.set_zlabel('Z Label')
    # plt.show()



    # visualize_all_rotations(all_R_BN)


        


            
