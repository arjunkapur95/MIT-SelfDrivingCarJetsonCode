# MIT Wireless Driver #

This contains the code for the wireless driver to interface with the motors.  

## Background ##

Since the motors are 'air-gapped' from the Jetson, a driver / adapter is required for sending information over WiFi or Bluetooth to a Raspberry Pi that will then control the motors.

## Install and Usage ##

To get this to work on the Raspberry Pi, follow these steps:


[How to set up Pi for SSP](https://github.com/engn1931z/lab4)

[How to setup rfcomm port](http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/bluetooth/serial-over-bluetooth)

[How to list serial ports](https://www.raspberrypi.org/forums/viewtopic.php?f=50&t=31141)

```
Pi BT Serial Port: /dev/ttyAMA0
```

```
pip3 install pyserial
```