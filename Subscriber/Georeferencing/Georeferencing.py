import json
import math
import numpy as np

from Classes import SonarData, TelemetryDataPosition, TelemetryDataPose, TelemetryDataHeading, TelemetryDataDepth, TelemetryDataAltitude
from Visualization import visualize_all_rotations
from Math import llh2ecef

# Function to load data from JSON file
def load_data_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

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
    filename = "sonar_telemetry_data_Nyhavna30sek.json"  # Name of your JSON file
    data = load_data_from_json(filename)

    # Lists for saving data from loop 
    all_R_BN = []
    all_P_N = []
    all_T_N = []
    # R_BN_first = 0
    # R_BN_second = 0


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
        R_BN_second = R_BN_first
        R_BN_first = R_BN

        total_change += R_BN
        print("Difference in rotation", R_BN_second-R_BN_first)
        

        # Calculate the transformed points
        P_N = R_BN @ P_B  # Assuming P_B is correctly shaped for matrix multiplication
        # print(P_N)
        # If P_B represents multiple points, make sure it's of shape (3, N)
        # And your T_N should be broadcastable to the shape of P_N

        longitude = math.radians(position.longitude)
        latitude = math.radians(position.latitude)
        # print("long", longitude, "lat", latitude, "\n")
        x_ecef, y_ecef, z_ecef = llh2ecef(longitude, latitude, -depth.depth)
        # print("x_ecef", x_ecef, "y_ecef", y_ecef, "z_ecef", z_ecef, "\n")



        # T_N = np.array([x_ecef, y_ecef, z_ecef])
        # T_N = np.reshape(T_N, (3, 1))  # Reshape for broadcasting
        # all_T_N.append(T_N)  # Save T_N for each message

        # P_N += T_N  # Add T_N to each column of P_N
        # all_P_N.append(P_N)

    visualize_all_rotations(all_R_BN)


    


        
