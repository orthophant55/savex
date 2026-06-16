"""Metrics domain service.

Bridges analytics calculations and ML with the mock/real data layer.
"""

from typing import Any

from app.analytics.constants.kbo_environment import (
    KBO_LEAGUE_AVG,
    KBO_LEAGUE_ERA,
    KBO_LEAGUE_FIP,
    KBO_PYTHAGOREAN_EXPONENT,
)
from app.analytics.constants.metric_definitions import METRIC_CATALOG
from app.analytics.sabermetrics.batting import (
    calculate_avg,
    calculate_babip,
    calculate_iso,
    calculate_obp,
    calculate_ops,
    calculate_slg,
)
from app.analytics.sabermetrics.fip import calculate_fip, calculate_fip_minus
from app.analytics.sabermetrics.pitching import calculate_era, calculate_whip
from app.analytics.sabermetrics.pythagorean import (
    calculate_actual_minus_expected_wins,
    calculate_expected_wins,
    calculate_pythagorean_wp,
)
from app.analytics.sabermetrics.run_expectancy import DEFAULT_KBO_RE_TABLE
from app.analytics.sabermetrics.win_expectancy import DEFAULT_KBO_WE_TABLE
from app.analytics.sabermetrics.woba import calculate_woba, calculate_wraa
from app.core.exceptions import NotFoundError
from app.repositories.mock_repository import mock_repo


class MetricsService:
    def list_metric_definitions(self) -> list[dict]:
        return METRIC_CATALOG

    def get_run_expectancy_table(self) -> list[dict]:
        return DEFAULT_KBO_RE_TABLE

    def get_win_expectancy_table(self) -> list[dict]:
        return DEFAULT_KBO_WE_TABLE

    def calculate_player_basic_metrics(self, player_id: str) -> dict[str, Any]:
        player = mock_repo.get_player(player_id)
        if not player:
            raise NotFoundError(f"Player {player_id} not found")
        s = player.season_stat
        if not s:
            return {"player_id": player_id, "metrics": {}, "note": "No season stats"}

        ab = s.at_bats or 0
        h = s.hits or 0
        doubles = s.doubles or 0
        triples = s.triples or 0
        hr = s.home_runs or 0
        bb = s.walks or 0
        so = s.strikeouts_bat or 0
        hbp = 0
        sf = 0
        singles = h - doubles - triples - hr
        ip = s.innings_pitched or 0.0
        er = 0  # not tracked in current stat schema, use era if available

        metrics: dict[str, Any] = {}
        if ab > 0:
            metrics["avg"] = calculate_avg(h, ab)
            metrics["obp"] = calculate_obp(h, bb, hbp, ab, sf)
            slg = calculate_slg(singles, doubles, triples, hr, ab)
            metrics["slg"] = slg
            metrics["ops"] = calculate_ops(metrics["obp"], slg)
            metrics["iso"] = calculate_iso(slg, metrics["avg"])
            metrics["babip"] = calculate_babip(h, hr, ab, so, sf)
            ubb = max(bb - 0, 0)
            metrics["woba"] = calculate_woba(ubb, hbp, singles, doubles, triples, hr, ab)
            metrics["wraa"] = calculate_wraa(metrics["woba"], KBO_LEAGUE_AVG, ab + bb + sf)

        if ip > 0 and s.era is not None:
            er_est = round(s.era * ip / 9)
            metrics["fip"] = calculate_fip(hr, bb, hbp, so, ip)
            metrics["fip_minus"] = calculate_fip_minus(metrics["fip"], KBO_LEAGUE_FIP)

        return {
            "player_id": player_id,
            "season": s.season,
            "metric_version": "v1.0.0",
            "metrics": metrics,
        }

    def calculate_team_pythagorean(self, team_id: str) -> dict[str, Any]:
        standings = mock_repo.get_standings()
        standing = next((s for s in standings if s.team_id == team_id), None)
        if not standing:
            raise NotFoundError(f"Standing for team {team_id} not found")

        rs = standing.runs_scored if hasattr(standing, "runs_scored") else 400
        ra = standing.runs_allowed if hasattr(standing, "runs_allowed") else 380
        games = standing.wins + standing.losses + standing.draws
        pyth_wp = calculate_pythagorean_wp(rs, ra, KBO_PYTHAGOREAN_EXPONENT)
        exp_w = calculate_expected_wins(pyth_wp, games)
        a_minus_e = calculate_actual_minus_expected_wins(standing.wins, exp_w)

        return {
            "team_id": team_id,
            "season": 2025,
            "wins": standing.wins,
            "losses": standing.losses,
            "runs_scored": rs,
            "runs_allowed": ra,
            "pythagorean_wp": pyth_wp,
            "expected_wins": exp_w,
            "actual_minus_expected_wins": a_minus_e,
            "metric_version": "v1.0.0",
        }

    def get_game_context_metrics(self, game_id: str) -> dict[str, Any]:
        game = mock_repo.get_game(game_id)
        if not game:
            raise NotFoundError(f"Game {game_id} not found")

        events = game.play_events or []
        top_wpa = sorted(
            [e for e in events if e.wpa is not None],
            key=lambda e: abs(e.wpa or 0),
            reverse=True,
        )[:5]
        high_li = sorted(
            [e for e in events if e.li is not None],
            key=lambda e: e.li or 0,
            reverse=True,
        )[:5]

        return {
            "game_id": game_id,
            "top_wpa_plays": [
                {
                    "event_index": e.event_index,
                    "description": e.description,
                    "wpa": e.wpa,
                    "inning": e.inning,
                    "inning_half": e.inning_half,
                }
                for e in top_wpa
            ],
            "high_leverage_plays": [
                {
                    "event_index": e.event_index,
                    "description": e.description,
                    "li": e.li,
                    "inning": e.inning,
                    "inning_half": e.inning_half,
                }
                for e in high_li
            ],
            "metric_version": "v1.0.0",
        }

    def get_player_metric_summary(self, player_id: str) -> dict[str, Any]:
        basic = self.calculate_player_basic_metrics(player_id)
        return {
            "player_id": player_id,
            "basic_metrics": basic.get("metrics", {}),
            "metric_version": "v1.0.0",
            "data_note": "MOCK data — not official KBO statistics",
        }


metrics_service = MetricsService()
