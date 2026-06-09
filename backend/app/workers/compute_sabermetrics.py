"""Worker: 세이버매트릭스 배치 계산.

TODO: 실제 구현 시 다음을 대체한다.
- DB에서 원시 타석/투구 데이터를 읽어온다
- analytics.sabermetrics.batting / pitching 함수를 호출한다
- 결과를 player_season_stats 테이블에 저장한다
- 경기 종료 후 또는 매 이닝 후 트리거 (Celery beat / Arq cron)

Queue 연동 예시 (Celery):
    @celery.task
    def run(game_id: str):
        asyncio.run(main(game_id))
"""

import asyncio
import logging

logger = logging.getLogger(__name__)


async def main(game_id: str | None = None):
    logger.info(f"[compute_sabermetrics] Starting computation for game_id={game_id} (STUB)")
    # TODO: load raw stats from DB
    # TODO: call calculate_avg, calculate_fip, etc.
    # TODO: upsert computed stats
    logger.info("[compute_sabermetrics] Done (STUB)")


if __name__ == "__main__":
    asyncio.run(main())
