"""Worker: KBO schedule ingestion.

CLI-style runner for fetching KBO schedule data via kbo-data.

Usage (when KBO_DATA_ENABLED=true):
    cd backend
    KBO_DATA_ENABLED=true KBO_INGESTION_MODE=kbo-data \
    KBO_CHROMEDRIVER_PATH=/path/to/chromedriver \
    python -m app.workers.ingest_kbo_schedule --year 2025 --month 6 --day 16 --mode daily

NOTE: Actual scraping only runs when KBO_DATA_ENABLED=true.
      Default (KBO_DATA_ENABLED=false) is a dry-run that logs what would happen.
"""

import argparse
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest KBO schedule via kbo-data")
    parser.add_argument("--year",  type=int, required=True, help="Year (e.g. 2025)")
    parser.add_argument("--month", type=int, default=None, help="Month (1-12)")
    parser.add_argument("--day",   type=int, default=None, help="Day (1-31)")
    parser.add_argument(
        "--mode",
        choices=["daily", "monthly", "yearly"],
        default="daily",
        help="Schedule fetch mode",
    )
    args = parser.parse_args()

    from app.core.config import settings

    if not settings.KBO_DATA_ENABLED:
        logger.warning(
            "KBO_DATA_ENABLED=false — dry run only. "
            "Set KBO_DATA_ENABLED=true and KBO_INGESTION_MODE=kbo-data to run for real."
        )
        logger.info("Would fetch %s schedule for %d/%s/%s", args.mode, args.year, args.month, args.day)
        return 0

    if settings.KBO_INGESTION_MODE != "kbo-data":
        logger.error("KBO_INGESTION_MODE=%r — set to 'kbo-data' to run this worker", settings.KBO_INGESTION_MODE)
        return 1

    from app.schemas.ingestion import KboScheduleRequest
    from app.ingestion.kbo_data_adapter import kbo_data_adapter

    request = KboScheduleRequest(year=args.year, month=args.month, day=args.day, mode=args.mode)
    logger.info("Starting %s schedule ingestion for %d/%s/%s", args.mode, args.year, args.month, args.day)

    result = kbo_data_adapter.fetch_schedule(request)

    if result.success:
        logger.info("Schedule ingestion succeeded. count=%d ids=%s", result.count, result.raw_payload_ids)
        for w in result.warnings:
            logger.warning(w)
    else:
        logger.error("Schedule ingestion failed: %s", result.errors)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
