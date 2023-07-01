import scipy
import pygame
import numpy as np
import sys, time
import utils


class Conways():

    def __init__(self, initial_config=None, size=None):
        """ initialization

        the Game Of Life class

        Args:
            pix_x (int): width of world
            pix_y (int): height of world
            initial_config (np.array, optional): Initial configuration for conways. Defaults to None.
        """

        # set initial config
        if initial_config is None:
            assert len(size) == 2 and type(size) == type((0,)), "Not a vali"
            self.life = np.zeros(size)
            self.size = size
        else:
            assert initial_config is not None, "Too few parameters passed, either initial_config or size"
            self.life = initial_config
            self.size = initial_config.shape
        
        # used for convolution in update()
        self.filter = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        self.pixel_age = np.infty * np.ones_like(initial_config)
        return
    

    def update(self):
        """ implementation of one step of conways
        """

        # find neighbors of all positions
        num_neighbs = scipy.signal.convolve2d(self.life, self.filter, mode="same", boundary="wrap")

        # update rules
        self.life[np.logical_and(self.life == 1, num_neighbs < 2)] = 0
        self.life[np.logical_and(self.life == 1, num_neighbs > 3)] = 0
        self.life[np.logical_and(self.life == 0, num_neighbs == 3)] = 1

        self.pixel_age += 1
        self.pixel_age[self.life == 1] = 0
        return
    
    def get_grayscale(self, with_age=False, age_factor=0.5):

        if with_age:
            return np.exp(np.log(age_factor) * self.pixel_age) # grayscale value of aged pixels
        
        else:
            return self.life
    


if __name__ == "__main__":
    SIM_PIX_SIZE = 8
    UPDATE_TIME = 5e-2 # seconds
    WHITE = np.array([255, 255, 255])

    img_arr = utils.get_array_for_conway("procedural_generation/berry.png")
    world = Conways(initial_config=img_arr)

    num_sim_pix_y, num_sim_pix_x = world.size
    SCREEN_SIZE_X = num_sim_pix_x * SIM_PIX_SIZE
    SCREEN_SIZE_Y = num_sim_pix_y * SIM_PIX_SIZE


    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y)) 
    pygame.display.set_caption("The Classic Game of Life")


    running = True
    screen.fill((0,0,0))
    while running:
        time.sleep(UPDATE_TIME)

        # update world and get color vals
        world.update()
        graysc = world.get_grayscale(with_age=True, age_factor=0.3)

        for y in range(num_sim_pix_y):
            for x in range(num_sim_pix_x):
                screen_x = x * SIM_PIX_SIZE
                screen_y = y * SIM_PIX_SIZE

                pixel_color = tuple(WHITE * graysc[y, x])

                # draw the simulated pixel on the screen
                pygame.draw.rect(screen, pixel_color, (screen_x, screen_y, SIM_PIX_SIZE, SIM_PIX_SIZE))


        for event in pygame.event.get(): # exit condition
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()