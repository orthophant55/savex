"""ML model I/O contracts.

These Pydantic models define the interface between service layer and ML models.
Replace placeholder models with real implementations without changing these contracts.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class GameStateInput(BaseModel):
    inning: int
    inning_half: str          # "top" | "bottom"
    outs: int
    away_score: int
    home_score: int
    base_state: str           # e.g. "100"
    season: int = 2025


class WinProbabilityOutput(BaseModel):
    home_win_probability: float
    away_win_probability: float
    confidence: float
    model_name: str
    model_version: str


class PlayerProjectionInput(BaseModel):
    player_id: str
    season: int
    recent_stats: Dict[str, Any] = {}
    career_stats: Dict[str, Any] = {}


class PlayerProjectionOutput(BaseModel):
    projected_avg: Optional[float] = None
    projected_ops: Optional[float] = None
    projected_era: Optional[float] = None
    projected_war: Optional[float] = None
    confidence: float
    model_name: str
    model_version: str


class ArticleTopicInput(BaseModel):
    game_id: Optional[str] = None
    player_ids: List[str] = []
    team_ids: List[str] = []
    context: str = ""


class ArticleTopicOutput(BaseModel):
    ranked_topics: List[str]
    suggested_category: str
    confidence: float


class RegressionAdjustedBattingInput(BaseModel):
    player_id: str
    ab: int
    h: int
    bb: Optional[int] = None
    hr: Optional[int] = None
    league_avg: float = 0.269
    prior_strength: int = 100


class RegressionAdjustedBattingOutput(BaseModel):
    observed_avg: float
    adjusted_avg: float
    reliability_score: float
    shrinkage_amount: float
    confidence: float
    model_name: str
    model_version: str
