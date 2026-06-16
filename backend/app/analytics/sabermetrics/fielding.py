"""Fielding metrics module.

Traditional fielding statistics (Fielding Percentage, Range Factor) are
implemented here.  Advanced defensive metrics (UZR, DRS, OAA) require
detailed batted-ball location and outcome data not currently available in
the KBO public data pipeline; placeholder stubs are provided for future
implementation.
"""


def calculate_fielding_percentage(
    po: float, a: float, e: float
) -> float:
    """Calculate Fielding Percentage (FPct).

    FPct = (PO + A) / (PO + A + E)

    Measures the proportion of defensive chances handled without an error.
    A perfect fielding percentage is 1.000; lower values indicate more errors.
    FPct does not capture range — a player who rarely reaches balls in play
    can have a high FPct while still being a poor defender.

    Args:
        po: Putouts.
        a:  Assists.
        e:  Errors.

    Returns:
        Fielding percentage in [0, 1] rounded to 3 decimal places.
        Returns 0.0 if po + a + e == 0 (no chances).
    """
    total_chances = po + a + e
    if total_chances == 0:
        return 0.0
    return round((po + a) / total_chances, 3)


def calculate_range_factor(
    po: float, a: float, games: float
) -> float:
    """Calculate Range Factor (RF).

    RF = (PO + A) / G

    An approximate measure of a fielder's range — how many plays they
    successfully make per game.  RF is position-dependent and context-
    dependent (team pitching, ground-ball rate, etc.), limiting its
    comparability across positions and eras.

    Args:
        po:    Putouts.
        a:     Assists.
        games: Games played in the field.

    Returns:
        Range factor rounded to 2 decimal places.
        Returns 0.0 if games == 0.
    """
    if games == 0:
        return 0.0
    return round((po + a) / games, 2)


def calculate_uzr_placeholder() -> None:
    """Ultimate Zone Rating (UZR) — placeholder, not yet implemented.

    TODO: UZR requires:
      - Batted-ball location data (hit zones / spray charts) for KBO.
      - Base advancement tracking on each batted ball.
      - Multi-year sample for reliable estimation (≥ 3 seasons recommended).
    See: Mitchel Lichtman (MGL), "The Hardball Times", UZR methodology.

    Returns:
        None (not implemented).
    """
    # TODO: requires batted-ball location data not available in KBO public data
    return None


def calculate_drs_placeholder() -> None:
    """Defensive Runs Saved (DRS) — placeholder, not yet implemented.

    TODO: DRS requires:
      - Fielding Bible zone data with timer information.
      - Outfielder arm ratings (OAR) from baserunner hold/advance data.
      - Catcher framing and blocking data.
    See: John Dewan & Baseball Info Solutions, "The Fielding Bible".

    Returns:
        None (not implemented).
    """
    # TODO: requires Fielding Bible zone data not available in KBO public data
    return None


def calculate_oaa_placeholder() -> None:
    """Outs Above Average (OAA) — placeholder, not yet implemented.

    TODO: OAA requires:
      - Statcast-equivalent tracking data (ball trajectory, launch angle,
        hang time, fielder positioning, reaction time).
      - Sprint speed data for each fielder.
    KBO does not currently have a public Statcast-equivalent system.
    See: MLB Statcast documentation, Baseball Savant.

    Returns:
        None (not implemented).
    """
    # TODO: requires Statcast-equivalent tracking data not available in KBO
    return None
