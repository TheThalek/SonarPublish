import zmq
import sonarData_pb2
import json

# Function to deserialize and process sonar and telemetry data
def process_data(data):
    result = {}

    if data.HasField("sonar"):
        result["sonar"] = {
            "pointX": list(data.sonar.pointX),
            "pointY": list(data.sonar.pointY),
            "beamIdx": list(data.sonar.beamIdx),
            "quality": list(data.sonar.quality),
            "intensity": list(data.sonar.intensity),
        }

    if data.HasField("position"):
        result["position"] = {
            "latitude": data.position.latitude,
            "longitude": data.position.longitude,
            "position_timestep": data.position.position_timestep,
        }

    if data.HasField("pose"):
        result["pose"] = {
            "roll": data.pose.roll,
            "pitch": data.pose.pitch,
            "pose_timestep": data.pose.pose_timestep,
        }

    if data.HasField("heading"):
        result["heading"] = {
            "heading": data.heading.heading,
            "heading_timestep": data.heading.heading_timestep,
        }

    if data.HasField("depth"):
        result["depth"] = {
            "depth": data.depth.depth,
            "depth_timestep": data.depth.depth_timestep,
        }

    if data.HasField("altitude"):
        result["altitude"] = {
            "altitude": data.altitude.altitude,
            "altitude_timestep": data.altitude.altitude_timestep,
        } 

    return result

# Function to save data to a JSON file
def save_data_to_file(data, filename="sonar_telemetry_data.json"):
    try:
        with open(filename, "r") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(data)

    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=4)

if __name__ == "__main__":
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    try:
        while True:
            multipart_message = subscriber.recv_multipart()
            # The first part of the multipart message (Normal Ungeoref point cloud and telemetry data) is what we're interested in
            data_message = sonarData_pb2.Ungeoref_And_Telemetry()
            data_message.ParseFromString(multipart_message[0])

            processed_data = process_data(data_message)
            save_data_to_file(processed_data)

    except KeyboardInterrupt:
        print("Subscriber stopped")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        subscriber.close()
        context.term()
