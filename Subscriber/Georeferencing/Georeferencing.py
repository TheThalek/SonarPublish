import json
from Classes import SonarData, TelemetryDataPosition, TelemetryDataPose, TelemetryDataHeading, TelemetryDataDepth, TelemetryDataAltitude
import math
import numpy as np

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

    for message in data:
        sonar, position, pose, heading, depth, altitude = process_message(message)
        
        # Go from the raw sonar format to being a point cloud references in Sonar Frame
        P_S = np.vstack((np.zeros(len(sonar.pointX)), sonar.pointX, sonar.pointY))

        # Sonar to Body transformation
        T_B = np.array([-0.6881, 0.007, -0.061]).reshape((3, 1)) # Offset in [m] between sonar and body. No pose change
    
        P_B = P_S + T_B
            #  TO DO; Visualize these points, to see if P_S and P_B has a correct offset wrt. each other
        
        # Body to NED transformation
        R_X = np.array([
            [1, 0, 0],
            [0, math.cos(pose.roll), -math.sin(pose.roll)],
            [0, math.sin(pose.roll), math.cos(pose.roll)]
        ])

        R_Y = np.array([
            [math.cos(pose.pitch), 0, math.sin(pose.pitch)],
            [0, 1, 0],
            [-math.sin(pose.pitch), 0, math.cos(pose.pitch)]
        ])

        R_Z = np.array([
            [math.cos(heading.heading), -math.sin(heading.heading), 0],
            [math.sin(heading.heading), math.cos(heading.heading), 0],
            [0, 0, 1]
        ])

        R_BN = R_Z @ R_Y @ R_X # Rotation matrix from body to NED
            # TO DO; Visualize this rotation matrix, to see if the rotation makes sense

        # Calculate the transformed points
        P_N = R_BN @ P_B  # Assuming P_B is correctly shaped for matrix multiplication

        # If P_B represents multiple points, make sure it's of shape (3, N)
        # And your T_N should be broadcastable to the shape of P_N
        T_N = np.array([0, 0, 0])
        T_N = np.reshape(T_N, (3, 1))  # Reshape for broadcasting

        P_N += T_N  # Add T_N to each column of P_N
            # TO DO; Visualize these points, to see that they follow the rotation matrix as well




        
