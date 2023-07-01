import numpy as np
import plants, genome
import time

def now():
    return time.process_time()

class World():
    def __init__(self, config):
        """ initialize world

        Args:
            config (dictionary): global parameters for the evolution
        """

        self.config = config
        self.world_age = 0

        self.dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.pix_x = self.config["pix_x"]
        self.pix_y = self.config["pix_y"]

        self.entities = []

        # global 2D arrays initialization
        self.life = np.zeros((self.config["pix_y"], self.config["pix_x"])) # pixel life location indicator
        self.light = np.ones_like(self.life) * self.config["sun_energy"] # how much light hits each location
        self.infos = np.zeros((self.pix_y, self.pix_x), dtype=np.int8) # info at each location
        self.energies = np.zeros_like(self.life) # sent energies at each location
        self.nutrients = np.ones((self.pix_x, self.pix_y, self.config["num_nutrients"])) # nutrients at each location


        # initialize life on field randomly
        locations_pool = [(x, y) for y in range(self.pix_y) for x in range(self.pix_x)]
        np.random.shuffle(locations_pool)
        locations = locations_pool[:self.config["starting_num"]]
        
        for loc in locations:
            self.entities.append(plants.PlantCell(self.config, loc, None, energy=1))
            self.life[loc] = 1

        return
    
    def update(self):
        """ update all life in the world at one time step
        """

        # preprocess plant pass
        self.world_age += 1

        self.nutrients += self.config["nutrient_restore"] # restore nutrients

        arr = np.random.permutation(len(self.entities)) # set random update order
        new_entities = []
        dead_entities = []
        new_energies = np.zeros_like(self.light)
        new_infos = np.zeros_like(self.infos)

        # pass over all plants
        for idx in arr:
            plant = self.entities[idx]
            y, x = plant.location

            # process choices of one plant
            repr, send_e, set_inf = plant.choices(self.light[plant.location], self.life, self.infos, self.nutrients)

            # check whether the plant died, or random death
            if not plant.alive or np.random.uniform() < self.config["death_chance"]: 
                self.life[y,x] = 0
                dead_entities.append(plant)

            # process the plants decisions
            for idx in range(4):
                dy, dx = self.dirs[idx]
                new_loc = ((y+dy) % self.pix_y, (x+dx) % self.pix_x)
                
                if repr[idx] == 1 and self.life[new_loc] == 0: # check to add new plant?
                    new_entities.append(plants.PlantCell(self.config, new_loc, plant.genome, energy=1.0))
                    self.life[new_loc] = 1

                new_energies[new_loc] += send_e[idx] # spread energy

            # set plant info
            new_infos[y, x] = set_inf


        # update informations and energies for new turn
        self.infos = new_infos
        self.energies = new_energies

        # remove killed entities, add new ones
        for ent in dead_entities:
            self.entities.remove(ent)
        self.entities += new_entities