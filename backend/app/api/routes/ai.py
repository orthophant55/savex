from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional

from app.core.exceptions import NotFoundError
from app.schemas.ai import GameRecapRequest, PlayerAnalysisRequest

router = APIRouter(prefix="/ai", tags=["ai"])


class TeamAnalysisRequest(BaseModel):
    team_id: str


class SabermetricColumnRequest(BaseModel):
    topic: str
    metric_names: List[str] = []


@router.post("/game-recap")
async def ai_game_recap(req: GameRecapRequest):
    from app.ai.generation_service import generation_service

    async def generate():
        try:
            async for chunk in generation_service.game_recap_stream(req.game_id):
                yield chunk.encode("utf-8")
        except NotFoundError as e:
            yield f"ERROR: {e}".encode("utf-8")

    return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")


@router.post("/player-analysis")
async def ai_player_analysis(req: PlayerAnalysisRequest):
    from app.ai.generation_service import generation_service

    async def generate():
        try:
            async for chunk in generation_service.player_analysis_stream(req.player_id):
                yield chunk.encode("utf-8")
        except NotFoundError as e:
            yield f"ERROR: {e}".encode("utf-8")

    return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")


@router.post("/team-analysis")
async def ai_team_analysis(req: TeamAnalysisRequest):
    from app.ai.generation_service import generation_service

    async def generate():
        try:
            async for chunk in generation_service.team_analysis_stream(req.team_id):
                yield chunk.encode("utf-8")
        except NotFoundError as e:
            yield f"ERROR: {e}".encode("utf-8")

    return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")


@router.post("/sabermetric-column")
async def ai_sabermetric_column(req: SabermetricColumnRequest):
    from app.ai.generation_service import generation_service

    async def generate():
        async for chunk in generation_service.sabermetric_column_stream(
            req.topic, req.metric_names
        ):
            yield chunk.encode("utf-8")

    return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")
