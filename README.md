# GstSonarPublish

## Overview
GstSonarPublish is the result from a specialization project aimed at enabling real-time access to point clouds generated using multi-beam echo sounders. It is an extension of the GstSonar and Gstreamer plugins developed by Eelume AS. The project introduces a new sink element, SonarPublish, which extracts sonar data from SBD files or directly from the Eely robot via a TCP connection. This data is then published to other programs on your PC. Additionally, a Python server is included to demonstrate how to read data from the GstSonarPublish code. This server serves as a foundation for further development, such as adding visualization capabilities for the sonar data.

## System Requirements
- Windows PC with WSL2 (Windows Subsystem for Linux 2).
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
1. **Generate The Proto Library** Similar to the Python server, generate a new `.proto` library.
2. **Install Dependencies**:
   ```bash
   sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-good libsdl2-dev libglew-dev libeigen3-dev
3. **Build Program **
mkdir build
cd build
cmake ..
make
5. **Other dependencies** Try running the code, see if any other libraries are lacking

Usage
Start the Python Server: Run the server using the command python3 ./Server.py. Ensure it's correctly listening for incoming data.
Run GstSonarPublish: Depending on your data source (SBD or TCP), use the respective command:
For TCP: GST_PLUGIN_PATH=. gst-launch-1.0 tcpclientsrc host=<IP_ADDRESS> port=<PORT> ! sonarparse ! sonarmux name=mux ! sonarpublish tcpclientsrc host=<IP_ADDRESS> port=<PORT> ! nmeaparse ! eelnmeadec ! mux.
For SBD: export SBD=<PATH_TO_SBD_FILE> GST_PLUGIN_PATH=. GST_DEBUG=2,sonarsink:9 gst-launch-1.0 filesrc location=$SBD ! sonarparse ! sonarmux name=mux ! sonarpublish zoom=0.1 filesrc location=$SBD ! nmeaparse ! eelnmeadec ! mux.



# GstSonarPublish
The result of the Specialization Project "Enabling Real-time Access to Point Clouds Generated using Multi-beam Echo Sounder"

Based on code from Eelume AS GstSonar and Gstreamer plugins at https://github.com/EelumeAS/gstsonar/tree/main. I have added a new sink element, SonarPublish, which extracts sonar data from SBD files or directly from the Eely robot from a TCP connection, to then publish this data to other programs on your pc. In addition a python server, that can read from the GstSonarPublish code, mostly as a "proof of concept" file or as a mal for new programs, maybe someone can add visualization code in this python script later so that the sonar data can be visualized after being published as well. 

I have a windows pc with WSL2 that I run on. Not possible on windows, because of the Unix Servers used for transferring the data between the two programs

Program consits of two folders
Consists of two folders, one for the GstSonarPublish, and Python Server. 
To run GstSonarPublish, have to run the python server first, running it by using the command: python3 ./Server.py
After correctly listening, "Listening for incoming data..."
Remember to cancel the program using ctrl c, not e.g. ctrlz, as this will leave the socket being used for communication as still used, and then you will have to change the server names manually in both the server and gstsonarpublish programs. 


To run the GstSonarpublish, two different command depending on if you want to use sbd or tcp. 
Example for tcp: 
GST_PLUGIN_PATH=. gst-launch-1.0 tcpclientsrc host=192.168.6.121 port=2210 ! sonarparse ! sonarmux name=mux ! sonarpublish tcpclientsrc host=192.168.6.100 port=11000 ! nmeaparse ! eelnmeadec ! mux.

Example for sbd:
export SBD=./samples/2022-11-22_09-41-38_eelume_ntnu_Nyhavna.SBD
GST_PLUGIN_PATH=. GST_DEBUG=2,sonarsink:9 gst-launch-1.0 filesrc location=$SBD ! sonarparse ! sonarmux name=mux ! sonarpublish zoom=0.1 filesrc location=$SBD ! nmeaparse ! eelnmeadec ! mux.




To set up both programs, set up python server first, as you can test this without c code running at the same time: 

**Python server:**
Download proto library 
Start by generating a new .proto library (The library responsible for serializing the data before transfer, and deserialize it after it has been received by the python script)
Then, download necessary libraries for getting Unix to run. 

**GstSonarpublish server:**
Download proto library 
Start by generating a new .proto library (The library responsible for serializing the data before transfer, and deserialize it after it has been received by the python script)
$ sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-good libsdl2-dev libglew-dev libeigen3-dev

To build it
$ mkdir build
$ cd build
$ cmake ..
$ make



**Notes: **
Make sure the .proto file is the same for both  the pytho nserver and the gstsonarpublish code. These also have to be regenerated each time they are changed, to update the protobuf source code
Also make sure the names of the sockets are the same for both the server and gstsonarpublish code. Socket name in server can be found in file Server.py, and in Sonarpublish.C in gstsonarpublish
