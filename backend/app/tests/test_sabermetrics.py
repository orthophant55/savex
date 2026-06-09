"""Sabermetrics calculation unit tests.

Run: cd backend && pytest -v
"""

import pytest

from app.analytics.sabermetrics.batting import (
    calculate_avg,
    calculate_babip,
    calculate_iso,
    calculate_obp,
    calculate_ops,
    calculate_slg,
)
from app.analytics.sabermetrics.pitching import (
    calculate_bb_rate,
    calculate_era,
    calculate_fip,
    calculate_k_rate,
    calculate_whip,
)
from app.analytics.sabermetrics.wpa import (
    calculate_leverage_index,
    calculate_wpa,
    clamp_probability,
)


# ── Batting ──────────────────────────────────

class TestAVG:
    def test_normal(self):
        assert calculate_avg(150, 500) == pytest.approx(0.300)

    def test_zero_ab(self):
        assert calculate_avg(0, 0) == 0.0

    def test_perfect(self):
        assert calculate_avg(1, 1) == pytest.approx(1.000)


class TestOBP:
    def test_normal(self):
        # (150+50+5) / (500+50+5+10) = 205/565 ≈ 0.363
        result = calculate_obp(h=150, bb=50, hbp=5, ab=500, sf=10)
        assert result == pytest.approx(205 / 565, abs=0.001)

    def test_zero_denominator(self):
        assert calculate_obp(0, 0, 0, 0, 0) == 0.0


class TestSLG:
    def test_normal(self):
        # singles=80, doubles=25, triples=5, hr=20, ab=400
        # TB = 80 + 50 + 15 + 80 = 225; SLG = 225/400 = 0.5625
        result = calculate_slg(80, 25, 5, 20, 400)
        assert result == pytest.approx(0.5625, abs=0.001)

    def test_zero_ab(self):
        assert calculate_slg(10, 5, 1, 3, 0) == 0.0


class TestOPS:
    def test_normal(self):
        assert calculate_ops(0.350, 0.500) == pytest.approx(0.850)

    def test_zero(self):
        assert calculate_ops(0.0, 0.0) == 0.0


class TestISO:
    def test_normal(self):
        assert calculate_iso(0.500, 0.280) == pytest.approx(0.220)

    def test_negative_rounds_ok(self):
        # SLG should always >= AVG but guard against bad input
        result = calculate_iso(0.250, 0.300)
        assert result == pytest.approx(-0.050)


class TestBABIP:
    def test_normal(self):
        # (H-HR) / (AB - SO - HR + SF)
        # (150-20) / (500 - 80 - 20 + 5) = 130/405 ≈ 0.321
        result = calculate_babip(h=150, hr=20, ab=500, so=80, sf=5)
        assert result == pytest.approx(130 / 405, abs=0.001)

    def test_zero_denominator(self):
        assert calculate_babip(0, 0, 0, 0, 0) == 0.0


# ── Pitching ─────────────────────────────────

class TestERA:
    def test_normal(self):
        assert calculate_era(50, 162) == pytest.approx(9 * 50 / 162, abs=0.01)

    def test_zero_ip(self):
        assert calculate_era(5, 0) == 0.0

    def test_perfect(self):
        assert calculate_era(0, 100) == 0.0


class TestWHIP:
    def test_normal(self):
        assert calculate_whip(40, 140, 162) == pytest.approx(180 / 162, abs=0.01)

    def test_zero_ip(self):
        assert calculate_whip(10, 20, 0) == 0.0


class TestKRate:
    def test_normal(self):
        assert calculate_k_rate(180, 600) == pytest.approx(0.300)

    def test_zero_bf(self):
        assert calculate_k_rate(10, 0) == 0.0


class TestBBRate:
    def test_normal(self):
        assert calculate_bb_rate(60, 600) == pytest.approx(0.100)

    def test_zero_bf(self):
        assert calculate_bb_rate(5, 0) == 0.0


class TestFIP:
    def test_normal(self):
        # (13×20 + 3×(50+5) - 2×180) / 162 + 3.10
        # = (260 + 165 - 360) / 162 + 3.10 = 65/162 + 3.10 ≈ 3.50
        expected = (13 * 20 + 3 * (50 + 5) - 2 * 180) / 162 + 3.10
        result = calculate_fip(hr=20, bb=50, hbp=5, so=180, innings_pitched=162)
        assert result == pytest.approx(expected, abs=0.01)

    def test_zero_ip(self):
        assert calculate_fip(5, 3, 0, 10, 0) == 0.0


# ── WPA / LI ─────────────────────────────────

class TestClampProbability:
    def test_in_range(self):
        assert clamp_probability(0.65) == 0.65

    def test_below_zero(self):
        assert clamp_probability(-0.1) == 0.0

    def test_above_one(self):
        assert clamp_probability(1.2) == 1.0


class TestWPA:
    def test_positive_wpa(self):
        # Home team goes from 40% to 65% → WPA = +0.25
        result = calculate_wpa(0.40, 0.65)
        assert result == pytest.approx(0.25)

    def test_negative_wpa(self):
        result = calculate_wpa(0.70, 0.50)
        assert result == pytest.approx(-0.20)

    def test_clamps_inputs(self):
        result = calculate_wpa(-0.1, 1.1)
        assert result == pytest.approx(1.0)


class TestLeverageIndex:
    def test_normal(self):
        # LI = |0.15| / 0.05 = 3.0
        result = calculate_leverage_index(0.15, 0.05)
        assert result == pytest.approx(3.0)

    def test_zero_avg(self):
        assert calculate_leverage_index(0.10, 0.0) == 0.0

    def test_negative_change_uses_abs(self):
        result = calculate_leverage_index(-0.10, 0.05)
        assert result == pytest.approx(2.0)
