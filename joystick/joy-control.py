#!/bin/usr/python
"""
    This script is built to read input from a joystick and at the same
    time, save a number of files while images are being captured.

    Author: @wallarug
    Date: 12/10/2017

"""

import pygame
from time import sleep
import sys

# start pygame
pygame.init()

# count how many joysticks there are...
joycount = pygame.joystick.get_count()

# check that a joystick is actually connected.
if joycount < 1:
    print("No Joystick detected!")
    sys.exit(0)

# there is atleast one joystick, let's get it.
j = pygame.joystick.Joystick(0)
j.init()

# joystick static storage setup
axes = [0] * j.get_numaxes()
buts = [0] * j.get_numbuttons()

# display which joystick is being used
print("You are using the {0} controller.".format(j.get_name))

try:
    while True:
        pygame.event.pump() # keep everything current

        output = ""

        # get axis values and store them in static storage
        #  for this exact moment in time.
        for i in range(j.get_numaxes()):
            axes[i] = j.get_axis(i)
            output += "axis {0} {1}\n".format(i, axes[i])

        # get button values and store them in static storage
        #  for this exact moment in time.
        for i in range(j.get_numbuttons()):
            buts[i] = j.get_button(i)
            output += "button {0} {1}\n".format(i, buts[i])

        #   IMPROVEMENT:  Only query the axes that you want (will reduce
        #                 processing time).  
        #   IMPROVEMENT:  Do it in-line.  No real need for a "for loop" here
        #                 this can be done by just getting the relevant
        #                 axes.
        #   IMPROVEMENT:  remove buttons, you don't need them afaik

        # display the axis
        print(output)

        # set a polling period (~10 polls / second = 0.1)
        sleep(0.1)


except KeyboardInterrupt:
    j.quit()
    sys.exit("Thank you, come again!")
