"""Win Probability Added (WPA) and Leverage Index calculations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from app.schemas.kbo import PlayEvent


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


def rank_plays_by_wpa(play_events: list[Any]) -> list[Any]:
    """Sort play events by absolute WPA value descending.

    Events without a wpa field are excluded from the ranking.
    """
    with_wpa = [e for e in play_events if getattr(e, "wpa", None) is not None]
    return sorted(with_wpa, key=lambda e: abs(e.wpa or 0), reverse=True)


def rank_plays_by_li(play_events: list[Any]) -> list[Any]:
    """Sort play events by Leverage Index descending.

    Events without a li field are excluded from the ranking.
    """
    with_li = [e for e in play_events if getattr(e, "li", None) is not None]
    return sorted(with_li, key=lambda e: e.li or 0, reverse=True)
