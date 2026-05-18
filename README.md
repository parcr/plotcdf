# plotcdf

`plotcdf` provides utilities to model and visualize discrete random variables.

The package validates support and probability inputs and generates plots for:

- Probability mass functions (PMF)
- Cumulative distribution functions (CDF)
- Quantile functions

## Features

- Input validation for support values, probabilities, tolerance, and tail flags
- Conversion helpers between PMF and CDF representations
- Configurable Matplotlib styles for points, lines, and grids

## Usage

Create an `RV` object with support and probabilities, then call a plotting method:

```python
from plotcdf.discrete.plot import RV

rv = RV(
	support=[0, 1, 2, 3],
	prob=[0.1, 0.2, 0.3, 0.4],
	is_pmf=True,
)

rv.plot_pmf(rv_name="X", graph_name="example", save=False)
rv.plot_cdf(rv_name="X", graph_name="example", save=False)
rv.plot_quantile(rv_name="X", graph_name="example", save=False)
```

## Notes

- `prob` can represent PMF values (`is_pmf=True`) or CDF values (`is_pmf=False`).
- Plot methods return a `(figure, axes)` tuple for further customization.
