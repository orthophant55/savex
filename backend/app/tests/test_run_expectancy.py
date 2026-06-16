"""Run Expectancy unit tests."""

import pytest

from app.analytics.sabermetrics.run_expectancy import (
    DEFAULT_KBO_RE_TABLE,
    BASE_STATES,
    base_state_to_label,
    calculate_re24,
    decode_base_state,
    encode_base_state,
    lookup_run_expectancy,
)


class TestEncodeBaseState:
    def test_empty(self):
        assert encode_base_state(False, False, False) == "000"

    def test_runner_on_first(self):
        assert encode_base_state(True, False, False) == "100"

    def test_runner_on_second(self):
        assert encode_base_state(False, True, False) == "010"

    def test_runner_on_third(self):
        assert encode_base_state(False, False, True) == "001"

    def test_first_and_second(self):
        assert encode_base_state(True, True, False) == "110"

    def test_bases_loaded(self):
        assert encode_base_state(True, True, True) == "111"


class TestDecodeBaseState:
    def test_empty(self):
        d = decode_base_state("000")
        assert d == {"on_first": False, "on_second": False, "on_third": False}

    def test_first(self):
        d = decode_base_state("100")
        assert d["on_first"] is True
        assert d["on_second"] is False
        assert d["on_third"] is False

    def test_loaded(self):
        d = decode_base_state("111")
        assert all(d.values())

    def test_roundtrip(self):
        for state in BASE_STATES:
            d = decode_base_state(state)
            encoded = encode_base_state(d["on_first"], d["on_second"], d["on_third"])
            assert encoded == state


class TestBaseStateLabel:
    def test_empty(self):
        assert base_state_to_label("000") == "주자 없음"

    def test_bases_loaded(self):
        assert base_state_to_label("111") == "만루"

    def test_first_and_third(self):
        assert base_state_to_label("101") == "1,3루"

    def test_unknown(self):
        label = base_state_to_label("999")
        assert "999" in label


class TestCalculateRE24:
    def test_positive_play(self):
        # 무사 1루(0.87) → 0사 2루(1.07), 0점 득점
        result = calculate_re24(before_re=0.87, after_re=1.07, runs_scored=0)
        assert result == pytest.approx(0.20)

    def test_home_run(self):
        # 무사 1루(0.87) → 무사 주자없음(0.50), 2점 득점
        result = calculate_re24(before_re=0.87, after_re=0.50, runs_scored=2)
        assert result == pytest.approx(2 + 0.50 - 0.87)

    def test_strikeout(self):
        # 0아웃 주자없음(0.50) → 1아웃 주자없음(0.28), 0점 득점
        result = calculate_re24(before_re=0.50, after_re=0.28, runs_scored=0)
        assert result == pytest.approx(-0.22)

    def test_inning_ending_out(self):
        # 2아웃 주자없음(0.10) → 이닝 종료(0.0), 0점 득점
        result = calculate_re24(before_re=0.10, after_re=0.0, runs_scored=0)
        assert result == pytest.approx(-0.10)


class TestLookupRunExpectancy:
    def test_known_state_0out_empty(self):
        result = lookup_run_expectancy(DEFAULT_KBO_RE_TABLE, "000", 0)
        assert result == pytest.approx(0.50)

    def test_known_state_loaded_0out(self):
        result = lookup_run_expectancy(DEFAULT_KBO_RE_TABLE, "111", 0)
        assert result == pytest.approx(2.33)

    def test_2out_empty(self):
        result = lookup_run_expectancy(DEFAULT_KBO_RE_TABLE, "000", 2)
        assert result == pytest.approx(0.10)

    def test_unknown_state_returns_zero(self):
        result = lookup_run_expectancy(DEFAULT_KBO_RE_TABLE, "000", 5)
        assert result == 0.0

    def test_table_has_24_rows(self):
        assert len(DEFAULT_KBO_RE_TABLE) == 24

    def test_re_increases_with_runners(self):
        empty = lookup_run_expectancy(DEFAULT_KBO_RE_TABLE, "000", 0)
        first = lookup_run_expectancy(DEFAULT_KBO_RE_TABLE, "100", 0)
        loaded = lookup_run_expectancy(DEFAULT_KBO_RE_TABLE, "111", 0)
        assert empty < first < loaded

    def test_re_decreases_with_outs(self):
        re_0 = lookup_run_expectancy(DEFAULT_KBO_RE_TABLE, "000", 0)
        re_1 = lookup_run_expectancy(DEFAULT_KBO_RE_TABLE, "000", 1)
        re_2 = lookup_run_expectancy(DEFAULT_KBO_RE_TABLE, "000", 2)
        assert re_0 > re_1 > re_2
