"""Geometric example for plotcdf.

Demonstrates how to work with truncated support for distributions with infinite
tails by setting `complete_left` and `complete_right` appropriately.
"""

import os
import sys

import matplotlib.pyplot as plt
from scipy.stats import geom

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


def _summarize_support(rv, lower_q: float, upper_q: float):
	"""Build truncated support and return support, pmf, and cumulative sum."""
	min_range = int(rv.ppf(lower_q)) + 1
	max_range = int(rv.ppf(upper_q)) + 1
	support = range(min_range, max_range)
	prob = rv.pmf(support)
	prob_sum = prob.cumsum()
	return support, prob, prob_sum


def main() -> None:
	output_folder = _build_output_folder()
	rv_name = "geometric"

	p = 0.5
	rv = geom(p=p)

	# Case 1: right tail is truncated.
	support, prob, prob_sum = _summarize_support(rv, lower_q=0.0, upper_q=0.95)
	print(f"Support: {list(support)}")
	print(f"Probabilities: {list(prob)}")
	print(f"Cumulative Probabilities: {list(prob_sum)}")

	geometric_from_pmf = plot.RV(support=support, prob=prob, complete_right=False)
	geometric_rv = plot.RV(support=support, prob=prob_sum, is_pmf=False, complete_right=False)

	fig_cdf, _ = geometric_rv.plot_cdf(rv_name=rv_name, save=False)
	fig_cdf.savefig(os.path.join(output_folder, f"{rv_name}_cdf.png"), dpi=300)

	fig_pmf, _ = geometric_from_pmf.plot_pmf(rv_name=rv_name, save=False)
	fig_pmf.savefig(os.path.join(output_folder, f"{rv_name}_pmf.png"), dpi=300)

	fig_qt, _ = geometric_rv.plot_quantile(rv_name=rv_name, save=False)
	fig_qt.savefig(os.path.join(output_folder, f"{rv_name}_quantile.png"), dpi=300)

	# Case 2: both left and right tails are truncated.
	support, prob, prob_sum = _summarize_support(rv, lower_q=0.25, upper_q=0.995)
	print(f"Support: {list(support)}")
	print(f"Probabilities: {list(prob)}")
	print(f"Cumulative Probabilities: {list(prob_sum)}")

	geometric_from_pmf = plot.RV(
		support=support,
		prob=prob,
		complete_left=False,
		complete_right=False,
	)
	geometric_rv = plot.RV(
		support=support,
		prob=prob_sum,
		is_pmf=False,
		complete_left=False,
		complete_right=False,
	)

	fig_cdf, _ = geometric_rv.plot_cdf(rv_name=rv_name, save=False)
	fig_cdf.savefig(os.path.join(output_folder, f"{rv_name}_2_cdf.png"), dpi=300)

	fig_pmf, _ = geometric_from_pmf.plot_pmf(rv_name=rv_name, save=False)
	fig_pmf.savefig(os.path.join(output_folder, f"{rv_name}_2_pmf.png"), dpi=300)

	fig_qt, _ = geometric_rv.plot_quantile(rv_name=rv_name, save=False)
	fig_qt.savefig(os.path.join(output_folder, f"{rv_name}_2_quantile.png"), dpi=300)

	_show_if_interactive()


if __name__ == "__main__":
	main()