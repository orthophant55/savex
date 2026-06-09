from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.core.exceptions import NotFoundError
from app.schemas.ai import GameRecapRequest, PlayerAnalysisRequest

router = APIRouter(prefix="/ai", tags=["ai"])


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
