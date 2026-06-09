"""Pitching sabermetrics calculation functions.

All functions return 0.0 on division-by-zero rather than raising.
"""


def calculate_era(er: float, innings_pitched: float) -> float:
    """ERA = 9 × ER / IP"""
    if innings_pitched == 0:
        return 0.0
    return round(9 * er / innings_pitched, 2)


def calculate_whip(bb: float, h: float, innings_pitched: float) -> float:
    """WHIP = (BB + H) / IP"""
    if innings_pitched == 0:
        return 0.0
    return round((bb + h) / innings_pitched, 2)


def calculate_k_rate(so: float, batters_faced: float) -> float:
    """K% = SO / BF"""
    if batters_faced == 0:
        return 0.0
    return round(so / batters_faced, 3)


def calculate_bb_rate(bb: float, batters_faced: float) -> float:
    """BB% = BB / BF"""
    if batters_faced == 0:
        return 0.0
    return round(bb / batters_faced, 3)


def calculate_fip(
    hr: float,
    bb: float,
    hbp: float,
    so: float,
    innings_pitched: float,
    constant: float = 3.10,
) -> float:
    """FIP = (13×HR + 3×(BB+HBP) - 2×SO) / IP + constant"""
    if innings_pitched == 0:
        return 0.0
    fip = (13 * hr + 3 * (bb + hbp) - 2 * so) / innings_pitched + constant
    return round(fip, 2)
