"""Bernoulli example for plotcdf.

This script builds a Bernoulli random variable, generates PMF/CDF/quantile
plots, and saves them under `examples/bernoulli_output/`.
"""

import os
import sys

import matplotlib.pyplot as plt

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
	rv_name = "bernoulli"

	p = 0.5

	# Input as PMF values.
	bernoulli_from_pmf = plot.RV(support=[0, 1], prob=[1 - p, p])
	# Equivalent input as CDF values.
	bernoulli = plot.RV(support=[0, 1], prob=[1 - p, 1.0], is_pmf=False)

	fig_cdf, _ = bernoulli.plot_cdf(rv_name=rv_name, save=False)
	fig_cdf.savefig(os.path.join(output_folder, f"{rv_name}_cdf.png"), dpi=300)

	fig_pmf, _ = bernoulli_from_pmf.plot_pmf(rv_name=rv_name, save=False)
	fig_pmf.savefig(os.path.join(output_folder, f"{rv_name}_pmf.png"), dpi=300)

	fig_qt, _ = bernoulli.plot_quantile(rv_name=rv_name, save=False)
	fig_qt.savefig(os.path.join(output_folder, f"{rv_name}_quantile.png"), dpi=300)

	_show_if_interactive()


if __name__ == "__main__":
	main()
