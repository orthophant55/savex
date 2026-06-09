from typing import List, Optional

from app.core.exceptions import NotFoundError
from app.repositories.mock_repository import mock_repo
from app.schemas.kbo import BoxScore, Game, PlayEvent, WinProbabilityPoint


class GamesService:
    def list_games(self, date: Optional[str] = None) -> List[Game]:
        return mock_repo.list_games(date=date)

    def get_today_games(self) -> List[Game]:
        return mock_repo.get_today_games()

    def get_game(self, game_id: str) -> Game:
        game = mock_repo.get_game(game_id)
        if not game:
            raise NotFoundError("Game", game_id)
        return game

    def get_game_detail(self, game_id: str) -> Game:
        """Return game with box_score, play_events, and win_probability included."""
        return self.get_game(game_id)

    def get_box_score(self, game_id: str) -> BoxScore:
        game = self.get_game(game_id)
        if not game.box_score:
            raise NotFoundError("BoxScore", game_id)
        return game.box_score

    def get_play_by_play(self, game_id: str) -> List[PlayEvent]:
        game = self.get_game(game_id)
        return game.play_events or []

    def get_win_probability(self, game_id: str) -> List[WinProbabilityPoint]:
        game = self.get_game(game_id)
        return game.win_probability or []


games_service = GamesService()
