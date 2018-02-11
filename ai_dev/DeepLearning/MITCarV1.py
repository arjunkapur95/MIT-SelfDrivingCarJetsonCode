

'''
This script includes several functions that should be enough for:
1. Transform images into appropriate format
2. Read in images
3. Build the model, currently is VGG19
4. Train the model
5. Produce output

Run in Python3, Keras 2.08

Author: Chester Wang - 450647297
'''


from PIL import Image
import os
import scipy.misc
import numpy as np
import random
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.utils import np_utils
from keras.models import Sequential, Model
from keras.layers import Input, Flatten, Dense, Dropout, Conv2D, MaxPooling2D



# Returns a numpy array in shape (x,y,4)
# Two images (PIL.Image objects) have to in same resolution!
# It'd be better in square shape
def merge_image(original_image_path, depth_image_path, width, height):

    d_img = load_img(depth_image_path, grayscale=True)
    d_array = img_to_array(d_img).reshape(height, width)
    print(d_array.shape)

    o_img = load_img(original_image_path, grayscale=False)
    o_array = img_to_array(o_img)
    print(o_array.shape)


    combined_array = np.zeros((height, width, 4), dtype="float32")
    combined_array[:, :, 0:3] = o_array # The first three layers will be the original one
    combined_array[:, :, 3] = d_array

    return combined_array


# Since no images captured yet, this function is to be implemented
# TODO: Need to know: the name of images, the format of labels, the structure of directories
# Returns data, label
def load_data_from_directory():
    return None, None


# input_shape is a tuple, such as (800, 1200) height, width
def build_model(input_shape, nb_class):

    img_input = Input(shape=input_shape)

    model = Sequential()

    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1')(img_input)
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)


    x = Flatten(name='flatten')(x)
    x = Dense(4096, activation='relu', name='fc1')(x)
    x = Dense(4096, activation='relu', name='fc2')(x)
    x = Dense(nb_class, activation='softmax', name='predictions')(x)

    model = Model(img_input, x, name='vgg16')

    model.summary()

    return model


# Train the model, notice that this function has to be called before evaluate
def train(data, label, input_shape, nb_class):

    model = build_model(input_shape=input_shape, nb_class=nb_class)

    model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])

    if(data is not None and label is not None):
        model.fit(data, label, batch_size=64, epochs=1, validation_split=0.2, verbose=1, shuffle=True)

    print("\n\nTraining done!")


# train first then evaluate
def evaluate(test_data, test_label, model):
    if (test_data is not None and test_label is not None):
        scores = model.evaluate(test_data, test_label, verbose=1)
        print("Overall Accuracy: %.2f%%" % (scores[1] * 100))



if __name__ == "__main__":
    # For testing correctness only
    train(None, None, (200, 200, 4), 10)