#!/usr/bin/python3

# Custom Socket Server (Sender)
#
#  @author: wallarug
#  @date: 2017-10-27 02:45 AM
#

import socket
import struct

import time

from capture import Capture


class CommServerS:
    """
    A Custom Socket Server that sends UDP packets to the localhost
    which will be running python2.  This allows communication
    between python3 and python2.
    """
    def __init__(self):
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 5053
        self.socksend = socket.socket(socket.AF_INET, #Internet
                                    socket.SOCK_DGRAM) #UDP

        self.packer = struct.Struct('f f')

        print("[INFO] Server has started on 127.0.0.1:5053")

    def send(self, throttle, steering):
        # encode the values into an array
        val = (round(throttle,2), round(steering,2))

        # pack the values into the right format
        data = self.packer.pack(*val)
        
        # send the data over the UDP socket.
        self.socksend.sendto(data, (self.UDP_IP, self.UDP_PORT))


class Spammer:
    """
    A class for generating sample values to simulate a NN.
    """
    def __init__(self):
        self.a = 0
        self.comms = CommServerS()

        print("[INFO] Spam Bot is firing!")
                

    def generate(self):
        a=0
        while a < 100:
            a+=0.01
            time.sleep(0.05)
            if a >= 0.5:
                a=-0.5
            self.comms.send(0.0, a)

class AIDrive:
    """
    A class to interface with the Neural Net which captures data from
    the ZED STEREO VISION camera and then calls the SocketServer for
    sending that information to the VESC.
    """
    def __init__(self):
        self.model_name="models/30epoch_depthrgb.hdf5"
        self.throttle=0.0
        self.image_size=250

        self.throttle = 0.0
        self.steering = 0.0

        self.comms = CommServerS()

        self.capture = Capture(self.model_name)

        print("[INFO] AI Neural Net is firing!")

    def run(self):
        # get image from camera
        img = self.capture.capture_image(self.image_size)

        # get steering value from the NN
        self.steering = self.capture.evaluate_one(img)

        # send values over UDP socket.
        self.comms.send(self.throttle, self.steering)

    def generate(self):
        while(1):
            self.run()
            


if __name__ == '__main__':
    try:
        # uncomment for spammer
        #spam = Spammer()
        #spam.generate()

        # uncomment for AI
        ai = AIDrive()
        ai.generate()
    except KeyboardInterrupt:
        exit(0)
