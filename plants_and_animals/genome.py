from abc import abstractmethod, ABC
import numpy as np

class Genome(ABC):
    def __init__(self, config, parent_genes=None):
        """ init a Genome

        Args:
            config (dictionary): dictionary set in main, which marks global parameters
            parent_genes (Genome, optional): Genome of the parent plant. Defaults to None.
            shapes (list(tuple), optional): If Genome of parent is None, initialize choice genes using shapes (ignored otherwise). Defaults to None.
        """

        self.var = config["genome_mutation"] # list of hyperparameters used in the mutation_func
        self.num_nutrients = config["num_nutrients"] # size of nutrient vector
            
        
        if parent_genes is None:

            # initialize choice genes
            self.normal_genes = []
            for shp in config["genome_size"]:
                self.normal_genes.append(np.random.uniform(low=-1, high=1, size=shp))

            # initialize and normalize nutrition genes
            self.nutrition = np.random.uniform(low=0, high=1, size=self.num_nutrients)
            self.nutrition /= np.sum(self.nutrition)

        else:

            # initialize and vary choice genome based on parent
            self.normal_genes = []
            for i in range(len(parent_genes.normal_genes)):
                par = parent_genes.normal_genes[i]
                self.normal_genes.append(self.mutation_func(par))

            # initialize, vary and normalize nutrition genome based on parent
            self.nutrition = self.mutation_func(parent_genes.nutrition)
            self.nutrition /= np.sum(np.abs(self.nutrition))

        # set the color of the plant
        self.color = self.compute_color()

        return
    

    def compute_color(self):
        """ compute the color based on the genes to vaguely indicate how closely
        related two plant cells are

        Returns:
            tuple: RGB code of plant cell
        """
        gene_array = np.concatenate(self.normal_genes).flatten()
        lga = int(gene_array.shape[0]/3)
        color = [0,0,0]
        for idx in range(3):
            color[idx] = int(2 * np.mean(np.abs(gene_array[idx*lga:(idx+1)*lga])) * 255) % 256
        
        return tuple(color)
    

    def get_color(self):
        """ returns the color array for this genome

        Returns:
            tuple: length 3 tuple containing RGB code
        """
        return self.color
    
    def get_normal_genes(self):
        """ returns a list of genes (matrices) that are used to make decisions each turn.

        Returns:
            list: list of numpy arrays that match for multiplication purposes
        """
        return self.normal_genes
    

    def mutation_func(self, input):
        """ mutation function that contains the mechanism with which genes mutate.
        It uses the self.var variable, that contains a list of variation parameters
        used to set specific probabilities, etc. when varying genes.

        Args:
            input (np.array): N-dimensional np.array to be changed

        Returns:
            np.array: varied version of np.array
        """
        x = input.copy()
        x += np.random.normal(scale=self.var[0], size=input.shape)

        if np.random.uniform() < self.var[1]:
            random_index = np.random.choice(x.size)
            idx = np.unravel_index(random_index, x.shape)

            # Modify the randomly selected element
            x[idx] = 1 - x[idx]

        # if np.random.uniform() < self.var[2]:
        #     flip_size = np.random.choice(x.size)
        #     elems = np.random.choice(x.size, size=flip_size)

        #     indices = np.unravel_index(elems, x.shape)
        #     # next_indices = tuple((np.array(indices) + 1) % np.array(x.shape))

        #     # x[indices] = x[next_indices]

        return x
