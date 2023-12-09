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

Example for sbd:

