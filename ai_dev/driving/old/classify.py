import numpy as np
import pickle
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img

# Evaluate one pickle file
def evaluate_one_pickle(pickle_file, model_path):
    model = load_model(model_path)
    
    pickle_file = pickle.load(open(pickle_file, 'rb')).reshape((1, pickle_file.shape[0], pickle_file.shape[1], pickle_file.shape[2]))
    
    class_index = np.argmax(model.predict(pickle_file))
    steering_value = ((class_index / 5.0) + ((class_index + 1) / 5.0)) / 2
    return steering_value
    
    
def evaluate_one_image(image_file, model_path):
    model = load_model(model_path)
    data = img_to_array(load_img(image_file, grayscale=True))
    wh = data.shape[0]
    data = data.reshape(wh, wh)
    image_data = np.zeros((1, wh, wh, 3), dtype="float32")
    
    class_index = np.argmax(model.predict(image_data))
    
    steering_value = ((class_index / 5.0) + ((class_index + 1) / 5.0)) / 2
    return steering_value
    
    