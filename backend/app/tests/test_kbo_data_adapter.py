"""KBO data adapter unit tests.

These tests run without kbodata installed and without ChromeDriver.
Monkeypatching is used to simulate kbodata responses.
"""

import json
import tempfile
import pytest

from app.ingestion.normalization import (
    build_game_id,
    map_kbo_team_to_internal_id,
    normalize_game_date,
    normalize_player_name,
    normalize_team_name,
)
from app.ingestion.exceptions import KboDataUnavailableError, ChromeDriverNotFoundError
from app.ingestion.raw_payload_store import RawPayloadStore


# ── normalize_team_name ──────────────────────────────────────────

class TestNormalizeTeamName:
    def test_lg_variants(self):
        assert normalize_team_name("LG") == "LG"
        assert normalize_team_name("LG 트윈스") == "LG"
        assert normalize_team_name("LG트윈스") == "LG"

    def test_kia_variants(self):
        assert normalize_team_name("KIA") == "KIA"
        assert normalize_team_name("KIA 타이거즈") == "KIA"

    def test_doosan_variants(self):
        assert normalize_team_name("두산") == "DOOSAN"
        assert normalize_team_name("두산 베어스") == "DOOSAN"

    def test_kiwoom_variants(self):
        assert normalize_team_name("키움") == "KIWOOM"
        assert normalize_team_name("키움 히어로즈") == "KIWOOM"

    def test_hanwha_variants(self):
        assert normalize_team_name("한화") == "HANWHA"
        assert normalize_team_name("한화 이글스") == "HANWHA"

    def test_samsung(self):
        assert normalize_team_name("삼성 라이온즈") == "SAMSUNG"

    def test_lotte(self):
        assert normalize_team_name("롯데 자이언츠") == "LOTTE"

    def test_empty_string(self):
        assert normalize_team_name("") == ""


# ── build_game_id ────────────────────────────────────────────────

class TestBuildGameId:
    def test_basic(self):
        gid = build_game_id("2025-06-16", "LG", "KIA")
        assert gid == "20250616_LG_KIA"

    def test_compact_date(self):
        gid = build_game_id("20250616", "두산", "롯데 자이언츠")
        assert gid == "20250616_DOOSAN_LOTTE"

    def test_dot_date(self):
        gid = build_game_id("2025.06.16", "KT", "SSG")
        assert gid == "20250616_KT_SSG"


# ── normalize_game_date ──────────────────────────────────────────

class TestNormalizeGameDate:
    def test_iso(self):
        assert normalize_game_date("2025-06-16") == "2025-06-16"

    def test_compact(self):
        assert normalize_game_date("20250616") == "2025-06-16"

    def test_dot_format(self):
        assert normalize_game_date("2025.06.16") == "2025-06-16"

    def test_slash_format(self):
        assert normalize_game_date("2025/06/16") == "2025-06-16"

    def test_empty(self):
        assert normalize_game_date("") == ""

    def test_none(self):
        assert normalize_game_date(None) == ""


# ── map_kbo_team_to_internal_id ──────────────────────────────────

class TestMapKboTeamToInternalId:
    def test_lg(self):
        assert map_kbo_team_to_internal_id("LG 트윈스") == "lg"

    def test_doosan(self):
        assert map_kbo_team_to_internal_id("두산") == "doosan"

    def test_kiwoom(self):
        assert map_kbo_team_to_internal_id("키움 히어로즈") == "kiwoom"


# ── RawPayloadStore ──────────────────────────────────────────────

class TestRawPayloadStore:
    def test_save_and_load(self, tmp_path):
        store = RawPayloadStore(base_dir=str(tmp_path))
        payload = {"scoreboard": {"away_team": "LG", "home_team": "KIA", "away_score": 5, "home_score": 3}}
        record = store.save(payload_type="scoreboard", payload_json=payload)

        assert record.id is not None
        assert record.checksum
        assert record.payload_type == "scoreboard"

        loaded = store.load(record.id)
        assert loaded is not None
        assert loaded.id == record.id
        assert loaded.payload_json == payload

    def test_load_nonexistent(self, tmp_path):
        store = RawPayloadStore(base_dir=str(tmp_path))
        result = store.load("nonexistent-id")
        assert result is None

    def test_checksum_deterministic(self, tmp_path):
        store = RawPayloadStore(base_dir=str(tmp_path))
        payload = {"key": "value"}
        c1 = store.calculate_checksum(payload)
        c2 = store.calculate_checksum(payload)
        assert c1 == c2

    def test_save_text_payload(self, tmp_path):
        store = RawPayloadStore(base_dir=str(tmp_path))
        record = store.save(payload_type="raw_html", payload_text="<html>test</html>")
        assert record.payload_text == "<html>test</html>"
        loaded = store.load(record.id)
        assert loaded.payload_text == "<html>test</html>"


# ── KboDataClient availability ────────────────────────────────────

