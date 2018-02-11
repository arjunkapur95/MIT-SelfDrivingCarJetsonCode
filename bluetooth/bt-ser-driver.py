#!/usr/bin/python3

import serial

# set up bluetooth port /dev/rfcomm0 or /dev/ttyAMA0
usb = serial.Serial('/dev/ttyAMA0', 9600, timeout=0.5)
bt = serial.Serial('/dev/rfcomm0', 9600, timeout=0.5)

while True:
    # read command from Jetson
    data = bt.read()

    # write command to VESC
    usb.write(data)

    # wait for response from VESC
    data = usb.read()

    # send data back to Jetson
    bt.write(data)

    #repeat

usb.close()
bt.close()
    
