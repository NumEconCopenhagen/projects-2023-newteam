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

        
    #define utility functions
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

#im not sure about this part we might look at that again
def solve_discrete(self,do_print=False):
        
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        
        # a. all possible choices
        x = np.linspace(0,24,49)
        LM,HM,LF,HF = np.meshgrid(x,x,x,x) # all combinations
    
        LM = LM.ravel() # vector
        HM = HM.ravel()
        LF = LF.ravel()
        HF = HF.ravel()

#until here im not sure if its correct (becuase its just a copy of his code)


