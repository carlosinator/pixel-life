import numpy as np
from PIL import Image

def get_array_for_conway(path):

    img = Image.open(path).convert("L")

    arr = np.round(np.asarray(img))
    arr = np.rot90(arr, 1)
    arr = np.flip(arr, axis=0)
    img_arr = np.zeros_like(arr)

    img_arr[arr < 255] = 1

    return img_arr