"""WPA / LI unit tests."""

import pytest

from app.analytics.sabermetrics.wpa import (
    calculate_leverage_index,
    calculate_wpa,
    clamp_probability,
    rank_plays_by_li,
    rank_plays_by_wpa,
)


class TestClampProbability:
    def test_in_range(self):
        assert clamp_probability(0.65) == pytest.approx(0.65)

    def test_below_zero(self):
        assert clamp_probability(-0.1) == 0.0

    def test_above_one(self):
        assert clamp_probability(1.2) == 1.0

    def test_edge_zero(self):
        assert clamp_probability(0.0) == 0.0

    def test_edge_one(self):
        assert clamp_probability(1.0) == 1.0


class TestWPA:
    def test_positive_wpa(self):
        result = calculate_wpa(0.40, 0.65)
        assert result == pytest.approx(0.25)

    def test_negative_wpa(self):
        result = calculate_wpa(0.70, 0.50)
        assert result == pytest.approx(-0.20)

    def test_clamps_inputs(self):
        result = calculate_wpa(-0.1, 1.1)
        assert result == pytest.approx(1.0)

    def test_no_change(self):
        assert calculate_wpa(0.50, 0.50) == pytest.approx(0.0)

    def test_large_positive(self):
        result = calculate_wpa(0.10, 0.90)
        assert result == pytest.approx(0.80)


class TestLeverageIndex:
    def test_normal(self):
        result = calculate_leverage_index(0.15, 0.05)
        assert result == pytest.approx(3.0)

    def test_zero_avg(self):
        assert calculate_leverage_index(0.10, 0.0) == 0.0

    def test_negative_change_uses_abs(self):
        result = calculate_leverage_index(-0.10, 0.05)
        assert result == pytest.approx(2.0)

    def test_average_play(self):
        result = calculate_leverage_index(0.05, 0.05)
        assert result == pytest.approx(1.0)


class TestRankPlaysByWPA:
    def _make_event(self, event_index: int, wpa: float):
        from app.schemas.kbo import PlayEvent
        return PlayEvent(
            id=f"e{event_index}",
            game_id="g1",
            inning=5,
            inning_half="top",
            event_index=event_index,
            batting_team_id="LG",
            fielding_team_id="KIA",
            event_type="hit",
            description="단타",
            outs_before=0,
            outs_after=0,
            base_state_before="000",
            base_state_after="100",
            away_score_before=0,
            home_score_before=0,
            away_score_after=0,
            home_score_after=0,
            wpa=wpa,
        )

    def test_sorted_desc_abs_wpa(self):
        events = [
            self._make_event(1, 0.10),
            self._make_event(2, -0.35),
            self._make_event(3, 0.25),
        ]
        ranked = rank_plays_by_wpa(events)
        assert ranked[0].event_index == 2  # abs(-0.35) is largest
        assert ranked[1].event_index == 3
        assert ranked[2].event_index == 1

    def test_empty(self):
        assert rank_plays_by_wpa([]) == []


class TestRankPlaysByLI:
    def _make_event_li(self, event_index: int, li: float):
        from app.schemas.kbo import PlayEvent
        return PlayEvent(
            id=f"e{event_index}",
            game_id="g1",
            inning=9,
            inning_half="bottom",
            event_index=event_index,
            batting_team_id="LG",
            fielding_team_id="KIA",
            event_type="hit",
            description="홈런",
            outs_before=0,
            outs_after=0,
            base_state_before="000",
            base_state_after="000",
            away_score_before=0,
            home_score_before=0,
            away_score_after=0,
            home_score_after=1,
            li=li,
        )

    def test_sorted_desc_li(self):
        events = [
            self._make_event_li(1, 1.5),
            self._make_event_li(2, 3.0),
            self._make_event_li(3, 0.8),
        ]
        ranked = rank_plays_by_li(events)
        assert ranked[0].event_index == 2
        assert ranked[1].event_index == 1
