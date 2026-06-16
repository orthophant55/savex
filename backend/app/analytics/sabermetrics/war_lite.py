"""WAR-Lite (Wins Above Replacement — Lightweight) module.

This module provides a simplified WAR framework suitable for the KBO platform
given current data availability constraints.  It is explicitly a skeleton:
several components are either rough approximations or hardcoded placeholders
pending richer data sources.

Architecture of WAR-Lite:
    WAR = (Batting Runs + Baserunning Runs + Fielding Runs
           + Pitching Runs - Replacement Runs) / Runs per Win

Component availability:
  - Batting runs (wRAA):       AVAILABLE — computed from wOBA.
  - Baserunning runs:          APPROXIMATION — from SB/CS only; no UBR/BsR.
  - Fielding runs:             PLACEHOLDER — returns 0.0; requires UZR/DRS data.
  - Pitching runs:             APPROXIMATION — from ERA vs. league ERA.
  - Replacement runs:          FORMULA — fixed runs-per-PA constant.

References:
  - openWAR (Baumer & Zimbalist 2014) for uncertainty methodology.
  - FanGraphs WAR for component definitions.
"""

# ---------------------------------------------------------------------------
# Module-level constant
# ---------------------------------------------------------------------------

REPLACEMENT_LEVEL_RUNS_PER_PA: float = -0.03
"""Runs per plate appearance below average for a replacement-level player.

A replacement-level player is expected to produce -0.03 runs per PA relative
to the league average.  This calibrates WAR so that replacement level ≈ 0 WAR.

TODO: Calibrate the KBO replacement level from KBO minor-league and call-up
data to reflect the actual KBO talent pool depth.
"""


# ---------------------------------------------------------------------------
# Batting component
# ---------------------------------------------------------------------------


def calculate_batting_runs(wraa: float) -> float:
    """Return batting runs above average (= wRAA directly).

    wRAA is already expressed in runs above average, so no transformation
    is needed.  This function exists for interface symmetry with other
    WAR components.

    Args:
        wraa: Weighted Runs Above Average (from woba.calculate_wraa).

    Returns:
        wraa unchanged.
    """
    return wraa


# ---------------------------------------------------------------------------
# Baserunning component
# ---------------------------------------------------------------------------


def calculate_baserunning_runs(
    sb: int, cs: int, sb_rate: float = 0.72
) -> float:
    """Estimate baserunning runs from stolen base data (rough approximation).

    Formula: (SB - 1.5 * CS) * 0.2

    This is a simplified proxy for full baserunning value (BsR / UBR).
    The coefficient 1.5 reflects that a CS is roughly 1.5× more costly than
    an SB is beneficial.  The scalar 0.20 converts the net SB count to runs.

    TODO: Proper BsR/UBR requires Statcast-equivalent baserunner tracking data
    (lead distance, route efficiency, takes/holds) not available in KBO public
    data.  Until then this approximation captures only SB/CS contribution.

    Args:
        sb:      Stolen bases.
        cs:      Caught stealing.
        sb_rate: Unused — reserved for future break-even rate adjustment.
                 Currently the formula does not use this parameter.

    Returns:
        Estimated baserunning runs, rounded to 2 decimal places.
    """
    # TODO: proper BsR/UBR requires Statcast-equivalent data
    return round((sb - 1.5 * cs) * 0.2, 2)


# ---------------------------------------------------------------------------
# Fielding component (placeholder)
# ---------------------------------------------------------------------------


def calculate_fielding_runs_placeholder(
    position: str, innings_played: float
) -> float:
    """Fielding runs placeholder — always returns 0.0.

    TODO: requires UZR/DRS data not available in KBO public data.
    A proper implementation would use:
      - UZR (Ultimate Zone Rating) for outfielders and infielders.
      - DRS (Defensive Runs Saved) as an alternative metric.
      - OAA (Outs Above Average) for Statcast-equivalent environments.
    All three require detailed batted-ball location and outcome data that is
    not currently available in the KBO public data pipeline.

    Args:
        position:       Fielding position (e.g. "CF", "SS", "C").
        innings_played: Innings in the field (for positional scarcity adjustment).

    Returns:
        0.0 always (placeholder).
    """
    # TODO: requires UZR/DRS data not available in KBO public data
    return 0.0


# ---------------------------------------------------------------------------
# Replacement level component
# ---------------------------------------------------------------------------


