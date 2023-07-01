import numpy as np


def network(genome, inputs):
    """ standard network used in the plant cells to generate decisions.
    
    NB:
    The tanh activation function has proved to be advantageous to ensure
    a larger fraction of the initially generated plants survives. (This is
    likely because with a probability of 0.5 an output is negative and thus 
    ignored and the plant survives through inaction)

    Args:
        genome (Genome): genome of plant cell
        inputs (np.array): the "sensory" inputs to a plant cell at a given moment

    Returns:
        np.array: network outputs
    """
    weights = genome.get_normal_genes()
    x = inputs

    for w in weights:
        x = linear(w, x)
        x = tanh(x)

    return x

def linear(weights, inputs):
    """ linear layer

    NB:
    The transpose makes the config notation more intuitive

    Args:
        weights (np.array): weights
        inputs (np.array): inputs from prev layer

    Returns:
        np.array: layer output
    """
    return weights.T @ inputs

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)