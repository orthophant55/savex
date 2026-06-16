"""Slump risk model — placeholder.

Estimates slump risk based on BABIP deviation, K%, BB%, recent OPS,
and sample size.  Returns a mock risk score.

TODO: Train on KBO player game-log data.
"""

from pydantic import BaseModel


class SlumpRiskInput(BaseModel):
    player_id: str
    babip: float = 0.300
    k_rate: float = 0.200
    bb_rate: float = 0.080
    recent_ops: float = 0.750
    sample_size: int = 100


class SlumpRiskOutput(BaseModel):
    player_id: str
    risk_score: float   # 0~1, higher = higher slump risk
    risk_label: str     # "low" | "medium" | "high"
    factors: list[str]
    model_name: str
    model_version: str


class SlumpRiskModel:
    model_name = "slump_risk"
    model_version = "v0.1.0-placeholder"

    def predict(self, inp: SlumpRiskInput) -> SlumpRiskOutput:
        factors: list[str] = []
        score = 0.0

        # BABIP significantly above .350 suggests positive luck → regression risk
        if inp.babip > 0.350:
            score += 0.25
            factors.append(f"BABIP {inp.babip:.3f}가 리그 평균 초과 → 회귀 가능성")

        # High K rate increases slump risk
        if inp.k_rate > 0.280:
            score += 0.20
            factors.append(f"K% {inp.k_rate:.1%} 높음")

        # Low BB rate reduces plate discipline signal
        if inp.bb_rate < 0.060:
            score += 0.10
            factors.append(f"BB% {inp.bb_rate:.1%} 낮음")

        # Low recent OPS
        if inp.recent_ops < 0.700:
            score += 0.25
            factors.append(f"최근 OPS {inp.recent_ops:.3f} 하락")

        # Small sample = high uncertainty = high risk by default
        if inp.sample_size < 80:
            score += 0.20
            factors.append(f"표본 {inp.sample_size} PA — 불안정 구간")

        score = min(round(score, 3), 1.0)
        if score >= 0.60:
            label = "high"
        elif score >= 0.35:
            label = "medium"
        else:
            label = "low"

        return SlumpRiskOutput(
            player_id=inp.player_id,
            risk_score=score,
            risk_label=label,
            factors=factors if factors else ["정상 범위"],
            model_name=self.model_name,
            model_version=self.model_version,
        )
