import numpy as np
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, GlobalAveragePooling2D, Activation, merge, ZeroPadding2D, Input, BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D, AveragePooling2D
from keras.utils import np_utils


# The model is used to test if four channel images can be used as input
def buildTestingModel():

    model = Sequential()

    img_input = Input(shape=(50, 50, 4))

    # Block 1
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1')(img_input)
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Classification block
    x = Flatten(name='flatten')(x)
    x = Dense(256, activation='relu', name='fc2')(x)
    x = Dense(2, activation='softmax', name='predictions')(x)

    model = Model(img_input, x, name='AiGoNet')

    return model


def generate_fake_dataset():
    random_image = np.ndarray(shape=(2, 50, 50, 4), dtype=float, order='F')
    random_label = np_utils.to_categorical(np.asarray([0, 1]), 2)

    return random_image, random_label


fake_data, fake_label = generate_fake_dataset()
print(fake_data.shape, fake_label.shape)
print(fake_label)


model = buildTestingModel()
model.compile(loss='categorical_crossentropy',optimizer='Adam', metrics=['accuracy'])

model.fit(fake_data, fake_label, batch_size=1,verbose=1)