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
            message = subscriber.recv() # REceiving serialized data
            main_data = sonarData_pb2.Data() 
            main_data.ParseFromString(message)  # Deserialize using Protocol Buffers

            if main_data.HasField("sonar"):
                process_sonar_data(main_data.sonar)

            if main_data.HasField("position"):
                process_telemetry_position(main_data.position)

            if main_data.HasField("pose"):
                process_telemetry_pose(main_data.pose)

            if main_data.HasField("heading"):
                process_telemetry_heading(main_data.heading)

            if main_data.HasField("depth"):
                process_telemetry_depth(main_data.depth)

            if main_data.HasField("altitude"):
                process_telemetry_altitude(main_data.altitude)

    except KeyboardInterrupt:
        print("Subscriber stopped")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally: 
        subscriber.close()
        context.term()
    