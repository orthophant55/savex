from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.core.exceptions import NotFoundError
from app.domain.players.service import players_service
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
