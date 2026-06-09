/**
 * AI 경기 요약 Mock Streaming API
 *
 * 실제 LLM 연동 시 교체 포인트:
 *   1. generateGameRecapText() → Anthropic/OpenAI API 호출
 *   2. 아래 ReadableStream의 청크 방식 → SDK의 stream().on('text', ...) 패턴
 *   3. API 키는 반드시 서버 환경변수로만 관리 (브라우저에 절대 노출 금지)
 */

import { NextRequest, NextResponse } from "next/server";
import { getGameById, getTeamById } from "@/lib/api/kbo";
import type { Game } from "@/lib/types/kbo";

function delay(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms));
}

function splitToChunks(text: string): string[] {
  const result: string[] = [];
  const lines = text.split("\n");
  lines.forEach((line, li) => {
    const words = line.split(/\s+/).filter(Boolean);
    for (let i = 0; i < words.length; i += 3) {
      const group = words.slice(i, i + 3).join(" ");
      result.push(i + 3 < words.length ? group + " " : group);
    }
    if (li < lines.length - 1) result.push("\n");
  });
  return result.filter((s) => s.length > 0);
}

async function generateGameRecapText(game: Game): Promise<string> {
  const [awayTeam, homeTeam] = await Promise.all([
    getTeamById(game.awayTeamId),
    getTeamById(game.homeTeamId),
  ]);
  const away = awayTeam?.name ?? game.awayTeamId;
  const home = homeTeam?.name ?? game.homeTeamId;

  if (game.status === "scheduled") {
    return `# ${away} vs ${home} — 프리뷰

오늘 ${game.startTime} ${game.stadium}에서 ${away}와 ${home}의 경기가 예정되어 있다.

## 선발 매치업

${game.awayStartingPitcher ? `${away}는 ${game.awayStartingPitcher}를` : `${away}의`} 선발로 내세웠고, ${game.homeStartingPitcher ? `${home}는 ${game.homeStartingPitcher}가` : `${home}의 선발이`} 마운드에 오른다.

## 관전 포인트

두 팀의 최근 흐름과 선발 투수의 컨디션이 경기의 향방을 가를 전망이다. 세이버 지표 기반으로 볼 때 홈 어드밴티지와 불펜 깊이가 승패를 가를 핵심 변수다.`;
  }

  if (game.status === "live") {
    const awayScore = game.awayScore ?? 0;
    const homeScore = game.homeScore ?? 0;
    const leader = awayScore > homeScore ? away : homeScore > awayScore ? home : null;
    const inningStr = `${game.currentInning}회 ${game.isTopInning ? "초" : "말"}`;

    return `# ${away} vs ${home} — 실시간 분석 (${inningStr})

현재 ${inningStr}, ${awayScore === homeScore ? "동점 상황" : `${leader}가 ${Math.abs(awayScore - homeScore)}점 앞서고 있다`}. (${away} ${awayScore} : ${homeScore} ${home})

## 경기 흐름

${game.playByPlay?.length ? `총 ${game.playByPlay.length}번의 주요 플레이가 기록됐다. ` : ""}중반 이후 승부가 결정될 가능성이 높으며, 불펜 운용이 핵심 변수가 될 전망이다.

## 세이버 분석

현재까지의 경기에서 기대득점(xR)과 실제 득점의 격차를 주목해야 한다. LI(레버리지 인덱스)가 높은 상황에서의 타석 결과가 최종 승패를 가를 것이다.`;
  }

  // Final game
  const awayScore = game.awayScore ?? 0;
  const homeScore = game.homeScore ?? 0;
  const winner = awayScore > homeScore ? away : home;
  const loser = awayScore > homeScore ? home : away;
  const winScore = Math.max(awayScore, homeScore);
  const loseScore = Math.min(awayScore, homeScore);

  const topWpa = (game.playByPlay ?? [])
    .sort((a, b) => Math.abs(b.wpa) - Math.abs(a.wpa))
    .slice(0, 2);

  return `# ${winner} ${winScore}-${loseScore} ${loser} — 세이버매트릭스 경기 분석

${winner}이(가) ${game.stadium}에서 ${loser}를 ${winScore}-${loseScore}로 꺾었다.${game.awayStartingPitcher || game.homeStartingPitcher ? ` 선발 ${game.awayTeamId === (awayScore > homeScore ? game.awayTeamId : game.homeTeamId) ? game.awayStartingPitcher : game.homeStartingPitcher}의 호투가 승리를 이끌었다.` : ""}

## 경기 흐름

${topWpa.length > 0
      ? topWpa
          .map(
            (p) =>
              `${p.inning}회 ${p.isTop ? "초" : "말"} ${p.description}(WPA ${p.wpa > 0 ? "+" : ""}${p.wpa.toFixed(2)})${p.li >= 1.2 ? ` — 레버리지 ${p.li.toFixed(1)}의 고비였다` : ""}.`
          )
          .join(" ")
      : "경기는 초반 리드를 지켜낸 팀이 결국 승리를 가져갔다."}

## 선발 투수 분석

${game.awayStartingPitcher
      ? `${game.awayTeamId === (awayScore > homeScore ? game.awayTeamId : game.homeTeamId)
          ? `승리 투수 ${game.awayStartingPitcher ?? game.homeStartingPitcher}는 오늘 경기에서 안정적인 투구를 이어갔다. FIP 기준으로 볼 때 구위와 제구 모두 시즌 평균 이상의 내용이었다.`
          : `선발 ${game.homeStartingPitcher}는 오늘 패전을 기록했으나, 피칭 내용은 결과보다 나았다. 수비 실책(E: ${game.boxScore?.homeErrors ?? 0})이 점수를 불리게 만든 측면이 있다.`
        }`
      : "양 팀 선발 모두 인상적인 피칭을 선보였다."}

## WPA 분석

오늘 경기에서 승리 기여도(WPA)를 가장 많이 올린 플레이어는 결정적 상황에서 팀에 도움이 된 선수였다. WPA는 단순 득점보다 승리 확률 변화를 반영하기 때문에, 작은 안타 하나가 홈런보다 높은 WPA를 기록하는 경우도 있다.

## 총평

${winner}은 이번 승리로 리그 내 위상을 높였다. 반면 ${loser}는 ${loseScore}득점에 그쳐 타선 개선이 시급해 보인다. 특히 RISP(득점권 상황) 타율 향상이 후반기 성적의 관건이 될 것이다.`;
}

export async function POST(req: NextRequest) {
  let body: { gameId?: string };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON" }, { status: 400 });
  }

  const { gameId } = body;
  if (!gameId) {
    return NextResponse.json({ error: "gameId is required" }, { status: 400 });
  }

  const game = await getGameById(gameId);
  const text = await generateGameRecapText(
    game ?? {
      id: gameId,
      date: new Date().toISOString().slice(0, 10),
      startTime: "18:30",
      awayTeamId: "TBD",
      homeTeamId: "TBD",
      stadium: "미정",
      status: "scheduled",
      awayScore: null,
      homeScore: null,
    }
  );

  const chunks = splitToChunks(text);

  const stream = new ReadableStream({
    async start(controller) {
      const encoder = new TextEncoder();
      for (const chunk of chunks) {
        // 줄바꿈은 빠르게, 단어는 80~200ms 간격으로
        const ms = chunk === "\n" ? 20 : 80 + Math.floor(Math.random() * 120);
        await delay(ms);
        controller.enqueue(encoder.encode(chunk));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-cache, no-transform",
      "X-Content-Type-Options": "nosniff",
    },
  });
}
