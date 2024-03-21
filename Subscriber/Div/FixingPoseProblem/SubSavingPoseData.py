import zmq
import sonarData_pb2
import json
import os


def save_data_to_file(data, filename="pose_data.json"):
    """
    Append data to a file in JSON format, ensuring the file remains valid JSON.
    """
    # Check if the file already exists and has content
    try:
        with open(filename, "r") as file:
            existing_data = json.load(file)
            if not isinstance(existing_data, list):
                existing_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(data)

    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=4)


def process_telemetry_pose(data):
    print(f"Received telemetry pose: Roll={data.roll}, Pitch={data.pitch}, Pose Timestep={data.pose_timestep}")
    return {"roll": data.roll, "pitch": data.pitch}

def process_telemetry_heading(data):
    print(f"Received telemetry heading: Heading={data.heading}, Heading Timestep={data.heading_timestep}")
    return {"heading": data.heading}

if __name__ == "__main__":
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")


    # Set a timeout for the recv operation
    subscriber.setsockopt(zmq.RCVTIMEO, 1000)

    try:
        while True:
            message = subscriber.recv()  # Receiving serialized data
            main_data = sonarData_pb2.Data() 
            main_data.ParseFromString(message)  # Deserialize using Protocol Buffers

            combined_data = {}

            # if main_data.HasField("sonar"):
            #     combined_data["sonar"] = process_sonar_data(main_data.sonar)

            # if main_data.HasField("position"):
            #     combined_data["position"] = process_telemetry_position(main_data.position)

            if main_data.HasField("pose"):
                combined_data["pose"] = process_telemetry_pose(main_data.pose)

            if main_data.HasField("heading"):
                combined_data["heading"] = process_telemetry_heading(main_data.heading)

            # Assume similar blocks for depth and altitude if necessary

            # Save the combined data to file
            if combined_data:
                save_data_to_file(combined_data)

    except KeyboardInterrupt:
        print("Subscriber stopped")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        subscriber.close()
        context.term()
