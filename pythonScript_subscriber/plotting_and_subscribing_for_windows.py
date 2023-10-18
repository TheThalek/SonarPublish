import threading
import socket
import sonarData_pb2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a figure and a 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize global z value
z = 0

# Function to process incoming data
def process_sonar_data(data):
    global z

    # Access the data fields (which are repeated fields)
    pointX_list = data.pointX
    pointY_list = data.pointY
    beamIdx_list = data.beamIdx

    # Increment Z value for each data point. Could be changed to fit the scale of the x and y points
    z += 1

    # Print and plot the received data
    for i in range(len(pointX_list)):
        pointX = pointX_list[i]
        pointY = pointY_list[i]
        beamIdx = beamIdx_list[i]

        # Plot the data point with the updated Z value
        ax.scatter(pointX, pointY, z, c='b', marker='o')

        # Set plot limits based on data range
        ax.set_xlim(min(pointX_list), max(pointX_list))
        ax.set_ylim(min(pointY_list), max(pointY_list))
        ax.set_zlim(0, z)

        plt.draw()  # Update the plot

        print(f"Received sonar data: pointX={pointX}, pointY={pointY}, beamIdx={beamIdx}")

# Function to run the server
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 8888))
    server_socket.listen(1)
    print("Server is listening for incoming connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        while True:
            data = client_socket.recv(4096)
            if not data:
                break

            sonar_data = sonarData_pb2.sonarData()
            sonar_data.ParseFromString(data)

            process_sonar_data(sonar_data)

        client_socket.close()

# Start the server in a separate thread
server_thread = threading.Thread(target=run_server)
server_thread.start()

# Continue with the client logic (your existing code)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
max_retries = 5
retry_interval = 2
retries = 0

try:
    client_socket.connect(("127.0.0.1", 8888))

    print("Listening for incoming data...")

    while True:
        data = client_socket.recv(4096)

        if data:
            sonar_data = sonarData_pb2.sonarData()
            sonar_data.ParseFromString(data)

            process_sonar_data(sonar_data)
except KeyboardInterrupt:
    print("Socket client terminated.")
except Exception as e:
    print(f"An error occurred: {e}")

plt.show()  # Add this line to display the plot
