"""Win Expectancy (WE) module.

Win expectancy is the probability that the home team wins the game given
the current game state (inning, half-inning, score differential, outs,
base configuration).  Changes in win expectancy across plays are used to
compute WPA (Win Probability Added).

NOTE: DEFAULT_KBO_WE_TABLE contains a small set of hand-crafted approximate
values for development/testing.  A production win expectancy table should be
derived from historical KBO game data via simulation or logistic regression
over game states.
"""

# ---------------------------------------------------------------------------
# Score-differential bucketing
# ---------------------------------------------------------------------------


def bucket_score_diff(score_diff: int) -> str:
    """Convert a raw score differential to a bucket label for WE table lookup.

    Buckets extreme values to reduce table size while preserving precision
    in close-game situations.

    Args:
        score_diff: home_score - away_score (positive = home team leading).

    Returns:
        Bucket label string: "-4+", "-3", "-2", "-1", "0", "+1", "+2", "+3", "+4+"
    """
    if score_diff <= -4:
        return "-4+"
    if score_diff == -3:
        return "-3"
    if score_diff == -2:
        return "-2"
    if score_diff == -1:
        return "-1"
    if score_diff == 0:
        return "0"
    if score_diff == 1:
        return "+1"
    if score_diff == 2:
        return "+2"
    if score_diff == 3:
        return "+3"
    # score_diff >= 4
    return "+4+"


# ---------------------------------------------------------------------------
# Win expectancy lookup
# ---------------------------------------------------------------------------


def lookup_win_expectancy(
    table: list[dict],
    inning: int,
    inning_half: str,
    score_diff: int,
    outs: int,
    base_state: str,
) -> float:
    """Look up win probability from a win expectancy table.

    Args:
        table:       List of dicts with keys:
                       inning (int), inning_half (str "top"/"bottom"),
                       score_diff_bucket (str), outs (int),
                       base_state (str), home_win_probability (float).
        inning:      Current inning number (1-indexed).
        inning_half: "top" or "bottom".
        score_diff:  home_score - away_score (bucketed internally).
        outs:        Number of outs (0, 1, or 2).
        base_state:  3-character base state string (e.g. "000").

    Returns:
        home_win_probability from the matching row, or 0.5 if not found
        (defaulting to coin-flip when the exact state is unavailable).
    """
    bucket = bucket_score_diff(score_diff)
    for row in table:
        if (
            row.get("inning") == inning
            and row.get("inning_half") == inning_half
            and row.get("score_diff_bucket") == bucket
            and row.get("outs") == outs
            and row.get("base_state") == base_state
        ):
            return float(row.get("home_win_probability", 0.5))
    return 0.5


# ---------------------------------------------------------------------------
# Before / after win probability pair
# ---------------------------------------------------------------------------


def calculate_win_probability_before_after(
    before_state: dict,
    after_state: dict,
    table: list[dict],
) -> tuple[float, float]:
    """Retrieve the win probabilities immediately before and after a play.

    Args:
        before_state: Dict describing the game state BEFORE the play.
                      Required keys: inning, inning_half, score_diff,
                                     outs, base_state.
        after_state:  Dict describing the game state AFTER the play.
                      Same required keys as before_state.
        table:        Win expectancy lookup table (see lookup_win_expectancy).

    Returns:
        (before_wp, after_wp) tuple of home-team win probabilities.
    """
    before_wp = lookup_win_expectancy(
        table,
        inning=before_state["inning"],
        inning_half=before_state["inning_half"],
        score_diff=before_state["score_diff"],
        outs=before_state["outs"],
        base_state=before_state["base_state"],
    )
    after_wp = lookup_win_expectancy(
        table,
        inning=after_state["inning"],
        inning_half=after_state["inning_half"],
        score_diff=after_state["score_diff"],
        outs=after_state["outs"],
        base_state=after_state["base_state"],
    )
    return (before_wp, after_wp)


# ---------------------------------------------------------------------------
# Default KBO win expectancy table (development placeholder)
# ---------------------------------------------------------------------------

