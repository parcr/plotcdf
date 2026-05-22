# API Reference

## Class `RV`

`RV` models a discrete random variable and provides PMF/CDF/quantile plotting.

### Constructor

```python
RV(
    support,
    prob,
    is_pmf=True,
    complete_left=True,
    complete_right=True,
    max_tol=1e-12,
)
```

Parameters:

- `support`: iterable of support values (mass points)
- `prob`: PMF values if `is_pmf=True`; CDF values if `is_pmf=False`
- `is_pmf`: interpretation of `prob`
- `complete_left`, `complete_right`: whether tails are complete
- `max_tol`: tolerance used in probability sum checks

### Properties

- `support`: validated support array
- `prob`: validated PMF array
- `cum_prob`: CDF array
- `is_pmf`: whether input was PMF
- `tol`: tolerance value
- `warning`: warning text if probability sum differs from 1 by more than `tol`

### Conversion helpers

- `RV.from_pmf_to_cdf(probs)`
- `RV.from_cdf_to_pmf(cum_probs)`

### Plotting methods

All plotting methods return `(figure, axes)` and accept optional style dictionaries.

- `plot_pmf(...)`
- `plot_cdf(...)`
- `plot_quantile(...)`

Style dictionaries are copied internally, so caller dictionaries are not mutated.

If `save=True`, output files are saved as:

- `<graph_name>_pmf_<rv_name>.png`
- `<graph_name>_cdf_<rv_name>.png`
- `<graph_name>_quantile_<rv_name>.png`

## Validation message constants

Validation text constants are defined in `plotcdf.discrete.messages`.

See [Validation Messages](messages.md) for the grouped list and usage context.

## System utilities

Platform helper functions are defined in `plotcdf.library.systems`.

See [System Utilities](systems.md) for available helpers and usage.
