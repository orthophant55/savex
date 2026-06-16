"""Projections domain service.

Routes projection requests through ModelRegistry so API routes
never import ML models directly.
"""

from typing import Any

from app.analytics.constants.kbo_environment import KBO_LEAGUE_AVG
from app.core.exceptions import NotFoundError
from app.ml.contracts import (
    PlayerProjectionInput,
    RegressionAdjustedBattingInput,
)
from app.ml.registry import registry
from app.repositories.mock_repository import mock_repo


class ProjectionsService:
    def get_regression_adjusted_batting(self, player_id: str) -> dict[str, Any]:
        player = mock_repo.get_player(player_id)
        if not player:
            raise NotFoundError(f"Player {player_id} not found")
        s = player.season_stat
        ab = s.at_bats or 0 if s else 0
        h = s.hits or 0 if s else 0

        model = registry.get("regression_adjusted_batting")
        inp = RegressionAdjustedBattingInput(
            player_id=player_id,
            ab=ab,
            h=h,
            league_avg=KBO_LEAGUE_AVG,
            prior_strength=100,
        )
        output = model.predict(inp)
        return {
            **output.model_dump(),
            "player_name": player.name_ko,
            "season": s.season if s else 2025,
            "data_note": "MOCK data — not official KBO statistics",
        }

    def get_player_projection(self, player_id: str) -> dict[str, Any]:
        player = mock_repo.get_player(player_id)
        if not player:
            raise NotFoundError(f"Player {player_id} not found")
        s = player.season_stat

        recent_stats: dict[str, Any] = {}
        if s:
            if s.avg is not None:
                recent_stats["avg"] = s.avg
            if s.ops is not None:
                recent_stats["ops"] = s.ops
            if s.era is not None:
                recent_stats["era"] = s.era

        model = registry.get("player_projection")
        inp = PlayerProjectionInput(
            player_id=player_id,
            season=s.season if s else 2025,
            recent_stats=recent_stats,
        )
        output = model.predict(inp)
        return {
            **output.model_dump(),
            "player_name": player.name_ko,
            "data_note": "MOCK projection — not official KBO statistics",
        }

    def get_slump_risk(self, player_id: str) -> dict[str, Any]:
        player = mock_repo.get_player(player_id)
        if not player:
            raise NotFoundError(f"Player {player_id} not found")
        s = player.season_stat

        from app.ml.models.slump_risk_model import SlumpRiskInput
        model = registry.get("slump_risk")
        inp = SlumpRiskInput(
            player_id=player_id,
            babip=s.babip or 0.300 if s else 0.300,
            k_rate=0.200,
            bb_rate=0.080,
            recent_ops=s.ops or 0.750 if s else 0.750,
            sample_size=s.at_bats or 100 if s else 100,
        )
        output = model.predict(inp)
        return {
            **output.model_dump(),
            "player_name": player.name_ko,
            "data_note": "MOCK risk score — not official KBO statistics",
        }


projections_service = ProjectionsService()
