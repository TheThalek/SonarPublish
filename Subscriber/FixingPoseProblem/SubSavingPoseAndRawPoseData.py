import zmq
import sonarData_pb2
import json
import os


def save_data_to_file(data, filename="pose_and_rawPose_data.json"):
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
    # print(f"Received telemetry pose: Roll={data.roll}, Pitch={data.pitch}, Pose Timestep={data.pose_timestep}")
    return {"roll": data.roll, "pitch": data.pitch}

def process_telemetry_heading(data):
    # print(f"Received telemetry heading: Heading={data.heading}, Heading Timestep={data.heading_timestep}")
    return {"heading": data.heading}

def process_telemetry_rawPose(data):
    # print(f"Received raw pose: raw Roll={data.raw_roll}, raw Pitch={data.raw_pitch}, raw Pose Timestep={data.raw_pose_timestep}")
    return {"rawRoll": data.raw_roll, "rawPitch": data.raw_pitch}

def process_telemetry_rawHeading(data):
    # print(f"Received raw heading: rawHeading={data.raw_heading}, raw Heading Timestep={data.raw_heading_timestep}")
    return {"rawHeading": data.raw_heading}

if __name__ == "__main__":
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    try:
        while True:
            multipart_message = subscriber.recv_multipart()  # Receiving serialized data

            combined_data = {}

            # Deserializing the Ungeoreferences Point Cloud and Its Telemetry Data
            Ungeoref_And_Telemetry = sonarData_pb2.Ungeoref_And_Telemetry()
            Ungeoref_And_Telemetry.ParseFromString(multipart_message[0])

            if Ungeoref_And_Telemetry.HasField("pose"):
                combined_data["pose"] = process_telemetry_pose(Ungeoref_And_Telemetry.pose)

            if Ungeoref_And_Telemetry.HasField("heading"):
                combined_data["heading"] = process_telemetry_heading(Ungeoref_And_Telemetry.heading)


            # Deserializing the Raw Pose Data (From before the interpolation) For Testing
            TestData_RawPoses = sonarData_pb2.TestData_RawPoses()
            TestData_RawPoses.ParseFromString(multipart_message[1])

            if TestData_RawPoses.HasField("raw_rollAndpitch"):
                combined_data["rawPose"] = process_telemetry_rawPose(TestData_RawPoses.raw_rollAndpitch)

            if TestData_RawPoses.HasField("raw_heading"):
                combined_data["rawHeading"] = process_telemetry_rawHeading (TestData_RawPoses.raw_heading)


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
