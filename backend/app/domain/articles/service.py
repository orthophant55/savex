from typing import List, Optional

from app.core.exceptions import NotFoundError
from app.repositories.mock_repository import mock_repo
from app.schemas.article import Article


class ArticlesService:
    def list_articles(self, category: Optional[str] = None) -> List[Article]:
        return mock_repo.list_articles(category=category)

    def get_article(self, article_id: str) -> Article:
        article = mock_repo.get_article(article_id)
        if not article:
            raise NotFoundError("Article", article_id)
        return article


articles_service = ArticlesService()
