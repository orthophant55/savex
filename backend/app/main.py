from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import AppValidationError, NotFoundError
from app.core.logging import get_logger
from app.api.routes import health, teams, players, games, stats, articles, ai

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} [{settings.APP_ENV}] mock_mode={settings.MOCK_MODE}")
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="KBO 세이버매트릭스 + AI 기사 생성 백엔드 API (MVP · mock mode)",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(AppValidationError)
async def validation_handler(request: Request, exc: AppValidationError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


prefix = settings.API_V1_PREFIX

app.include_router(health.router, prefix=prefix)
app.include_router(teams.router, prefix=prefix)
app.include_router(players.router, prefix=prefix)
app.include_router(games.router, prefix=prefix)
app.include_router(stats.router, prefix=prefix)
app.include_router(articles.router, prefix=prefix)
app.include_router(ai.router, prefix=prefix)


