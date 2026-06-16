"""Pitching sabermetrics unit tests."""

import pytest

from app.analytics.sabermetrics.pitching import (
    calculate_bb_rate,
    calculate_era,
    calculate_k_rate,
    calculate_whip,
)
from app.analytics.sabermetrics.fip import (
    calculate_bb_per_9,
    calculate_fip,
    calculate_fip_minus,
    calculate_hr_per_9,
    calculate_k_minus_bb_rate,
    calculate_k_per_9,
    calculate_ra9,
)


class TestERA:
    def test_normal(self):
        expected = round(9 * 50 / 162, 2)
        assert calculate_era(50, 162) == pytest.approx(expected, abs=0.01)

    def test_zero_ip(self):
        assert calculate_era(5, 0) == 0.0

    def test_perfect(self):
        assert calculate_era(0, 100) == 0.0

    def test_high_era(self):
        result = calculate_era(100, 100)
        assert result == pytest.approx(9.0)


class TestRA9:
    def test_normal(self):
        result = calculate_ra9(60, 162)
        assert result == pytest.approx(9 * 60 / 162, abs=0.01)

    def test_zero_ip(self):
        assert calculate_ra9(5, 0) == 0.0


class TestWHIP:
    def test_normal(self):
        result = calculate_whip(40, 140, 162)
        assert result == pytest.approx(180 / 162, abs=0.01)

    def test_zero_ip(self):
        assert calculate_whip(10, 20, 0) == 0.0

    def test_elite_whip(self):
        result = calculate_whip(20, 80, 200)
        assert result < 1.0


class TestKPer9:
    def test_normal(self):
        result = calculate_k_per_9(200, 200)
        assert result == pytest.approx(9.0)

    def test_zero_ip(self):
        assert calculate_k_per_9(10, 0) == 0.0


class TestBBPer9:
    def test_normal(self):
        result = calculate_bb_per_9(40, 180)
        assert result == pytest.approx(9 * 40 / 180, abs=0.01)

    def test_zero_ip(self):
        assert calculate_bb_per_9(5, 0) == 0.0


class TestHRPer9:
    def test_normal(self):
        result = calculate_hr_per_9(20, 180)
        assert result == pytest.approx(9 * 20 / 180, abs=0.01)

    def test_zero_ip(self):
        assert calculate_hr_per_9(5, 0) == 0.0


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


class TestKMinusBBRate:
    def test_positive(self):
        result = calculate_k_minus_bb_rate(0.25, 0.08)
        assert result == pytest.approx(0.17)

    def test_negative(self):
        result = calculate_k_minus_bb_rate(0.15, 0.20)
        assert result == pytest.approx(-0.05)

    def test_zero(self):
        assert calculate_k_minus_bb_rate(0.20, 0.20) == pytest.approx(0.0)


class TestFIP:
    def test_normal(self):
        expected = (13 * 20 + 3 * (50 + 5) - 2 * 180) / 162 + 3.10
        result = calculate_fip(hr=20, bb=50, hbp=5, so=180, innings_pitched=162)
        assert result == pytest.approx(expected, abs=0.01)

    def test_zero_ip(self):
        assert calculate_fip(5, 3, 0, 10, 0) == 0.0

    def test_high_k_low_hr(self):
        result = calculate_fip(hr=5, bb=20, hbp=2, so=250, innings_pitched=200)
        assert result < 3.50


class TestFIPMinus:
    def test_league_average(self):
        assert calculate_fip_minus(fip=4.0, league_fip=4.0) == 100

    def test_above_average_pitcher(self):
        result = calculate_fip_minus(fip=3.0, league_fip=4.0)
        assert result < 100

    def test_below_average_pitcher(self):
        result = calculate_fip_minus(fip=5.0, league_fip=4.0)
        assert result > 100

    def test_zero_league_fip(self):
        assert calculate_fip_minus(4.0, 0.0) == 0
