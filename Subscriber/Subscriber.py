import zmq
import sonarData_pb2
import time 

# Function to process incoming data
def process_sonar_data(data):
    # Access the data fields (which are repeated fields)
    pointX_list = data.pointX
    pointY_list = data.pointY
    beamIdx_list = data.beamIdx
    quality_list = data.quality
    intensity_list = data.intensity

    # Print the received sonar data
    for i in range(len(pointX_list)):
        pointX = pointX_list[i]
        pointY = pointY_list[i]
        beamIdx = beamIdx_list[i]
        quality = quality_list[i]
        intensity = intensity_list[i]

        print(f"Received sonar data: pointX={pointX}, pointY={pointY}, beamIdx={beamIdx}, quality={quality}, intensity={intensity}")

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

def process_rawPoses(data):
    raw_roll = data.raw_roll
    raw_pitch = data.raw_pitch
    print(f"Received raw poses: Roll={raw_roll}, Pitch={raw_pitch}")

def process_rawheading(data):
    raw_heading = data.raw_heading
    print(f"Received raw heading: Heading={raw_heading}")




def cleanup_socket(socket_path):
    if os.path.exists(socket_path):
        os.remove(socket_path)

if __name__ == "__main__":
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")


    try:
        while True:
            # multipart_message = subscriber.recv()
            multipart_message = subscriber.recv_multipart()  # Receiving serialized data
                

            # Deserializing the Ungeoreferences Point Cloud and Its Telemetry Data
            Ungeoref_And_Telemetry = sonarData_pb2.Ungeoref_And_Telemetry()
            Ungeoref_And_Telemetry.ParseFromString(multipart_message[0])

            if Ungeoref_And_Telemetry.HasField("sonar"):
                process_sonar_data(Ungeoref_And_Telemetry.sonar)

            if Ungeoref_And_Telemetry.HasField("position"):
                process_telemetry_position(Ungeoref_And_Telemetry.position)

            if Ungeoref_And_Telemetry.HasField("pose"):
                process_telemetry_pose(Ungeoref_And_Telemetry.pose)

            if Ungeoref_And_Telemetry.HasField("heading"):
                process_telemetry_heading(Ungeoref_And_Telemetry.heading)

            if Ungeoref_And_Telemetry.HasField("depth"):
                process_telemetry_depth(Ungeoref_And_Telemetry.depth)

            if Ungeoref_And_Telemetry.HasField("altitude"):
                process_telemetry_altitude(Ungeoref_And_Telemetry.altitude)

            # Deserializing the Raw Pose Data (From before the interpolation) For Testing
            TestData_RawPoses = sonarData_pb2.TestData_RawPoses()
            TestData_RawPoses.ParseFromString(multipart_message[1])

            if TestData_RawPoses.HasField("raw_rollAndpitch"):
                process_rawPoses(TestData_RawPoses.raw_rollAndpitch)
            if TestData_RawPoses.HasField("raw_heading"):
                process_rawheading(TestData_RawPoses.raw_heading)

    except KeyboardInterrupt:
        print("Subscriber stopped")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally: 
        subscriber.close()
        context.term()
    