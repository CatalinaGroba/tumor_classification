# FUNCTIONS FOR THE API.

def get_key_by_value(d, value):
    for k, v in d.items():
        if v == value:
            return k
    # If the value is not found in the dictionary, return None
    return None
