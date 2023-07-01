import numpy as np
import scipy
# from scipy import signal

class Conways():
    

    def __init__(self, pix_x, pix_y, initial_config=None):

        if initial_config is None:
            self.life = np.zeros((pix_x, pix_y))
        else:
            assert initial_config.shape == (pix_x, pix_y)
            self.life = initial_config
        
        self.filter = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        return
    

    def update(self):
        num_neighbs = scipy.signal.convolve2d(self.life, self.filter, mode="same", boundary="wrap")
        self.life[np.logical_and(self.life == 1, num_neighbs < 2)] = 0
        self.life[np.logical_and(self.life == 1, num_neighbs > 3)] = 0
        self.life[np.logical_and(self.life == 0, num_neighbs == 3)] = 1
        return
    
    def color(self):
        return