"""Binomial example for plotcdf.

This script derives support and probabilities from SciPy's binomial
distribution and renders PMF/CDF/quantile plots.
"""

import os
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from scipy.stats import binom

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from plotcdf.discrete import plot


def _build_output_folder() -> str:
	"""Create output directory based on script file name."""
	main_file = getattr(sys.modules.get("__main__"), "__file__", None)
	main_name = os.path.basename(main_file) if main_file else "output"
	main_name = os.path.splitext(main_name)[0] if main_name else "output"

	output_folder = os.path.join(os.path.dirname(__file__), f"{main_name}_output")
	os.makedirs(output_folder, exist_ok=True)
	return output_folder


def _show_if_interactive() -> None:
	"""Display figures only when a GUI backend is available."""
	if "agg" in plt.get_backend().lower():
		print("Matplotlib is using a non-interactive backend; skipping on-screen display.")
		return
	plt.show(block=True)


def main() -> None:
	output_folder = _build_output_folder()
	rv_name = "binomial"

	n = 5
	p = 0.5
	rv = binom(n=n, p=p)

	# For finite support distributions, ppf(0) and ppf(1) bound all masses.
	support = range(int(rv.ppf(0)) + 1, int(rv.ppf(1)) + 1)
	prob = rv.pmf(support)
	prob_sum = prob.cumsum()

	print(f"Support: {list(support)}")
	print(f"Probabilities: {list(prob)}")
	print(f"Cumulative Probabilities: {list(prob_sum)}")

	# Build from PMF and CDF to show both input modes.
	binomial_from_pmf = plot.RV(support=support, prob=prob)
	binomial = plot.RV(support=support, prob=prob_sum, is_pmf=False)

	fig_cdf, _ = binomial.plot_cdf(rv_name=rv_name, save=False, 
								right_points={'markerfacecolor': 'red', 'markeredgecolor': 'orange', 
					  'markersize': 12},
					  left_points={'markerfacecolor': 'green', 'markeredgecolor': 'blue', 
					  'markersize': 12})
	
	# Use Matplotlib's formatter for scientific notation on the y-axis.
	ax = fig_cdf.axes[0]
	formatter = ScalarFormatter(useMathText=True)
	formatter.set_scientific(True)
	formatter.set_powerlimits((0, 0))
	ax.yaxis.set_major_formatter(formatter)
	ax.tick_params(axis="y", labelrotation=0)
	for label in ax.get_yticklabels():
		label.set_ha("center")
	# Adjust layout to prevent label cutoff
	fig_cdf.tight_layout()
	fig_cdf.savefig(os.path.join(output_folder, f"{rv_name}_2_cdf.png"), dpi=300)

	fig_pmf, _ = binomial_from_pmf.plot_pmf(rv_name=rv_name, save=False)
	fig_pmf.savefig(os.path.join(output_folder, f"{rv_name}_2_pmf.png"), dpi=300)

	fig_qt, _ = binomial.plot_quantile(rv_name=rv_name, save=False)

	# Use Matplotlib's formatter for scientific notation on the x-axis.
	ax = fig_qt.axes[0]
	formatter = ScalarFormatter(useMathText=True)
	formatter.set_scientific(True)
	formatter.set_powerlimits((0, 0))
	ax.xaxis.set_major_formatter(formatter)
	ax.tick_params(axis="x", labelrotation=90)
	for label in ax.get_xticklabels():
		label.set_ha("center")

	# Adjust layout to prevent label cutoff
	fig_qt.tight_layout()
	fig_qt.savefig(os.path.join(output_folder, f"{rv_name}_2_quantile.png"), dpi=300)
	
	_show_if_interactive()


if __name__ == "__main__":
	main()