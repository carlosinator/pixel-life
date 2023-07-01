import pygame
import numpy as np
import sys
import time


class CycleLangtons():
    def __init__(self, pix_x, pix_y, rules="RL", colors=[(0, 0, 0), (255, 255, 255)], ant_color=(255, 0, 0), initial_config=None):
        """ initialize Langtons

        NB:
        This class called CycleLangtons because it is a generalization of "standard" Langtons
        Essentially, the rule string determines what to do, when on a certain color:
        For "RL" and [black, white] (see standard values) the ant turns right, when on black and
        left when on white.
        See: https://en.wikipedia.org/wiki/Langton%27s_ant#Extension_to_multiple_colors


        Args:
            pix_x (int): width of ant world
            pix_y (int): height of ant word
            rules (string, optional): Rule string determining turning behavior. Defaults to "RL".
            colors (list, optional): Colors to be displayed. If None, then chosen randomly. Defaults to [(0, 0, 0), (255, 255, 255)].
            ant_color (tuple, optional): Ant color, if None, chosen randomly. Defaults to (255, 0, 0).
        """
        
        # initialize world, standard: empty
        self.life = initial_config
        if self.life is None:
            self.life = np.zeros((pix_y, pix_x), dtype=np.int8)

        # initialize ant color, standard: red
        self.ant_color = ant_color
        if ant_color is None:
            self.ant_color = tuple(np.random.choice(256, size=3))


        # initial ant position and direction
        self.ant_x = pix_x // 2 - 1
        self.ant_y = pix_y // 2 - 1
        self.direction = (-1, 0)
        self.orientation = 0
        
        self.dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.pix_x = pix_x
        self.pix_y = pix_y


        # initialize colors
        if colors is None: 
            # randomly generate colors, for asthetic purposes, the first one is always black
            colors = [(0,0,0)]
            for x in range(len(rules) - 1):
                colors.append(tuple(np.random.choice(256, size=3)))

            print("Generated color RGBs: ", colors) # if one finds a nice combo by coincidence :)


        assert len(rules) == len(colors)

        self.rules = rules
        self.colors = colors
        self.num_rules = len(self.rules)

        # list to keep track of which pixels need to be updated on the display at a certain step
        self.changes = []
        return
    
    def _turn_left(self):
        """ implements left turn of ant (cycles through self.dirs vector)
        """
        self.orientation += 1
        self.orientation = self.orientation % 4
        self.direction = self.dirs[self.orientation]
        return
    
    def _turn_right(self):
        """ implements right turn of ant (cycles through self.dirs vector)
        """
        self.orientation -= 1
        self.orientation = self.orientation % 4
        self.direction = self.dirs[self.orientation]
        return

    def _turn(self, letter):
        """ function that handles both turns aesthetically

        Args:
            letter (string): direction in which to turn

        Raises:
            ValueError: raised for unexpected letter passed
        """
        if letter == "L" or letter == "l":
            self._turn_left()
        elif letter == "R" or letter == "r":
            self._turn_right()
        else:
            raise ValueError("unexpected letter " + str(letter))
        return
    
    def _ant_step(self):
        """ handles the ant taking a step in the direction it is currently pointing
        """
        # update loc
        self.ant_x += self.direction[0]
        self.ant_y += self.direction[1]

        # ensure still on map
        self.ant_x = self.ant_x % self.pix_x
        self.ant_y = self.ant_y % self.pix_y
        return


    def update(self):
        """ handles one "turn" of the ant
        """

        self.changes = [(self.ant_x, self.ant_y)]

        # get color of location and update the direction of the ant
        color = self.life[self.ant_y, self.ant_x]
        self._turn(self.rules[color])

        # set new color value of location, take ant step
        self.life[self.ant_y, self.ant_x] = (self.life[self.ant_y, self.ant_x] + 1) % self.num_rules
        self._ant_step()

        self.changes.append((self.ant_x, self.ant_y))
        return
    

    def get_color(self, x, y):
        """ returns the color tuple at a certain coordinate

        Args:
            x (int): x-axis location
            y (int): y-axis location

        Returns:
            tuple: RGB value of pixel
        """
        if y == self.ant_y and x == self.ant_x: # check if its the ant!
            return self.ant_color
        
        return self.colors[self.life[y,x]]



if __name__ == "__main__":

    UPDATE_TIME = 0 # seconds
    SIM_PIX_SIZE = 8 # how many real pixels is a simulated pixel long?
    num_sim_pix_y, num_sim_pix_x = (128, 128) # dimensions of world in simulated pixels
    rules = "RLLR" 
    colors = [(0, 0, 0), (95, 180, 245), (13, 61, 163), (136, 84, 240)] # this rule and color combo is pretty cool
    # colors = [(0, 0, 0), (79, 160, 121), (58, 130, 111), (176, 112, 152)]
    ant_color = (255, 0, 0)
    world = CycleLangtons(num_sim_pix_x, num_sim_pix_y, rules=rules, colors=colors, ant_color=ant_color)

    SCREEN_SIZE_X = num_sim_pix_x * SIM_PIX_SIZE
    SCREEN_SIZE_Y = num_sim_pix_y * SIM_PIX_SIZE

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y)) 
    pygame.display.set_caption("One Upon A Time... there was a little ant that was fond of procedural generation")


    running = True
    screen.fill(world.colors[0])
    while running:
        time.sleep(UPDATE_TIME)
        world.update()

        for elem in world.changes:
            x, y = elem
            # calculate the position of the simulated pixel on the screen
            screen_x = x * SIM_PIX_SIZE
            screen_y = y * SIM_PIX_SIZE

            # get and draw the simulated pixel on the screen
            pixel_color = world.get_color(x,y)
            pygame.draw.rect(screen, pixel_color, (screen_x, screen_y, SIM_PIX_SIZE, SIM_PIX_SIZE))


        for event in pygame.event.get(): # exit condition
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()