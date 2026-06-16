"""AI generation service.

Routes between mock and real LLM based on settings.LLM_PROVIDER.
Currently only "mock" is implemented. Add "openai", "anthropic", etc. as needed.
"""

from typing import AsyncGenerator

from app.core.config import settings
from app.core.exceptions import NotFoundError
from app.repositories.mock_repository import MockRepository, mock_repo


class GenerationService:
    def __init__(self, repo: MockRepository):
        self._repo = repo

    async def game_recap_stream(self, game_id: str) -> AsyncGenerator[str, None]:
        game = self._repo.get_game(game_id)
        if not game:
            raise NotFoundError("Game", game_id)

        if settings.LLM_PROVIDER == "mock":
            from app.ai.mock_generator import stream_game_recap
            async for chunk in stream_game_recap(game):
                yield chunk
        else:
            # TODO: implement real LLM call
            # prompt = build_game_recap_prompt(game, {})
            # async for chunk in llm_client.stream(prompt):
            #     yield chunk
            raise NotImplementedError(f"LLM provider '{settings.LLM_PROVIDER}' not yet implemented")

    async def player_analysis_stream(self, player_id: str) -> AsyncGenerator[str, None]:
        player = self._repo.get_player(player_id)
        if not player:
            raise NotFoundError("Player", player_id)

        if settings.LLM_PROVIDER == "mock":
            from app.ai.mock_generator import stream_player_analysis
            async for chunk in stream_player_analysis(player):
                yield chunk
        else:
            raise NotImplementedError(f"LLM provider '{settings.LLM_PROVIDER}' not yet implemented")

    async def team_analysis_stream(self, team_id: str) -> AsyncGenerator[str, None]:
        team = self._repo.get_team(team_id)
        if not team:
            raise NotFoundError("Team", team_id)

        if settings.LLM_PROVIDER == "mock":
            from app.ai.mock_generator import stream_team_analysis
            async for chunk in stream_team_analysis(team):
                yield chunk
        else:
            raise NotImplementedError(f"LLM provider '{settings.LLM_PROVIDER}' not yet implemented")

    async def sabermetric_column_stream(
        self, topic: str, metric_names: list[str]
    ) -> AsyncGenerator[str, None]:
        if settings.LLM_PROVIDER == "mock":
            from app.ai.mock_generator import stream_sabermetric_column
            async for chunk in stream_sabermetric_column(topic, metric_names):
                yield chunk
        else:
            raise NotImplementedError(f"LLM provider '{settings.LLM_PROVIDER}' not yet implemented")


generation_service = GenerationService(mock_repo)