def calculate_replacement_runs(pa: float) -> float:
    """Calculate runs relative to replacement level for a given number of PA.

    replacement_runs = REPLACEMENT_LEVEL_RUNS_PER_PA * PA

    This is negative (a replacement player costs runs relative to average),
    so subtracting it in the WAR formula adds value back — players above
    replacement level produce positive WAR.

    Args:
        pa: Plate appearances.

    Returns:
        Replacement-level runs (negative number), rounded to 2 decimal places.
    """
    return round(REPLACEMENT_LEVEL_RUNS_PER_PA * pa, 2)


# ---------------------------------------------------------------------------
# Pitching component
# ---------------------------------------------------------------------------


def calculate_pitching_runs(
    era: float, league_era: float, innings_pitched: float
) -> float:
    """Estimate pitching runs above replacement (rough approximation).

    Formula:
        runs_above_avg = (league_ERA - ERA) / 9 * IP
        replacement_adjustment = 0.03 * IP * 3   # rough placeholder

    The replacement adjustment adds ~0.09 runs per inning to convert from
    above-average to above-replacement.  This constant is a rough placeholder
    (see calculate_replacement_runs for the batting equivalent).

    TODO: Refine using KBO-specific replacement level for pitchers and apply
    leverage adjustments for relievers (gmLI scaling).

    Args:
        era:             Pitcher's ERA.
        league_era:      League-average ERA.
        innings_pitched: Innings pitched.

    Returns:
        Estimated pitching runs above replacement, rounded to 1 decimal place.
    """
    runs_above_avg = (league_era - era) / 9 * innings_pitched
    replacement_adjustment = 0.03 * innings_pitched * 3  # rough placeholder
    return round(runs_above_avg + replacement_adjustment, 1)


# ---------------------------------------------------------------------------
# WAR-Lite aggregation
# ---------------------------------------------------------------------------


def calculate_war_lite(
    batting_runs: float,
    pitching_runs: float,
    baserunning_runs: float,
    fielding_runs: float,
    replacement_runs: float,
    runs_per_win: float = 10.0,
) -> float:
    """Calculate WAR-Lite from component runs values.

    WAR = (batting + pitching + baserunning + fielding - replacement_runs)
          / runs_per_win

    Note: replacement_runs is negative (cost of replacement production), so
    subtracting it increases WAR.  Alternatively: pass replacement_runs as a
    negative number, and this formula converts it correctly.

    runs_per_win ≈ 10 for a typical MLB/KBO run environment (~4–5 R/G per team).
    The exact value depends on the run environment: higher-scoring environments
    require more runs to win an additional game.

    TODO: Calibrate runs_per_win from KBO seasonal data.

    Args:
        batting_runs:      Batting runs above average (wRAA).
        pitching_runs:     Pitching runs above replacement.
        baserunning_runs:  Baserunning runs (approximate).
        fielding_runs:     Fielding runs (0.0 placeholder).
        replacement_runs:  Runs cost of replacement level (negative number).
        runs_per_win:      Run environment calibration (default 10.0).

    Returns:
        WAR-Lite rounded to 1 decimal place.
    """
    total_runs = (
        batting_runs
        + pitching_runs
        + baserunning_runs
        + fielding_runs
        - replacement_runs
    )
    if runs_per_win == 0:
        return 0.0
    return round(total_runs / runs_per_win, 1)


# ---------------------------------------------------------------------------
# Uncertainty interval placeholder
# ---------------------------------------------------------------------------


def calculate_war_uncertainty_interval_placeholder(
    war_lite: float,
) -> tuple[float, float]:
    """Return a rough ±1 win uncertainty interval for WAR-Lite.

    A full uncertainty quantification (openWAR bootstrap methodology) requires
    repeated simulation across all play outcomes.  This placeholder returns a
    fixed ±1 WAR interval — an empirical rule of thumb from FanGraphs / openWAR
    literature suggesting single-season WAR estimates carry ~±1 win uncertainty
    for typical playing-time samples.

    TODO: proper uncertainty from openWAR bootstrap methodology:
      1. Resample play-by-play data with replacement.
      2. Recompute WAR for each bootstrap sample.
      3. Report 2.5th and 97.5th percentile as the 95% CI.

    Args:
        war_lite: WAR-Lite point estimate.

    Returns:
        (lower, upper) = (war_lite - 1.0, war_lite + 1.0)
    """
    # TODO: proper uncertainty from openWAR bootstrap methodology
    return (war_lite - 1.0, war_lite + 1.0)
