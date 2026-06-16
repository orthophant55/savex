"""Thin wrapper around the kbodata package.

kbodata requires ChromeDriver and scrapes the KBO official website.
If kbodata is not installed or ChromeDriver is missing, is_available() returns
False and all methods raise KboDataUnavailableError / ChromeDriverNotFoundError.

Usage:
    client = KboDataClient(chromedriver_path="/path/to/chromedriver")
    if client.is_available():
        schedule = client.get_daily_schedule(2025, 6, 16)
"""

import logging
import time
from typing import Any

from app.core.config import settings
from app.ingestion.exceptions import (
    ChromeDriverNotFoundError,
    KboDataClientError,
    KboDataUnavailableError,
)

logger = logging.getLogger(__name__)

try:
    import kbodata as _kbodata  # noqa: F401
    _KBODATA_AVAILABLE = True
except ImportError:
    _KBODATA_AVAILABLE = False
    logger.warning(
        "kbodata package is not installed. "
        "Run `pip install kbodata` and ensure ChromeDriver is available. "
        "KBO ingestion will fall back to mock data."
    )


class KboDataClient:
    def __init__(self, chromedriver_path: str | None = None):
        self._driver_path = chromedriver_path or settings.KBO_CHROMEDRIVER_PATH
        self._delay = settings.KBO_REQUEST_DELAY_SECONDS

    def is_available(self) -> bool:
        """Return True only if kbodata is installed and a driver path is set."""
        return _KBODATA_AVAILABLE and bool(self._driver_path)

    def _require_available(self) -> None:
        if not _KBODATA_AVAILABLE:
            raise KboDataUnavailableError(
                "kbodata is not installed. Install with: pip install kbodata"
            )
        if not self._driver_path:
            raise ChromeDriverNotFoundError(
                "ChromeDriver path is not configured. "
                "Set KBO_CHROMEDRIVER_PATH in environment or pass chromedriver_path."
            )

    def _sleep(self) -> None:
        time.sleep(self._delay)

    def get_daily_schedule(self, year: int, month: int, day: int) -> Any:
        self._require_available()
        try:
            import kbodata
            logger.info("Fetching daily schedule %d-%02d-%02d", year, month, day)
            result = kbodata.get_daily_schedule(year, month, day, self._driver_path)
            self._sleep()
            return result
        except Exception as exc:
            raise KboDataClientError(f"get_daily_schedule failed: {exc}") from exc

    def get_monthly_schedule(self, year: int, month: int) -> Any:
        self._require_available()
        try:
            import kbodata
            logger.info("Fetching monthly schedule %d-%02d", year, month)
            result = kbodata.get_monthly_schedule(year, month, self._driver_path)
            self._sleep()
            return result
        except Exception as exc:
            raise KboDataClientError(f"get_monthly_schedule failed: {exc}") from exc

    def get_yearly_schedule(self, year: int) -> Any:
        self._require_available()
        try:
            import kbodata
            logger.info("Fetching yearly schedule %d", year)
            result = kbodata.get_yearly_schedule(year, self._driver_path)
            self._sleep()
            return result
        except Exception as exc:
            raise KboDataClientError(f"get_yearly_schedule failed: {exc}") from exc

    def get_game_data(self, schedule: Any) -> Any:
        self._require_available()
        try:
            import kbodata
            logger.info("Fetching game data for schedule")
            result = kbodata.get_game_data(schedule, self._driver_path)
            self._sleep()
            return result
        except Exception as exc:
            raise KboDataClientError(f"get_game_data failed: {exc}") from exc

    def scoreboard_to_dict(self, data: Any) -> dict:
        self._require_available()
        try:
            import kbodata
            return kbodata.scoreboard_to_Dict(data)
        except Exception as exc:
            raise KboDataClientError(f"scoreboard_to_dict failed: {exc}") from exc

    def batter_to_dict(self, data: Any) -> dict:
        self._require_available()
        try:
            import kbodata
            return kbodata.batter_to_Dict(data)
        except Exception as exc:
            raise KboDataClientError(f"batter_to_dict failed: {exc}") from exc

    def pitcher_to_dict(self, data: Any) -> dict:
        self._require_available()
        try:
            import kbodata
            return kbodata.pitcher_to_Dict(data)
        except Exception as exc:
            raise KboDataClientError(f"pitcher_to_dict failed: {exc}") from exc


kbo_data_client = KboDataClient()
