# Validation Messages

The module [plotcdf/discrete/messages.py](https://github.com/parcr/plotcdf/blob/master/plotcdf/discrete/messages.py) centralizes string constants used by input checks.

Keeping these strings in one place ensures:

- consistent validation text across modules
- easier maintenance when wording changes
- a single source for user-facing diagnostics

## Exported constants

### Support shape and cardinality

- `support_dim`
- `needs_array`
- `needs_1_dim_array`
- `needs_more_than_1`

### Probability and compatibility

- `needs_all_positive`
- `needs_lesser_1`
- `needs_same_length`
- `needs_same_size`

### Tolerance and tails

- `sum_of_prob`
- `tolerance`
- `tails`

### Input mode

- `is_pmf`

## Where they are used

These constants are consumed primarily by checks in `plotcdf.discrete.checks` and then surfaced through exceptions and warnings raised by `plotcdf.discrete.plot.RV`.
