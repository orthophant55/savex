"""Win Probability model — rule-based placeholder.

Replace predict() with a trained model (e.g. LightGBM, sklearn, PyTorch)
loaded via ModelRegistry without changing the contract.
"""

from app.analytics.sabermetrics.wpa import clamp_probability
from app.ml.contracts import GameStateInput, WinProbabilityOutput


class WinProbabilityModel:
    model_name = "win_probability_v0"
    model_version = "0.1.0-rule-based"

    def predict(self, state: GameStateInput) -> WinProbabilityOutput:
        # Rule-based heuristic:
        # Base probability 0.5, adjusted by run differential and inning progress.
        total_innings = 9
        inning_progress = min(state.inning / total_innings, 1.0)

        # Late innings + large lead → higher confidence
        run_diff = state.home_score - state.away_score
        run_factor = run_diff * 0.06 * inning_progress

        # Bottom half of inning: home team slight advantage
        half_factor = 0.01 if state.inning_half == "bottom" else 0.0

        home_wp = clamp_probability(0.50 + run_factor + half_factor)
        away_wp = clamp_probability(1.0 - home_wp)

        confidence = min(0.5 + inning_progress * 0.4, 0.9)

        return WinProbabilityOutput(
            home_win_probability=round(home_wp, 4),
            away_win_probability=round(away_wp, 4),
            confidence=round(confidence, 3),
            model_name=self.model_name,
            model_version=self.model_version,
        )
