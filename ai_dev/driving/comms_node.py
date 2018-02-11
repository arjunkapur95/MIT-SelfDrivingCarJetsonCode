#!/usr/bin/python

# Custom Socket Server (Receiver)
#
#  @author: wallarug
#  @date: 2017-10-27 02:35 AM
#

import socket
import struct

import importlib

import rospy
from ackermann_msgs.msg import AckermannDriveStamped
from std_msgs.msg import Int8

class CommServerRecv:
    """
    A Custom Socket Server that receives UDP packets from
    the localhost running python3.
    This allows communication between python3 and python2.
    """
    def __init__(self):
        # set up the UDP stuff.
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 5053
        self.sockrecv = socket.socket(socket.AF_INET, #Internet
                                    socket.SOCK_DGRAM) #UDP
        self.sockrecv.bind((self.UDP_IP, self.UDP_PORT))

        # data drop space
        self.rdata = {}

        # build a struct object
        self.unpacker = struct.Struct('f f')
        
        # now let's subscribe to the ackermann topic
        rospy.Subscriber("ai", Int8, self.callback)

        # now let's tell everyone we are also going to be publishing
        self.pubVESC = rospy.Publisher("/vesc/low_level/ackermann_cmd_mux/input/teleop", AckermannDriveStamped, queue_size = 1)

        #rospy.init_node("CommServerRecv")

    def recv(self):
        # wait for packet to be received
        data, addr = self.sockrecv.recvfrom(self.unpacker.size)

        # unpack the data.
        udata = self.unpacker.unpack(data)

        self.rdata['speed'] = udata[0]
        self.rdata['steering'] = udata[1]

    def callback(self, data):
        # we are go...
        # recieve the packet
        self.recv()
        
        # process data from AI / spammer
        speed = self.rdata['speed']
        steer = self.rdata['steering']
          
        # send to vesc
        msg = AckermannDriveStamped()
        msg.drive.speed = speed
        msg.drive.steering_angle = steer
        msg.header.stamp = rospy.Time.now()
        self.pubVESC.publish(msg)


if __name__ == "__main__":
    try:
        rospy.init_node("comms_node")
        node = CommServerRecv()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
