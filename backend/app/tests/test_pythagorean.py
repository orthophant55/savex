"""Pythagorean winning percentage unit tests."""

import pytest

from app.analytics.sabermetrics.pythagorean import (
    calculate_actual_minus_expected_wins,
    calculate_expected_wins,
    calculate_pythagorean_wp,
    estimate_pythagorean_exponent_placeholder,
)


class TestPythagoreanWP:
    def test_equal_rs_ra(self):
        assert calculate_pythagorean_wp(500, 500) == pytest.approx(0.500)

    def test_dominant_offense(self):
        result = calculate_pythagorean_wp(700, 300)
        assert result > 0.7

    def test_weak_offense(self):
        result = calculate_pythagorean_wp(300, 700)
        assert result < 0.3

    def test_zero_rs(self):
        assert calculate_pythagorean_wp(0, 500) == 0.0

    def test_zero_ra(self):
        assert calculate_pythagorean_wp(500, 0) == 1.0

    def test_both_zero(self):
        assert calculate_pythagorean_wp(0, 0) == pytest.approx(0.5)

    def test_exponent_2(self):
        result = calculate_pythagorean_wp(600, 400, exponent=2.0)
        expected = 600**2 / (600**2 + 400**2)
        assert result == pytest.approx(expected, abs=0.001)

    def test_exponent_183(self):
        result = calculate_pythagorean_wp(600, 400, exponent=1.83)
        assert 0.5 < result < 0.7

    def test_result_in_range(self):
        for rs in [300, 400, 500, 600, 700]:
            for ra in [300, 400, 500, 600, 700]:
                wp = calculate_pythagorean_wp(rs, ra)
                assert 0.0 <= wp <= 1.0


class TestExpectedWins:
    def test_normal(self):
        result = calculate_expected_wins(0.600, 144)
        assert result == pytest.approx(86.4)

    def test_zero_wp(self):
        assert calculate_expected_wins(0.0, 144) == 0.0

    def test_perfect_wp(self):
        assert calculate_expected_wins(1.0, 144) == pytest.approx(144.0)


class TestActualMinusExpected:
    def test_over_performer(self):
        result = calculate_actual_minus_expected_wins(actual_wins=92, expected_wins=85.0)
        assert result == pytest.approx(7.0)

    def test_under_performer(self):
        result = calculate_actual_minus_expected_wins(actual_wins=75, expected_wins=85.0)
        assert result == pytest.approx(-10.0)

    def test_exactly_expected(self):
        result = calculate_actual_minus_expected_wins(actual_wins=86, expected_wins=86.0)
        assert result == pytest.approx(0.0)


class TestEstimateExponent:
    def test_returns_placeholder(self):
        result = estimate_pythagorean_exponent_placeholder([])
        assert result == pytest.approx(1.83)

    def test_ignores_input(self):
        data = [{"runs_scored": 500, "runs_allowed": 400, "won": True}]
        result = estimate_pythagorean_exponent_placeholder(data)
        assert result == pytest.approx(1.83)
