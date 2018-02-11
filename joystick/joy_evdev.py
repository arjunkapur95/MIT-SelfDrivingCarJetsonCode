
from evdev import InputDevice, categorize, ecodes

#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/js0')


print('device info')
#prints out device info at start
print(gamepad)

print('capabilities')
print(gamepad.capabilities())