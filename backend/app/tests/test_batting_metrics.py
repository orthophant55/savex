"""Batting sabermetrics unit tests."""

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
    calculate_k_rate,
)
from app.analytics.sabermetrics.woba import (
    calculate_woba,
    calculate_wrc,
    calculate_wrc_plus,
    calculate_wraa,
)


class TestAVG:
    def test_normal(self):
        assert calculate_avg(150, 500) == pytest.approx(0.300)

    def test_zero_ab(self):
        assert calculate_avg(0, 0) == 0.0

    def test_perfect(self):
        assert calculate_avg(1, 1) == pytest.approx(1.000)

    def test_low_average(self):
        assert calculate_avg(50, 400) == pytest.approx(0.125)


class TestOBP:
    def test_normal(self):
        result = calculate_obp(h=150, bb=50, hbp=5, ab=500, sf=10)
        assert result == pytest.approx(205 / 565, abs=0.001)

    def test_zero_denominator(self):
        assert calculate_obp(0, 0, 0, 0, 0) == 0.0

    def test_high_obp(self):
        result = calculate_obp(h=200, bb=100, hbp=10, ab=500, sf=5)
        assert result == pytest.approx(310 / 615, abs=0.001)


class TestSLG:
    def test_normal(self):
        result = calculate_slg(80, 25, 5, 20, 400)
        assert result == pytest.approx(0.5625, abs=0.001)

    def test_zero_ab(self):
        assert calculate_slg(10, 5, 1, 3, 0) == 0.0

    def test_singles_only(self):
        assert calculate_slg(100, 0, 0, 0, 400) == pytest.approx(0.250)

    def test_all_hr(self):
        assert calculate_slg(0, 0, 0, 10, 10) == pytest.approx(4.000)


class TestOPS:
    def test_normal(self):
        assert calculate_ops(0.350, 0.500) == pytest.approx(0.850)

    def test_zero(self):
        assert calculate_ops(0.0, 0.0) == 0.0

    def test_elite(self):
        assert calculate_ops(0.420, 0.680) == pytest.approx(1.100)


class TestISO:
    def test_normal(self):
        assert calculate_iso(0.500, 0.280) == pytest.approx(0.220)

    def test_zero_power(self):
        # Singles-only hitter: SLG ≈ AVG
        assert calculate_iso(0.280, 0.280) == pytest.approx(0.000)


class TestBBRate:
    def test_normal(self):
        result = calculate_bb_rate(60, 600)
        assert result == pytest.approx(0.100)

    def test_zero_pa(self):
        assert calculate_bb_rate(5, 0) == 0.0


class TestKRate:
    def test_normal(self):
        result = calculate_k_rate(180, 600)
        assert result == pytest.approx(0.300)

    def test_zero_pa(self):
        assert calculate_k_rate(10, 0) == 0.0


class TestBABIP:
    def test_normal(self):
        result = calculate_babip(h=150, hr=20, ab=500, so=80, sf=5)
        assert result == pytest.approx(130 / 405, abs=0.001)

    def test_zero_denominator(self):
        assert calculate_babip(0, 0, 0, 0, 0) == 0.0

    def test_no_babip_events(self):
        # ab=HR+SO: all hits are HRs or all outs are Ks
        assert calculate_babip(h=10, hr=10, ab=50, so=40, sf=0) == 0.0


class TestWOBA:
    def test_normal(self):
        result = calculate_woba(
            ubb=40, hbp=5, singles=80, doubles=25, triples=3, hr=20,
            ab=400, ibb=0, sf=5,
        )
        assert 0.300 < result < 0.420

    def test_zero_denominator(self):
        assert calculate_woba(0, 0, 0, 0, 0, 0, 0, 0, 0) == 0.0

    def test_ibb_excluded(self):
        r1 = calculate_woba(ubb=10, hbp=0, singles=50, doubles=10, triples=0, hr=5, ab=200)
        r2 = calculate_woba(ubb=10, hbp=0, singles=50, doubles=10, triples=0, hr=5, ab=200, ibb=20)
        assert r1 == r2


class TestWRAA:
    def test_above_average(self):
        result = calculate_wraa(woba=0.380, league_woba=0.320, pa=500, woba_scale=1.15)
        assert result > 0

    def test_below_average(self):
        result = calculate_wraa(woba=0.260, league_woba=0.320, pa=500, woba_scale=1.15)
        assert result < 0

    def test_league_average(self):
        result = calculate_wraa(woba=0.320, league_woba=0.320, pa=500, woba_scale=1.15)
        assert result == pytest.approx(0.0)

    def test_zero_scale(self):
        assert calculate_wraa(0.350, 0.320, 500, 0.0) == 0.0


class TestWRC:
    def test_above_average(self):
        wraa = calculate_wraa(0.380, 0.320, 500, 1.15)
        result = calculate_wrc(wraa, league_runs_per_pa=0.120, pa=500)
        assert result > 0

    def test_components(self):
        wraa = 10.0
        result = calculate_wrc(wraa, league_runs_per_pa=0.1, pa=100)
        assert result == pytest.approx(10.0 + 0.1 * 100, abs=0.1)


class TestWRCPlus:
    def test_above_average(self):
        result = calculate_wrc_plus(wrc_per_pa=0.15, league_wrc_per_pa=0.12)
        assert result > 100

    def test_league_average(self):
        result = calculate_wrc_plus(wrc_per_pa=0.12, league_wrc_per_pa=0.12)
        assert result == 100

    def test_zero_denominator(self):
        assert calculate_wrc_plus(0.12, 0.0) == 0
