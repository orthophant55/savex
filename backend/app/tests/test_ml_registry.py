"""ML registry and model unit tests."""

import pytest

from app.ml.registry import registry
from app.ml.contracts import (
    GameStateInput,
    PlayerProjectionInput,
    RegressionAdjustedBattingInput,
)


class TestModelRegistry:
    def test_get_win_probability(self):
        model = registry.get("win_probability")
        assert model is not None

    def test_get_player_projection(self):
        model = registry.get("player_projection")
        assert model is not None

    def test_get_article_topic(self):
        model = registry.get("article_topic")
        assert model is not None

    def test_get_regression_adjusted_batting(self):
        model = registry.get("regression_adjusted_batting")
        assert model is not None

    def test_get_slump_risk(self):
        model = registry.get("slump_risk")
        assert model is not None

    def test_unknown_model_raises(self):
        with pytest.raises(KeyError):
            registry.get("nonexistent_model_xyz")


class TestWinProbabilityModel:
    @pytest.fixture
    def model(self):
        return registry.get("win_probability")

    def test_predict_returns_output(self, model):
        state = GameStateInput(
            inning=9, inning_half="bottom", outs=0,
            away_score=3, home_score=3, base_state="000",
        )
        out = model.predict(state)
        assert 0 <= out.home_win_probability <= 1
        assert 0 <= out.away_win_probability <= 1
        assert out.model_name is not None
        assert out.model_version is not None

    def test_probabilities_sum_to_one(self, model):
        state = GameStateInput(
            inning=7, inning_half="top", outs=1,
            away_score=2, home_score=1, base_state="100",
        )
        out = model.predict(state)
        total = out.home_win_probability + out.away_win_probability
        assert abs(total - 1.0) < 0.01

    def test_home_leads_late_inning(self, model):
        state = GameStateInput(
            inning=9, inning_half="bottom", outs=2,
            away_score=0, home_score=5, base_state="000",
        )
        out = model.predict(state)
        assert out.home_win_probability > 0.5

    def test_confidence_in_range(self, model):
        state = GameStateInput(
            inning=1, inning_half="top", outs=0,
            away_score=0, home_score=0, base_state="000",
        )
        out = model.predict(state)
        assert 0 <= out.confidence <= 1


class TestPlayerProjectionModel:
    @pytest.fixture
    def model(self):
        return registry.get("player_projection")

    def test_predict_returns_output(self, model):
        inp = PlayerProjectionInput(
            player_id="KIA001",
            season=2025,
            recent_stats={"avg": 0.320, "ops": 0.950},
        )
        out = model.predict(inp)
        assert out.model_name is not None
        assert out.model_version is not None
        assert 0 <= out.confidence <= 1


class TestRegressionAdjustedBattingModel:
    @pytest.fixture
    def model(self):
        return registry.get("regression_adjusted_batting")

    def test_shrinks_to_league_average(self, model):
        inp = RegressionAdjustedBattingInput(
            player_id="test001",
            ab=10,
            h=8,  # .800 observed, should shrink toward .269
            league_avg=0.269,
            prior_strength=100,
        )
        out = model.predict(inp)
        assert out.adjusted_avg < 0.800
        assert out.adjusted_avg >= 0.269

    def test_reliability_increases_with_sample(self, model):
        small = RegressionAdjustedBattingInput(
            player_id="t1", ab=20, h=6, league_avg=0.269, prior_strength=100,
        )
        large = RegressionAdjustedBattingInput(
            player_id="t1", ab=500, h=150, league_avg=0.269, prior_strength=100,
        )
        out_small = model.predict(small)
        out_large = model.predict(large)
        assert out_small.reliability_score < out_large.reliability_score

    def test_reliability_score_in_range(self, model):
        inp = RegressionAdjustedBattingInput(
            player_id="t1", ab=300, h=90, league_avg=0.269, prior_strength=100,
        )
        out = model.predict(inp)
        assert 0 <= out.reliability_score <= 1

    def test_has_all_required_fields(self, model):
        inp = RegressionAdjustedBattingInput(
            player_id="t1", ab=200, h=60, league_avg=0.269, prior_strength=100,
        )
        out = model.predict(inp)
        assert hasattr(out, "observed_avg")
        assert hasattr(out, "adjusted_avg")
        assert hasattr(out, "reliability_score")
        assert hasattr(out, "shrinkage_amount")
        assert hasattr(out, "confidence")
        assert hasattr(out, "model_name")
        assert hasattr(out, "model_version")
