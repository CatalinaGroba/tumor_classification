# FUNCTIONS FOR THE API.
import numpy as np
import nbimporter
from jupyter import load_tumor_images


klk = load_tumor_images()

def get_key_by_value(d, value):
    for k, v in d.items():
        if v == value:
            return k
    # If the value is not found in the dictionary, return None
    return None

def predict_class(img):
    temp = np.random.randint(0,4,1)
    return temp
