import os
import sys

import matplotlib.pyplot as plt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from plotcdf.discrete import plot
import scipy.stats as stat

x = ['hj', 2, 4]
p = (.3, .5, .2)
discrete_rv = plot.RV(x, p)

x = [1, 2, 4]
p = ('v', .5, .2)
discrete_rv = plot.RV(x, p)

x = [1, 2, 4]
p = (.3, .5, .2)
sp=(.3, .8, 1.)
discrete_rv = plot.RV(x, sp, is_pmf=False)


x = (0, 2, 4)
p = (.3, .5, .2)
sp = ['v', .8, 1]
discrete_rv = plot.RV(x, sp, is_pmf=False)


x = (0, 2, 4)
p = (.3, .5, .2)
sp = [.3, .8, 1.1]
discrete_rv = plot.RV(x, sp, is_pmf=False)

x = (0, 2, 4)
p = (.3, .5, .2)
sp = [.3, .8, 1]
discrete_rv = plot.RV(x, p)
print(discrete_rv.support)
print(discrete_rv.prob)
discrete_rv.plot_cdf()


x = (0, 1, 2, 3, 4)
p = (1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5)
sp = (1 / 5, 2 / 5, 3 / 5, 4 / 5, 5 / 5)
discrete_rv = plot.RV(x, p)
print(discrete_rv.support)
print(discrete_rv.prob)
discrete_rv.plot_cdf()

n = 10
x = list(range(n + 1))
my_dist = stat.binom(n, .5)
p = my_dist.pmf(x)*.95

# discrete_rv = plot.RV(support=x, prob=p, complete_left=True, complete_right=True, max_tol=1e-12)
discrete_rv = plot.RV(x, p)
print(sum(discrete_rv.prob))
