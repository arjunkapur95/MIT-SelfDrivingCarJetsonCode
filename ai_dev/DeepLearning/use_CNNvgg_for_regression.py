########################################################################################################################
# Use CNN(vgg) for regression - ReadMe
# Author: czha5168
# Editor: jodu0512
########################################################################################################################
# 1. Function Declaration:
#        build_model()                               ----- Created by Original Author(ai_dev/DeepLearning/MITCarV2.py)
#        build_model_for_regression()                ----- Modify CNN for regression, instead of classification
#        load_pretrained_vgg()                       ----- Simply show how to load the VGG pre-trained on IMAGENET
#                                                          dataset via 1-line-command from keras
#
# 2. Problem about build_model():
#        The original build_model() only created a VGG from sketch.
#        However it could not be used for MITCAR project directly, for the following reasons:
#               a. It only have 1 output(with 2 class).
#               b. It only deal with categorical data(class/label). AKA, a classification task.
#        The model we want to achieve:
#               a. It should have 2 output(output_angle and output_throttle)
#                  output_angle    for the angle of rotation
#                  output_throttle for the speed
#                  * In other words, we expect to see 2 independent outputs.
#               b. It is more reasonable to modify the VGG so that it could be used for Regression.
#                  angle_out    -  Continuous data in the range of [0, 180] (or [-1,+1] if normalizaiton is applied)
#                  throttle_out -  Continuous data in the range of [-max_speed, max_speed] (or [-1, +1] if normalization 
#                                  is applied
#
# 3. Some basic concepts in the domain of deep learning(CNN):
#        a. For classification task, the corresponding configuration should be:
#                   number_of_neuron_in_last_layer     = number_of_classes
#                   activation_func_used_in_last_layer = softmax
#                   loss_func_used_for optimization    = categorical_crossentropy
#        b. For regression task, the corresponding configuration should be:
#                   number_of_neuron_in_last_layer     = number_of_output (in our case(=2), speed and angle)
#                   activation_func_used_in_last_layer = linear or relu
#                   loss_func_used_for optimization    = mean_absolute_error
#        c. Use Dropout layer to prevent overfitting
#        d. Transfer Learning:
#               A more common way to apply VGG for other projects is Transfer Learning.
#               The disadvantage of not using transfer learning:
#                       1. It takes 2-3 weeks with a system of 4 NVIDIA Titan to train a VGG from sketch.
#                          For CPU, it would be months.
#                          * Please refer to Karen's "VERY DEEP CONVOLUTIONAL NETWORKS FOR LARGE-SCALE IMAGE RECOGNITION"
#                       2. Considering the significantly enormous number of parameters stored in VGG, we may need to
#                          collect at least 1 million images for training process.
#                          * Please refer to Feifei's "ImageNet: A Large-Scale Hierarchical Image Database",
#                          they build a IMAGENET dataset with 1.2 million images to train a VGG.
#               The advantage of using transfer learning:
#                       Well... we can simply load the weights pre-trained on IMAGENET and do the fine-tuning on our
#                       own dataset. In other words, fast and amazing performance.
#        e. Potential issue for using Vgg:
#               We have to do experiments to check whether the model could be used for prediction in real-time.
#               It depends on the calculation power provided by the chip from nvidia.
#               From my experience, it is toooooooooooo slow to use for real-time detection, via GTX1070
# 4. Note:
#        a.load_pretrained_vgg() only show how to load pre-trained vgg from keras easily. However, to use it for this
#          project, we still need to modify it for regression task. But I did not do it, because it seems that there
#          might be a chance that VGG cannot be used in real-time. In that case, it would be totally a waste of time
#          to do it.
#
#          Well...If we test that VGG is good for real-time by experiments later, we can make the modification done easily.
#        b. The expected input_shape for VGG is (224,224,3).
#           Please note that for our depth camera, the total channel captured would be 4 instead of 3,
#           which is [r g b depth].
#           It means we may need to modify the parameters for convolutional part of VGG.
#######################################################################################################################
import keras
from keras.models import Sequential, Model
from keras.layers import Input, Flatten, Dense, Dropout, Conv2D, MaxPooling2D
def build_model(input_shape=(224,224,3), nb_class=2):
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
def build_model_for_regression(input_shape=(224,224,3)):
    img_input = Input(shape=input_shape)
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1')(img_input)
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)
    x = Flatten(name='flatten')(x)
    # The following code is modified
    x = Dense(4096, activation='relu', name='fc1')(x)
    x = Dropout(.5)(x)
    x = Dense(4096, activation='relu', name='fc2')(x)
    x = Dropout(.5)(x)
    out_angle = Dense(1, activation='relu', name='out_angle')(x)
    out_throttle = Dense(1, activation='relu', name='out_throttle')(x)
    model = Model(inputs=[img_input], outputs=[out_angle, out_throttle])
    model.compile(optimizer='rmsprop',
                  loss={'out_angle': 'mean_squared_error',
                        'out_throttle': 'mean_squared_error'},
                  loss_weights={'out_angle': 0.9, 'out_throttle': .001})

    model.summary()
    return model
def load_pretrained_vgg():
    # This pretrained VGG could not be used for our project without an appropriate modifcation on its framework
    model = keras.applications.vgg19.VGG19(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000)
    model.summary()
    return model
if __name__=='__main__':
    vgg =  build_model()
    vgg4regession = build_model_for_regression()
    pre_vgg = load_pretrained_vgg()
