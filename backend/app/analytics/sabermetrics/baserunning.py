"""Baserunning metrics module.

Covers stolen-base efficiency metrics and net run value of stolen base attempts.
These are the components of baserunning value computable from box-score-level
KBO data.

Higher-order baserunning metrics (UBR, BsR, OAA-equivalent for bases) require
play-by-play event data with base advancement tracking, which is not yet
available in the KBO public data pipeline.
"""


def calculate_sb_percentage(sb: float, cs: float) -> float:
    """Calculate stolen base success percentage.

    SB% = SB / (SB + CS)

    Args:
        sb: Stolen bases.
        cs: Caught stealing.

    Returns:
        SB% in [0, 1] rounded to 3 decimal places.
        Returns 0.0 if both sb and cs are 0 (no attempts).
    """
    total_attempts = sb + cs
    if total_attempts == 0:
        return 0.0
    return round(sb / total_attempts, 3)


def calculate_breakeven_sb_rate(
    run_value_sb: float = 0.20,
    run_value_cs: float = -0.42,
) -> float:
    """Calculate the stolen base break-even success rate.

    Break-even% = |CS value| / (|CS value| + SB value)

    At exactly the break-even rate, attempting to steal is a zero-sum play:
    expected runs from successful steals exactly cancel the expected cost of
    caught-stealing events.  Players should only run when their expected
    success rate exceeds this threshold.

    With default values:
        break-even = 0.42 / (0.42 + 0.20) = 0.42 / 0.62 ≈ 0.677

    Args:
        run_value_sb: Run value of a successful stolen base (default +0.20).
        run_value_cs: Run value of a caught stealing (default -0.42, negative).

    Returns:
        Break-even stolen base rate rounded to 3 decimal places.
    """
    cs_abs = abs(run_value_cs)
    return round(cs_abs / (cs_abs + run_value_sb), 3)


def calculate_net_sb_runs(
    sb: int,
    cs: int,
    run_value_sb: float = 0.20,
    run_value_cs: float = -0.42,
) -> float:
    """Calculate net runs contributed by stolen base attempts.

    Net SB Runs = SB * run_value_sb + CS * run_value_cs

    Note: run_value_cs should be passed as a negative number (e.g. -0.42).

    Args:
        sb:           Stolen bases.
        cs:           Caught stealing.
        run_value_sb: Run value per successful steal (default +0.20).
        run_value_cs: Run value per caught stealing (default -0.42).

    Returns:
        Net SB runs rounded to 2 decimal places.
        Positive = net contributor; negative = net drain on offense.
    """
    return round(sb * run_value_sb + cs * run_value_cs, 2)
