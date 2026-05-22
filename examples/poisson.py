import sys
import os
from scipy.stats import poisson
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from plotcdf.discrete import plot

# Get the name of the main file to use in the output file names
main_file = getattr(sys.modules.get("__main__"), "__file__", None)
main_name = os.path.basename(main_file) if main_file else 'output'
# remove the extension from the main file name
main_name = os.path.splitext(main_name)[0] if main_name else 'output'


# the output foder is set to examples/poisson_output
output_folder = os.path.join(os.path.dirname(__file__), main_name + '_output')
os.makedirs(output_folder, exist_ok=True)
rv_name = 'poisson'

mu=3
rv=poisson(mu=mu)
# in this case we've incomplete tails, so we need to adjust the support to include only a finite number of values. We can use the ppf function to find the support values that correspond to the cumulative probabilities of 0 and 1, and then create a range of integers between those values.
min_range=int(rv.ppf(0))+1 # this is the smallest integer value that has a non-zero probability
max_range=int(rv.ppf(.95)) + 1 # this is the largest integer value that has a non-zero probability


# Incomplete right tail, so we need to adjust the support to include only a finite number of values. We can use the ppf function to find the support values that correspond to the cumulative probabilities of 0 and 1, and then create a range of integers between those values.
support=range(min_range, max_range)
prob=rv.pmf(support)
print(f'Support: {list(support)}')
print(f'Probabilities: {list(prob)}')
prob_sum=prob.cumsum()
print(f'Cumulative Probabilities: {list(prob_sum)}')

poisson_rv = plot.RV(support=support, prob=prob, complete_right=False)
poisson_rv = plot.RV(support=support, prob=prob_sum, is_pmf=False, complete_right=False)

fig_cdf, ax_cdf=poisson_rv.plot_cdf(rv_name=rv_name, save=False)
fig_cdf.savefig(os.path.join(output_folder, f'{rv_name}_cdf.png'), dpi=300)

fig_pmf, ax_pmf=poisson_rv.plot_pmf(rv_name=rv_name, save=False)
fig_pmf.savefig(os.path.join(output_folder, f'{rv_name}_pmf.png'), dpi=300)

fig_qt, ax_qt=poisson_rv.plot_quantile(rv_name=rv_name, save=False)
fig_qt.savefig(os.path.join(output_folder, f'{rv_name}_quantile.png'), dpi=300)


# Incomplete left and right tails, so we need to adjust the support to include only a finite number of values. We can use the ppf function to find the support values that correspond to the cumulative probabilities of 0 and 1, and then create a range of integers between those values.
min_range=int(rv.ppf(.25))+1 # this is the smallest integer value that has a non-zero probability
max_range=int(rv.ppf(.995)) + 1 # this is the largest integer value that has a non-zero probability
support=range(min_range, max_range)
prob=rv.pmf(support)
print(f'Support: {list(support)}')
print(f'Probabilities: {list(prob)}')
prob_sum=prob.cumsum()
print(f'Cumulative Probabilities: {list(prob_sum)}')

poisson_rv = plot.RV(support=support, prob=prob, complete_left=False, complete_right=False)
poisson_rv = plot.RV(support=support, prob=prob_sum, is_pmf=False, complete_left=False, complete_right=False)

fig_cdf, ax_cdf=poisson_rv.plot_cdf(rv_name=rv_name, save=False)
fig_cdf.savefig(os.path.join(output_folder, f'{rv_name}_2_cdf.png'), dpi=300)

fig_pmf, ax_pmf=poisson_rv.plot_pmf(rv_name=rv_name, save=False)
fig_pmf.savefig(os.path.join(output_folder, f'{rv_name}_2_pmf.png'), dpi=300)

fig_qt, ax_qt=poisson_rv.plot_quantile(rv_name=rv_name, save=False)
fig_qt.savefig(os.path.join(output_folder, f'{rv_name}_2_quantile.png'), dpi=300)