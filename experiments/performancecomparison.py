

#!/usr/bin/env python

import time
import numpy as np

# We'll create a large array of x-values
N = 100_000
x_vals = np.linspace(-5, 5, N)
mu_vals = np.linspace(-5, 5, N)


# Just to show the shape
print(f"Number of x-values: {len(x_vals)}\n")


# ----------------------------------------------------------------------------
# 1) statistics.NormalDist
# ----------------------------------------------------------------------------
print("=== 1) statistics.NormalDist ===")

# We measure from the creation of the NormalDist object all the way
start = time.time()

from statistics import NormalDist
for x, mu in zip(x_vals,mu_vals):
    _ = NormalDist(mu=mu, sigma=1).pdf(x)

end = time.time()
stats_time = end - start
print(f"Total time (setup + PDF eval): {stats_time:.6f} seconds.\n")


# ----------------------------------------------------------------------------
# 2) scipy.stats.norm
# ----------------------------------------------------------------------------
print("=== 2) scipy.stats.norm ===")


from scipy.stats import norm
start = time.time()
for x, mu in zip(x_vals,mu_vals):
    _ = norm(loc=mu, scale=1).pdf(x)

end = time.time()
scipy_time = end - start
print(f"Total time (setup + PDF eval): {scipy_time:.6f} seconds.\n")



# ----------------------------------------------------------------------------
# 4) Sympy (symbolic -> lambdify)
# ----------------------------------------------------------------------------
print("=== 4) Sympy (symbolic -> lambdify) ===")

import sympy
from sympy import lambdify

x_sym = sympy.Symbol('x', real=True)
mu_sym = sympy.Symbol('mu', real=True)
sigma_sym = sympy.Symbol('sigma', real=True, positive=True)

expr = (1/(sympy.sqrt(2*sympy.pi)*sigma_sym)
        * sympy.exp(-((x_sym - mu_sym)**2)/(2*sigma_sym**2)))

# Create a numeric function via lambdify
pdf_sympy_func = lambdify((x_sym, mu_sym, sigma_sym), expr, 'numpy')


start = time.time()

# Evaluate on array
for x,mu in zip(x_vals,mu_vals):
    pdf_sympy = pdf_sympy_func(x, mu, 1)

end = time.time()
sympy_time = end - start
print(f"Total time (symbol creation + lambdify + PDF eval): {sympy_time:.6f} seconds.\n")


# ----------------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------------
print("=== Summary of Timings (seconds) ===")
print(f"  statistics.NormalDist : {stats_time:.6f}")
print(f"  scipy.stats.norm      : {scipy_time:.6f}")
print(f"  Sympy (lambdify)      : {sympy_time:.6f}")
