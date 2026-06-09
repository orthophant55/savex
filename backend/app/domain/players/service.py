from typing import List, Optional

from app.core.exceptions import NotFoundError
from app.repositories.mock_repository import mock_repo
from app.schemas.kbo import Player


class PlayersService:
    def list_players(
        self,
        team_id: Optional[str] = None,
        position: Optional[str] = None,
        query: Optional[str] = None,
    ) -> List[Player]:
        return mock_repo.list_players(team_id=team_id, position=position, query=query)

    def get_player(self, player_id: str) -> Player:
        player = mock_repo.get_player(player_id)
        if not player:
            raise NotFoundError("Player", player_id)
        return player


players_service = PlayersService()
