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
    def calc_utility(self , ):

       return

    def find_max(self , L , K , u1 = 0.5 , u2 = 0.5 ):
        U_max = 0
        for l in range(L):
            for k in range(K):

                utility = self.calc_utility(u1 , u2 , l , k)
                if utility > U_max:
                    U_max = utility
                    L_opt = l
                    K_opt = k
        return U_max , L_opt , K_opt     
    
    
        
    def trade():

        def constraint21(x):
                    la , ka , lb , kb , t , tr = x # Country A cant put more capital into product 1 than it has available
                    return KA - ka

        def constraint22(x):
            la , ka , lb , kb , t , tr = x # Country A cant put more labor into product 1 than it has available
            return LA - la
        def constraint23(x):
            la , ka , lb , kb , t , tr = x # Country B cant put more capital into product 1 than it has available
            return KB - kb
        def constraint24(x):
            la , ka , lb , kb , t , tr = x # Country B cant put more labor into product 1 than it has available
            return LB - lb
        def constraint25(x):
            la , ka , lb , kb , t , tr = x # Country A cant trade more than they have of product 1
            return QA1_max - t
        def constraint26(x):
            la , ka , lb , kb , t , tr = x # Country B cant trade more than they have of product 1
            return  QB1_max + t
        def constraint27(x):
            la , ka , lb , kb , t , tr = x # Country A cant trade more than they have of product 2
            return QA2_max + (t * tr)
        def constraint28(x):
            la , ka , lb , kb , t , tr = x # Country B cant trade more than they have of product 2
            return QB2_max - (t * tr)

        cons_2 = [{'type':'ineq', 'fun':constraint21},
                {'type':'ineq', 'fun':constraint22},
                {'type':'ineq', 'fun':constraint23},
                {'type':'ineq', 'fun':constraint24},
                {'type':'ineq', 'fun':constraint25},
                {'type':'ineq', 'fun':constraint26},
                {'type':'ineq', 'fun':constraint27},
                {'type':'ineq', 'fun':constraint28}]

        x0 = [opt_KA , opt_LA , opt_KB , opt_LB , 70 , 1 ] # initial guess


        bounds_2 = [(0, LA), (0, KA), (0, LB), (0, KB) , (0, QA1_max) , (0.001, None)]  # bounds of input variables

        sol2 = optimize.minimize(objective2, x0 , method='SLSQP', bounds=bounds_2, constraints=cons_2)

        LTA , KTA , LTB , KTB , T1 , Tr = sol2.x[0] , sol2.x[1] , sol2.x[2] , sol2.x[3] , sol2.x[4] , sol2.x[5]

        print ("inputs are  LA = %.0f, KA = %.0f, LB = %.0f, KB = %.0f, T = %.0f and , Tr = %.2f " % (LTA , KTA , LTB , KTB , T1 , Tr))

        trade1 = sol2.x[4]
        trade_rate = sol2.x[5]
        trade2 = trade1 * trade_rate

        print("\nTrade: %.0f units of good 1 for %.0f units of good 2" % (trade1 , trade2))

        print(LA , LTA, KA , KTA)
        print(LB , LTB , KB , KTB)

        # Goods Produced
        PA1 = Q1(LTA ,  KTA) 
        PA2 = Q2(LA , LTA, KA , KTA) 
        PB1 = Q1(LTB , KTB)
        PB2 = Q2(LB , LTB , KB , KTB)

        # Goods consumed
        CA1 = PA1 - trade1
        CA2 = PA1 + (trade1 * trade_rate)
        CB1 = PB1 + trade1
        CB2 = PB2 - (trade1 * trade_rate)

        print("\nCountry A:\n product 1: %.0f produced, %.0f consumed\n product 2: %.0f produced, %.0f consumed\n product 1: %.0f produced, %.0f consumed \n product 2: %.0f produced, %.0f consumed " % (PA1 , CA1 , PA2 , CA2 , PB1 , CB1 , PB2 , CB2))

        Ut_A = CA1**betaA*CA2**(1-betaA)
        Ut_B = CB1**betaB*CB2**(1-betaB)

        print("\nUtility of country A: \nbefore trade: %.0f\nafter trade: %.0f\n\nUtility of country B:\nbefore trade: %.0f\nafter trade: %.0f\n" % (UA_closed, Ut_A ,  UB_closed , Ut_B))









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