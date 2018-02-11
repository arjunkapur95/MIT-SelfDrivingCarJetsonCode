# installRACECAR
Install the MIT RACECAR ROS software and dependencies
To install the MIT RACECAR ROS packages on a NVIDIA Jetson Dev Kit:

$ ./installRACECAR.sh [dirname]

Where dirname is an optional parameter that indicates the top level Catkin Workspace directory in which to install the RACECAR packages. The default directory if the dirname is not specified is ~/racecar-ws

The script will fetch the RACECAR packages and place them into the workspace src directory and then install the required dependencies. Then the script will run catkin_make.
