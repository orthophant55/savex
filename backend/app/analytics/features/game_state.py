from dataclasses import dataclass
from typing import Optional

from app.schemas.kbo import PlayEvent


@dataclass
class GameState:
    inning: int
    inning_half: str       # "top" | "bottom"
    outs: int
    away_score: int
    home_score: int
    base_state: str        # 3-char string: "000"=empty, "100"=runner on 1st, etc.
    run_differential: int  # home_score - away_score


def extract_game_state(play_event: PlayEvent) -> GameState:
    """Extract a GameState snapshot from a PlayEvent (state after the play)."""
    return GameState(
        inning=play_event.inning,
        inning_half=play_event.inning_half,
        outs=play_event.outs_after,
        away_score=play_event.away_score_after,
        home_score=play_event.home_score_after,
        base_state=play_event.base_state_after,
        run_differential=play_event.home_score_after - play_event.away_score_after,
    )
