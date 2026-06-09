from pydantic import BaseModel


class GameRecapRequest(BaseModel):
    game_id: str


class PlayerAnalysisRequest(BaseModel):
    player_id: str


class GenerationResponse(BaseModel):
    job_id: str
    status: str
    message: str
