import numpy as np
from scipy.optimize import minimize

def refined_global_optimizer(bounds, tolerance, warmup_iterations, max_iterations):
    best_solution = None

    for k in range(max_iterations):
        # Random initialization
        x_k = np.random.uniform(bounds[0], bounds[1], size=len(bounds))

        if k < warmup_iterations:
            # Skip to step E during warm-up iterations
            x_k_star = minimize(objective_function, x_k, method='BFGS', tol=tolerance).x
        else:
            # Calculate chi^k
            chi_k = 0.5 * 2 / (1 + np.exp((k - warmup_iterations) / 100))

            # Refined initialization
            x_k0 = chi_k * x_k + (1 - chi_k) * best_solution

            # Optimization run with refined initialization
            x_k_star = minimize(objective_function, x_k0, method='BFGS', tol=tolerance).x

        if best_solution is None or objective_function(x_k_star) < objective_function(best_solution):
            # Update the best solution
            best_solution = x_k_star

        if objective_function(best_solution) < tolerance:
            # Stopping condition
            break

    return best_solution

def objective_function(x):
    # Objective function to be maximized
    return -((x[0]**2 + x[1]**2) - np.cos(0.1 * x[0]) - np.cos(0.2 * x[1]))

# Set the optimization settings
bounds = [np.array([-600, -600]), np.array([600, 600])]
tolerance = 1e-8
warmup_iterations = 10
max_iterations = 1000

# Run the refined global optimizer
result = refined_global_optimizer(bounds, tolerance, warmup_iterations, max_iterations)

# Print the result
print("Optimal solution:", result)






# Question 2 def
# write your code here

def profit_function(kappa, eta, w):
    return ((kappa * (1 - eta)/w)**(1-eta))