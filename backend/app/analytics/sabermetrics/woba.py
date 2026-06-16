"""Weighted On-Base Average (wOBA) and related run-value metrics.

wOBA scales each plate appearance outcome by its empirical run value, producing
a rate stat that is both on the OBP scale and linearly related to run scoring.
wRAA and wRC chain from wOBA to give context-free run contributions.
wRC+ normalises wRC for park and league, making it the single best all-in-one
offensive rate stat in this module.

NOTE: All weights here are MLB FanGraphs 2024 values used as KBO placeholders.
KBO-specific wOBA weights require regression on KBO linear weights / run
expectancy derived from actual KBO play-by-play data.
See: https://www.fangraphs.com/guts.aspx?type=cn
"""


# ---------------------------------------------------------------------------
# Module-level constants (KBO placeholders — update when KBO data available)
# ---------------------------------------------------------------------------

KBO_WOBA_WEIGHTS: dict = {
    "BB": 0.690,
    "HBP": 0.722,
    "1B": 0.888,
    "2B": 1.271,
    "3B": 1.616,
    "HR": 2.101,
}
"""MLB FanGraphs 2024 wOBA weights used as KBO placeholder.

TODO: Estimate KBO-specific wOBA weights via linear-weights regression on
KBO run-expectancy tables once play-by-play data is available.
"""

KBO_LEAGUE_WOBA: float = 0.320
"""League-average wOBA placeholder (approx. KBO 2024).

TODO: Compute directly from KBO seasonal play-by-play or box-score data.
"""


# ---------------------------------------------------------------------------
# Core wOBA calculation
# ---------------------------------------------------------------------------


def calculate_woba(
    ubb: float,
    hbp: float,
    singles: float,
    doubles: float,
    triples: float,
    hr: float,
    ab: float,
    ibb: float = 0.0,
    sf: float = 0.0,
    weights: dict | None = None,
) -> float:
    """Calculate Weighted On-Base Average (wOBA).

    Follows the FanGraphs definition: IBB is excluded from the numerator
    (intentional walks are excluded since they are not a true offensive skill)
    but IBB is also NOT added to the denominator — only unintentional BB (ubb)
    enter both numerator and denominator.

    Args:
        ubb:     Unintentional walks (BB - IBB).
        hbp:     Hit by pitch.
        singles: Singles.
        doubles: Doubles.
        triples: Triples.
        hr:      Home runs.
        ab:      At-bats.
        ibb:     Intentional walks (excluded from calculation per FanGraphs).
        sf:      Sacrifice flies.
        weights: Optional custom wOBA weight dict with keys
                 "BB", "HBP", "1B", "2B", "3B", "HR".
                 Defaults to KBO_WOBA_WEIGHTS.

    Returns:
        wOBA rounded to 3 decimal places, or 0.0 if denominator is zero.
    """
    if weights is None:
        weights = KBO_WOBA_WEIGHTS

    numerator = (
        weights["BB"] * ubb
        + weights["HBP"] * hbp
        + weights["1B"] * singles
        + weights["2B"] * doubles
        + weights["3B"] * triples
        + weights["HR"] * hr
    )
    # Denominator follows FanGraphs: AB + unintentional BB + SF + HBP
    # IBB is intentionally excluded from both numerator and denominator.
    denominator = ab + ubb + sf + hbp
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 3)


# ---------------------------------------------------------------------------
# wRAA — Weighted Runs Above Average
# ---------------------------------------------------------------------------


def calculate_wraa(
    woba: float,
    league_woba: float,
    pa: float,
    woba_scale: float = 1.15,
) -> float:
    """Calculate Weighted Runs Above Average (wRAA).

    wRAA = ((wOBA - lgwOBA) / wOBA_scale) * PA

    wOBA_scale converts the wOBA difference from the probability-like wOBA
    scale back into raw runs.  The FanGraphs wOBA scale is typically ~1.15
    for recent MLB seasons; the same placeholder is used for KBO.

    Args:
        woba:        Player's wOBA.
        league_woba: League-average wOBA (use KBO_LEAGUE_WOBA as default).
        pa:          Plate appearances.
        woba_scale:  Conversion factor from wOBA to runs (default 1.15).

    Returns:
        wRAA in runs above average, rounded to 1 decimal place.
        Returns 0.0 if woba_scale is zero.
    """
    if woba_scale == 0:
        return 0.0
    wraa = ((woba - league_woba) / woba_scale) * pa
    return round(wraa, 1)


# ---------------------------------------------------------------------------
# wRC — Weighted Runs Created
# ---------------------------------------------------------------------------


def calculate_wrc(
    wraa: float,
    league_runs_per_pa: float,
    pa: float,
) -> float:
    """Calculate Weighted Runs Created (wRC).

    wRC = wRAA + (lgR/PA * PA)

    Converts wRAA (runs above average) to an absolute runs-created count by
    adding back the expected runs a league-average player would produce.

    Args:
        wraa:               Player's wRAA (from calculate_wraa).
        league_runs_per_pa: League runs per plate appearance (lgR / lgPA).
        pa:                 Player's plate appearances.

    Returns:
        wRC in runs, rounded to 1 decimal place.
    """
    wrc = wraa + (league_runs_per_pa * pa)
    return round(wrc, 1)


# ---------------------------------------------------------------------------
# wRC+ — Park and League Adjusted wRC
# ---------------------------------------------------------------------------


def calculate_wrc_plus(
    wrc_per_pa: float,
    league_wrc_per_pa: float,
    park_factor: float = 1.0,
) -> int:
    """Calculate Park- and League-Adjusted Weighted Runs Created (wRC+).

    wRC+ = (wRC/PA / (Park Factor * lgwRC/PA)) * 100

    100 = league average; values above 100 indicate above-average offense.
    Park factors default to 1.0 (neutral) until KBO park factors are estimated.

    Args:
        wrc_per_pa:       Player's wRC per plate appearance (wRC / PA).
        league_wrc_per_pa: League wRC per plate appearance.
        park_factor:      Multiplicative park factor (default 1.0 = neutral).

    Returns:
        wRC+ as an integer (100 = league average).
        Returns 0 if league_wrc_per_pa or park_factor is zero.
    """
    if league_wrc_per_pa == 0 or park_factor == 0:
        return 0
    wrc_plus = (wrc_per_pa / (park_factor * league_wrc_per_pa)) * 100
    return round(wrc_plus)
