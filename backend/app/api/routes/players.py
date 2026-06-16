from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.core.exceptions import NotFoundError
from app.domain.players.service import players_service
from app.domain.projections.service import projections_service
from app.schemas.kbo import Player

router = APIRouter(prefix="/players", tags=["players"])


@router.get("", response_model=List[Player])
def list_players(
    team_id: Optional[str] = Query(None),
    position: Optional[str] = Query(None),
    query: Optional[str] = Query(None),
):
    return players_service.list_players(team_id=team_id, position=position, query=query)


@router.get("/{player_id}", response_model=Player)
def get_player(player_id: str):
    try:
        return players_service.get_player(player_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{player_id}/stats")
def get_player_stats(player_id: str):
    try:
        player = players_service.get_player(player_id)
        return {"player_id": player_id, "season_stat": player.season_stat}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{player_id}/projection")
def get_player_projection(player_id: str):
    try:
        return projections_service.get_player_projection(player_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{player_id}/regression-adjusted")
def get_regression_adjusted(player_id: str):
    try:
        return projections_service.get_regression_adjusted_batting(player_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{player_id}/slump-risk")
def get_slump_risk(player_id: str):
    try:
        return projections_service.get_slump_risk(player_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
