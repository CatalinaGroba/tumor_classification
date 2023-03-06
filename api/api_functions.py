# FUNCTIONS FOR THE API.
import numpy as np

def get_key_by_value(d, value):
    for k, v in d.items():
        if v == value:
            return k
    # If the value is not found in the dictionary, return None
    return None

def predict_class(img):
    return np.randint(0,4,1)


