# FUNCTIONS FOR THE API.
import numpy as np
#from tumor_class.jupyter import load_tumor_images
from tensorflow.keras.applications.efficientnet import EfficientNetB0
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#klk = load_tumor_images()

def get_key_by_value(d, value):
    for k, v in d.items():
        if v == value:
            return k
    # If the value is not found in the dictionary, return None
    return None

def predict_class(img, model):
    return model.predict(img)

def resize_image(img):
    #generator= ImageDataGenerator()
    #image = generator.flow(target_size=(256, 256))
    img= img.resize(256,256).expand_dims(axis=-1)
    return np.array(img)

def load_model():

    model = EfficientNetB0(weights='imagenet',include_top=False,input_shape=(256, 256,3))
    model.trainable = False

    flatten_layer = layers.Flatten()
    dense_layer = layers.Dense(100, activation='relu')
    dropout_layer = layers.Dropout(0.2)

    prediction_layer = layers.Dense(4, activation='softmax')


    model = models.Sequential([
        model,
        flatten_layer,
        dense_layer,
        dropout_layer,
        prediction_layer
    ])

    return model
