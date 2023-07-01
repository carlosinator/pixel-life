import numpy as np
from PIL import Image

def get_array_for_conway(path):
    """ Creates a numpy array from an image

    NB:
    Anything that is not WHITE (or fully 255) will be set to be alive,
    the rest will be set to dead.

    Args:
        path (_type_): _description_

    Returns:
        np.array: image array that can be used in the Conways() config
    """

    img = Image.open(path).convert("L")

    arr = np.round(np.asarray(img))

    img_arr = np.zeros_like(arr)
    img_arr[arr < 255] = 1

    return img_arr