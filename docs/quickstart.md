# Quickstart

## Basic example

```python
from plotcdf.discrete.plot import RV

rv = RV(
    support=[0, 1, 2, 3],
    prob=[0.1, 0.2, 0.3, 0.4],
    is_pmf=True,
)

fig_pmf, ax_pmf = rv.plot_pmf(rv_name="X", graph_name="example", save=False)
fig_cdf, ax_cdf = rv.plot_cdf(rv_name="X", graph_name="example", save=False)
fig_q, ax_q = rv.plot_quantile(rv_name="X", graph_name="example", save=False)
```

## Working with CDF input

Set `is_pmf=False` when `prob` is already cumulative:

```python
rv = RV(
    support=[0, 1, 2, 3],
    prob=[0.1, 0.4, 0.8, 1.0],
    is_pmf=False,
)
```

Internally, the class converts CDF input to PMF for unified validation.

## Tails and truncated support

If your support is truncated (for example, left or right tail omitted), set:

- `complete_left=False`
- `complete_right=False`

This affects warning behavior and plot rendering for edge segments.

For more complete, distribution-specific samples, see [Examples](examples.md).
