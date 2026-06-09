"""Worker: AI 기사 자동 생성.

TODO: 실제 구현 시 다음을 대체한다.
- 경기 종료 이벤트를 구독 (Redis pub/sub, Celery signal 등)
- generation_service.game_recap_stream() 또는 실제 LLM gateway 호출
- 생성된 기사를 articles 테이블에 draft 상태로 저장
- 팩트 체크 워커(fact_checker.py)에 작업 전달
- 에디터 승인 후 published 상태로 변경

Queue 연동 예시 (Celery):
    @celery.task
    def run(game_id: str):
        asyncio.run(main(game_id))
"""

import asyncio
import logging

logger = logging.getLogger(__name__)


async def main(game_id: str | None = None):
    logger.info(f"[generate_articles] Starting article generation for game_id={game_id} (STUB)")
    # TODO: call generation_service.game_recap_stream(game_id)
    # TODO: collect streamed text and save to DB as Article(status=draft)
    # TODO: trigger fact_check worker
    logger.info("[generate_articles] Done (STUB)")


if __name__ == "__main__":
    asyncio.run(main())
