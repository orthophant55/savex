"""Mock streaming text generator.

NOTE: This is a MOCK implementation. No LLM API is called.
All text is pre-written template content yielded in chunks with simulated delays.
Replace with real LLM streaming when LLM_PROVIDER != "mock".
"""

import asyncio
import random
from typing import AsyncGenerator

from app.schemas.article import Article
from app.schemas.kbo import Game, Player


def _chunks(text: str, size: int = 20):
    """Split text into chunks of approximately `size` characters."""
    for i in range(0, len(text), size):
        yield text[i: i + size]


async def stream_game_recap(game: Game) -> AsyncGenerator[str, None]:
    """Generate a mock KBO game recap as a streaming text response."""
    away = game.away_team_id
    home = game.home_team_id
    away_score = game.away_score
    home_score = game.home_score
    winner = away if away_score > home_score else home
    loser = home if away_score > home_score else away
    score_str = f"{away_score}-{home_score}"

    # Summarize top WPA play if available
    top_play = ""
    if game.play_events:
        scoring = [e for e in game.play_events if e.is_scoring_play and e.wpa is not None]
        if scoring:
            best = max(scoring, key=lambda e: abs(e.wpa or 0))
            top_play = f"\n\n**최고 WPA 플레이 (+{best.wpa:.3f})**\n{best.description}"

    recap_text = (
        f"## {away} vs {home} 경기 리캡\n\n"
        f"{away}가 {game.game_date} {game.stadium}에서 열린 경기에서 "
        f"{home}를 {score_str}으로 {'제압' if away_score > home_score else '격파'}했다.\n\n"
        f"{'원정팀 ' + away if away_score > home_score else '홈팀 ' + home}는 "
        f"{'끈질긴 추격을 뿌리치고 승리를 거뒀다.' if abs(away_score - home_score) <= 2 else '압도적인 경기력으로 승리했다.'}"
        f"{top_play}\n\n"
        f"**세이버매트릭스 분석**\n"
        f"- 득점권 타율: {winner} .341 vs {loser} .198\n"
        f"- 선발 FIP: {away} 선발 3.42 / {home} 선발 4.15\n"
        f"- 팀 wOBA: {winner} .358 / {loser} .302\n\n"
        f"> ⚠️ 이 분석은 MOCK AI가 생성한 콘텐츠입니다. 실제 수치와 다를 수 있습니다.\n\n"
        f"[DONE]"
    )

    for chunk in _chunks(recap_text, size=random.randint(15, 35)):
        yield chunk
        await asyncio.sleep(random.uniform(0.08, 0.25))


async def stream_player_analysis(player: Player) -> AsyncGenerator[str, None]:
    """Generate a mock player analysis as a streaming text response."""
    stat = player.season_stat
    is_pitcher = stat and stat.era is not None

    if is_pitcher:
        era = stat.era or 0.0
        fip = stat.fip or 0.0
        k9 = stat.k_per_9 or 0.0
        war = stat.war_pit or 0.0
        body = (
            f"## {player.name_ko} 투수 분석 (2025)\n\n"
            f"**강점**\n"
            f"- ERA {era:.2f}, FIP {fip:.2f}로 리그 상위권 안정성 유지\n"
            f"- K/9 {k9:.1f}: 삼진 능력 우수\n\n"
            f"**약점**\n"
            f"- FIP-ERA 차이 {fip - era:+.2f} → 수비 의존도 점검 필요\n"
            f"- BABIP 운영 변동성 존재\n\n"
            f"**최근 흐름**\n"
            f"- 최근 5경기 평균 이닝: 6.1, 자책점 2.2\n"
            f"- 구속 소폭 하락 (−0.8 km/h)\n\n"
            f"**회귀 가능성**\n"
            f"- FIP > ERA인 경우 ERA 상승 가능성 존재\n"
            f"- WAR {war:.1f}은 현 페이스 유지 시 시즌 말 {war * 2:.1f} 달성 예상\n\n"
            f"> ⚠️ MOCK AI 생성 콘텐츠입니다.\n\n"
            f"[DONE]"
        )
    else:
        avg = (stat.avg or 0.0) if stat else 0.0
        ops = (stat.ops or 0.0) if stat else 0.0
        wrc = (stat.wrc_plus or 100) if stat else 100
        babip = (stat.babip or 0.0) if stat else 0.0
        war = (stat.war_bat or 0.0) if stat else 0.0
        body = (
            f"## {player.name_ko} 타자 분석 (2025)\n\n"
            f"**강점**\n"
            f"- OPS {ops:.3f}, wRC+ {wrc}: 리그 평균 대비 {wrc - 100:+d}% 우수\n"
            f"- 타율 {avg:.3f}로 꾸준한 컨택 능력\n\n"
            f"**약점**\n"
            f"- 삼진 비율 관리 필요\n"
            f"- 상대 좌완 투수 대비 OPS 0.072 하락\n\n"
            f"**최근 흐름**\n"
            f"- 최근 15경기 타율 {avg + 0.018:.3f}: 정상 페이스\n"
            f"- 홈런 페이스 유지 중\n\n"
            f"**회귀 가능성**\n"
            f"- BABIP {babip:.3f}은 리그 평균 수준으로 지속 가능\n"
            f"- WAR {war:.1f} → 풀시즌 환산 {war * 2:.1f} WAR 예상\n\n"
            f"> ⚠️ MOCK AI 생성 콘텐츠입니다.\n\n"
            f"[DONE]"
        )

    for chunk in _chunks(body, size=random.randint(15, 35)):
        yield chunk
        await asyncio.sleep(random.uniform(0.08, 0.25))
