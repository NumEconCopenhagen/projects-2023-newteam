from types import SimpleNamespace
import numpy as np

class inauguralproject:

    def __init__(self):
    # a. create namespaces
        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()

    # add preferences
        par.rho = 2
        par.v = 0.001
        par.omega = 0.5 
        par.epsilon = 1
       

    # add household production
        par.alpha = 0.5
        par.sigma = 1
    
    # add wages
        par.wM = 1
        par.wF = 1
        par.wF_vec = np.linspace(0.8,1.2,5)

        

    def calc (self,LM,HM,LF,HF):
        
        par = self.par

        # Consumption 
        C = par.wM*LM + par.wF*LF

        # Home production
        H = HM**(1-par.alpha)*HF**par.alpha

        # Total consumption
        Q = C**par.omega*H**(1-par.omega)

        #Utility of work
        utility = (Q**(1-par.p))/(1-par.p)

        #Utility-cost of work
        TM = LM*HM
        TF = LF*HF
        cost = par.v*(TM**(1+1/par.epsilon)/(1+1/par.epsilon)+TF**(1+1/par.epsilon)/(1+1/par.epsilon))
        
        #Total utility
        tot_utility = utility - cost
        return tot_utility 



    def func_marketgoods():
    """ square numpy array
    
    Args:
    
        x (ndarray): input array
        
    Returns:
    
        y (ndarray): output array
    
    """
    
    y = x**2
    return y