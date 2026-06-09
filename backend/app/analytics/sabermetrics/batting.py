"""Batting sabermetrics calculation functions.

All functions return 0.0 on division-by-zero rather than raising.
"""


def calculate_avg(h: float, ab: float) -> float:
    """Batting Average = H / AB"""
    if ab == 0:
        return 0.0
    return round(h / ab, 3)


def calculate_obp(h: float, bb: float, hbp: float, ab: float, sf: float) -> float:
    """On-Base Percentage = (H + BB + HBP) / (AB + BB + HBP + SF)"""
    denominator = ab + bb + hbp + sf
    if denominator == 0:
        return 0.0
    return round((h + bb + hbp) / denominator, 3)


def calculate_slg(singles: float, doubles: float, triples: float, hr: float, ab: float) -> float:
    """Slugging Percentage = (1B + 2×2B + 3×3B + 4×HR) / AB"""
    if ab == 0:
        return 0.0
    tb = singles + 2 * doubles + 3 * triples + 4 * hr
    return round(tb / ab, 3)


def calculate_ops(obp: float, slg: float) -> float:
    """OPS = OBP + SLG"""
    return round(obp + slg, 3)


def calculate_iso(slg: float, avg: float) -> float:
    """Isolated Power = SLG - AVG"""
    return round(slg - avg, 3)


def calculate_babip(h: float, hr: float, ab: float, so: float, sf: float) -> float:
    """BABIP = (H - HR) / (AB - SO - HR + SF)"""
    denominator = ab - so - hr + sf
    if denominator == 0:
        return 0.0
    return round((h - hr) / denominator, 3)
