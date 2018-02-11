# README #

This repository includes all the software and documentation required for the University of Sydney branch of the MIT Car Race Challenge.  Completed under the CAPSTONE project for students doing INFO3600 (1) or COMP3615 (2).

# Wiki #

[Wiki Home](https://bitbucket.org/usydmitplatform2017/mit-racecar-usyd/wiki/Home)

# Slack #

[usyd-mitracecarcomp.slack.com](https://usyd-mitracecarcomp.slack.com)

# Layout #
## docs ##

* datasheets: contains all the information about the parts that are used on the RACECAR.

* manuals: contains instruction manuals for the Jetson, VESC and other devices.


## mit-racecar ##

All the pre-written code written by the MIT 6.141 class.  This is here as a copy for everyone to play with and hack at.  This repository only contains the sub-repositories that were useful to this project.

* hardware: all the 3D printing templates for the MIT RACECAR and the configuration files (.xml) for the VESC.

* racecar: respository that has control scripts for the MIT RACECAR.

* racecar-simulator: as stated.

* vesc: contains drivers and software to make the VESC work with the MIT RACECAR.


## wdriver ##

Special wireless / bluetooth driver for communicating between an RPi and Jetson boards.  This creates an air gap between the two devices for safety.


# Hardware List #

**Computer**

Jetson TX2 Developer Kit

Raspberry Pi Model B 3


**Sensors**

LIDAR (Scanse Sweep) from SparkFun

Stereo Vision Camera (Stereo Labs Zed)

Vision Camera (FLIR Blackfly 2.3MP)


**Motors**

FOCBOX VESC-X Motor Controller

Velineon 3500 Brushless Motor


# BLDC Tool #

This is a tool for uploading firmware and configurations to the VESC.  It is avaiable for both Windows, OSX and Linux.

## Linux ##

```
git clone https://github.com/jetsonhacks/installBLDC.git
```

## Windows ##

Download the executable from: 

http://www.enertionboards.com/new-focbox-speed-controller/focbox-bldc-tool-win/

Also avaiable temporarily here (on Google Drive):

https://drive.google.com/file/d/0B0OrXzyTLfIiQTRNbFh4X3FLMDA/view?usp=sharing



# Wiki Resources #

[Team Member List (all teams)](https://bitbucket.org/usydmitplatform2017/mit-racecar-usyd/wiki/Teams%20and%20Members)

[MIT Car Build Guide](https://bitbucket.org/usydmitplatform2017/mit-racecar-usyd/wiki/MIT%20Build%20Instructions)

[Resource Links](https://bitbucket.org/usydmitplatform2017/mit-racecar-usyd/wiki/Resources)

[Location of Parts](https://bitbucket.org/usydmitplatform2017/mit-racecar-usyd/wiki/Parts%20Location%20Matrix)




# Assistance #
If you require assistance with this repository, please contact Cian Byrne (@wallarug) via email:  cbyr2401@uni.sydney.edu.au

Racecar backwards is Racecar
