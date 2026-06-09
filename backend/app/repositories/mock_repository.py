from typing import List, Optional

from app.mock.data import (
    MOCK_ARTICLES,
    MOCK_GAMES,
    MOCK_PLAYERS,
    MOCK_STANDINGS,
    MOCK_STAT_LEADERS,
    MOCK_TEAMS,
)
from app.schemas.article import (
    Article,
    ArticleCategory,
    ArticleRelated,
    AiGenerationStatus,
    ArticleSourceType,
)
from app.schemas.kbo import (
    BoxScore,
    BoxScoreLine,
    Game,
    GameStatus,
    PlayEvent,
    Player,
    PlayerSeasonStat,
    Standing,
    StatLeader,
    StatLeaderEntry,
    Team,
    WinProbabilityPoint,
)


def _build_team(raw: dict) -> Team:
    return Team(**raw)


def _build_player_season_stat(raw: dict) -> PlayerSeasonStat:
    return PlayerSeasonStat(**raw)


def _build_player(raw: dict) -> Player:
    data = dict(raw)
    if data.get("season_stat"):
        data["season_stat"] = _build_player_season_stat(data["season_stat"])
    return Player(**data)


def _build_box_score(raw: dict) -> BoxScore:
    lines = [BoxScoreLine(**l) for l in raw["lines"]]
    return BoxScore(
        lines=lines,
        away_hits=raw["away_hits"],
        home_hits=raw["home_hits"],
        away_errors=raw["away_errors"],
        home_errors=raw["home_errors"],
        away_total=raw["away_total"],
        home_total=raw["home_total"],
    )


def _build_play_event(raw: dict) -> PlayEvent:
    return PlayEvent(**raw)


def _build_win_prob(raw: dict) -> WinProbabilityPoint:
    return WinProbabilityPoint(**raw)


def _build_game(raw: dict) -> Game:
    data = dict(raw)
    if data.get("box_score"):
        data["box_score"] = _build_box_score(data["box_score"])
    if data.get("play_events"):
        data["play_events"] = [_build_play_event(e) for e in data["play_events"]]
    if data.get("win_probability"):
        data["win_probability"] = [_build_win_prob(p) for p in data["win_probability"]]
    return Game(**data)


def _build_standing(raw: dict) -> Standing:
    return Standing(**raw)


def _build_stat_leader(raw: dict) -> StatLeader:
    leaders = [StatLeaderEntry(**e) for e in raw["leaders"]]
    return StatLeader(
        category=raw["category"],
        category_ko=raw["category_ko"],
        unit=raw["unit"],
        is_lower_better=raw["is_lower_better"],
        leaders=leaders,
    )


def _build_article(raw: dict) -> Article:
    data = dict(raw)
    data["related"] = ArticleRelated(**data["related"])
    return Article(**data)


class MockRepository:
    def list_teams(self) -> List[Team]:
        return [_build_team(t) for t in MOCK_TEAMS]

    def get_team(self, team_id: str) -> Optional[Team]:
        for t in MOCK_TEAMS:
            if t["id"] == team_id:
                return _build_team(t)
        return None

    def list_players(
        self,
        team_id: Optional[str] = None,
        position: Optional[str] = None,
        query: Optional[str] = None,
    ) -> List[Player]:
        result = [_build_player(p) for p in MOCK_PLAYERS]
        if team_id:
            result = [p for p in result if p.team_id == team_id]
        if position:
            result = [p for p in result if p.position == position]
        if query:
            q = query.lower()
            result = [p for p in result if q in p.name_ko.lower() or (p.name_en and q in p.name_en.lower())]
        return result

    def get_player(self, player_id: str) -> Optional[Player]:
        for p in MOCK_PLAYERS:
            if p["id"] == player_id:
                return _build_player(p)
        return None

    def list_games(self, date: Optional[str] = None) -> List[Game]:
        result = [_build_game(g) for g in MOCK_GAMES]
        if date:
            result = [g for g in result if g.game_date == date]
        return result

    def get_game(self, game_id: str) -> Optional[Game]:
        for g in MOCK_GAMES:
            if g["id"] == game_id:
                return _build_game(g)
        return None

    def get_today_games(self) -> List[Game]:
        # In mock mode return all games (they're all dated 2025-06-09)
        return [_build_game(g) for g in MOCK_GAMES]

    def get_standings(self) -> List[Standing]:
        return [_build_standing(s) for s in MOCK_STANDINGS]

    def get_stat_leaders(self) -> List[StatLeader]:
        return [_build_stat_leader(s) for s in MOCK_STAT_LEADERS]

    def list_articles(self, category: Optional[str] = None) -> List[Article]:
        result = [_build_article(a) for a in MOCK_ARTICLES]
        if category:
            result = [a for a in result if a.category.value == category]
        return result

    def get_article(self, article_id: str) -> Optional[Article]:
        for a in MOCK_ARTICLES:
            if a["id"] == article_id:
                return _build_article(a)
        return None


mock_repo = MockRepository()
