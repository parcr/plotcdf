import sys
import os
from scipy.stats import binom
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from plotcdf.discrete import plot

# Get the name of the main file to use in the output file names
main_file = getattr(sys.modules.get("__main__"), "__file__", None)
main_name = os.path.basename(main_file) if main_file else 'output'
# remove the extension from the main file name
main_name = os.path.splitext(main_name)[0] if main_name else 'output'


# the output foder is set to examples/binomial_output
output_folder = os.path.join(os.path.dirname(__file__), main_name + '_output')
os.makedirs(output_folder, exist_ok=True)
rv_name = 'binomial'

n=5
p=0.5
rv=binom(n=n, p=p)
support=range(int(rv.ppf(0))+1, int(rv.ppf(1)) + 1)
prob=rv.pmf(support)
print(f'Support: {list(support)}')
print(f'Probabilities: {list(prob)}')
prob_sum=prob.cumsum()
print(f'Cumulative Probabilities: {list(prob_sum)}')

binomial = plot.RV(support=support, prob=prob)
binomial = plot.RV(support=support, prob=prob_sum, is_pmf=False)

fig_cdf, ax_cdf=binomial.plot_cdf(rv_name=rv_name, save=False)
fig_cdf.savefig(os.path.join(output_folder, f'{rv_name}_cdf.png'), dpi=300)

fig_pmf, ax_pmf=binomial.plot_pmf(rv_name=rv_name, save=False)
fig_pmf.savefig(os.path.join(output_folder, f'{rv_name}_pmf.png'), dpi=300)

fig_qt, ax_qt=binomial.plot_quantile(rv_name=rv_name, save=False)
fig_qt.savefig(os.path.join(output_folder, f'{rv_name}_quantile.png'), dpi=300)