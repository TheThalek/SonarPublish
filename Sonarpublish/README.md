$ sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-good libsdl2-dev libglew-dev libeigen3-dev

sudo apt install gstreamer1.0-tools

$ sudo apt-get install git-lfs
$ git lfs pull


$ sudo apt-get install libprotobuf-c-dev



$ mkdir build
$ cd build
$ cmake ..
$ make


Run with for instance:
GST_PLUGIN_PATH=. gst-launch-1.0 filesrc location=./samples/2023-01-13_11-56-48_eelume_Airplane.SBD ! sonarparse ! sonarpublish