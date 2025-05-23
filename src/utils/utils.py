import numpy as np

def softmax(array):
    exp_array = np.exp(array)
    assert not np.isnan((exp_array/np.nansum(exp_array))[~np.isnan(array)]).any()
    return exp_array / np.nansum(exp_array)