"""Fielding Independent Pitching (FIP) and related peripheral pitching metrics.

FIP isolates the outcomes a pitcher directly controls (HR, BB, HBP, K) from
those influenced by fielders and luck (balls in play).  This dedicated module
extends the basic FIP function already present in pitching.py with park/league
adjustments (FIP-) and a full suite of per-9 rate metrics.

NOTE: The FIP constant must be estimated from the run environment so that
league-average FIP equals league-average ERA.  FIP_CONSTANT_KBO = 3.10 is an
MLB-approximate placeholder; a KBO-specific constant should be derived from
KBO seasonal data using: FIP_constant = lgERA - (13*lgHR + 3*(lgBB+lgHBP) - 2*lgK) / lgIP
"""

# ---------------------------------------------------------------------------
# Module-level constant
# ---------------------------------------------------------------------------

FIP_CONSTANT_KBO: float = 3.10
"""KBO FIP constant placeholder (MLB-approximate).

TODO: Estimate from KBO seasonal data.
Formula: lgERA - (13*lgHR + 3*(lgBB+lgHBP) - 2*lgK) / lgIP
This ensures that league-average FIP == league-average ERA.
"""


# ---------------------------------------------------------------------------
# FIP
# ---------------------------------------------------------------------------


def calculate_fip(
    hr: float,
    bb: float,
    hbp: float,
    so: float,
    innings_pitched: float,
    constant: float = FIP_CONSTANT_KBO,
) -> float:
    """Calculate Fielding Independent Pitching (FIP).

    FIP = (13*HR + 3*(BB+HBP) - 2*SO) / IP + constant

    Args:
        hr:              Home runs allowed.
        bb:              Walks allowed (unintentional + intentional).
        hbp:             Hit batters.
        so:              Strikeouts.
        innings_pitched: Innings pitched (decimal form, e.g. 6.2 = 6⅔ IP).
        constant:        FIP constant that normalises to ERA scale.
                         Defaults to FIP_CONSTANT_KBO.

    Returns:
        FIP rounded to 2 decimal places, or 0.0 if innings_pitched == 0.
    """
    if innings_pitched == 0:
        return 0.0
    fip = (13 * hr + 3 * (bb + hbp) - 2 * so) / innings_pitched + constant
    return round(fip, 2)


def calculate_fip_minus(
    fip: float,
    league_fip: float,
    park_factor: float = 1.0,
) -> int:
    """Calculate park- and league-adjusted FIP (FIP-).

    FIP- = (FIP / (park_factor * lgFIP)) * 100

    100 = league average; values below 100 indicate better-than-average pitching.
    Lower is better (unlike most rate stats).

    Args:
        fip:         Pitcher's FIP.
        league_fip:  League-average FIP.
        park_factor: Multiplicative park factor (default 1.0 = neutral).

    Returns:
        FIP- as an integer (100 = league average, lower is better).
        Returns 0 if league_fip or park_factor is zero.
    """
    if league_fip == 0 or park_factor == 0:
        return 0
    fip_minus = (fip / (park_factor * league_fip)) * 100
    return round(fip_minus)


# ---------------------------------------------------------------------------
# RA9 — Runs Allowed per 9 Innings
# ---------------------------------------------------------------------------


def calculate_ra9(r: float, innings_pitched: float) -> float:
    """Calculate Runs Allowed per 9 Innings (RA9).

    RA9 = 9 * R / IP

    Includes both earned and unearned runs, unlike ERA.  RA9 is a better
    measure of actual run prevention since the earned/unearned distinction is
    partly arbitrary (dependent on scorer judgement).

    Args:
        r:               Total runs allowed (earned + unearned).
        innings_pitched: Innings pitched.

    Returns:
        RA9 rounded to 2 decimal places, or 0.0 if innings_pitched == 0.
    """
    if innings_pitched == 0:
        return 0.0
    return round(9 * r / innings_pitched, 2)


# ---------------------------------------------------------------------------
# Per-9 rate stats
# ---------------------------------------------------------------------------


def calculate_k_per_9(so: float, innings_pitched: float) -> float:
    """Calculate strikeouts per 9 innings (K/9).

    K/9 = 9 * SO / IP

    Args:
        so:              Strikeouts.
        innings_pitched: Innings pitched.

    Returns:
        K/9 rounded to 2 decimal places, or 0.0 if innings_pitched == 0.
    """
    if innings_pitched == 0:
        return 0.0
    return round(9 * so / innings_pitched, 2)


def calculate_bb_per_9(bb: float, innings_pitched: float) -> float:
    """Calculate walks per 9 innings (BB/9).

    BB/9 = 9 * BB / IP

    Args:
        bb:              Walks allowed.
        innings_pitched: Innings pitched.

    Returns:
        BB/9 rounded to 2 decimal places, or 0.0 if innings_pitched == 0.
    """
    if innings_pitched == 0:
        return 0.0
    return round(9 * bb / innings_pitched, 2)


def calculate_hr_per_9(hr: float, innings_pitched: float) -> float:
    """Calculate home runs allowed per 9 innings (HR/9).

    HR/9 = 9 * HR / IP

    Args:
        hr:              Home runs allowed.
        innings_pitched: Innings pitched.

    Returns:
        HR/9 rounded to 2 decimal places, or 0.0 if innings_pitched == 0.
    """
    if innings_pitched == 0:
        return 0.0
    return round(9 * hr / innings_pitched, 2)


# ---------------------------------------------------------------------------
# K-BB%
# ---------------------------------------------------------------------------


def calculate_k_minus_bb_rate(k_rate: float, bb_rate: float) -> float:
    """Calculate K-BB% (strikeout rate minus walk rate).

    K-BB% = K% - BB%

    A simple command-of-the-zone metric.  Higher values indicate a pitcher
    who strikes out batters at a high rate relative to walks issued.

    Args:
        k_rate:  Pitcher's strikeout rate (K / BF), as a decimal (e.g. 0.25).
        bb_rate: Pitcher's walk rate (BB / BF), as a decimal (e.g. 0.08).

    Returns:
        K-BB% as a decimal, rounded to 3 decimal places.
    """
    return round(k_rate - bb_rate, 3)
