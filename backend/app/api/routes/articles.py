from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.core.exceptions import NotFoundError
from app.domain.articles.service import articles_service
from app.schemas.article import Article

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=List[Article])
def list_articles(category: Optional[str] = Query(None)):
    return articles_service.list_articles(category=category)


@router.get("/{article_id}", response_model=Article)
def get_article(article_id: str):
    try:
        return articles_service.get_article(article_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
