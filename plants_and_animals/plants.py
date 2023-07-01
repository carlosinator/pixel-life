import activations, genome
import numpy as np
import time

class PlantCell():
    def __init__(self, config, location, parent_genome, energy, context=None):
        """ initialization of one plant cell

        Args:
            config (dictionary): _description_
            location (tuple): _description_
            genome (Genome): _description_
            energy (float): _description_
            context (np.array, optional): currently meaningless. Defaults to None.
        """
        self.config = config
        self.location = location

        self.genome = genome.Genome(self.config, parent_genes=parent_genome)

        # currently not used
        self.context = context
        if context is None:
            self.context = np.zeros(config["context_size"])
        
        # initialize state vars
        self.energy = energy
        self.init_e = self.energy
        self.alive = True
        self.decision = np.zeros(12)
        self.inputs = np.zeros(10)
        self.age = 0
        
        # set coordinates relative to cell
        y, x = self.location
        self.left = (x - 1) % self.config["pix_x"]
        self.right = (x + 1) % self.config["pix_x"]
        self.up = (y - 1) % self.config["pix_y"]
        self.down = (y + 1) % self.config["pix_y"]

        # insert and process config values
        self.repr_cost = self.config["reproduction_cost"]
        self.e_send_cost =  1 + self.config["energy_sending_cost"]
        self.info_send_cost = self.config["info_sending_cost"]
        self.nutr_greed = self.config["nutrient_greed"]

        return
    
    
    def choices(self, new_energy, curr_life, curr_infos, curr_nurtients):
        """ process a plants entire turn

        Args:
            new_energy (float): energy gained from sun and neighbors
            curr_life (np.array): 2D array that indicates all life
            curr_infos (np.array): 2D array that indicates all neighbor infos
            curr_nurtients (np.array: 2D array that gives the nutrient state of the plant cells

        Returns:
            tuple(np.array, np.array, float): (
                repr: 1D-indicator array where to reproduce,
                send_e: 1D-float array how much energy to send,
                send_inf: float indicating how to set information state
                )
        """

        self.energy += new_energy
        self.init_e = self.energy
        self.age += 1
        
        y, x = self.location

        # extract relevant figures (those directly adjacent)
        neighb = [curr_life[self.up, x], curr_life[y, self.right], curr_life[self.down, x], curr_life[y, self.left]]
        infos = [curr_infos[self.up, x], curr_infos[y, self.right], curr_infos[self.down, x], curr_infos[y, self.left]]

        age_cost = self.config["sun_energy"] * 1.1 * (1 - np.exp(-self.config["energy_cost_age"] * self.age))

        
        # compile input array
        self.inputs[0] = self.energy
        self.inputs[1] = age_cost
        self.inputs[2:6] = neighb
        self.inputs[6:] = infos

        # process network forward pass
        repr, send_e, set_inf = self.think()
        
        # calculate cost of this turn
        cost = age_cost
        cost += np.sum(repr) * self.repr_cost
        cost += np.sum(send_e) * self.e_send_cost
        cost += set_inf * self.info_send_cost
        self.energy -= cost

        # calculate the necessary nutrient pull
        nutr_pull = cost * self.genome.nutrition * self.nutr_greed
        nutr_tile = curr_nurtients[y,x] - nutr_pull

        # if use more energy than in stores, or not enough nutrients available: die
        if self.energy < 0 or len(nutr_tile[nutr_tile < 0]) > 0:
            self.alive = False
            return repr*0, send_e*0, set_inf*0
        
        # update nutrient tile
        curr_nurtients[y,x] = nutr_tile

        # dissipation tax on unspent energy (very communist)
        self.energy -= self.energy * self.config["energy_cost_dissipation"] * self.config["sun_energy"]

        return repr, send_e, set_inf
    

    def think(self):
        """ process network pass and clean outputs

        Returns:
            tuple(np.array, np.array, np.array, float): (
                repr : 1D-array that indicates in clockwise dir where to add a descendant,
                send_e : 1D-array that indicates in clockwise dir how much energy to send,
                send_inf : Sets the information status of the cell
            )
        """
        out = activations.network(self.genome, self.inputs)
        self.decision = out.copy()

        # assign meanings to network outputs
        raw_repr = out[:4]
        raw_e = out[4:8]
        raw_inf = out[8:]

        # process outputs
        repr = np.zeros_like(raw_repr)
        repr[raw_repr >= 0.5] = 1 # round to indicate clear decision

        send_e = raw_e
        send_e[send_e < 0] = 0 # cannot send negative energy (that's mean)

        set_inf = 0
        if raw_inf[0] >= 0.5: set_inf = 1 # round to indicate clear information

        return repr, send_e, set_inf
    
    
    def summary(self):
        """ debug function indicating the state of the plant
        """
        dec_cost = np.sum(np.round(self.decision[:4])) * self.config["reproduction_cost"]
        info_cost = np.sum(np.round(self.decision[8:])) * self.config["info_sending_cost"]
        e_cost = np.sum(self.decision[4:8]) * self.e_send_cost
        delta = self.init_e - dec_cost - info_cost - e_cost - self.energy
        # print(f"plant at {self.location}, with energy {self.energy:.2f}, shared energy {np.sum(self.decision[4:8])}")
        print(f'plant at {self.location}, with repr cost {dec_cost:.5f}, shared_e {e_cost:.5f}, shared info {info_cost:.5f}, initial_e {self.init_e:.5f}, final_e {self.energy:.5f}, delta {delta:.5f}')
    