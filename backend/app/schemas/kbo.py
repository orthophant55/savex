from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class GameStatus(str, Enum):
    scheduled = "scheduled"
    pre_game = "pre_game"
    live = "live"
    delayed = "delayed"
    suspended = "suspended"
    final = "final"
    cancelled = "cancelled"
    postponed = "postponed"


class Team(BaseModel):
    id: str
    name_ko: str
    name_en: str
    short_name: str
    home_city: str
    stadium: str
    primary_color: str
    secondary_color: str
    logo_url: Optional[str] = None


class PlayerSeasonStat(BaseModel):
    season: int
    # 타자
    games: Optional[int] = None
    at_bats: Optional[int] = None
    hits: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
    home_runs: Optional[int] = None
    rbi: Optional[int] = None
    runs: Optional[int] = None
    stolen_bases: Optional[int] = None
    walks: Optional[int] = None
    strikeouts_bat: Optional[int] = None
    avg: Optional[float] = None
    obp: Optional[float] = None
    slg: Optional[float] = None
    ops: Optional[float] = None
    woba: Optional[float] = None
    wrc_plus: Optional[int] = None
    babip: Optional[float] = None
    iso: Optional[float] = None
    war_bat: Optional[float] = None
    # 투수
    wins: Optional[int] = None
    losses: Optional[int] = None
    saves: Optional[int] = None
    holds: Optional[int] = None
    innings_pitched: Optional[float] = None
    era: Optional[float] = None
    whip: Optional[float] = None
    fip: Optional[float] = None
    xfip: Optional[float] = None
    k_per_9: Optional[float] = None
    bb_per_9: Optional[float] = None
    hr_per_9: Optional[float] = None
    lob_pct: Optional[float] = None
    gb_pct: Optional[float] = None
    strikeouts_pit: Optional[int] = None
    war_pit: Optional[float] = None


class Player(BaseModel):
    id: str
    team_id: str
    name_ko: str
    name_en: Optional[str] = None
    position: str
    bats: Optional[str] = None
    throws: Optional[str] = None
    jersey_number: Optional[str] = None
    birth_date: Optional[str] = None
    active_status: bool = True
    season_stat: Optional[PlayerSeasonStat] = None


class BoxScoreLine(BaseModel):
    inning: int
    away_runs: int
    home_runs: int


class BoxScore(BaseModel):
    lines: List[BoxScoreLine]
    away_hits: int
    home_hits: int
    away_errors: int
    home_errors: int
    away_total: int
    home_total: int


class PlayEvent(BaseModel):
    id: str
    game_id: str
    inning: int
    inning_half: str  # "top" | "bottom"
    event_index: int
    batting_team_id: str
    fielding_team_id: str
    batter_id: Optional[str] = None
    pitcher_id: Optional[str] = None
    event_type: str
    description: str
    outs_before: int
    outs_after: int
    base_state_before: str  # e.g. "000", "100", "110"
    base_state_after: str
    away_score_before: int
    home_score_before: int
    away_score_after: int
    home_score_after: int
    rbi: int = 0
    is_scoring_play: bool = False
    is_home_run: bool = False
    wpa: Optional[float] = None
    li: Optional[float] = None


class WinProbabilityPoint(BaseModel):
    play_index: int
    inning: int
    inning_half: str
    home_win_probability: float
    away_win_probability: float
    description: Optional[str] = None


class Game(BaseModel):
    id: str
    season: int
    game_date: str
    start_time: str
    stadium: str
    away_team_id: str
    home_team_id: str
    away_score: int
    home_score: int
    status: GameStatus
    inning: Optional[int] = None
    box_score: Optional[BoxScore] = None
    play_events: Optional[List[PlayEvent]] = None
    win_probability: Optional[List[WinProbabilityPoint]] = None


class Standing(BaseModel):
    rank: int
    team_id: str
    wins: int
    losses: int
    draws: int
    win_rate: float
    games_behind: float
    streak: str
    recent_form: List[str]
    runs_scored: Optional[int] = None
    runs_allowed: Optional[int] = None
    run_differential: Optional[int] = None
    pythagorean_wp: Optional[float] = None


class StatLeaderEntry(BaseModel):
    rank: int
    player_id: str
    player_name: str
    team_id: str
    value: float


class StatLeader(BaseModel):
    category: str
    category_ko: str
    unit: str
    is_lower_better: bool
    leaders: List[StatLeaderEntry]


class SabermetricSnapshot(BaseModel):
    player_id: str
    season: int
    wrc_plus: Optional[int] = None
    war: Optional[float] = None
    babip: Optional[float] = None
    iso: Optional[float] = None
    fip: Optional[float] = None
    xfip: Optional[float] = None
