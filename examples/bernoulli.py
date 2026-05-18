import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from plotcdf.discrete import plot

bernoulli = plot.RV(support=[0, 1], prob=[.5, .5])

bernoulli = plot.RV(support=[0, 1], prob=[.5, 1.], is_pmf=False)

bernoulli.plot_cdf()

bernoulli.plot_pmf()

print()