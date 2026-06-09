from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class ArticleCategory(str, Enum):
    game_recap = "game_recap"
    player_analysis = "player_analysis"
    team_analysis = "team_analysis"
    sabermetric_column = "sabermetric_column"


class ArticleSourceType(str, Enum):
    ai_generated = "ai_generated"
    human_written = "human_written"
    ai_assisted = "ai_assisted"


class AiGenerationStatus(str, Enum):
    draft = "draft"
    generating = "generating"
    generated = "generated"
    fact_checking = "fact_checking"
    needs_review = "needs_review"
    approved = "approved"
    published = "published"
    failed = "failed"


class ArticleRelated(BaseModel):
    game_id: Optional[str] = None
    player_ids: List[str] = []
    team_ids: List[str] = []


class Article(BaseModel):
    id: str
    title: str
    summary: str
    body: str
    category: ArticleCategory
    source_type: ArticleSourceType
    ai_generation_status: AiGenerationStatus
    published_at: str
    author: Optional[str] = None
    related: ArticleRelated = ArticleRelated()
    tags: List[str] = []
    thumbnail_color: Optional[str] = None
    reading_time_minutes: Optional[int] = None


class ArticleGenerationJob(BaseModel):
    id: str
    game_id: Optional[str] = None
    player_id: Optional[str] = None
    category: ArticleCategory
    status: AiGenerationStatus
    created_at: str
    completed_at: Optional[str] = None


class ArticleFactCheck(BaseModel):
    article_id: str
    checked_at: str
    issues: List[str] = []
    approved: bool
