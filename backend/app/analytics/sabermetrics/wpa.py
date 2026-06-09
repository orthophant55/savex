"""Win Probability Added (WPA) and Leverage Index calculations."""


def clamp_probability(value: float) -> float:
    """Clamp win probability to [0.0, 1.0]."""
    return max(0.0, min(1.0, value))


def calculate_wpa(before_home_wp: float, after_home_wp: float) -> float:
    """WPA = after_home_wp - before_home_wp (from home team perspective)."""
    before = clamp_probability(before_home_wp)
    after = clamp_probability(after_home_wp)
    return round(after - before, 4)


def calculate_leverage_index(abs_wp_change: float, avg_abs_wp_change: float) -> float:
    """LI = |WP change| / average |WP change|.

    Returns 0.0 if avg_abs_wp_change is zero to avoid division by zero.
    """
    if avg_abs_wp_change == 0:
        return 0.0
    return round(abs(abs_wp_change) / avg_abs_wp_change, 3)
