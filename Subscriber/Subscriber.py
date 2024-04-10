import zmq
import sonarData_pb2
import time 

# Function to process incoming data
def process_georef_data(data):
    # Access the data fields (which are repeated fields)
    Georef_pointX = data.pointX
    Georef_pointY = data.pointY
    Georef_pointZ = data.pointZ
    Georef_rotationMatrix = data.rotationMatrix


    # Print the received sonar data
    for i in range(len(Georef_pointX)):
        pointX = Georef_pointX[i]
        pointY = Georef_pointY[i]
        pointZ = Georef_pointZ[i]

        # Using repr() to print full precision
        print(f"Received Georeferenced Point Cloud: PointX={repr(pointX)}, PointY={repr(pointY)}, PointZ={repr(pointZ)}")


    # for i in range(3):
    #     for j in range(3):
    #         # Printing each element in the rotation matrix on a new line for clarity
    #         print(f"{Georef_rotationMatrix[i * 3 + j]:.15f}")  # Using .15f for high precision, adjust as needed



# Function to process incoming data
def process_ungeoref_data(data):
    Ungeoref_pointX = data.pointX
    Ungeoref_pointY = data.pointY
    Ungeoref_beamIdx = data.beamIdx
    Ungeoref_quality = data.quality
    Ungeoref_intensity = data.intensity

    # Print the received sonar data
    for i in range(len(Ungeoref_pointX)):
        pointX = Ungeoref_pointX[i]
        pointY = Ungeoref_pointY[i]
        beamIdx = Ungeoref_beamIdx[i]
        quality = Ungeoref_quality[i]
        intensity = Ungeoref_intensity[i]

        print(f"Received Ungeoreferenced Point Cloud: PointX={pointX}, PointY={pointY}, BeamIdx={beamIdx}, Quality={quality}, Intensity={intensity}")


def process_telemetry_position(data):
    latitude = data.latitude
    longitude = data.longitude
    position_timestep = data.position_timestep

    print(f"Received telemetry position: Latitude={latitude}, Longitude={longitude}, Position Timestep={position_timestep}")

def process_telemetry_pose(data):
    roll = data.roll
    pitch = data.pitch
    pose_timestep = data.pose_timestep

    print(f"Received telemetry pose: Roll={roll}, Pitch={pitch}, Pose Timestep={pose_timestep}")

def process_telemetry_heading(data):
    heading = data.heading
    heading_timestep = data.heading_timestep

    print(f"Received telemetry heading: Heading={heading}, Heading Timestep={heading_timestep}")

def process_telemetry_depth(data):
    depth = data.depth
    depth_timestep = data.depth_timestep

    print(f"Received telemetry depth: Depth={depth}, Depth Timestep={depth_timestep}")

def process_telemetry_altitude(data):
    altitude = data.altitude
    altitude_timestep = data.altitude_timestep

    print(f"Received telemetry altitude: Altitude={altitude}, Altitude Timestep={altitude_timestep}")


if __name__ == "__main__":
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
    subscriber.setsockopt(zmq.RCVTIMEO, 1000)  # Set timeout in milliseconds

    try:
        while True:
            try: 
                # multipart_message = subscriber.recv()
                multipart_message = subscriber.recv_multipart()  # Receiving serialized data
                    
                # Deserializing the Ungeoreferenced Point Cloud 
                Ungeoref = sonarData_pb2.Ungeoref()
                Ungeoref.ParseFromString(multipart_message[0])
                process_ungeoref_data(Ungeoref)

                # Deserializing the Telemetry Data
                Telemetry = sonarData_pb2.Telemetry()
                Telemetry.ParseFromString(multipart_message[1])

                if Telemetry.HasField("position"):
                    process_telemetry_position(Telemetry.position)
                
                if Telemetry.HasField("pose"):
                    process_telemetry_pose(Telemetry.pose)

                if Telemetry.HasField("heading"):
                    process_telemetry_heading(Telemetry.heading)
                
                if Telemetry.HasField("depth"):
                    process_telemetry_depth(Telemetry.depth)
                
                if Telemetry.HasField("altitude"):
                    process_telemetry_altitude(Telemetry.altitude)
                

                # Deserializing the Georeferenced Point Cloud 
                Georef = sonarData_pb2.Georef()
                Georef.ParseFromString(multipart_message[2])
                process_georef_data(Georef)

            except zmq.Again:
                # This block catches the timeout exception
                continue  # This allows the loop to continue running

    except KeyboardInterrupt:
        print("Subscriber stopped")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally: 
        subscriber.close()
        context.term()