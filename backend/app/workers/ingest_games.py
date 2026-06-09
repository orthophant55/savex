"""Worker: KBO 경기 데이터 수집.

TODO: 실제 구현 시 다음을 대체한다.
- KBO 공식 API 또는 인가된 데이터 소스에서 당일 경기 데이터를 수집
- repository.upsert_game() 호출로 DB에 저장
- Celery/RQ/Arq 태스크로 등록하여 주기적으로 실행 (예: 경기 중 30초 간격)

Queue 연동 예시 (Celery):
    @celery.task
    def run():
        asyncio.run(main())
"""

import asyncio
import logging

logger = logging.getLogger(__name__)


async def main():
    logger.info("[ingest_games] Starting game ingestion (STUB)")
    # TODO: fetch today's games from KBO data source
    # TODO: upsert into PostgreSQL via real repository
    logger.info("[ingest_games] Done (STUB — no data fetched)")


if __name__ == "__main__":
    asyncio.run(main())
