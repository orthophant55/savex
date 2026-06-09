"""Player projection model — dummy placeholder.

Replace predict() with a trained regression model (sklearn, LightGBM, etc.)
loaded at startup via ModelRegistry.
"""

from app.ml.contracts import PlayerProjectionInput, PlayerProjectionOutput


class PlayerProjectionModel:
    model_name = "player_projection_v0"
    model_version = "0.1.0-dummy"

    def predict(self, input: PlayerProjectionInput) -> PlayerProjectionOutput:
        # Dummy: return recent stats with negligible regression-to-mean adjustment
        recent = input.recent_stats
        projected_avg = None
        projected_ops = None
        projected_era = None
        projected_war = None

        if "avg" in recent:
            # Slight regression toward .280 league average
            projected_avg = round(recent["avg"] * 0.95 + 0.280 * 0.05, 3)
        if "ops" in recent:
            projected_ops = round(recent["ops"] * 0.95 + 0.750 * 0.05, 3)
        if "era" in recent:
            projected_era = round(recent["era"] * 0.95 + 4.00 * 0.05, 2)
        if "war" in recent:
            projected_war = round(recent["war"] * 0.90, 2)

        return PlayerProjectionOutput(
            projected_avg=projected_avg,
            projected_ops=projected_ops,
            projected_era=projected_era,
            projected_war=projected_war,
            confidence=0.4,
            model_name=self.model_name,
            model_version=self.model_version,
        )
