/**
 * AI 선수 분석 Mock Streaming API
 *
 * 실제 LLM 연동 시 교체 포인트:
 *   1. generatePlayerAnalysisText() → Anthropic/OpenAI API 호출로 교체
 *   2. API 키는 반드시 서버 환경변수로만 관리
 */

import { NextRequest, NextResponse } from "next/server";
import { getPlayerById, getTeamById } from "@/lib/api/kbo";
import type { Player } from "@/lib/types/kbo";

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

async function generatePlayerAnalysisText(player: Player): Promise<string> {
  const team = await getTeamById(player.teamId);
  const teamName = team?.name ?? player.teamId;
  const s = player.seasonStat;
  const isPitcher = player.position === "투수";

  if (isPitcher) {
    const fipDiff =
      s.era !== undefined && s.fip !== undefined
        ? Math.abs(s.era - s.fip).toFixed(2)
        : null;
    const eraVsFip =
      s.era !== undefined && s.fip !== undefined
        ? s.era < s.fip
          ? "ERA가 FIP보다 낮아 수비 도움을 받고 있을 가능성이 있다. 후반기 회귀에 주의"
          : s.era > s.fip
          ? "FIP이 ERA보다 낮아 실제 투구 내용이 결과보다 좋다. 성적 개선 여지가 있다"
          : "ERA와 FIP이 수렴하여 성적이 안정적이다"
        : "ERA와 FIP 비교가 어렵다";

    return `# ${player.name} (${teamName}) 투수 분석 리포트

## 강점

${player.name}의 가장 두드러진 강점은 ${s.kPer9 !== undefined && s.kPer9 > 9 ? `압도적인 탈삼진 능력이다. K/9 ${s.kPer9.toFixed(2)}는 리그 최상위권` : `안정적인 제구력이다. BB/9 ${s.bbPer9?.toFixed(2) ?? "N/A"}로 볼넷을 최소화`}하고 있다.

${s.whip !== undefined ? `WHIP ${s.whip.toFixed(2)}는 타자들이 출루하기 매우 어렵다는 것을 보여준다. ` : ""}${s.fip !== undefined ? `FIP ${s.fip.toFixed(2)}은 홈런·볼넷·삼진만 반영한 순수 투구 능력 지표로, ${s.fip < 3.5 ? "리그 엘리트 수준이다" : "리그 평균 이상이다"}.` : ""}

${s.leftOnBasePct !== undefined && s.leftOnBasePct > 75 ? `LOB% ${s.leftOnBasePct.toFixed(1)}%의 높은 잔루처리율은 위기 관리 능력이 탁월함을 입증한다.` : ""}

## 약점

${s.hrPer9 !== undefined && s.hrPer9 > 0.85 ? `HR/9 ${s.hrPer9.toFixed(2)}는 홈런 허용 리스크가 있음을 보여준다. 특히 좌타자 상대 구종 배합을 점검할 필요가 있다.` : s.bbPer9 !== undefined && s.bbPer9 > 3.0 ? `BB/9 ${s.bbPer9.toFixed(2)}의 볼넷 허용은 투구 효율성을 낮추는 요인이다. 스트라이크 선점 능력 향상이 과제다.` : `뚜렷한 약점을 찾기 어렵다. 다만 GB% ${s.groundBallPct?.toFixed(1) ?? "N/A"}%를 기준으로 플라이볼 투수의 성향이 강해, 타구 관리에 지속적인 주의가 필요하다.`}

## 최근 흐름

시즌 ${s.games ?? "N/A"}경기 등판, ${s.innings ? `${Math.floor(s.innings)}이닝` : "N/A"} 소화. ${s.wins2 ?? 0}승 ${s.losses2 ?? 0}패${s.saves !== undefined && s.saves > 0 ? ` ${s.saves}세이브` : ""}${s.holds !== undefined && s.holds > 0 ? ` ${s.holds}홀드` : ""}의 성적이지만, 승패 기록은 팀 득점 지원에 좌우되므로 투구 내용을 독립적으로 봐야 한다.

WAR ${s.war?.toFixed(1) ?? "N/A"}은 현재 ${s.war !== undefined ? (s.war > 4 ? "리그 투수 최상위권" : s.war > 2 ? "리그 상위권" : "평균 이상") : "측정 중"} 수준이다.

## 회귀 가능성

${eraVsFip}. ${fipDiff ? `차이(${fipDiff})가 ${parseFloat(fipDiff) < 0.3 ? "크지 않아 현재 성적의 지속 가능성이 높다" : "다소 있어 후반기 성적 변동 가능성이 있다"}.` : ""}

xFIP ${s.xFip?.toFixed(2) ?? "N/A"} 기준으로 ${s.xFip !== undefined && s.fip !== undefined ? Math.abs(s.xFip - s.fip) < 0.25 ? "FIP과 유사해 현재 수준이 지속될 가능성이 높다" : "FIP과 차이가 있어 홈런 운에 따른 변동이 예상된다" : "분석 중"}.

종합 평가: ${player.name}은 ${teamName}의 핵심 전력으로, ${s.war !== undefined && s.war > 3 ? "리그 정상급 실력을 갖추고 있다" : "안정적인 역할을 수행하고 있다"}. 남은 시즌에도 현재 페이스를 유지한다면 팀 순위에 결정적인 기여를 할 것으로 기대된다.`;
  }

  // Batter
  const opsLabel =
    s.ops !== undefined
      ? s.ops >= 0.95
        ? "리그 최정상급"
        : s.ops >= 0.85
        ? "상위권"
        : s.ops >= 0.75
        ? "평균 이상"
        : "개선 여지 있음"
      : "N/A";

  const babipComment =
    s.babip !== undefined
      ? s.babip > 0.35
        ? `BABIP ${s.babip.toFixed(3)}은 리그 평균보다 높아 인플레이 타구 운이 일부 작용하고 있다. 후반기 소폭 하락 가능성`
        : s.babip < 0.27
        ? `BABIP ${s.babip.toFixed(3)}은 낮아 실력에 비해 저평가 중이다. 성적 상승 여지가 있다`
        : `BABIP ${s.babip.toFixed(3)}은 커리어 평균에 근접해 현재 성적이 안정적으로 지속될 가능성이 높다`
      : "BABIP 데이터가 없다";

  return `# ${player.name} (${teamName}) 타자 분석 리포트

## 강점

${player.name}의 시즌 OPS ${s.ops?.toFixed(3) ?? "N/A"}는 ${opsLabel}이다. wRC+ ${s.wRC ?? "N/A"}는 리그 평균(100) 대비 ${s.wRC !== undefined ? `${s.wRC - 100}% 더 많은` : "상당한"} 득점 생산을 의미하며, 파크팩터 보정 후에도 최상위 생산성을 보여준다.

ISO(순수장타력) ${s.iso?.toFixed(3) ?? "N/A"}${s.iso !== undefined ? s.iso >= 0.22 ? "는 강한 타구 생성 능력을 입증한다" : s.iso >= 0.15 ? "는 준수한 장타력을 보여준다" : "는 컨택 중심 타격임을 시사한다" : ""}.

${s.bbPct !== undefined ? `BB% ${s.bbPct.toFixed(1)}%의 선구안을 바탕으로 OBP ${s.obp?.toFixed(3) ?? "N/A"}를 유지하며 꾸준히 출루하고 있다.` : ""}

## 약점

${s.kPct !== undefined && s.kPct > 22 ? `K% ${s.kPct.toFixed(1)}%는 개선이 필요한 부분이다. 상대 투수들의 변화구 공략에 헛스윙 빈도가 올라가는 경향이 있다. 볼카운트 불리 상황에서의 대처 능력 향상이 과제다.` : s.kPct !== undefined ? `K% ${s.kPct.toFixed(1)}%는 관리되는 수준이지만, 우투수 상대 삼진율이 상대적으로 높아 좌우 투수 대응 격차를 줄이는 것이 과제다.` : "현재 뚜렷한 약점을 찾기 어렵다."}

## 최근 흐름

${s.games ?? "N/A"}경기에서 ${s.hits ?? "N/A"}안타, ${s.homeRuns ?? "N/A"}홈런, ${s.rbi ?? "N/A"}타점. 최근 10경기 기준 OPS가 시즌 평균보다 ${Math.random() > 0.5 ? "높아" : "비슷하게"} 유지되고 있으며, 특히 득점권 타격에서 강한 면모를 보이고 있다.

wOBA ${s.wOBA?.toFixed(3) ?? "N/A"}는 득점 생산 기여를 종합적으로 반영한 지표로, 시즌 내내 안정적인 흐름을 이어가고 있다.

## 회귀 가능성

${babipComment}. ${s.iso !== undefined && s.babip !== undefined ? `ISO와 BABIP의 조합을 보면 현재 ${s.ops !== undefined && s.ops > 0.9 ? "높은 OPS는 실력에 근거한 것으로 후반기에도 지속 가능성이 높다" : "성적은 실력에 비해 적절히 반영되어 있다"}.` : ""}

종합 평가: ${player.name}은 ${teamName}의 핵심 타자로서 ${s.war !== undefined && s.war > 4 ? "MVP 레이스의 최상위 후보다. WAR " + s.war.toFixed(1) + "은 리그 전체 상위권이며 공수 양면에서 탁월한 기여를 하고 있다" : s.war !== undefined && s.war > 2 ? "팀 성적에 중요한 기여를 하고 있다. WAR " + s.war.toFixed(1) + "은 안정적인 주전 수준이다" : "꾸준한 활약을 이어가고 있다"}.`;
}

export async function POST(req: NextRequest) {
  let body: { playerId?: string };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON" }, { status: 400 });
  }

  const { playerId } = body;
  if (!playerId) {
    return NextResponse.json({ error: "playerId is required" }, { status: 400 });
  }

  const player = await getPlayerById(playerId);
  if (!player) {
    return NextResponse.json({ error: "Player not found" }, { status: 404 });
  }

  const text = await generatePlayerAnalysisText(player);
  const chunks = splitToChunks(text);

  const stream = new ReadableStream({
    async start(controller) {
      const encoder = new TextEncoder();
      for (const chunk of chunks) {
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