DEFAULT_KBO_WE_TABLE: list[dict] = [
    # ── Inning 9, bottom ─────────────────────────────────────────────────
    # Tie game — pure coin flip before any runners/outs
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "0",
     "outs": 0, "base_state": "000", "home_win_probability": 0.50},
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "0",
     "outs": 1, "base_state": "000", "home_win_probability": 0.50},
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "0",
     "outs": 2, "base_state": "000", "home_win_probability": 0.50},
    # Home leading by 1 in the 9th — home team heavily favoured
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "+1",
     "outs": 0, "base_state": "000", "home_win_probability": 0.85},
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "+1",
     "outs": 1, "base_state": "000", "home_win_probability": 0.88},
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "+1",
     "outs": 2, "base_state": "000", "home_win_probability": 0.92},
    # Home trailing by 1 in the 9th
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "-1",
     "outs": 0, "base_state": "000", "home_win_probability": 0.15},
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "-1",
     "outs": 1, "base_state": "000", "home_win_probability": 0.12},
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "-1",
     "outs": 2, "base_state": "000", "home_win_probability": 0.08},
    # Home leading by 2 in the 9th
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "+2",
     "outs": 0, "base_state": "000", "home_win_probability": 0.94},
    # Home trailing by 2 in the 9th
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "-2",
     "outs": 0, "base_state": "000", "home_win_probability": 0.06},
    # Walk-off situation: 9th inning bottom, tie, runner on base
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "0",
     "outs": 0, "base_state": "100", "home_win_probability": 0.62},
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "0",
     "outs": 0, "base_state": "110", "home_win_probability": 0.68},
    {"inning": 9, "inning_half": "bottom", "score_diff_bucket": "-1",
     "outs": 0, "base_state": "100", "home_win_probability": 0.22},
    # ── Inning 1, top — game effectively 50/50 regardless ────────────────
    {"inning": 1, "inning_half": "top", "score_diff_bucket": "0",
     "outs": 0, "base_state": "000", "home_win_probability": 0.50},
    {"inning": 1, "inning_half": "top", "score_diff_bucket": "+1",
     "outs": 0, "base_state": "000", "home_win_probability": 0.56},
    {"inning": 1, "inning_half": "top", "score_diff_bucket": "-1",
     "outs": 0, "base_state": "000", "home_win_probability": 0.44},
    # ── Inning 5, top — mid-game neutral ─────────────────────────────────
    {"inning": 5, "inning_half": "top", "score_diff_bucket": "0",
     "outs": 0, "base_state": "000", "home_win_probability": 0.50},
    {"inning": 5, "inning_half": "top", "score_diff_bucket": "+1",
     "outs": 0, "base_state": "000", "home_win_probability": 0.62},
    {"inning": 5, "inning_half": "top", "score_diff_bucket": "-1",
     "outs": 0, "base_state": "000", "home_win_probability": 0.38},
    # ── Inning 7, bottom — late game ─────────────────────────────────────
    {"inning": 7, "inning_half": "bottom", "score_diff_bucket": "0",
     "outs": 0, "base_state": "000", "home_win_probability": 0.50},
    {"inning": 7, "inning_half": "bottom", "score_diff_bucket": "+1",
     "outs": 0, "base_state": "000", "home_win_probability": 0.68},
    {"inning": 7, "inning_half": "bottom", "score_diff_bucket": "-1",
     "outs": 0, "base_state": "000", "home_win_probability": 0.32},
    {"inning": 7, "inning_half": "bottom", "score_diff_bucket": "+3",
     "outs": 0, "base_state": "000", "home_win_probability": 0.88},
    {"inning": 7, "inning_half": "bottom", "score_diff_bucket": "-3",
     "outs": 0, "base_state": "000", "home_win_probability": 0.12},
    # ── Inning 9, top — close game situations ────────────────────────────
    {"inning": 9, "inning_half": "top", "score_diff_bucket": "0",
     "outs": 0, "base_state": "000", "home_win_probability": 0.50},
    {"inning": 9, "inning_half": "top", "score_diff_bucket": "+1",
     "outs": 0, "base_state": "000", "home_win_probability": 0.72},
    {"inning": 9, "inning_half": "top", "score_diff_bucket": "-1",
     "outs": 0, "base_state": "000", "home_win_probability": 0.28},
    {"inning": 9, "inning_half": "top", "score_diff_bucket": "+2",
     "outs": 2, "base_state": "000", "home_win_probability": 0.90},
    {"inning": 9, "inning_half": "top", "score_diff_bucket": "-2",
     "outs": 2, "base_state": "000", "home_win_probability": 0.10},
]
"""Small mock win expectancy table for development and testing.

Covers representative high-leverage situations: walk-off 9th inning,
mid-game states, and clean-inning (000 base state) entries for innings
1, 5, 7, and 9.

TODO: Replace with a full KBO-derived win expectancy table (all 24 base×out
cells × score diff buckets × 18 half-innings) trained on historical KBO data.
"""
