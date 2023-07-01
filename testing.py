from PIL import Image
import numpy as np
import time

my_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Flattened array size
array_size = my_array.size

# Randomly select an index
random_index = np.random.choice(array_size)

# Convert the flattened index to the corresponding row and column indices
row_index, col_index = np.unravel_index(random_index, my_array.shape)

# Modify the randomly selected element
my_array[row_index, col_index] = 100


print(my_array.size)