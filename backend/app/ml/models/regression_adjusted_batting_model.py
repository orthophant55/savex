"""Regression-adjusted batting model (empirical Bayes / shrinkage placeholder).

Based on Efron & Morris (1975) James-Stein shrinkage and Brown (2008)
in-season batting average prediction approach.

Replace with a proper hierarchical Bayesian implementation when KBO historical
data is available.
"""

from app.analytics.sabermetrics.regression_adjustment import (
    calculate_regression_adjusted_avg,
    calculate_regression_adjusted_ops,
    calculate_reliability,
)
from app.analytics.constants.kbo_environment import (
    KBO_LEAGUE_AVG,
    KBO_LEAGUE_OPS,
    STABILIZATION_POINTS,
)
from app.ml.contracts import RegressionAdjustedBattingInput, RegressionAdjustedBattingOutput


class RegressionAdjustedBattingModel:
    model_name = "regression_adjusted_batting"
    model_version = "v0.1.0-shrinkage"

    def predict(
        self, inp: RegressionAdjustedBattingInput
    ) -> RegressionAdjustedBattingOutput:
        observed_avg = inp.h / inp.ab if inp.ab > 0 else inp.league_avg
        adjusted_avg = calculate_regression_adjusted_avg(
            h=inp.h,
            ab=inp.ab,
            league_avg=inp.league_avg,
            prior_strength=inp.prior_strength,
        )
        reliability = calculate_reliability(
            sample_size=inp.ab,
            stabilization_point=STABILIZATION_POINTS["AVG"],
        )
        shrinkage = round(observed_avg - adjusted_avg, 4)

        return RegressionAdjustedBattingOutput(
            observed_avg=round(observed_avg, 3),
            adjusted_avg=round(adjusted_avg, 3),
            reliability_score=round(reliability, 3),
            shrinkage_amount=shrinkage,
            confidence=round(reliability * 0.9, 3),
            model_name=self.model_name,
            model_version=self.model_version,
        )
