from typing import List

from fastapi import APIRouter

from app.repositories.mock_repository import mock_repo
from app.schemas.kbo import Standing, StatLeader

router = APIRouter(tags=["stats"])


@router.get("/standings", response_model=List[Standing])
def get_standings():
    return mock_repo.get_standings()


@router.get("/stat-leaders", response_model=List[StatLeader])
def get_stat_leaders():
    return mock_repo.get_stat_leaders()
