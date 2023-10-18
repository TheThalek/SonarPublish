import sonarData_pb2
import sys
import socket
import os 
import time 

# IMPORTANT; USE ctrl + c to end the code in the terminal, if not you have to change the socket name socket_path = "/tmp/sonarsocket"
    # in both the c code and in this python code


# THe corrct file

# Function to process incoming data
def process_sonar_data(data):
    # Access the data fields (which are repeated fields)
    pointX_list = data.pointX
    pointY_list = data.pointY
    beamIdx_list = data.beamIdx
    quality_list = data.quality

    # Print the received data
    for i in range(len(pointX_list)):
        pointX = pointX_list[i]
        pointY = pointY_list[i]
        beamIdx = beamIdx_list[i]
        quality = quality_list[i]

        print(f"Received sonar data: pointX={pointX}, pointY={pointY}, beamIdx={beamIdx}, quality={quality}")


def cleanup_socket(socket_path):
    if os.path.exists(socket_path):
        os.remove(socket_path)

if __name__ == "__main__":
    socket_path = "/tmp/socket"
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    max_retries = 5
    retry_interval = 2

    retries = 0

    try:
        while retries < max_retries:
            try:
                server_socket.bind(socket_path)
                break
            except OSError as e:
                if e.errno == 98:
                    print("Address is already in use. Retrying in {} seconds...".format(retry_interval))
                    time.sleep(retry_interval)
                    retries += 1
                else:
                    print(f"Error binding to the socket: {e}")
                    server_socket.close()
                    sys.exit(1)
        else:
            print("Max retries reached. Exiting.")
            server_socket.close()
            sys.exit(1)

        server_socket.listen(1)

        print("Listening for incoming data...")

        try: # Try receiving data
            while True:
                connection, client_address = server_socket.accept()
                data = connection.recv(4096)

                if data: # If data received, translate and process it
                    sonar_data = sonarData_pb2.sonarData()
                    sonar_data.ParseFromString(data)

                    process_sonar_data(sonar_data)
        except KeyboardInterrupt:
            print("Socket server terminated.")
        finally:
            server_socket.close()
            cleanup_socket(socket_path)
    except Exception as e:
        print(f"An error occurred: {e}")