class TestKboDataClientAvailability:
    def test_is_available_false_when_no_driver(self):
        from app.ingestion.kbo_data_client import KboDataClient
        client = KboDataClient(chromedriver_path=None)
        # Without ChromeDriver configured, should not be available
        # (kbodata may or may not be installed)
        if not client._driver_path:
            assert client.is_available() is False

    def test_requires_driver_raises(self):
        from app.ingestion.kbo_data_client import KboDataClient
        client = KboDataClient(chromedriver_path=None)
        if not client._driver_path:
            with pytest.raises((ChromeDriverNotFoundError, KboDataUnavailableError)):
                client.get_daily_schedule(2025, 6, 16)


# ── KboDataAdapter — normalize without real kbodata ──────────────

class TestKboDataAdapterNormalize:
    @pytest.fixture
    def adapter(self, tmp_path):
        from app.ingestion.kbo_data_adapter import KboDataAdapter
        from app.ingestion.kbo_data_client import KboDataClient
        from app.ingestion.raw_payload_store import RawPayloadStore
        client = KboDataClient(chromedriver_path=None)
        store = RawPayloadStore(base_dir=str(tmp_path))
        return KboDataAdapter(client=client, store=store)

    def test_normalize_scoreboard_basic(self, adapter):
        raw = [{"date": "20250616", "away_team": "LG 트윈스", "home_team": "KIA 타이거즈",
                "away_score": 5, "home_score": 3, "stadium": "광주"}]
        result = adapter.normalize_scoreboard(raw)
        assert len(result) == 1
        r = result[0]
        assert r["away_team_id"] == "LG"
        assert r["home_team_id"] == "KIA"
        assert r["away_score"] == 5
        assert r["home_score"] == 3
        assert r["game_date"] == "2025-06-16"

    def test_normalize_scoreboard_missing_key_warns(self, adapter, caplog):
        import logging
        raw = [{"away_team": "LG", "home_team": "KIA"}]  # missing date
        with caplog.at_level(logging.WARNING):
            result = adapter.normalize_scoreboard(raw)
        # Should not raise, and should return partial result
        assert len(result) == 1

    def test_normalize_batters_basic(self, adapter):
        raw = [{"name": "이정후", "team": "키움 히어로즈", "AB": 4, "H": 2, "HR": 1, "RBI": 2}]
        result = adapter.normalize_batters(raw)
        assert len(result) == 1
        assert result[0]["player_name"] == "이정후"
        assert result[0]["team"] == "KIWOOM"
        assert result[0]["ab"] == 4
        assert result[0]["h"] == 2

    def test_normalize_batters_missing_key(self, adapter, caplog):
        import logging
        raw = [{"name": "김선수"}]  # missing team, stats
        with caplog.at_level(logging.WARNING):
            result = adapter.normalize_batters(raw)
        assert len(result) == 1
        assert result[0]["ab"] is None

    def test_normalize_pitchers_basic(self, adapter):
        raw = [{"name": "류현진", "team": "한화 이글스", "IP": 7.0, "ER": 1, "BB": 2, "SO": 8}]
        result = adapter.normalize_pitchers(raw)
        assert result[0]["player_name"] == "류현진"
        assert result[0]["team"] == "HANWHA"
        assert result[0]["ip"] == 7.0

    def test_normalize_game_payload_full(self, adapter):
        raw = {
            "scoreboard": {"date": "20250616", "away_team": "LG", "home_team": "KIA",
                           "away_score": 3, "home_score": 2},
            "away_batter": [{"name": "타자1", "team": "LG", "AB": 3, "H": 1}],
            "home_batter": [{"name": "타자2", "team": "KIA", "AB": 4, "H": 2}],
            "away_pitcher": [{"name": "투수1", "team": "LG", "IP": 6.0}],
            "home_pitcher": [{"name": "투수2", "team": "KIA", "IP": 5.0}],
        }
        result = adapter.normalize_game_payload(raw)
        assert result["source"] == "kbo-data"
        assert len(result["away_batters"]) == 1
        assert len(result["home_batters"]) == 1
        assert len(result["away_pitchers"]) == 1

    def test_normalize_game_payload_missing_keys(self, adapter, caplog):
        import logging
        raw = {"scoreboard": {}}  # minimal
        with caplog.at_level(logging.WARNING):
            result = adapter.normalize_game_payload(raw)
        assert result["source"] == "kbo-data"

    def test_normalize_empty_inputs(self, adapter):
        assert adapter.normalize_scoreboard([]) == []
        assert adapter.normalize_batters([]) == []
        assert adapter.normalize_pitchers([]) == []

    def test_fetch_schedule_disabled_by_config(self, adapter, monkeypatch):
        from app.core import config
        monkeypatch.setattr(config.settings, "KBO_DATA_ENABLED", False)
        from app.schemas.ingestion import KboScheduleRequest
        req = KboScheduleRequest(year=2025, month=6, day=16, mode="daily")
        result = adapter.fetch_schedule(req)
        assert result.success is False
        assert any("false" in e.lower() or "KBO_DATA_ENABLED" in e for e in result.errors)
