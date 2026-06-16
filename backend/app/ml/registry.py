"""Model registry.

Usage:
    from app.ml.registry import registry
    model = registry.get("win_probability")
    output = model.predict(state)

To swap in a real model:
    registry.register("win_probability", "1.0.0-lgbm", RealWinProbModel())
"""

from typing import Any, Dict


class ModelRegistry:
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}  # {name: {version: model}}
        self._latest: Dict[str, str] = {}             # {name: latest_version}

    def register(self, name: str, version: str, model: Any) -> None:
        if name not in self._store:
            self._store[name] = {}
        self._store[name][version] = model
        self._latest[name] = version

    def get(self, name: str, version: str = "latest") -> Any:
        if name not in self._store:
            raise KeyError(f"Model '{name}' not registered")
        if version == "latest":
            version = self._latest[name]
        if version not in self._store[name]:
            raise KeyError(f"Model '{name}' version '{version}' not found")
        return self._store[name][version]


def _build_registry() -> ModelRegistry:
    from app.ml.models.win_probability_model import WinProbabilityModel
    from app.ml.models.player_projection_model import PlayerProjectionModel
    from app.ml.models.article_topic_model import ArticleTopicModel
    from app.ml.models.regression_adjusted_batting_model import RegressionAdjustedBattingModel
    from app.ml.models.slump_risk_model import SlumpRiskModel

    reg = ModelRegistry()
    reg.register("win_probability",              "0.1.0-rule-based", WinProbabilityModel())
    reg.register("player_projection",            "0.1.0-dummy",      PlayerProjectionModel())
    reg.register("article_topic",                "0.1.0-mock",       ArticleTopicModel())
    reg.register("regression_adjusted_batting",  "0.1.0-shrinkage",  RegressionAdjustedBattingModel())
    reg.register("slump_risk",                   "0.1.0-placeholder", SlumpRiskModel())
    return reg


registry = _build_registry()
