#Optical Flow for CNN and Car Autonomous Driving

### this needs optimisation & testing on the CNN.

import numpy as np
import cv2

## takes in video input from current laptop camera (livefeed)
cap = cv2.VideoCapture(0)

## detection of corners
feature_params = dict( maxCorners = 150, # Display #num of frames (Dot Points)
                      qualityLevel = 0.3,
                      minDistance = 5,
                      blockSize = 50 ) # Small window is more sensitive to noise and may miss larger motions

## using lk of
# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (150,150),  #15 x 15 set pixel dimensions
                 maxLevel = 22,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 25, 0.3))

# Take first frame (initial conditions) and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

## we may want to compare each old frame to the previous
while(1):
    
    #Create a new mask image for drawing purposes (this makes each frame have unique lines. getting rid of this will saturate the image with lines)
    mask = np.zeros_like(old_frame)
    
    #Takes in input
    ret,frame = cap.read()
    
    #Converts input to greyscale for opticalflow comparison
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #Calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    
    #Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]
    
    #Draw the tracks to image
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        mask = cv2.line(mask, (a,b),(c,d), (103, 209, 51), 6) ## visual line (track) which is connected to the dot point
        frame = cv2.circle(frame,(a,b),5, (255, 255, 255), 2) ## visual circle dot point
        img = cv2.add(frame, mask) ## adds the dot and line together into an image.
    
    #Merge the mask (image + track line) with frame (corner detection dot)
    cv2.imshow('frame',img)

    #If you hold down 'esc' program will exit infinite loop
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


#Save each image captured
#TODO: this is currently way too slow!
#    from matplotlib import pyplot as plt
#    fig, ax = plt.subplots()
#    ax.imshow(img)
#    plt.savefig(str(i) + '.png', bbox_inches='tight')
#    plt.close()
#    i = i + 1

##  OG update the previous frame and previous points
    old_gray = frame_gray.copy()

##  NEW refresh each frame
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

    #issue when all points leave the frame, program crashes.
    #thus there always needs to be a frame on the screen.




cv2.destroyAllWindows()
cap.release()
