"""Pythagorean Win Expectancy module.

The Pythagorean expectation (Bill James, 1980s) estimates a team's expected
winning percentage from its runs scored (RS) and runs allowed (RA):

    W% = RS^x / (RS^x + RA^x)

The exponent x ≈ 2.0 in the original formula; the Pythagenpat variant
(Smyth/Patriot) uses x = (RS + RA) / G ^ 0.287 for a per-game adjustment.

A comparison of a team's actual wins vs. expected wins (Actual - Expected)
reveals whether a team has out- or under-performed its underlying run
differential, often due to performance in close games.

NOTE: PYTHAGOREAN_EXPONENT_KBO_PLACEHOLDER = 1.83 is a common baseball
estimate (from Pythagenport by Clay Davenport).  The true best-fit exponent
for KBO should be estimated from historical KBO data.
"""

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

PYTHAGOREAN_EXPONENT_DEFAULT: float = 2.0
"""Original Bill James Pythagorean exponent."""

PYTHAGOREAN_EXPONENT_KBO_PLACEHOLDER: float = 1.83
"""Common baseball Pythagenport estimate used as KBO placeholder.

TODO: Calibrate with historical KBO team data using:
    x = exp( mean( log(RS/RA) - log(W/L) ) )  [log5 regression]
or the Pythagenpat per-game adjustment.
"""


# ---------------------------------------------------------------------------
# Core Pythagorean win percentage
# ---------------------------------------------------------------------------


def calculate_pythagorean_wp(
    runs_scored: float,
    runs_allowed: float,
    exponent: float = PYTHAGOREAN_EXPONENT_DEFAULT,
) -> float:
    """Calculate Pythagorean expected winning percentage.

    Formula: RS^x / (RS^x + RA^x)

    Edge cases:
      - Both RS and RA are 0 → returns 0.5 (undefined; coin flip).
      - RS == 0, RA > 0        → returns 0.0 (team cannot win without scoring).
      - RS > 0, RA == 0        → returns 1.0 (team never allows a run).

    Args:
        runs_scored:  Total runs scored by the team.
        runs_allowed: Total runs allowed by the team.
        exponent:     Pythagorean exponent (default 2.0).

    Returns:
        Expected winning percentage in [0, 1], rounded to 3 decimal places.
    """
    if runs_scored == 0 and runs_allowed == 0:
        return 0.5
    if runs_scored == 0:
        return 0.0
    if runs_allowed == 0:
        return 1.0
    rs_exp = runs_scored ** exponent
    ra_exp = runs_allowed ** exponent
    return round(rs_exp / (rs_exp + ra_exp), 3)


# ---------------------------------------------------------------------------
# Expected wins
# ---------------------------------------------------------------------------


def calculate_expected_wins(pythagorean_wp: float, games: int) -> float:
    """Calculate expected wins from Pythagorean win percentage.

    Args:
        pythagorean_wp: Pythagorean winning percentage (0–1).
        games:          Total games played.

    Returns:
        Expected wins rounded to 1 decimal place.
    """
    return round(pythagorean_wp * games, 1)


# ---------------------------------------------------------------------------
# Actual minus expected wins
# ---------------------------------------------------------------------------


def calculate_actual_minus_expected_wins(
    actual_wins: int, expected_wins: float
) -> float:
    """Calculate the difference between actual and Pythagorean expected wins.

    A positive value means the team won more games than expected (often due
    to a strong bullpen or luck in close games).  A negative value suggests
    regression candidates.

    Args:
        actual_wins:   Actual win total.
        expected_wins: Pythagorean expected wins (from calculate_expected_wins).

    Returns:
        actual_wins - expected_wins, rounded to 1 decimal place.
    """
    return round(actual_wins - expected_wins, 1)


# ---------------------------------------------------------------------------
# Exponent estimation placeholder
# ---------------------------------------------------------------------------


def estimate_pythagorean_exponent_placeholder(
    team_results: list[dict],
) -> float:
    """Placeholder function for estimating the Pythagorean exponent.

    Always returns 1.83 (common Pythagenpat / Pythagenport estimate).

    TODO: Implement actual estimation using:
        For each team-season, compute log(W/L) / log(RS/RA).
        The best-fit exponent is the mean (or OLS estimate) across many
        team-seasons.  Run this on KBO historical team data (seasons 2010+)
        to get a KBO-specific exponent.

    Args:
        team_results: List of dicts with keys:
                        "runs_scored" (int), "runs_allowed" (int), "won" (bool).
                      Not used in this placeholder; included for future interface
                      compatibility.

    Returns:
        1.83 always (placeholder).
    """
    # TODO: actual estimation uses log(W/L) / log(RS/RA) regression
    return 1.83
