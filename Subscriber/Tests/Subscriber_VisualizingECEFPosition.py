import zmq
import sonarData_pb2
import numpy as np
import threading
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

# Lists to hold ECEF data
all_x_ecef = []
all_y_ecef = []
all_z_ecef = []

running = True

def process_georef_ECEF_data(data):
    global all_x_ecef, all_y_ecef, all_z_ecef
    all_x_ecef.append(data.x_body_position_ECEF)
    all_y_ecef.append(data.y_body_position_ECEF)
    all_z_ecef.append(data.z_body_position_ECEF)

def data_receiver():
    global running
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
    subscriber.setsockopt(zmq.RCVTIMEO, 1000)  # Set timeout in milliseconds
    try:
        while running:
            try:
                multipart_message = subscriber.recv_multipart()
                if len(multipart_message) > 3:
                    georef_ecef = sonarData_pb2.Georef_ECEF()
                    georef_ecef.ParseFromString(multipart_message[3])
                    process_georef_ECEF_data(georef_ecef)
            except zmq.Again:
                continue
    except KeyboardInterrupt:
        running = False
        print("Data receiver stopped by KeyboardInterrupt.")
    except Exception as e:
        running = False
        print(f"An error occurred in the data receiver thread: {e}")
    finally:
        subscriber.close()
        context.term()

def visualize_ecef():
    if len(all_x_ecef) == 0:
        print("No data to plot.")
        return

    # Calculate differences from the first measurement
    x_diff = np.array(all_x_ecef) - all_x_ecef[0]
    y_diff = np.array(all_y_ecef) - all_y_ecef[0]
    z_diff = np.array(all_z_ecef) - all_z_ecef[0]

    # Ensure the first point is (0, 0, 0)
    x_diff[0] = 0
    y_diff[0] = 0
    z_diff[0] = 0

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_diff, y_diff, z_diff, marker='o', linestyle='-', label='Relative ECEF Coordinates')
    ax.set_xlabel('Relative X ECEF (meters)', fontsize=14)
    ax.set_ylabel('Relative Y ECEF (meters)', fontsize=14)
    ax.set_zlabel('Relative Z ECEF (meters)', fontsize=14)
    ax.set_title('3D Plot of Relative ECEF Coordinates over 200 Measurements', fontsize=16)
    ax.legend()
    
    # Increase the size of the tick labels
    ax.tick_params(axis='both', which='major', labelsize=12)

    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    receiver_thread = threading.Thread(target=data_receiver)
    receiver_thread.start()

    try:
        while len(all_x_ecef) < 200:
            time.sleep(0.1)  # Avoid busy-waiting
    finally:
        running = False
        receiver_thread.join()
        if all_x_ecef:
            visualize_ecef()
        print("Program exiting...")
