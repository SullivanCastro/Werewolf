import numpy as np

def softmax(array):
    exp_array = np.exp(array)
    return exp_array / np.nansum(exp_array)