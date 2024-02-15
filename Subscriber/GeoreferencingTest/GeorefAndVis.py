import json

def read_data_from_file(filename):
    """
    Read data from a JSON file where each line is a separate JSON object.
    Attempts to decode each line and yields the JSON object if successful.
    Skips lines that cannot be decoded, logging an error message.
    """
    with open(filename, "r") as file:
        for line_number, line in enumerate(file, 1):
            try:
                yield json.loads(line)
            except json.decoder.JSONDecodeError as e:
                print(f"Error decoding JSON on line {line_number}: {e}")

def print_data(data):
    """
    Print the data in a format similar to the original script.
    """
    if "sonar" in data:
        sonar_data = data["sonar"]
        for pointX, pointY, beamIdx, quality, intensity in zip(sonar_data["pointX"], sonar_data["pointY"], sonar_data["beamIdx"], sonar_data["quality"], sonar_data["intensity"]):
            print(f"Received sonar data: pointX={pointX}, pointY={pointY}, beamIdx={beamIdx}, quality={quality}, intensity={intensity}")

    if "position" in data:
        position_data = data["position"]
        print(f"Received telemetry position: Latitude={position_data['latitude']}, Longitude={position_data['longitude']}")

    if "pose" in data:
        pose_data = data["pose"]
        print(f"Received telemetry pose: Roll={pose_data['roll']}, Pitch={pose_data['pitch']}")

    if "heading" in data:
        heading_data = data["heading"]
        print(f"Received telemetry heading: Heading={heading_data['heading']}")

if __name__ == "__main__":
    filename = "sonar_telemetry_data_Nyhavna_firstXsecs.json"  # Change this to your actual file path
    for data in read_data_from_file(filename):
        print_data(data)
