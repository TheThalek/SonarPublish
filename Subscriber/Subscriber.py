import zmq
import sonarData_pb2
import time 


# Function to process incoming data
def process_georef_NED_data(data):
    PointCloud_body_x = data.x_pointCld_body_NED  # X coordinates of points, referenced wrt. body frame of robot. Have been rotated wrt. NED frame, no translation vector added yet
    PointCloud_body_y = data.y_pointCld_body_NED
    PointCloud_body_z = data.z_pointCld_body_NED

    Georef_rotationMatrix = data.rotationMatrix_NED # Rotation Matrix from body frame to NED frame

    print(f"Received Georeferenced Data wrt. NED Frame")

    # Printing lists of point cloud data
    # for i in range(len(PointCloud_body_x)):
    #     x = PointCloud_body_x[i]
    #     y = PointCloud_body_y[i]
    #     z = PointCloud_body_z[i]
    #     print(f"Georeferenced Point Cloud: X={x}, Y={y}, Z={z}")

    # Printing Rotation Matrix
    # for i in range(3):
    #     for j in range(3):
    #         # Printing each element in the rotation matrix on a new line for clarity
    #         print(f"{Georef_rotationMatrix[i * 3 + j]:.15f}")




def process_georef_ECEF_data(data):
    PointCloud_body_x = data.x_pointCld_body_ECEF # X coordinates of points, referenced wrt. body frame of robot. Have been rotated wrt. ECEF frame, no translation vector added yet
    PointCloud_body_y = data.y_pointCld_body_ECEF
    PointCloud_body_z = data.z_pointCld_body_ECEF

    Georef_rotationMatrix = data.rotationMatrix_ECEF # Rotation Matrix from body frame to ECEF frame

    body_position_ECEF_x = data.x_body_position_ECEF # X Position of body in ECEF frame
    body_position_ECEF_y = data.y_body_position_ECEF
    body_position_ECEF_z = data.z_body_position_ECEF

    print(f"Received Georeferenced Data wrt. ECEF Frame")

    # Printing lists of point cloud data
    # for i in range(len(PointCloud_body_x)):
    #     x = PointCloud_body_x[i]
    #     y = PointCloud_body_y[i]
    #     z = PointCloud_body_z[i]
    #     print(f"Georeferenced Point Cloud: X={x}, Y={y}, Z={z}")

    
    # Printing Rotation Matrix
    # for i in range(3):
    #     for j in range(3):
    #         # Printing each element in the rotation matrix on a new line for clarity
    #         print(f"{Georef_rotationMatrix[i * 3 + j]:.15f}")

    # Printing Body Position in ECEF Frame
    # print(f"Body Position in ECEF Frame: X={body_position_ECEF_x}, Y={body_position_ECEF_y}, Z={body_position_ECEF_z}")



# Function to process incoming data
def process_ungeoref_data(data):
    Ungeoref_pointX = data.pointX
    Ungeoref_pointY = data.pointY
    Ungeoref_beamIdx = data.beamIdx
    Ungeoref_quality = data.quality
    Ungeoref_intensity = data.intensity

    # Print the received sonar data
    for i in range(len(Ungeoref_pointX)):
        pointX = Ungeoref_pointX[i]
        pointY = Ungeoref_pointY[i]
        beamIdx = Ungeoref_beamIdx[i]
        quality = Ungeoref_quality[i]
        intensity = Ungeoref_intensity[i]

        print(f"Received Ungeoreferenced Point Cloud: PointX={pointX}, PointY={pointY}, BeamIdx={beamIdx}, Quality={quality}, Intensity={intensity}")


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


if __name__ == "__main__":
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
    subscriber.setsockopt(zmq.RCVTIMEO, 1000)  # Set timeout in milliseconds

    try:
        while True:
            try: 
                # multipart_message = subscriber.recv()
                multipart_message = subscriber.recv_multipart()  # Receiving serialized data
                    
                # Deserializing the Ungeoreferenced Point Cloud 
                Ungeoref = sonarData_pb2.Ungeoref()
                Ungeoref.ParseFromString(multipart_message[0])
                process_ungeoref_data(Ungeoref)



                # Deserializing the Telemetry Data
                Telemetry = sonarData_pb2.Telemetry()
                Telemetry.ParseFromString(multipart_message[1])

                if Telemetry.HasField("position"):
                    process_telemetry_position(Telemetry.position)
                
                if Telemetry.HasField("pose"):
                    process_telemetry_pose(Telemetry.pose)

                if Telemetry.HasField("heading"):
                    process_telemetry_heading(Telemetry.heading)
                
                if Telemetry.HasField("depth"):
                    process_telemetry_depth(Telemetry.depth)
                
                if Telemetry.HasField("altitude"):
                    process_telemetry_altitude(Telemetry.altitude)
                

                # Deserializing the Georef_NED Point Cloud
                Georef_NED = sonarData_pb2.Georef_NED()
                Georef_NED.ParseFromString(multipart_message[2])
                process_georef_NED_data(Georef_NED)



                # Deserializing the Georef_ECEF Point Cloud
                Georef_ECEF = sonarData_pb2.Georef_ECEF()
                Georef_ECEF.ParseFromString(multipart_message[3])
                process_georef_ECEF_data(Georef_ECEF)


            except zmq.Again:
                # This block catches the timeout exception
                continue  # This allows the loop to continue running

    except KeyboardInterrupt:
        print("Subscriber stopped")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally: 
        subscriber.close()
        context.term()