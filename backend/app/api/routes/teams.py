from typing import List

from fastapi import APIRouter, HTTPException

from app.core.exceptions import NotFoundError
from app.domain.teams.service import teams_service
from app.schemas.kbo import Team

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("", response_model=List[Team])
def list_teams():
    return teams_service.list_teams()


@router.get("/{team_id}", response_model=Team)
def get_team(team_id: str):
    try:
        return teams_service.get_team(team_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
