#!/usr/bin/python3

import pyzed.camera as zcam
import pyzed.defines as sl
import pyzed.types as tp
import pyzed.core as core
import numpy as np
import cv2
import sys
import os

import pickle
from keras.models import load_model

print('Setting up camera.')


class Capture:
    def __init__(self, model_path):
        print('[INFO] Capture: Setting up camera.')
        # Create a PyZEDCamera object
        self.zed = zcam.PyZEDCamera()

        # Create a PyInitParameters object and set configuration parameters
        init_params = zcam.PyInitParameters()
        init_params.depth_mode = sl.PyDEPTH_MODE.PyDEPTH_MODE_PERFORMANCE  # Use PERFORMANCE depth mode
        init_params.coordinate_units = sl.PyUNIT.PyUNIT_MILLIMETER  # Use milliliter units (for depth measurements)

        # Open the camera
        err = self.zed.open(init_params)
        if err != tp.PyERROR_CODE.PySUCCESS:
            exit(1)

        # Create and set PyRuntimeParameters after opening the camera
        self.runtime_parameters = zcam.PyRuntimeParameters()
        self.runtime_parameters.sensing_mode = sl.PySENSING_MODE.PySENSING_MODE_STANDARD  # Use STANDARD sensing mode

        i = 0 #counter
        self.image = core.PyMat()
        print('[INFO] Capture: Camera setup complete.')
        print('[INFO] Capture: Setting up model...')

        # load model once
        self.model = load_model(model_path) #TODO hard code model
        print('[INFO] Capture: Model loaded successfully.')

    def capture_image(self, square_image_size):
        """
        Copied and modified from capture.py.
        Captures one image from the ZED camera and generates a
        pickle file.
        """
        # A new image is available if grab() returns PySUCCESS
        if self.zed.grab(self.runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            # Retrieve left image
            self.zed.retrieve_image(self.image, sl.PyVIEW.PyVIEW_LEFT)
            data = self.image.get_data()
            data=cv2.resize(data,(square_image_size,square_image_size))

            #grey = cv2.cvtColor( data, cv2.COLOR_RGB2GRAY )

            #convert to arrays
            return data
        else:
            print('image collection failed')

    
    def evaluate_one(self, pickle_RICK):
        """
        Copied and modified from classify.py
        Evaluates one image based on the given model and returns
        the steering value for moving the servo.
        """
        # import one file...        
        pickle_RICKSTER = pickle_RICK.reshape((1, pickle_RICK.shape[0], pickle_RICK.shape[1], 1))

        # classify the pickled model.
        class_index = np.argmax(self.model.predict(pickle_RICK))

        # calculate the steering value...
        steering_value = class_index/5.0

        return steering_value
