"""Run Expectancy (RE24) module.

The run expectancy matrix (RE24 matrix) captures the expected number of runs
that will score from a given game state (base state × outs combination) to the
end of the inning.  RE24 for a play is then:

    RE24 = runs_scored + RE(after state) - RE(before state)

This allows attribution of run value to each play independent of context.

NOTE: DEFAULT_KBO_RE_TABLE contains MLB-approximate values used as KBO
placeholders.  KBO-specific values should be derived from KBO play-by-play
data by averaging actual runs-scored-to-end-of-inning for each of the 24
base-state × out combinations.
"""

# ---------------------------------------------------------------------------
# Module-level constant: canonical base state ordering
# ---------------------------------------------------------------------------

BASE_STATES: list[str] = ["000", "100", "010", "001", "110", "101", "011", "111"]
"""All 8 possible base states in canonical order.

Format: 3-character string where each character is "0" (empty) or "1" (occupied).
  Position 0 → first base
  Position 1 → second base
  Position 2 → third base
"""


# ---------------------------------------------------------------------------
# Base state encoding / decoding
# ---------------------------------------------------------------------------


def encode_base_state(
    on_first: bool, on_second: bool, on_third: bool
) -> str:
    """Encode a base configuration as a 3-character string.

    Args:
        on_first:  True if there is a runner on first base.
        on_second: True if there is a runner on second base.
        on_third:  True if there is a runner on third base.

    Returns:
        3-character string "XYZ" where X=first, Y=second, Z=third;
        "1" means runner present, "0" means base empty.
        E.g. runners on first and third → "101".
    """
    return (
        ("1" if on_first else "0")
        + ("1" if on_second else "0")
        + ("1" if on_third else "0")
    )


def decode_base_state(base_state: str) -> dict:
    """Decode a 3-character base state string into a boolean dict.

    Args:
        base_state: 3-character string such as "101".

    Returns:
        Dict with keys "on_first", "on_second", "on_third" (bool values).
    """
    return {
        "on_first": base_state[0] == "1",
        "on_second": base_state[1] == "1",
        "on_third": base_state[2] == "1",
    }


def base_state_to_label(base_state: str) -> str:
    """Return a human-readable Korean label for a base state.

    Args:
        base_state: 3-character base state string (see BASE_STATES).

    Returns:
        Korean label describing which bases are occupied, e.g.
        "000" → "주자 없음", "100" → "1루", "111" → "만루".
    """
    labels: dict[str, str] = {
        "000": "주자 없음",
        "100": "1루",
        "010": "2루",
        "001": "3루",
        "110": "1,2루",
        "101": "1,3루",
        "011": "2,3루",
        "111": "만루",
    }
    return labels.get(base_state, f"알 수 없음({base_state})")


# ---------------------------------------------------------------------------
# RE24 calculation
# ---------------------------------------------------------------------------


def calculate_re24(
    before_re: float, after_re: float, runs_scored: int
) -> float:
    """Calculate RE24 (run expectancy change) for a single play.

    RE24 = runs_scored + RE(after state) - RE(before state)

    Positive values indicate the batter/runner helped their team;
    negative values indicate they hurt their team relative to expectation.

    Args:
        before_re:   Run expectancy in the state BEFORE the play.
        after_re:    Run expectancy in the state AFTER the play
                     (0.0 if the inning ended on this play).
        runs_scored: Number of runs that scored on this play.

    Returns:
        RE24 value rounded to 2 decimal places.
    """
    return round(runs_scored + after_re - before_re, 2)


# ---------------------------------------------------------------------------
# RE table lookup
# ---------------------------------------------------------------------------


def lookup_run_expectancy(
    table: list[dict], base_state: str, outs: int
) -> float:
    """Look up expected runs from a run expectancy table.

    Args:
        table:      List of dicts, each with keys:
                      "base_state" (str), "outs" (int), "expected_runs" (float).
                    Additional keys (e.g. "season", "sample_size") are ignored.
        base_state: 3-character base state string (e.g. "100").
        outs:       Number of outs (0, 1, or 2).

    Returns:
        The expected_runs value from the matching row, or 0.0 if not found.
    """
    for row in table:
        if row.get("base_state") == base_state and row.get("outs") == outs:
            return float(row.get("expected_runs", 0.0))
    return 0.0


# ---------------------------------------------------------------------------
# Default KBO run expectancy table (MLB-approximate placeholder)
# ---------------------------------------------------------------------------

# MLB-approximate run expectancy values (2019-2023 average).
# 24 cells: 8 base states × 3 out states.
# TODO: Replace with values derived from actual KBO play-by-play data.

_RE_ROWS: list[tuple[str, int, float]] = [
    # (base_state, outs, expected_runs)
    # 0 outs
    ("000", 0, 0.50),
    ("100", 0, 0.87),
    ("010", 0, 1.07),
    ("001", 0, 1.35),
    ("110", 0, 1.46),
    ("101", 0, 1.77),
    ("011", 0, 1.95),
    ("111", 0, 2.33),
    # 1 out
    ("000", 1, 0.28),
    ("100", 1, 0.53),
    ("010", 1, 0.67),
    ("001", 1, 0.95),
    ("110", 1, 0.93),
    ("101", 1, 1.22),
    ("011", 1, 1.43),
    ("111", 1, 1.62),
    # 2 outs
    ("000", 2, 0.10),
    ("100", 2, 0.24),
    ("010", 2, 0.32),
    ("001", 2, 0.37),
    ("110", 2, 0.45),
    ("101", 2, 0.50),
    ("011", 2, 0.57),
    ("111", 2, 0.75),
]

DEFAULT_KBO_RE_TABLE: list[dict] = [
    {
        "season": "2024-mock",
        "base_state": base_state,
        "outs": outs,
        "expected_runs": expected_runs,
        "sample_size": 0,
    }
    for base_state, outs, expected_runs in _RE_ROWS
]
"""MLB-approximate run expectancy table used as KBO placeholder (24 cells).

Each dict has keys: season, base_state, outs, expected_runs, sample_size.
sample_size=0 signals these are mock/placeholder values.

TODO: Derive KBO-specific values from KBO play-by-play data by computing
the average runs scored to end of inning for each (base_state, outs) cell.
"""
