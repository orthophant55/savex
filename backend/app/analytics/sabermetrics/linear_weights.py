"""Linear weights sabermetrics module.

Implements event-level run value calculations using the linear weights method.

NOTE: The weights provided in get_default_linear_weights() are MLB-approximate values
used as KBO placeholders. KBO-specific linear weights require regression analysis on
KBO run expectancy tables (RE24 matrix) and actual KBO play-by-play data.
Until such data is available and analyzed, these MLB-based weights are reasonable
first-order approximations for the KBO run environment.
"""


def calculate_event_run_value(
    before_re: float, after_re: float, runs_scored: int
) -> float:
    """Calculate the run value of a single event.

    Args:
        before_re: Run expectancy before the play (from the RE24 matrix).
        after_re: Run expectancy after the play (from the RE24 matrix).
        runs_scored: Number of runs that scored on this play.

    Returns:
        Run value = runs_scored + after_re - before_re
    """
    return runs_scored + after_re - before_re


def get_default_linear_weights() -> dict:
    """Return KBO-approximate linear weights per batting event.

    NOTE: These are MLB-approximate weights (circa 2019-2023 MLB average)
    used as placeholders until KBO-specific weights are estimated from
    KBO play-by-play data via RE24 regression.

    Keys and approximate values:
      1B  = 0.47   (single)
      2B  = 0.76   (double)
      3B  = 1.04   (triple)
      HR  = 1.40   (home run)
      BB  = 0.30   (walk)
      IBB = 0.30   (intentional walk — same as BB as placeholder)
      HBP = 0.33   (hit by pitch)
      OUT = -0.26  (generic out)
      SO  = -0.28  (strikeout — slightly worse than generic out)
      GDP = -0.50  (grounded into double play)

    Returns:
        dict mapping event type string to run value float.
    """
    return {
        "1B": 0.47,
        "2B": 0.76,
        "3B": 1.04,
        "HR": 1.40,
        "BB": 0.30,
        "IBB": 0.30,
        "HBP": 0.33,
        "OUT": -0.26,
        "SO": -0.28,
        "GDP": -0.50,
    }


def calculate_linear_weighted_runs(
    events: dict, weights: dict | None = None
) -> float:
    """Calculate total run value from a dictionary of event counts.

    Args:
        events: Mapping of event type to count, e.g.
                {"1B": 100, "HR": 20, "OUT": 300, "SO": 80}.
                Event types not present in weights are ignored.
        weights: Optional custom weights dict. If None, uses
                 get_default_linear_weights().

    Returns:
        Sum of (count * weight) for each event type present in both
        the events dict and the weights dict.
    """
    if weights is None:
        weights = get_default_linear_weights()

    total = 0.0
    for event_type, count in events.items():
        if event_type in weights:
            total += count * weights[event_type]
    return total
