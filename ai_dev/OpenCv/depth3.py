#!/usr/bin/env python

'''
Simple example of stereo image matching and point cloud generation.

Resulting .ply file cam be easily viewed using MeshLab ( http://meshlab.sourceforge.net/ )
'''

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2

print('loading images...')
imgL = cv2.pyrDown( cv2.imread('aloeL.jpg') )  # downscale images for faster processing
imgR = cv2.pyrDown( cv2.imread('aloeR.jpg') )

# disparity range is tuned for 'aloe' image pair
window_size = 3
min_disp = 16
num_disp = 112-min_disp
stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
    numDisparities = num_disp,
    blockSize = 16,
    P1 = 8*3*window_size**2,
    P2 = 32*3*window_size**2,
    disp12MaxDiff = 1,
    uniquenessRatio = 10,
    speckleWindowSize = 100,
    speckleRange = 32
)

print('computing disparity...')
disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

print('generating 3d point cloud...',)
h, w = imgL.shape[:2]
f = 0.8*w                          # guess for focal length
Q = np.float32([[1, 0, 0, -0.5*w],
                [0,-1, 0,  0.5*h], # turn points 180 deg around x-axis,
                [0, 0, 0,     -f], # so that y-axis looks up
                [0, 0, 1,      0]])
points = cv2.reprojectImageTo3D(disp, Q)

x_points=[]
y_points=[]
z_points=[]

num_points=5000
point_freq=int(len(points)*len(points[0])/num_points)
counter=0
for i in points:
    for j in i:
        counter+=1
        if counter%point_freq==0:
            x_points.append(list(j)[0])
            y_points.append(list(j)[1])
            z_points.append(list(j)[2])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x_points,y_points,z_points, c=z_points)
plt.savefig('3dDepth.png')
plt.show()
