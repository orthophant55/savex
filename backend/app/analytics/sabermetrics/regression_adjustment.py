"""Regression-to-the-mean adjustments for sabermetric rate statistics.

Small sample sizes make observed rates unreliable predictors of true talent.
Bayesian shrinkage towards the league average — weighted by a prior proportional
to the stabilization point — produces more stable estimates.

Key concept: stabilization point (also called "reliability point") is the
sample size at which a stat is 50% signal and 50% noise.  Below that threshold
the league average is a better estimate; above it the observed rate dominates.

NOTE: All stabilization points here are MLB-based estimates used as KBO
placeholders.  KBO-specific points should be derived from split-half reliability
analysis on KBO career data.
"""


# ---------------------------------------------------------------------------
# Reliability (signal ratio)
# ---------------------------------------------------------------------------


def calculate_reliability(
    sample_size: float, stabilization_point: float
) -> float:
    """Calculate the reliability (signal proportion) of an observed rate stat.

    reliability = sample_size / (sample_size + stabilization_point)

    At exactly the stabilization point, reliability = 0.50 (50% signal).
    As sample_size → ∞, reliability → 1.0 (full confidence in observed rate).

    Approximate stabilization points (PA-based, MLB estimates as placeholder):
      AVG   ~ 500 PA
      OBP   ~ 500 PA
      K%    ~  80 PA
      BB%   ~ 120 PA
      HR/FB ~ 300 PA

    Args:
        sample_size:        Observed sample size (e.g. PA, BF).
        stabilization_point: The sample size at which reliability = 0.5.

    Returns:
        Reliability in [0, 1], rounded to 3 decimal places.
        Returns 0.0 if the denominator is <= 0.
    """
    denominator = sample_size + stabilization_point
    if denominator <= 0:
        return 0.0
    return round(sample_size / denominator, 3)


# ---------------------------------------------------------------------------
# Bayesian shrinkage
# ---------------------------------------------------------------------------


def shrink_rate_to_league_average(
    observed_rate: float,
    league_average: float,
    sample_size: float,
    prior_strength: float,
) -> float:
    """Shrink an observed rate towards the league average using a Beta prior.

    adjusted = (observed_rate * sample_size + league_average * prior_strength)
               / (sample_size + prior_strength)

    prior_strength acts as the stabilization point: when sample_size equals
    prior_strength, the adjusted rate is the midpoint between observed and league.

    Args:
        observed_rate:  The raw observed rate (e.g. 0.310 for AVG).
        league_average: League-average rate for the same stat.
        sample_size:    Observed sample size (e.g. AB for AVG, PA for BB%).
        prior_strength: Weight given to the league average (stabilization point).

    Returns:
        Bayesian-adjusted rate, rounded to 3 decimal places.
    """
    adjusted = (
        observed_rate * sample_size + league_average * prior_strength
    ) / (sample_size + prior_strength)
    return round(adjusted, 3)


# ---------------------------------------------------------------------------
# Stat-specific wrappers
# ---------------------------------------------------------------------------


def calculate_regression_adjusted_avg(
    h: float,
    ab: float,
    league_avg: float = 0.280,
    prior_strength: float = 100.0,
) -> float:
    """Calculate regression-adjusted batting average.

    Uses Bayesian shrinkage towards the KBO league average (~0.280 placeholder).

    Args:
        h:             Hits.
        ab:            At-bats.
        league_avg:    League-average batting average (default 0.280 KBO placeholder).
        prior_strength: Stabilization prior weight in AB units (default 100).

    Returns:
        Regression-adjusted AVG rounded to 3 decimal places.
        Falls back to league_avg if ab == 0.
    """
    observed_avg = h / ab if ab > 0 else league_avg
    return shrink_rate_to_league_average(
        observed_avg, league_avg, ab, prior_strength
    )


def calculate_regression_adjusted_ops(
    observed_ops: float,
    league_ops: float = 0.750,
    pa: float = 0.0,
    prior_strength: float = 200.0,
) -> float:
    """Calculate regression-adjusted OPS.

    Uses Bayesian shrinkage towards the KBO league OPS (~0.750 placeholder).

    Args:
        observed_ops:  Observed OPS value.
        league_ops:    League-average OPS (default 0.750 KBO placeholder).
        pa:            Plate appearances (sample size).
        prior_strength: Stabilization prior weight in PA units (default 200).

    Returns:
        Regression-adjusted OPS rounded to 3 decimal places.
    """
    return shrink_rate_to_league_average(
        observed_ops, league_ops, pa, prior_strength
    )


# ---------------------------------------------------------------------------
# Approximate confidence interval (Wald interval)
# ---------------------------------------------------------------------------


def calculate_confidence_interval_placeholder(
    rate: float, sample_size: float
) -> tuple[float, float]:
    """Compute an approximate 95% confidence interval for a proportion (Wald).

    CI = rate ± 1.96 * sqrt(rate * (1 - rate) / n)

    NOTE: The Wald interval is known to have poor coverage near 0 and 1.
    A Wilson score or Clopper-Pearson interval would be more accurate.
    This function is a placeholder for development use.

    Args:
        rate:        Observed proportion in [0, 1].
        sample_size: Sample size n.

    Returns:
        (lower, upper) tuple clamped to [0.0, 1.0], each rounded to 3 places.
        Returns (rate, rate) if sample_size <= 0.
    """
    if sample_size <= 0:
        return (rate, rate)
    import math
    margin = 1.96 * math.sqrt(rate * (1.0 - rate) / sample_size)
    lower = max(0.0, rate - margin)
    upper = min(1.0, rate + margin)
    return (round(lower, 3), round(upper, 3))
