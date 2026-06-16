"""Mock streaming text generator.

NOTE: This is a MOCK implementation. No LLM API is called.
All text is pre-written template content yielded in chunks with simulated delays.
Replace with real LLM streaming when LLM_PROVIDER != "mock".
"""

import asyncio
import random
from typing import AsyncGenerator

from app.schemas.article import Article
from app.schemas.kbo import Game, Player, Team


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


async def stream_team_analysis(team: Team) -> AsyncGenerator[str, None]:
    """Generate a mock team analysis as a streaming text response."""
    body = (
        f"## {team.name_ko} 팀 분석 (2025)\n\n"
        f"**팀 개요**\n"
        f"- 홈구장: {team.stadium} ({team.home_city})\n\n"
        f"**공격 요약**\n"
        f"- 팀 OPS .761 (리그 평균 수준)\n"
        f"- 팀 wOBA .320 — 기대 득점에 부합\n"
        f"- 득점 생산 효율: wRC+ 102\n\n"
        f"**투수 요약**\n"
        f"- 팀 ERA 4.20 / FIP 4.05\n"
        f"- FIP < ERA: 수비·운 혜택 일부 존재 → 추후 ERA 상승 가능성\n"
        f"- 불펜 홀드율 63%로 준수\n\n"
        f"**피타고라스 기대승률 분석**\n"
        f"- 득실점 기반 기대승률: .550\n"
        f"- 실제 승률: .578\n"
        f"- 실제 - 기대: +2.5승 → 클러치 or 불펜 강도\n\n"
        f"**전망**\n"
        f"- 기대승률 대비 과수행 중. 후반기 회귀 가능성 점검 필요.\n"
        f"- wRC+가 지속되면 상위권 유지 가능.\n\n"
        f"> ⚠️ MOCK AI 생성 콘텐츠입니다. 실제 수치와 다를 수 있습니다.\n\n"
        f"[DONE]"
    )
    for chunk in _chunks(body, size=random.randint(15, 35)):
        yield chunk
        await asyncio.sleep(random.uniform(0.08, 0.25))


async def stream_sabermetric_column(
    topic: str, metric_names: list[str]
) -> AsyncGenerator[str, None]:
    """Generate a mock sabermetric column as a streaming text response."""
    metrics_str = ", ".join(metric_names) if metric_names else "wOBA, FIP, WAR"
    body = (
        f"## 세이버매트릭스 칼럼: {topic}\n\n"
        f"**다루는 지표**: {metrics_str}\n\n"
        f"**핵심 개념**\n"
        f"야구 기록은 단순한 결과가 아니라 득점가치·승리기여·예측값으로 변환될 수 있다.\n"
        f"이 칼럼에서는 '{topic}'를 중심으로 KBO에서의 적용 방법을 살펴본다.\n\n"
        f"**wOBA (가중 출루율)**\n"
        f"- 단타, 2루타, 홈런, 볼넷의 실제 득점가치를 반영한 출루율 스케일 지표\n"
        f"- OPS보다 정확하게 타격 생산성을 측정함\n"
        f"- KBO 전용 가중치는 KBO RE table 기반 추정 필요 (현재 MLB placeholder 사용 중)\n\n"
        f"**FIP (수비무관 평균자책점)**\n"
        f"- HR, BB, HBP, K처럼 투수가 직접 통제하는 이벤트만 반영\n"
        f"- ERA와 FIP의 차이가 크면 수비·운 영향을 의심해야 함\n"
        f"- KBO FIP constant는 lgERA = lgFIP가 되도록 조정 필요\n\n"
        f"**KBO 적용 시 주의점**\n"
        f"- KBO 공개 데이터 한계로 일부 지표는 MLB 파라미터를 placeholder로 사용\n"
        f"- 구장 효과, 리그 득점환경, 시즌별 편차를 반드시 고려해야 함\n"
        f"- Statcast급 트래킹 데이터 없이는 xBA, xwOBA, HardHit% 구현 불가\n\n"
        f"> ⚠️ MOCK AI 생성 콘텐츠입니다. 실제 분석과 다를 수 있습니다.\n\n"
        f"[DONE]"
    )
    for chunk in _chunks(body, size=random.randint(15, 35)):
        yield chunk
        await asyncio.sleep(random.uniform(0.08, 0.25))
