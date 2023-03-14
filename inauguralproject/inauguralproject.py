from types import SimpleNamespace

class inauguralproject:

    def __init__(self):
    # a. create namespaces
        par = self.par = SimpleNamespace()

    # add preferences
        par.p = 2
        par.v = 0.001
        par.omega = 0.5 

    # add household production
        par.alpha = 0.5
        par.sigma = 1
    
    # add wages
        par.wM = 1
        par.wF = 1
        

    def func_marketgoods():
    """ square numpy array
    
    Args:
    
        x (ndarray): input array
        
    Returns:
    
        y (ndarray): output array
    
    """
    
    y = x**2
    return y