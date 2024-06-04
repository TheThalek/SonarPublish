# SonarPublish

## Overview
SonarPublish is the result from a master thesis aimed at enabling real-time access to point clouds generated using multi-beam echo sounders. It is an extension of the GstSonar and Gstreamer plugins developed by Eelume AS. The project introduces a new sink element, SonarPublish, which extracts sonar data from SBD files or directly from the Eely robot via a TCP connection. This data is then georeferenced, by transforming the sonar's point cloud from being referenced wrt. the sonar, to the NED and ECEF frames. And then the data is published to other programs locally on your PC or other PCs on your nerwork. Additionally, Python servers is included to demonstrate how to read data from the SonarPublish code. This server serves as a foundation for further development, such as adding visualization capabilities for the sonar data.

## System Requirements
You need two PCs (Or one if publishing locally), one Publisher PC (PubPC) and one Subscriber PC (SubPC). 

PubPC: 
- Windows PC with WSL2 
- Note: The project is not compatible with native Windows environments due to its reliance on Unix Servers for data transfer.

SubPC:
- When publishing to other PCs, you also need one of these, to run the subscriber code on.
- Can be any OS supported by ZeroMQ and Protobuf (libraries used for pub/sub in system)

## Structure
The project consists of two folders, in addition to a folder with SBD test files:
1. **SonarPublish**: The code extracting data from robot, georeferencing it and publishing the data to subscriber. 
2. **Subscriber**: Subscriber files for receiving data. Subscriber_ECEF_VisualizingGeorefData.py for visualizing the ECEF referenced point cloud, Subscriber_NED_VisualizingGeorefData_FakingTheShify.py for visualizing the NED referenced point cloud. There is also a test-folder containing subscribers visualizing the telemetry data from Eely. 

## Setup and Installation
### Python Server
1. **Download Proto Library**: sudo apt-get install protobuf-compiler
2. **Generate The Proto Library** Start by generating a new `.proto` library for data serialization and deserialization.
3. **Other dependencies** Try running the code, see if any other libraries are lacking

### SonarPublish
1. **Generate The Proto Library**: Similar to the Python server, generate a new `.proto` library.
2. **Install Dependencies**:
```
$ sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-good libsdl2-dev libglew-dev libeigen3-dev
```

```
$ sudo apt-get install libprotobuf-c-dev
$ sudo apt-get install protobuf-c-compiler
```
3. **Build Program**:
```
$ mkdir build
$ cd build
$ cmake ..
$ make
```
4. **Other dependencies**: Try running the code, see if any other libraries are lacking


## Usage
1. **Start the Python Server:** Run the server using the command. Can be started after publisher, but if using SBD files, then some data will be lost. 
   
2. **Run SonarPublish:** Depending on your data source (SBD or TCP), use the respective command:
   
*For TCP:*
```
GST_PLUGIN_PATH=. gst-launch-1.0 tcpclientsrc host=192.168.6.121 port=2210 ! sonarparse ! sonarmux name=mux ! sonarpublish tcpclientsrc host=192.168.6.100 port=11000 ! nmeaparse ! eelnmeadec ! mux.
```
*For SBD:*
```
export SBD=<PATH_TO_SBD_FILE>
GST_PLUGIN_PATH=. GST_DEBUG=2,sonarsink:9 gst-launch-1.0 filesrc location=$SBD ! sonarparse ! sonarmux name=mux ! sonarpublish zoom=0.1 filesrc location=$SBD ! nmeaparse ! eelnmeadec ! mux.
```

## Important Notes
1. Ensure the .proto files are identical in both the Python server and SonarPublish code. They must be regenerated each time they are modified.
2. Ensure IP addresses and port number subscriber connects to are correct. 



