from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class MetricCategory(str, Enum):
    observed = "observed"
    rate = "rate"
    run_value = "run_value"
    win_value = "win_value"
    projection = "projection"
    strategy = "strategy"
    tracking = "tracking"


class ImplementationStatus(str, Enum):
    implemented = "implemented"
    placeholder = "placeholder"
    future = "future"


class MetricDefinition(BaseModel):
    name: str
    display_name: str
    category: MetricCategory
    formula: Optional[str] = None
    interpretation: str
    implementation_status: ImplementationStatus = ImplementationStatus.implemented
    context_neutral: bool = True
    context_dependent: bool = False
    higher_is_better: Optional[bool] = None
    version: str = "v1.0.0"
    notes: Optional[str] = None


class MetricValue(BaseModel):
    entity_type: str  # "player" | "team" | "game" | "play"
    entity_id: str
    metric_name: str
    value: float
    season: Optional[int] = None
    date: Optional[str] = None
    metric_version: str = "v1.0.0"
    confidence: Optional[float] = None
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None
    explanation: Optional[str] = None


class RunExpectancyEntry(BaseModel):
    season: str
    base_state: str
    outs: int
    expected_runs: float
    sample_size: int = 0


class WinExpectancyEntry(BaseModel):
    season_group: str
    inning: int
    inning_half: str
    score_diff_bucket: int
    outs: int
    base_state: str
    home_win_probability: float
    sample_size: int = 0
