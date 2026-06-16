from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class RawKboPayload(BaseModel):
    id: str
    source: str = "kbo-data"
    source_url: Optional[str] = None
    payload_type: str
    payload_json: Optional[dict] = None
    payload_text: Optional[str] = None
    fetched_at: str
    checksum: str
    parser_version: str = "v1.0.0"


class KboScheduleRequest(BaseModel):
    year: int
    month: Optional[int] = None
    day: Optional[int] = None
    mode: str = "daily"  # "daily" | "monthly" | "yearly"


class KboGameDataRequest(BaseModel):
    year: int
    month: Optional[int] = None
    day: Optional[int] = None
    chromedriver_path: Optional[str] = None


class KboIngestionResult(BaseModel):
    success: bool
    source: str
    mode: str
    count: int = 0
    raw_payload_ids: List[str] = []
    warnings: List[str] = []
    errors: List[str] = []
