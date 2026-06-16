"""Team-level aggregate statistics module.

Aggregates individual player statistics into team-level metrics.
All functions handle empty input gracefully, returning 0.0 for missing data.
"""


def calculate_team_ops(players_stats: list[dict]) -> float:
    """Calculate team average OPS across all players who have an OPS value.

    Args:
        players_stats: List of player stat dicts.  Each dict should contain
                       an "ops" key with a float value.  Players without
                       the "ops" key, or whose OPS is None, are excluded.

    Returns:
        Average OPS across qualifying players, rounded to 3 decimal places.
        Returns 0.0 if no players have a valid OPS value.
    """
    ops_values = [
        p["ops"] for p in players_stats
        if p.get("ops") is not None
    ]
    if not ops_values:
        return 0.0
    return round(sum(ops_values) / len(ops_values), 3)


def calculate_team_era(pitchers_stats: list[dict]) -> float:
    """Calculate team ERA as a weighted average by innings pitched.

    Each pitcher's contribution to the team ERA is weighted by their
    share of total team innings pitched, which correctly aggregates
    ERAs across pitchers with different workloads.

    Args:
        pitchers_stats: List of pitcher stat dicts.  Each dict should have:
                          "era"              (float) — pitcher's ERA.
                          "innings_pitched"  (float) — IP in decimal form.
                        Pitchers with missing keys or zero IP are skipped.

    Returns:
        Weighted-average ERA rounded to 2 decimal places.
        Returns 0.0 if no pitchers have valid innings data.
    """
    total_ip = 0.0
    weighted_sum = 0.0
    for p in pitchers_stats:
        ip = p.get("innings_pitched", 0.0) or 0.0
        era = p.get("era", 0.0) or 0.0
        if ip > 0:
            weighted_sum += era * ip
            total_ip += ip
    if total_ip == 0:
        return 0.0
    return round(weighted_sum / total_ip, 2)


def calculate_run_differential(
    runs_scored: int, runs_allowed: int
) -> int:
    """Calculate team run differential.

    Run differential is a strong indicator of team quality — more predictive
    of future performance than win-loss record alone (see Pythagorean expectation).

    Args:
        runs_scored:  Total runs scored by the team.
        runs_allowed: Total runs allowed by the team.

    Returns:
        runs_scored - runs_allowed (positive = run surplus, negative = deficit).
    """
    return runs_scored - runs_allowed


def calculate_team_war_lite(players_war_list: list[float]) -> float:
    """Calculate total team WAR-Lite as the sum of individual player WAR values.

    Team WAR is simply additive across players (unlike some rate stats).

    Args:
        players_war_list: List of individual player WAR-Lite values.
                          Empty list returns 0.0.

    Returns:
        Sum of all WAR-Lite values, rounded to 1 decimal place.
    """
    if not players_war_list:
        return 0.0
    return round(sum(players_war_list), 1)
