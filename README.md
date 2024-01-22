# GstSonarPublish

## Overview
GstSonarPublish is the result from a specialization project aimed at enabling real-time access to point clouds generated using multi-beam echo sounders. It is an extension of the GstSonar and Gstreamer plugins developed by Eelume AS. The project introduces a new sink element, SonarPublish, which extracts sonar data from SBD files or directly from the Eely robot via a TCP connection. This data is then published to other programs on your PC. Additionally, a Python server is included to demonstrate how to read data from the GstSonarPublish code. This server serves as a foundation for further development, such as adding visualization capabilities for the sonar data.

## System Requirements
- Windows PC with WSL2 
- Note: The project is not compatible with native Windows environments due to its reliance on Unix Servers for data transfer.
- Important: There have been instances where WSL2 encountered issues connecting to the Windows network, which may affect connectivity with the Eely robot. Users should be aware of potential network connectivity challenges when using WSL2 and plan their setup accordingly. Using a Linux PC could be a solution to this problem

## Structure
The project consists of two main components, in addition to a folder with SBD test files:
1. **GstSonarPublish**: Handles the extraction and publication of sonar data.
2. **Python Server**: A server script for receiving and processing the published sonar data.

## Setup and Installation
### Python Server
1. **Download Proto Library**: sudo apt-get install protobuf-compiler
2. **Generate The Proto Library** Start by generating a new `.proto` library for data serialization and deserialization.
3. **Other dependencies** Try running the code, see if any other libraries are lacking

### GstSonarPublish
1. **Generate The Proto Library**: Similar to the Python server, generate a new `.proto` library.
2. **Install Dependencies**:
```
$ sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-good libsdl2-dev libglew-dev libeigen3-dev
```

```
$ sudo apt-get install libprotobuf-c-dev
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
1. **Start the Python Server:** Run the server using the command
```
python3 ./Server.py.
```
   Ensure it's correctly listening for incoming data.
   
2. **Run GstSonarPublish:** Depending on your data source (SBD or TCP), use the respective command:
   
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
1. Ensure the .proto files are identical in both the Python server and GstSonarPublish code. They must be regenerated each time they are modified.
2. Sockets used for communication between the server and GstSonarPublish should have matching names. Check Server.py for the socket name in the server and Sonarpublish.C in GstSonarPublish.
3. Remember to terminate the program using Ctrl + C to prevent socket communication issues.


