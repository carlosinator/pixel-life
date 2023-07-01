import numpy as np

class Langtons():
    def __init__(self, pix_x, pix_y, initial_config=None):

        if initial_config is None:
            self.life = np.zeros((pix_y, pix_x))
        else:
            assert initial_config.shape == (pix_y, pix_x)
            self.life = initial_config

        self.ant_x = pix_x // 2
        self.ant_y = pix_y // 2
        self.direction = (-1, 0)

        self.orientation = 0
        
        self.dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        self.pix_x = pix_x
        self.pix_y = pix_y

        self.color = np.zeros((pix_y, pix_x, 3))
        self.changes = []
        return
    
    def _turn_left(self):
        self.orientation += 1
        self.orientation = self.orientation % 4
        self.direction = self.dirs[self.orientation]
    
    def _turn_right(self):
        self.orientation -= 1
        self.orientation = self.orientation % 4
        self.direction = self.dirs[self.orientation]

    def _ant_step(self):
        self.ant_x += self.direction[0]
        self.ant_y += self.direction[1]

        self.ant_x = self.ant_x % self.pix_x
        self.ant_y = self.ant_y % self.pix_y

    
    def update(self):
        self.changes = [(self.ant_x, self.ant_y)]
        if self.life[self.ant_y, self.ant_x] == 1:
            # print("ant on light, turn right", self.ant_x, self.ant_y)
            self._turn_left()

        else:
            # print("ant on dark, turn left", self.ant_x, self.ant_y)
            self._turn_right()


        self.life[self.ant_y, self.ant_x] = 1 - self.life[self.ant_y, self.ant_x]
        
        self._ant_step()

        self.changes.append((self.ant_x, self.ant_y))

        return


class CycleLangtons():
    def __init__(self, pix_x, pix_y, rules=["R", "L"], colors=[(0, 0, 0), (255, 255, 255)], ant_color=(255, 0, 0)):

        self.life = np.zeros((pix_y, pix_x), dtype=np.int8)

        self.ant_color = ant_color

        self.ant_x = pix_x // 2 - 1
        self.ant_y = pix_y // 2 - 1
        self.direction = (-1, 0)

        self.orientation = 0
        
        self.dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        self.pix_x = pix_x
        self.pix_y = pix_y


        assert len(rules) == len(colors)

        self.rules = rules
        self.colors = colors
        self.num_rules = len(self.rules)

        self.changes = []
        return
    
    def _turn_left(self):
        self.orientation += 1
        self.orientation = self.orientation % 4
        self.direction = self.dirs[self.orientation]
        return
    
    def _turn_right(self):
        self.orientation -= 1
        self.orientation = self.orientation % 4
        self.direction = self.dirs[self.orientation]
        return

    def _turn(self, letter):
        if letter == "L":
            self._turn_left()
        elif letter == "R":
            self._turn_right()
        else:
            raise ValueError("unknown letter: " + str(letter))
        return
    
    def _ant_step(self):
        self.ant_x += self.direction[0]
        self.ant_y += self.direction[1]

        self.ant_x = self.ant_x % self.pix_x
        self.ant_y = self.ant_y % self.pix_y


    def update(self):
        self.changes = [(self.ant_x, self.ant_y)]

        color = self.life[self.ant_y, self.ant_x]
        self._turn(self.rules[color])

        self.life[self.ant_y, self.ant_x] = (self.life[self.ant_y, self.ant_x] + 1) % self.num_rules
        self._ant_step()

        self.changes.append((self.ant_x, self.ant_y))
        return





