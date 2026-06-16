"""
KBO run environment constants (approximate/placeholder values).
These need to be updated with actual KBO seasonal data.
All values marked with TODO should be estimated from KBO historical data.
"""

# KBO league average batting constants (2024 placeholder)
KBO_LEAGUE_AVG = 0.269  # TODO: compute from actual KBO data
KBO_LEAGUE_OBP = 0.344
KBO_LEAGUE_SLG = 0.417
KBO_LEAGUE_OPS = 0.761
KBO_LEAGUE_WOBA = 0.320  # TODO: compute using KBO linear weights
KBO_WOBA_SCALE = 1.15    # TODO: compute from KBO run environment

# KBO pitching environment
KBO_LEAGUE_ERA = 4.50    # TODO: update with actual KBO ERA
KBO_LEAGUE_FIP = 4.35
KBO_FIP_CONSTANT = 3.10  # TODO: KBO-specific constant estimation needed
KBO_RUNS_PER_GAME = 4.8  # TODO: from actual KBO data

# KBO pythagorean
KBO_PYTHAGOREAN_EXPONENT = 1.83  # TODO: calibrate with KBO historical W-L vs RS/RA

# wOBA weights (MLB FanGraphs 2024 used as placeholder - KBO regression needed)
KBO_WOBA_WEIGHTS = {
    "BB": 0.690,
    "HBP": 0.722,
    "1B": 0.888,
    "2B": 1.271,
    "3B": 1.616,
    "HR": 2.101,
}

# Linear weights (approximate, MLB-based placeholder)
KBO_LINEAR_WEIGHTS = {
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

# Stabilization points for regression to mean (PA-based, MLB estimates as placeholder)
STABILIZATION_POINTS = {
    "AVG": 500,
    "OBP": 500,
    "SLG": 550,
    "HR_RATE": 300,
    "BB_RATE": 120,
    "K_RATE": 80,
    "BABIP": 820,
    "WOBA": 500,
}

# Runs per win (approximate)
RUNS_PER_WIN = 10.0  # varies by run environment

# Park factors (placeholder: all 1.0 until KBO park factor data is available)
PARK_FACTORS = {
    "LG": 1.0,
    "DOOSAN": 1.0,  # same stadium as LG
    "KT": 1.0,
    "SSG": 1.0,
    "NC": 1.0,
    "KIA": 1.0,
    "LOTTE": 1.0,
    "SAMSUNG": 1.0,
    "HANWHA": 1.0,
    "KIWOOM": 1.0,
}
