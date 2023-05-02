from scipy import optimize
from types import SimpleNamespace

import numpy as np
from scipy import optimize

import pandas as pd 
import matplotlib.pyplot as plt

class model:

    def __inits__(self):

        # Namespaces
        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()

        # Input parameters
        # Capital and labor
        par.K1 = 2000
        par.K2 = 1000
        par.L1 = 2000
        par.L2 = 1000

        # Price of labor and capital
        par.w1 = 2
        par.w2 = 1
        par.r1 = 1
        par.r2 = 2









""""
def solve_ss(alpha, c):
     Example function. Solve for steady state k. 

    Args:
        c (float): costs
        alpha (float): parameter

    Returns:
        result (RootResults): the solution represented as a RootResults object.

     
    
    # a. Objective function, depends on k (endogenous) and c (exogenous).
    f = lambda k: k**alpha - c
    obj = lambda kss: kss - f(kss)

    #. b. call root finder to find kss.
    result = optimize.root_scalar(obj,bracket=[0.1,100],method='bisect')
    
    return result """