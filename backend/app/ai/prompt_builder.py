"""Prompt builder for LLM-based generation.

When LLM_PROVIDER != "mock", wire these functions into generation_service.py.
Prompts are in Korean to match the KBO Insight audience.
"""

from typing import Any, Dict

from app.schemas.kbo import Game, Player


def build_game_recap_prompt(game: Game, context: Dict[str, Any]) -> str:
    # TODO: Replace mock streaming with real LLM call using this prompt.
    away = context.get("away_team_name", game.away_team_id)
    home = context.get("home_team_name", game.home_team_id)
    prompt = (
        f"다음 KBO 경기를 세이버매트릭스 관점에서 분석하는 500자 이내의 경기 리캡 기사를 작성하라.\n\n"
        f"경기: {away} {game.away_score} vs {home} {game.home_score} ({game.status.value})\n"
        f"날짜: {game.game_date}, 경기장: {game.stadium}\n\n"
        f"포함 항목:\n"
        f"1. 경기 결과 요약\n"
        f"2. WPA 기준 MVP 플레이\n"
        f"3. 선발 투수 FIP vs ERA 비교\n"
        f"4. 한국어로 작성할 것\n"
    )
    return prompt


def build_player_analysis_prompt(player: Player, context: Dict[str, Any]) -> str:
    # TODO: Replace mock streaming with real LLM call using this prompt.
    team = context.get("team_name", player.team_id)
    stat = player.season_stat
    stat_summary = ""
    if stat:
        if stat.avg is not None:
            stat_summary = f"타율 {stat.avg}, OPS {stat.ops}, wRC+ {stat.wrc_plus}, WAR {stat.war_bat}"
        elif stat.era is not None:
            stat_summary = f"ERA {stat.era}, FIP {stat.fip}, K/9 {stat.k_per_9}, WAR {stat.war_pit}"

    prompt = (
        f"다음 KBO 선수를 세이버매트릭스 관점에서 분석하라.\n\n"
        f"선수: {player.name_ko} ({team}, {player.position})\n"
        f"2025 시즌 주요 지표: {stat_summary}\n\n"
        f"분석 항목:\n"
        f"1. 강점\n"
        f"2. 약점\n"
        f"3. 최근 흐름\n"
        f"4. 회귀 가능성 (BABIP, FIP 기반)\n"
        f"5. 한국어로 작성할 것\n"
    )
    return prompt
