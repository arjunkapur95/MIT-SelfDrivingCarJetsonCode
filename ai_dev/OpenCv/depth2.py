#Simple example of stereo image matching.

import numpy as np
from matplotlib import pyplot as plt
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

plt.imshow((disp-min_disp)/num_disp, 'gist_gray')
plt.savefig('depth.png', bbox_inches='tight')
plt.show()