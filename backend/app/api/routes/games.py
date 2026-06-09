from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.core.exceptions import NotFoundError
from app.domain.games.service import games_service
from app.schemas.kbo import BoxScore, Game, PlayEvent, WinProbabilityPoint

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/today", response_model=List[Game])
def get_today_games():
    return games_service.get_today_games()


@router.get("", response_model=List[Game])
def list_games(date: Optional[str] = Query(None, description="YYYY-MM-DD")):
    return games_service.list_games(date=date)


@router.get("/{game_id}", response_model=Game)
def get_game(game_id: str):
    try:
        return games_service.get_game_detail(game_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{game_id}/box-score", response_model=BoxScore)
def get_box_score(game_id: str):
    try:
        return games_service.get_box_score(game_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{game_id}/play-by-play", response_model=List[PlayEvent])
def get_play_by_play(game_id: str):
    try:
        return games_service.get_play_by_play(game_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{game_id}/win-probability", response_model=List[WinProbabilityPoint])
def get_win_probability(game_id: str):
    try:
        return games_service.get_win_probability(game_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
