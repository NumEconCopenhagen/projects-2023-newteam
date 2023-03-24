from types import SimpleNamespace

import numpy as np
from scipy import optimize

import pandas as pd 
import matplotlib.pyplot as plt

class inauguralproject:

    def __init__(self):
        """ setup model """

        # a. create namespaces
        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()

        # b. preferences
        par.rho = 2.0
        par.nu = 0.001
        par.epsilon = 1.0
        par.omega = 0.5 

        # c. household production
        par.alpha = 0.5
        par.sigma = 1.0

        # d. wages
        par.wM = 1.0
        par.wF = 1.0
        par.wF_vec = np.linspace(0.8,1.2,5)

        # e. targets
        par.beta0_target = 0.4
        par.beta1_target = -0.1

        # f. solution
        sol.LM_vec = np.zeros(par.wF_vec.size)
        sol.HM_vec = np.zeros(par.wF_vec.size)
        sol.LF_vec = np.zeros(par.wF_vec.size)
        sol.HF_vec = np.zeros(par.wF_vec.size)

        sol.beta0 = np.nan
        sol.beta1 = np.nan

    def calc_utility(self,LM,HM,LF,HF):
        """ calculate utility """

        par = self.par
        sol = self.sol

        # a. consumption of market goods
        C = par.wM*LM + par.wF*LF

        # b. home production
        if par.sigma == 1:
            H = HM**(1-par.alpha)*HF**par.alpha
        elif par.sigma == 0:
            H = np.min (HM, HF)
        else:
            H = ((1- par.alpha)*HM**((par.sigma -1)/par.sigma)+ par.alpha*HF**((par.sigma -1)/par.sigma))**(par.sigma/(par.sigma - 1))
         

        # c. total consumption utility
        Q = C**par.omega*H**(1-par.omega)
        utility = np.fmax(Q,1e-8)**(1-par.rho)/(1-par.rho)

        # d. disutlity of work
        epsilon_ = 1+1/par.epsilon
        TM = LM+HM
        TF = LF+HF
        disutility = par.nu*(TM**epsilon_/epsilon_+TF**epsilon_/epsilon_)
        
        return utility - disutility

    def solve_discrete(self,do_print=False):
        """ solve model discretely """
        
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

        # b. calculate utility
        u = self.calc_utility(LM,HM,LF,HF)
    
        # c. set to minus infinity if constraint is broken
        I = (LM+HM > 24) | (LF+HF > 24) # | is "or"
        u[I] = -np.inf
    
        # d. find maximizing argument
        j = np.argmax(u)
        
        opt.LM = LM[j]
        opt.HM = HM[j]
        opt.LF = LF[j]
        opt.HF = HF[j]

        # e. print
        if do_print:
            for k,v in opt.__dict__.items():
                print(f'{k} = {v:6.4f}')

        return opt

    def solve(self, do_print=False):
        """ solve model continuously """

        par = self.par
        sol = self.sol

        # a. set up objective function
        def obj(x):
            opt = self.calc_utility(x[0], x[1], x[2], x[3])
            return - opt
        
        # b. find optimal wage ratio for each wF
        for i in range(par.wF_vec.size):
            par.wF = par.wF_vec[i]
            result = optimize.minimize(obj, x0 = [12]*4, bounds = [(0,24)]*4)
            sol.HM_vec[i] = result.x[0]
            sol.HF_vec[i] = result.x[1]
            sol.LM_vec[i] = result.x[2]
            sol.LF_vec[i] = result.x[3]

    def solve_wF_vec(self,discrete=False):
        """ solve model for vector of female wages """

        par = self.par
        sol = self.sol
        opt = SimpleNamespace()

        if discrete ==True:
            for k,i in enumerate(par.wF_vec) :
                par.wF = i
                opt = self.solve_discrete()
                sol.HM_vec[i]=opt.HM
                sol.HF_vec[i]=opt.HF
                sol.LM_vec[i]=opt.LM
                sol.LF_vec[i]=opt.LF

        if discrete ==False:
            for k, i in enumerate(par.wF_vec):
                par.wF = i
                opt = self.solve()
                sol.HM_vec[i]=opt.HM
                sol.HF_vec[i]=opt.HF
                sol.LM_vec[i]=opt.LM
                sol.LF_vec[i]=opt.LF

        return sol

    def run_regression(self,print=False):
        """ run regression """

        par = self.par
        sol = self.sol

        x = np.log(par.wF_vec)
        y = np.log(sol.HF_vec/sol.HM_vec)
        A = np.vstack([np.ones(x.size),x]).T
        sol.beta0,sol.beta1 = np.linalg.lstsq(A,y,rcond=None)[0]
        if print == True :
            print("Beta0 = " + sol.beta0)
            print("Beta1 = " + sol.beta1)
    
    
    def estimate(self, alpha=np.nan, sigma=np.nan ):
        """ estimate alpha and sigma """

        par = self.par
        sol = self.sol

        min_var = np.nan
        A = np.nan
        S = np.nan
        i=1

        for alp  in enumerate(alpha):

            print ("alp: "+str(alp))

            par.alpha = alp[-1]

            print("par.alpha = "+str(par.alpha))

            for sig in enumerate(sigma):


                print ("sig: "+str(sig))
                par.sigma = sig[-1]

                print("par.sigma = "+str(par.sigma))

                self.solve_wF_vec
                self.run_regression(print==True)

                var = (par.beta0_target-sol.beta0)**2 + (par.beta1_target-sol.beta1)**2
                print(var)

                if min_var is np.nan:
                    A = par.alpha
                    S = par.sigma 
                    min_var = var
                    print("solution updated")
                    
                if var < min_var :
                    A = par.alpha
                    S = par.sigma 
                    min_var = var
                    print("solution updated")
                    
                print("end of loop iteration "+str(i))
                i+=1


        return A, S, min_var







        #Temporary/unfinished function: 
    def minimize_variance(self, alpha=[] , sigma=[] ):
        #FindS alpha and sigma that minimizes combined variance of the betas


        par = self.par
        sol = self.sol

        low_var = np.Infinity

        #Loop for every alpha variable
        for i in range(len(alpha)):

            #Loop for every sigma variable
            for j in range(len(sigma)):
             
             par.alpha = alpha[i]
             par.sigma = sigma[j]


             #?
             inauguralproject.solve

             #Calculate the variance

             #need some way to bring the beta values from regression function?
             tot_var = (sol.beta0-par.beta0_target)**2+(sol.beta1-par.beta1_target)**2

             #check if smaller
             if (tot_var<low_var):
                     low_var = tot_var
                     min_alpha = alpha(i)
                     min_sigma = sigma(j)
                     
        

        #Return alpha, sigma and lowest variance
        return min_alpha , min_sigma, low_var
    