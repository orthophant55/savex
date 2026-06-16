"""Adapter: kbo-data raw output → SAVEX normalized schema.

kbo-data game JSON structure (from README):
  {
    "scoreboard": ...,
    "ETC_info": ...,
    "away_batter": ...,
    "home_batter": ...,
    "away_pitcher": ...,
    "home_pitcher": ...
  }

Normalization is partial: some fields may be missing depending on what KBO
publishes.  All key accesses are guarded with .get() and warnings are logged.
"""

import logging
from typing import Any

from app.core.config import settings
from app.ingestion.exceptions import KboDataClientError, KboDataUnavailableError
from app.ingestion.kbo_data_client import KboDataClient
from app.ingestion.normalization import (
    build_game_id,
    normalize_game_date,
    normalize_player_name,
    normalize_team_name,
)
from app.ingestion.raw_payload_store import RawPayloadStore
from app.schemas.ingestion import (
    KboGameDataRequest,
    KboIngestionResult,
    KboScheduleRequest,
)

logger = logging.getLogger(__name__)

PARSER_VERSION = "v1.0.0"
_MISSING_SENTINEL = "__MISSING__"


def _safe_get(d: dict, key: str, default: Any = None, warn_label: str = "") -> Any:
    if not isinstance(d, dict):
        return default
    val = d.get(key, _MISSING_SENTINEL)
    if val is _MISSING_SENTINEL:
        if warn_label:
            logger.warning("Missing key '%s' in %s", key, warn_label)
        return default
    return val


