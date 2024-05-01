import zmq
import sonarData_pb2
import numpy as np
import threading
import matplotlib.pyplot as plt

# Lists to hold telemetry data
all_roll = []
all_pitch = []
all_yaw = []

running = True

def process_telemetry_data(telemetry):
    global all_roll, all_pitch, all_yaw
    all_roll.append(np.degrees(telemetry.pose.roll))  # Assuming roll is in radians
    all_pitch.append(np.degrees(telemetry.pose.pitch))
    all_yaw.append(np.degrees(telemetry.heading.heading))  # Assuming heading is in radians

def process_georef_data(Georef):
    # Implement this based on your georeferencing needs
    # For demonstration, we'll just print a message
    print("Processing Georef data...")

def data_receiver():
    global running
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
    try:
        while running:
            try:
                multipart_message = subscriber.recv_multipart()
                if len(multipart_message) > 1:  # Ensure there's a telemetry message
                    telemetry = sonarData_pb2.Telemetry()
                    telemetry.ParseFromString(multipart_message[1])  # Assuming second part is telemetry
                    process_telemetry_data(telemetry)
                if len(multipart_message) > 2:  # Ensure there's a Georef message
                    Georef = sonarData_pb2.Georef()
                    Georef.ParseFromString(multipart_message[2])
                    process_georef_data(Georef)
            except zmq.Again:
                continue
    except KeyboardInterrupt:
        running = False
        print("Data receiver stopped.")
    except Exception as e:
        running = False
        print(f"An error occurred in the data receiver thread: {e}")
    finally:
        subscriber.close()
        context.term()

def visualize_telemetry():
    # Plotting Roll
    plt.figure(figsize=(10, 4))
    plt.plot(all_roll, marker='x', linestyle='-', label='Roll (degrees)')
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Roll (degrees)', fontsize=14)
    plt.title('Roll over 200 Measurements', fontsize=16)
    plt.legend()
    plt.grid(True)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()

    # Plotting Pitch
    plt.figure(figsize=(10, 4))
    plt.plot(all_pitch, marker='x', linestyle='-', label='Pitch (degrees)')
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Pitch (degrees)', fontsize=14)
    plt.title('Pitch over 200 Measurements', fontsize=16)
    plt.legend()
    plt.grid(True)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()

    # Plotting Yaw (Heading)
    plt.figure(figsize=(10, 4))
    plt.plot(all_yaw, marker='x', linestyle='-', label='Yaw (degrees)')
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Yaw (degrees)', fontsize=14)
    plt.title('Yaw over 200 Measurements', fontsize=16)
    plt.legend()
    plt.grid(True)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()

if __name__ == "__main__":
    receiver_thread = threading.Thread(target=data_receiver)
    receiver_thread.start()

    try:
        # We can include a condition to wait until we have 200 measurements to visualize
        while len(all_roll) < 200:
            pass  # Just waiting
    finally:
        running = False
        receiver_thread.join()
        visualize_telemetry()
        print("Program exiting...")
