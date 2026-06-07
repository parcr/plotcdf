# Examples

This page documents all runnable Python scripts in `examples/`.

## Jump to an example

- [examples/bernoulli.py](#example-bernoulli)
- [examples/binomial.py](#example-binomial)
- [examples/binomial_2.py](#example-binomial-2)
- [examples/geometric.py](#example-geometric)
- [examples/negativeBinomial.py](#example-negative-binomial)
- [examples/poisson.py](#example-poisson)

## Run the scripts

From the repository root:

```bash
python examples/bernoulli.py
python examples/binomial.py
python examples/binomial_2.py
python examples/geometric.py
python examples/negativeBinomial.py
python examples/poisson.py
```

Each script writes plots into its own output directory:

- `examples/bernoulli_output/`
- `examples/binomial_output/`
- `examples/binomial_2_output/`
- `examples/geometric_output/`
- `examples/negativeBinomial_output/`
- `examples/poisson_output/`

## API links

Jump to the API reference for objects used in these examples:

- `plotcdf.discrete.plot.RV`: [RV class in API reference](api.md)
- Methods used in all scripts: `plot_pmf`, `plot_cdf`, `plot_quantile`

<a id="example-bernoulli"></a>

## `examples/bernoulli.py`

Goal: show a two-point Bernoulli random variable and generate PMF, CDF, and quantile plots.

Key implementation notes:

- Demonstrates both input modes: PMF (`is_pmf=True`, default) and CDF (`is_pmf=False`).
- Saves figures with deterministic names: `bernoulli_pmf.png`, `bernoulli_cdf.png`, `bernoulli_quantile.png`.
- Shows figures only when Matplotlib runs with an interactive backend.

Annotated core:

```python
p = 0.5

# PMF input: [P(X=0), P(X=1)]
bernoulli_from_pmf = plot.RV(support=[0, 1], prob=[1 - p, p])

# Equivalent CDF input: [F(0), F(1)]
bernoulli = plot.RV(support=[0, 1], prob=[1 - p, 1.0], is_pmf=False)
```

!!! example "Bernoulli PMF"
	![Bernoulli PMF](assets/examples/bernoulli_pmf.png)

!!! example "Bernoulli CDF"
	![Bernoulli CDF](assets/examples/bernoulli_cdf.png)

!!! example "Bernoulli quantile"
	![Bernoulli quantile](assets/examples/bernoulli_quantile.png)

<a id="example-binomial"></a>

### Binomial comparison at a glance

| Script | Plot style | Distinguishing behavior | Best use |
| --- | --- | --- | --- |
| `examples/binomial.py` | Standard | Uses library defaults and focuses on the core PMF/CDF/quantile workflow | Reference output and baseline checks |
| `examples/binomial_2.py` | Fancy | Adds custom CDF marker styling and scientific-notation formatting for improved presentation | Presentation-ready plots and style experimentation |

## `examples/binomial.py`

Goal: provide the baseline Binomial($n=5$, $p=0.5$) workflow and default plotting style.

Key implementation notes:

- Computes finite integer support from `ppf(0)` and `ppf(1)`.
- Prints support, PMF values, and cumulative probabilities.
- Constructs `RV` once from PMF and once from CDF to illustrate both input modes.
- Uses default plotting styles with no custom marker/color overrides.

Use this script when you want a clean reference result.

Annotated core:

```python
rv = binom(n=5, p=0.5)

# Finite support bounds for binomial are exact.
support = range(int(rv.ppf(0)) + 1, int(rv.ppf(1)) + 1)
prob = rv.pmf(support)
prob_sum = prob.cumsum()

binomial_from_pmf = plot.RV(support=support, prob=prob)
binomial = plot.RV(support=support, prob=prob_sum, is_pmf=False)
```

!!! example "Binomial (standard) PMF"
	![Binomial standard PMF](assets/examples/binomial_standard_pmf.png)

!!! example "Binomial (standard) CDF"
	![Binomial standard CDF](assets/examples/binomial_standard_cdf.png)

!!! example "Binomial (standard) quantile"
	![Binomial standard quantile](assets/examples/binomial_standard_quantile.png)

<a id="example-binomial-2"></a>

## `examples/binomial_2.py`

Goal: show a fancy-styled Binomial($n=5$, $p=0.5$) variant with custom visuals and axis formatting.

Key implementation notes:

- Derives support and probabilities from SciPy exactly like `binomial.py`.
- Passes custom style dictionaries to `plot_cdf` for colored markers.
- Applies scientific notation formatting to improve readability of dense tick labels.

Use this script when you want the same distribution with more expressive presentation.

Annotated core:

```python
rv = binom(n=5, p=0.5)
support = range(int(rv.ppf(0)) + 1, int(rv.ppf(1)) + 1)
prob = rv.pmf(support)
prob_sum = prob.cumsum()

fig_cdf, _ = binomial.plot_cdf(
    rv_name=rv_name,
    save=False,
    right_points={"markerfacecolor": "red", "markeredgecolor": "orange", "markersize": 12},
    left_points={"markerfacecolor": "green", "markeredgecolor": "blue", "markersize": 12},
)
```

!!! example "Binomial 2 (fancy) PMF"
	![Binomial fancy PMF](assets/examples/binomial_fancy_pmf.png)

!!! example "Binomial 2 (fancy) CDF"
	![Binomial fancy CDF](assets/examples/binomial_fancy_cdf.png)

!!! example "Binomial 2 (fancy) quantile"
	![Binomial fancy quantile](assets/examples/binomial_fancy_quantile.png)

<a id="example-geometric"></a>

## `examples/geometric.py`

Goal: document truncated-support workflows for the Geometric distribution.

Key implementation notes:

- Case 1 uses only right-tail truncation (`complete_right=False`).
- Case 2 uses both-tail truncation (`complete_left=False`, `complete_right=False`).
- Builds support from quantile bounds and passes PMF/CDF into `RV`.

Annotated core:

```python
rv = geom(p=0.5)

# Right tail truncated.
support, prob, prob_sum = _summarize_support(rv, lower_q=0.0, upper_q=0.95)
geometric_rv = plot.RV(support=support, prob=prob_sum, is_pmf=False, complete_right=False)

# Both tails truncated.
support, prob, prob_sum = _summarize_support(rv, lower_q=0.25, upper_q=0.995)
geometric_rv = plot.RV(
    support=support,
    prob=prob_sum,
    is_pmf=False,
    complete_left=False,
    complete_right=False,
)
```

!!! example "Geometric PMF (incomplete right tail)"
	![Geometric PMF](assets/examples/geometric_pmf.png)

!!! example "Geometric CDF (incomplete right tail)"
	![Geometric CDF](assets/examples/geometric_cdf.png)

!!! example "Geometric quantile (incomplete right tail)"
	![Geometric quantile](assets/examples/geometric_quantile.png)

!!! example "Geometric PMF (both tails incomplete)"
	![Geometric PMF truncated both tails](assets/examples/geometric_2_pmf.png)

!!! example "Geometric CDF (both tails incomplete)"
	![Geometric CDF truncated both tails](assets/examples/geometric_2_cdf.png)

!!! example "Geometric quantile (both tails incomplete)"
	![Geometric quantile truncated both tails](assets/examples/geometric_2_quantile.png)

<a id="example-negative-binomial"></a>

## `examples/negativeBinomial.py`

Goal: document truncated-support workflows for the Negative Binomial distribution.

Key implementation notes:

- Uses `scipy.stats.nbinom` to compute support window and probabilities.
- Case 1 truncates only the right tail.
- Case 2 truncates both tails.

Annotated core:

```python
rv = nbinom(5, 0.5)

# Right tail truncated.
support, prob, prob_sum = _summarize_support(rv, lower_q=0.0, upper_q=0.95)
negative_binomial_rv = plot.RV(support=support, prob=prob_sum, is_pmf=False, complete_right=False)

# Both tails truncated.
support, prob, prob_sum = _summarize_support(rv, lower_q=0.25, upper_q=0.995)
negative_binomial_rv = plot.RV(
    support=support,
    prob=prob_sum,
    is_pmf=False,
    complete_left=False,
    complete_right=False,
)
```

!!! example "Negative Binomial PMF (incomplete right tail)"
	![Negative Binomial PMF](assets/examples/negative_binomial_pmf.png)

!!! example "Negative Binomial CDF (incomplete right tail)"
	![Negative Binomial CDF](assets/examples/negative_binomial_cdf.png)

!!! example "Negative Binomial quantile (incomplete right tail)"
	![Negative Binomial quantile](assets/examples/negative_binomial_quantile.png)

!!! example "Negative Binomial PMF (both tails incomplete)"
	![Negative Binomial PMF truncated both tails](assets/examples/negative_binomial_2_pmf.png)

!!! example "Negative Binomial CDF (both tails incomplete)"
	![Negative Binomial CDF truncated both tails](assets/examples/negative_binomial_2_cdf.png)

!!! example "Negative Binomial quantile (both tails incomplete)"
	![Negative Binomial quantile truncated both tails](assets/examples/negative_binomial_2_quantile.png)

<a id="example-poisson"></a>

## `examples/poisson.py`

Goal: document truncated-support workflows for distributions with infinite tails.

Key implementation notes:

- Uses quantile bounds to build finite support windows.
- Case 1: right-tail truncation only (`complete_right=False`).
- Case 2: both-tail truncation (`complete_left=False`, `complete_right=False`).

Annotated core:

```python
rv = poisson(mu=3)

# Right tail truncated: keep mass up to the 95th percentile.
support, prob, prob_sum = _summarize_support(rv, lower_q=0.0, upper_q=0.95)
poisson_rv = plot.RV(support=support, prob=prob_sum, is_pmf=False, complete_right=False)

# Both tails truncated: drop very low and very high quantiles.
support, prob, prob_sum = _summarize_support(rv, lower_q=0.25, upper_q=0.995)
poisson_rv = plot.RV(
    support=support,
    prob=prob_sum,
    is_pmf=False,
    complete_left=False,
    complete_right=False,
)
```

!!! example "Poisson PMF (incomplete right tail)"
	![Poisson PMF](assets/examples/poisson_pmf.png)

!!! example "Poisson CDF (incomplete right tail)"
	![Poisson CDF](assets/examples/poisson_cdf.png)

!!! example "Poisson quantile (incomplete right tail)"
	![Poisson quantile](assets/examples/poisson_quantile.png)

!!! example "Poisson PMF (both tails incomplete)"
	![Poisson PMF truncated both tails](assets/examples/poisson_2_pmf.png)

!!! example "Poisson CDF (both tails incomplete)"
	![Poisson CDF truncated both tails](assets/examples/poisson_2_cdf.png)

!!! example "Poisson quantile (both tails incomplete)"
	![Poisson quantile truncated both tails](assets/examples/poisson_2_quantile.png)