class KboDataAdapter:
    def __init__(
        self,
        client: KboDataClient | None = None,
        store: RawPayloadStore | None = None,
    ):
        self._client = client or KboDataClient()
        self._store = store or RawPayloadStore()

    # ── Public ingestion methods ──────────────────────────────

    def fetch_schedule(self, request: KboScheduleRequest) -> KboIngestionResult:
        warnings: list[str] = []
        errors: list[str] = []

        if not settings.KBO_DATA_ENABLED:
            return KboIngestionResult(
                success=False,
                source="kbo-data",
                mode=request.mode,
                errors=["KBO_DATA_ENABLED is false. Set to true to enable ingestion."],
            )

        if not self._client.is_available():
            return KboIngestionResult(
                success=False,
                source="kbo-data",
                mode=request.mode,
                errors=[
                    "kbodata package not installed or ChromeDriver path not configured."
                ],
            )

        try:
            if request.mode == "daily":
                raw = self._client.get_daily_schedule(
                    request.year, request.month or 1, request.day or 1
                )
            elif request.mode == "monthly":
                raw = self._client.get_monthly_schedule(
                    request.year, request.month or 1
                )
            else:
                raw = self._client.get_yearly_schedule(request.year)

            payload = self._store.save(
                payload_type=f"schedule_{request.mode}",
                payload_json=raw if isinstance(raw, dict) else None,
                payload_text=str(raw) if not isinstance(raw, dict) else None,
            )
            return KboIngestionResult(
                success=True,
                source="kbo-data",
                mode=request.mode,
                count=1,
                raw_payload_ids=[payload.id],
                warnings=warnings,
                errors=errors,
            )
        except (KboDataClientError, KboDataUnavailableError) as exc:
            logger.error("Schedule ingestion failed: %s", exc)
            return KboIngestionResult(
                success=False,
                source="kbo-data",
                mode=request.mode,
                errors=[str(exc)],
            )

    def fetch_game_data(self, request: KboGameDataRequest) -> KboIngestionResult:
        warnings: list[str] = []
        errors: list[str] = []

        if not settings.KBO_DATA_ENABLED:
            return KboIngestionResult(
                success=False,
                source="kbo-data",
                mode="game_data",
                errors=["KBO_DATA_ENABLED is false."],
            )

        if not self._client.is_available():
            return KboIngestionResult(
                success=False,
                source="kbo-data",
                mode="game_data",
                errors=["kbodata unavailable."],
            )

        try:
            schedule = self._client.get_daily_schedule(
                request.year, request.month or 1, request.day or 1
            )
            raw_games = self._client.get_game_data(schedule)

            if not isinstance(raw_games, list):
                raw_games = [raw_games]

            ids = []
            for raw in raw_games:
                payload = self._store.save(
                    payload_type="game_data",
                    payload_json=raw if isinstance(raw, dict) else None,
                    payload_text=str(raw) if not isinstance(raw, dict) else None,
                )
                ids.append(payload.id)

            return KboIngestionResult(
                success=True,
                source="kbo-data",
                mode="game_data",
                count=len(ids),
                raw_payload_ids=ids,
                warnings=warnings,
                errors=errors,
            )
        except (KboDataClientError, KboDataUnavailableError) as exc:
            logger.error("Game data ingestion failed: %s", exc)
            return KboIngestionResult(
                success=False,
                source="kbo-data",
                mode="game_data",
                errors=[str(exc)],
            )

    # ── Normalization methods ─────────────────────────────────

    def normalize_scoreboard(self, raw_scoreboard: Any) -> list[dict]:
        if not raw_scoreboard:
            return []
        if not isinstance(raw_scoreboard, (dict, list)):
            logger.warning("normalize_scoreboard: unexpected type %s", type(raw_scoreboard))
            return []
        items = raw_scoreboard if isinstance(raw_scoreboard, list) else [raw_scoreboard]
        result = []
        for item in items:
            if not isinstance(item, dict):
                continue
            away_name = _safe_get(item, "away_team", warn_label="scoreboard.away_team")
            home_name = _safe_get(item, "home_team", warn_label="scoreboard.home_team")
            date_raw = _safe_get(item, "date", warn_label="scoreboard.date")
            result.append(
                {
                    "source": "kbo-data",
                    "parser_version": PARSER_VERSION,
                    "game_id": build_game_id(
                        date_raw or "",
                        away_name or "",
                        home_name or "",
                    ),
                    "game_date": normalize_game_date(date_raw),
                    "away_team_id": normalize_team_name(away_name or ""),
                    "home_team_id": normalize_team_name(home_name or ""),
                    "away_score": _safe_get(item, "away_score", 0, "scoreboard.away_score"),
                    "home_score": _safe_get(item, "home_score", 0, "scoreboard.home_score"),
                    "stadium": _safe_get(item, "stadium", warn_label="scoreboard.stadium"),
                    "raw": item,
                }
            )
        return result

    def normalize_batters(self, raw_batter: Any) -> list[dict]:
        if not raw_batter:
            return []
        if not isinstance(raw_batter, (dict, list)):
            logger.warning("normalize_batters: unexpected type %s", type(raw_batter))
            return []
        rows = raw_batter if isinstance(raw_batter, list) else [raw_batter]
        result = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            result.append(
                {
                    "source": "kbo-data",
                    "parser_version": PARSER_VERSION,
                    "player_name": normalize_player_name(
                        _safe_get(row, "name", "", "batter.name")
                    ),
                    "team": normalize_team_name(
                        _safe_get(row, "team", "", "batter.team")
                    ),
                    "ab": _safe_get(row, "AB", None, "batter.AB"),
                    "h": _safe_get(row, "H", None, "batter.H"),
                    "hr": _safe_get(row, "HR", None, "batter.HR"),
                    "rbi": _safe_get(row, "RBI", None, "batter.RBI"),
                    "bb": _safe_get(row, "BB", None, "batter.BB"),
                    "so": _safe_get(row, "SO", None, "batter.SO"),
                    "raw": row,
                }
            )
        return result

    def normalize_pitchers(self, raw_pitcher: Any) -> list[dict]:
        if not raw_pitcher:
            return []
        if not isinstance(raw_pitcher, (dict, list)):
            logger.warning("normalize_pitchers: unexpected type %s", type(raw_pitcher))
            return []
        rows = raw_pitcher if isinstance(raw_pitcher, list) else [raw_pitcher]
        result = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            result.append(
                {
                    "source": "kbo-data",
                    "parser_version": PARSER_VERSION,
                    "player_name": normalize_player_name(
                        _safe_get(row, "name", "", "pitcher.name")
                    ),
                    "team": normalize_team_name(
                        _safe_get(row, "team", "", "pitcher.team")
                    ),
                    "ip": _safe_get(row, "IP", None, "pitcher.IP"),
                    "er": _safe_get(row, "ER", None, "pitcher.ER"),
                    "bb": _safe_get(row, "BB", None, "pitcher.BB"),
                    "so": _safe_get(row, "SO", None, "pitcher.SO"),
                    "hr": _safe_get(row, "HR", None, "pitcher.HR"),
                    "raw": row,
                }
            )
        return result

    def normalize_game_payload(self, raw_payload: Any) -> dict:
        if not isinstance(raw_payload, dict):
            logger.warning("normalize_game_payload: expected dict, got %s", type(raw_payload))
            return {"source": "kbo-data", "parser_version": PARSER_VERSION, "error": "invalid payload type"}

        scoreboard = _safe_get(raw_payload, "scoreboard", {}, "game_payload.scoreboard")
        away_batter = _safe_get(raw_payload, "away_batter", [], "game_payload.away_batter")
        home_batter = _safe_get(raw_payload, "home_batter", [], "game_payload.home_batter")
        away_pitcher = _safe_get(raw_payload, "away_pitcher", [], "game_payload.away_pitcher")
        home_pitcher = _safe_get(raw_payload, "home_pitcher", [], "game_payload.home_pitcher")

        return {
            "source": "kbo-data",
            "parser_version": PARSER_VERSION,
            "scoreboard": self.normalize_scoreboard(scoreboard),
            "away_batters": self.normalize_batters(away_batter),
            "home_batters": self.normalize_batters(home_batter),
            "away_pitchers": self.normalize_pitchers(away_pitcher),
            "home_pitchers": self.normalize_pitchers(home_pitcher),
        }


kbo_data_adapter = KboDataAdapter()
