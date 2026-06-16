"""API integration tests using FastAPI TestClient.

Run: cd backend && pytest -v
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["mock_mode"] is True


def test_teams_returns_10():
    res = client.get("/api/v1/teams")
    assert res.status_code == 200
    teams = res.json()
    assert len(teams) == 10


def test_team_by_id():
    res = client.get("/api/v1/teams/KIA")
    assert res.status_code == 200
    team = res.json()
    assert team["id"] == "KIA"
    assert "name_ko" in team


def test_team_not_found():
    res = client.get("/api/v1/teams/UNKNOWN")
    assert res.status_code == 404


def test_players_returns_30():
    res = client.get("/api/v1/players")
    assert res.status_code == 200
    assert len(res.json()) == 30


def test_players_filter_by_team():
    res = client.get("/api/v1/players?team_id=LG")
    assert res.status_code == 200
    players = res.json()
    assert len(players) == 3
    assert all(p["team_id"] == "LG" for p in players)


def test_player_by_id():
    res = client.get("/api/v1/players/KIA001")
    assert res.status_code == 200
    assert res.json()["id"] == "KIA001"


def test_player_not_found():
    res = client.get("/api/v1/players/NOBODY999")
    assert res.status_code == 404


def test_today_games_returns_5():
    res = client.get("/api/v1/games/today")
    assert res.status_code == 200
    games = res.json()
    assert len(games) == 5


def test_games_list():
    res = client.get("/api/v1/games")
    assert res.status_code == 200
    assert len(res.json()) == 5


def test_game_detail_has_box_score():
    res = client.get("/api/v1/games/game_1")
    assert res.status_code == 200
    game = res.json()
    assert game["id"] == "game_1"
    assert game["box_score"] is not None
    assert len(game["box_score"]["lines"]) == 9


def test_game_detail_has_play_events():
    res = client.get("/api/v1/games/game_1")
    assert res.status_code == 200
    game = res.json()
    assert game["play_events"] is not None
    assert len(game["play_events"]) >= 12


def test_game_detail_has_win_probability():
    res = client.get("/api/v1/games/game_1")
    assert res.status_code == 200
    game = res.json()
    assert game["win_probability"] is not None
    assert len(game["win_probability"]) >= 12


def test_game_box_score_endpoint():
    res = client.get("/api/v1/games/game_1/box-score")
    assert res.status_code == 200
    bs = res.json()
    assert "lines" in bs
    assert bs["away_total"] == 5
    assert bs["home_total"] == 3


def test_game_play_by_play_endpoint():
    res = client.get("/api/v1/games/game_1/play-by-play")
    assert res.status_code == 200
    events = res.json()
    assert len(events) >= 12


def test_game_win_probability_endpoint():
    res = client.get("/api/v1/games/game_1/win-probability")
    assert res.status_code == 200
    points = res.json()
    assert len(points) >= 12
    # Probabilities should sum to 1.0 (approx)
    for pt in points:
        total = pt["home_win_probability"] + pt["away_win_probability"]
        assert abs(total - 1.0) < 0.01


def test_game_not_found():
    res = client.get("/api/v1/games/NOSUCHGAME")
    assert res.status_code == 404


def test_standings_returns_10():
    res = client.get("/api/v1/standings")
    assert res.status_code == 200
    standings = res.json()
    assert len(standings) == 10
    assert standings[0]["rank"] == 1


def test_stat_leaders_returns_6():
    res = client.get("/api/v1/stat-leaders")
    assert res.status_code == 200
    leaders = res.json()
    assert len(leaders) == 6


def test_articles_list():
    res = client.get("/api/v1/articles")
    assert res.status_code == 200
    articles = res.json()
    assert len(articles) >= 5


def test_articles_filter_by_category():
    res = client.get("/api/v1/articles?category=game_recap")
    assert res.status_code == 200
    articles = res.json()
    assert len(articles) >= 1
    assert all(a["category"] == "game_recap" for a in articles)


def test_article_by_id():
    res = client.get("/api/v1/articles/article_1")
    assert res.status_code == 200
    article = res.json()
    assert article["id"] == "article_1"
    assert "title" in article
    assert "body" in article


def test_article_not_found():
    res = client.get("/api/v1/articles/NO_ARTICLE")
    assert res.status_code == 404


# ── Metrics API ──────────────────────────────────────────────────

def test_metric_definitions():
    res = client.get("/api/v1/metrics/definitions")
    assert res.status_code == 200
    defs = res.json()
    assert len(defs) > 10
    names = [d["name"] for d in defs]
    assert "AVG" in names
    assert "wOBA" in names
    assert "FIP" in names
    assert "WPA" in names


def test_run_expectancy_table():
    res = client.get("/api/v1/metrics/run-expectancy")
    assert res.status_code == 200
    table = res.json()
    assert len(table) == 24


def test_win_expectancy_table():
    res = client.get("/api/v1/metrics/win-expectancy")
    assert res.status_code == 200
    table = res.json()
    assert len(table) > 0


def test_player_metric_summary():
    res = client.get("/api/v1/metrics/players/KIA001/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["player_id"] == "KIA001"
    assert "basic_metrics" in data


def test_team_pythagorean():
    res = client.get("/api/v1/metrics/teams/KIA/pythagorean")
    assert res.status_code == 200
    data = res.json()
    assert data["team_id"] == "KIA"
    assert 0 <= data["pythagorean_wp"] <= 1


def test_game_context_metrics():
    res = client.get("/api/v1/metrics/games/game_1/context")
    assert res.status_code == 200
    data = res.json()
    assert "top_wpa_plays" in data
    assert "high_leverage_plays" in data


# ── Player Projections ───────────────────────────────────────────

def test_player_projection():
    res = client.get("/api/v1/players/LG001/projection")
    assert res.status_code == 200
    data = res.json()
    assert "model_name" in data
    assert "model_version" in data
    assert "confidence" in data


def test_regression_adjusted():
    res = client.get("/api/v1/players/KIA001/regression-adjusted")
    assert res.status_code == 200
    data = res.json()
    assert "observed_avg" in data
    assert "adjusted_avg" in data
    assert "reliability_score" in data
    assert 0 <= data["reliability_score"] <= 1


def test_slump_risk():
    res = client.get("/api/v1/players/LG001/slump-risk")
    assert res.status_code == 200
    data = res.json()
    assert "risk_score" in data
    assert data["risk_label"] in ("low", "medium", "high")


# ── Ingestion API ─────────────────────────────────────────────────

def test_ingestion_status():
    res = client.get("/api/v1/ingestion/status")
    assert res.status_code == 200
    data = res.json()
    assert "kbo_data_enabled" in data
    assert data["kbo_data_enabled"] is False


def test_ingestion_schedule_disabled():
    """When KBO_DATA_ENABLED=false, schedule endpoint should return 403."""
    res = client.post(
        "/api/v1/ingestion/kbo-data/schedule",
        json={"year": 2025, "month": 6, "day": 16, "mode": "daily"},
    )
    assert res.status_code == 403


def test_ingestion_game_data_disabled():
    """When KBO_DATA_ENABLED=false, game-data endpoint should return 403."""
    res = client.post(
        "/api/v1/ingestion/kbo-data/game-data",
        json={"year": 2025, "month": 6, "day": 16},
    )
    assert res.status_code == 403


# ── AI Streaming ──────────────────────────────────────────────────

def test_ai_team_analysis():
    res = client.post("/api/v1/ai/team-analysis", json={"team_id": "LG"})
    assert res.status_code == 200
    content = res.text
    assert len(content) > 0


def test_ai_sabermetric_column():
    res = client.post(
        "/api/v1/ai/sabermetric-column",
        json={"topic": "wOBA와 FIP", "metric_names": ["wOBA", "FIP"]},
    )
    assert res.status_code == 200
    content = res.text
    assert len(content) > 0
