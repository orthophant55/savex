from typing import List, Optional

from app.core.exceptions import NotFoundError
from app.repositories.mock_repository import mock_repo
from app.schemas.kbo import Team


class TeamsService:
    def list_teams(self) -> List[Team]:
        return mock_repo.list_teams()

    def get_team(self, team_id: str) -> Team:
        team = mock_repo.get_team(team_id)
        if not team:
            raise NotFoundError("Team", team_id)
        return team


teams_service = TeamsService()
