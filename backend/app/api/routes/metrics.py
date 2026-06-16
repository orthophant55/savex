from fastapi import APIRouter, HTTPException

from app.core.exceptions import NotFoundError
from app.domain.metrics.service import metrics_service

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/definitions")
def list_metric_definitions():
    return metrics_service.list_metric_definitions()


@router.get("/run-expectancy")
def get_run_expectancy_table():
    return metrics_service.get_run_expectancy_table()


@router.get("/win-expectancy")
def get_win_expectancy_table():
    return metrics_service.get_win_expectancy_table()


@router.get("/players/{player_id}/summary")
def get_player_metric_summary(player_id: str):
    try:
        return metrics_service.get_player_metric_summary(player_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/teams/{team_id}/pythagorean")
def get_team_pythagorean(team_id: str):
    try:
        return metrics_service.calculate_team_pythagorean(team_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/games/{game_id}/context")
def get_game_context_metrics(game_id: str):
    try:
        return metrics_service.get_game_context_metrics(game_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
