# FUNCTIONS FOR THE API.
import numpy as np
import nbimporter
from google.cloud import storage



def get_key_by_value(d, value):
    for k, v in d.items():
        if v == value:
            return k
    # If the value is not found in the dictionary, return None
    return None

def predict_class(img, model):
    return model.predict(img)

def resize_image(img):
    image = img.resize((256, 256))
    return np.array(image)
