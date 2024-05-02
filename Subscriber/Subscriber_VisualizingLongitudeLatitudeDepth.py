import zmq
import sonarData_pb2
import numpy as np
import threading
import matplotlib.pyplot as plt

# Lists to hold telemetry data
all_latitude = []
all_longitude = []
all_depth = []

running = True

def process_telemetry_data(telemetry):
    global all_latitude, all_longitude, all_depth
    all_latitude.append(telemetry.position.latitude)
    all_longitude.append(telemetry.position.longitude)
    all_depth.append(telemetry.depth.depth)

def process_georef_data(Georef):
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
                if len(multipart_message) > 1:
                    telemetry = sonarData_pb2.Telemetry()
                    telemetry.ParseFromString(multipart_message[1])
                    process_telemetry_data(telemetry)
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

def visualize_latitude():
    plt.figure(figsize=(10, 4))
    plt.plot(all_latitude, marker='x', linestyle='-', label='Latitude (degrees)')
    plt.xlabel('Scan Number', fontsize=14)
    plt.ylabel('Latitude (degrees)', fontsize=14)
    plt.title('Latitude over 200 Measurements - Cubic Spline Interpolated', fontsize=16)
    plt.legend()
    plt.grid(True)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.ticklabel_format(useOffset=False, style='plain', axis='y')  # Avoid scientific notation
    plt.show()

def visualize_longitude():
    plt.figure(figsize=(10, 4))
    plt.plot(all_longitude, marker='x', linestyle='-', label='Longitude (degrees)')
    plt.xlabel('Scan Number', fontsize=14)
    plt.ylabel('Longitude (degrees)', fontsize=14)
    plt.title('Longitude over 200 Measurements - Cubic Spline Interpolated', fontsize=16)
    plt.legend()
    plt.grid(True)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.ticklabel_format(useOffset=False, style='plain', axis='y')  # Avoid scientific notation
    plt.show()

def visualize_depth():
    plt.figure(figsize=(10, 4))
    plt.plot(all_depth, marker='x', linestyle='-', label='Depth (meters)')
    plt.xlabel('Scan Number', fontsize=14)
    plt.ylabel('Depth (meters)', fontsize=14)
    plt.title('Depth over 200 Measurements - Cubic Spline Interpolated', fontsize=16)
    plt.legend()
    plt.grid(True)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()

if __name__ == "__main__":
    receiver_thread = threading.Thread(target=data_receiver)
    receiver_thread.start()

    try:
        while len(all_latitude) < 200:
            pass
    finally:
        running = False
        receiver_thread.join()
        visualize_latitude()
        visualize_longitude()
        visualize_depth()
        print("Program exiting...")
