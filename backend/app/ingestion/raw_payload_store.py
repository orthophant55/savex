"""Local file-based raw payload store.

Saves kbo-data raw payloads as JSON files under KBO_RAW_PAYLOAD_DIR.
Replace with a PostgreSQL / S3 store later without changing the interface.
"""

import hashlib
import json
import logging
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import settings
from app.schemas.ingestion import RawKboPayload

logger = logging.getLogger(__name__)

PARSER_VERSION = "v1.0.0"


class RawPayloadStore:
    def __init__(self, base_dir: str | None = None):
        self._base = Path(base_dir or settings.KBO_RAW_PAYLOAD_DIR)

    def _ensure_dir(self) -> Path:
        self._base.mkdir(parents=True, exist_ok=True)
        return self._base

    def calculate_checksum(self, payload: dict | str) -> str:
        if isinstance(payload, dict):
            raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        else:
            raw = str(payload)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def save(
        self,
        payload_type: str,
        payload_json: dict | None = None,
        payload_text: str | None = None,
        source: str = "kbo-data",
        source_url: str | None = None,
    ) -> RawKboPayload:
        payload_id = str(uuid.uuid4())
        fetched_at = datetime.now(timezone.utc).isoformat()
        checksum = self.calculate_checksum(payload_json or payload_text or "")

        record = RawKboPayload(
            id=payload_id,
            source=source,
            source_url=source_url,
            payload_type=payload_type,
            payload_json=payload_json,
            payload_text=payload_text,
            fetched_at=fetched_at,
            checksum=checksum,
            parser_version=PARSER_VERSION,
        )

        base = self._ensure_dir()
        file_path = base / f"{payload_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(record.model_dump(), f, ensure_ascii=False, indent=2)

        logger.info("Saved raw payload %s (%s) to %s", payload_id, payload_type, file_path)
        return record

    def load(self, payload_id: str) -> RawKboPayload | None:
        file_path = self._base / f"{payload_id}.json"
        if not file_path.exists():
            logger.warning("Payload %s not found at %s", payload_id, file_path)
            return None
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        return RawKboPayload(**data)


raw_payload_store = RawPayloadStore()
