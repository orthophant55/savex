"""Worker: KBO game data ingestion.

Fetches box score / batter / pitcher data for a given date.

Usage (when KBO_DATA_ENABLED=true):
    cd backend
    KBO_DATA_ENABLED=true KBO_INGESTION_MODE=kbo-data \
    KBO_CHROMEDRIVER_PATH=/path/to/chromedriver \
    python -m app.workers.ingest_kbo_game_data --year 2025 --month 6 --day 16

TODO:
  - Add retry logic with exponential backoff on network errors
  - Add incremental processing (skip already-saved payloads by checksum)
  - Push normalized data to PostgreSQL when DATABASE_URL is configured
"""

import argparse
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest KBO game data via kbo-data")
    parser.add_argument("--year",  type=int, required=True)
    parser.add_argument("--month", type=int, default=None)
    parser.add_argument("--day",   type=int, default=None)
    args = parser.parse_args()

    from app.core.config import settings

    if not settings.KBO_DATA_ENABLED:
        logger.warning("KBO_DATA_ENABLED=false — dry run only.")
        logger.info("Would fetch game data for %d/%s/%s", args.year, args.month, args.day)
        return 0

    if settings.KBO_INGESTION_MODE != "kbo-data":
        logger.error("KBO_INGESTION_MODE=%r — set to 'kbo-data'", settings.KBO_INGESTION_MODE)
        return 1

    from app.schemas.ingestion import KboGameDataRequest
    from app.ingestion.kbo_data_adapter import kbo_data_adapter

    request = KboGameDataRequest(year=args.year, month=args.month, day=args.day)
    logger.info("Starting game data ingestion for %d/%s/%s", args.year, args.month, args.day)

    result = kbo_data_adapter.fetch_game_data(request)

    if result.success:
        logger.info("Game data ingestion succeeded. count=%d", result.count)
        for pid in result.raw_payload_ids:
            logger.info("  Saved payload: %s", pid)
            # TODO: normalize and store to DB
            #   payload = raw_payload_store.load(pid)
            #   normalized = kbo_data_adapter.normalize_game_payload(payload.payload_json)
            #   db.upsert_game(normalized)
    else:
        logger.error("Game data ingestion failed: %s", result.errors)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
