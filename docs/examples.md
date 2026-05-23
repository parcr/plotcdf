# Examples

This page documents all runnable Python scripts in `examples/`.

## Run the scripts

From the repository root:

```bash
python examples/bernoulli.py
python examples/binomial.py
python examples/poisson.py
```

Each script writes plots into its own output directory:

- `examples/bernoulli_output/`
- `examples/binomial_output/`
- `examples/poisson_output/`

## API links

Jump to the API reference for objects used in these examples:

- `plotcdf.discrete.plot.RV`: [RV class in API reference](api.md)
- Methods used in all scripts: `plot_pmf`, `plot_cdf`, `plot_quantile`

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

## `examples/binomial.py`

Goal: build a Binomial($n=5$, $p=0.5$) model using SciPy probabilities and visualize all three functions.

Key implementation notes:

- Computes finite integer support from `ppf(0)` and `ppf(1)`.
- Prints support, PMF values, and cumulative probabilities.
- Constructs `RV` once from PMF and once from CDF to illustrate both paths.

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

!!! example "Binomial PMF"
	![Binomial PMF](assets/examples/binomial_pmf.png)

!!! example "Binomial CDF"
	![Binomial CDF](assets/examples/binomial_cdf.png)

!!! example "Binomial quantile"
	![Binomial quantile](assets/examples/binomial_quantile.png)

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
