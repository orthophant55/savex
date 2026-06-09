import { notFound } from "next/navigation";
import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { getPlayerById, getTeamById } from "@/lib/api/kbo";
import PlayerHeader from "@/components/players/PlayerHeader";
import PlayerStatsTable from "@/components/players/PlayerStatsTable";
import PlayerMetricChart from "@/components/players/PlayerMetricChart";
import AiPlayerAnalysisPanel from "@/components/players/AiPlayerAnalysisPanel";
import StatCard from "@/components/common/StatCard";
import { formatAvg, formatEra, formatPct } from "@/lib/utils";

interface Props {
  params: Promise<{ playerId: string }>;
}

// 결정론적 월별 데이터 생성 (수치는 예시)
function getMockMonthlyData(playerId: string, baseValue: number) {
  const seed = playerId.split("").reduce((a, c) => a + c.charCodeAt(0), 0);
  const months = ["3월", "4월", "5월", "6월"];
  return months.map((month, i) => {
    const variation = ((seed * (i + 1) * 17) % 100 - 50) / 50 * 0.05;
    return {
      month,
      value: parseFloat(Math.max(0.01, baseValue * (1 + variation)).toFixed(3)),
    };
  });
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { playerId } = await params;
  const player = await getPlayerById(playerId);
  if (!player) return { title: "선수를 찾을 수 없습니다" };
  return { title: `${player.name} — ${player.position}` };
}

export default async function PlayerDetailPage({ params }: Props) {
  const { playerId } = await params;

  const player = await getPlayerById(playerId);
  if (!player) notFound();

  const team = await getTeamById(player.teamId);
  if (!team) notFound();

  const isPitcher = player.position === "투수";
  const stat = player.seasonStat;

  // 월별 차트 데이터
  const chartBase = isPitcher ? (stat.era ?? 4.0) : (stat.ops ?? 0.750);
  const monthlyData = getMockMonthlyData(playerId, chartBase);
  const chartLabel = isPitcher ? "ERA" : "OPS";
  const isLowerBetter = isPitcher;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <Link
        href="/players"
        className="inline-flex items-center gap-1.5 text-sm text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 mb-6 transition-colors"
        aria-label="선수 목록으로"
      >
        <ArrowLeft className="h-4 w-4" aria-hidden />
        선수 목록
      </Link>

      <div className="space-y-8">
        {/* Header */}
        <PlayerHeader player={player} team={team} />

        {/* Season stat cards */}
        <div>
          <h2 className="text-sm font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">
            2026 시즌 주요 지표
          </h2>
          {isPitcher ? (
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
              <StatCard label="ERA" value={formatEra(stat.era)} highlight />
              <StatCard label="FIP" value={formatEra(stat.fip)} />
              <StatCard label="xFIP" value={formatEra(stat.xFip)} />
              <StatCard label="WHIP" value={formatEra(stat.whip)} />
              <StatCard label="K%" value={formatPct(stat.kPct)} />
              <StatCard label="BB%" value={formatPct(stat.bbPct)} />
              <StatCard label="K/9" value={stat.kPer9?.toFixed(2) ?? "-"} />
              <StatCard label="BB/9" value={stat.bbPer9?.toFixed(2) ?? "-"} />
              <StatCard label="HR/9" value={stat.hrPer9?.toFixed(2) ?? "-"} />
              <StatCard label="LOB%" value={formatPct(stat.leftOnBasePct)} />
              <StatCard label="GB%" value={formatPct(stat.groundBallPct)} />
              <StatCard label="WAR" value={stat.war?.toFixed(1) ?? "-"} highlight />
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
              <StatCard label="AVG" value={formatAvg(stat.avg)} highlight />
              <StatCard label="OBP" value={formatAvg(stat.obp)} />
              <StatCard label="SLG" value={formatAvg(stat.slg)} />
              <StatCard label="OPS" value={formatAvg(stat.ops)} highlight />
              <StatCard label="wOBA" value={formatAvg(stat.wOBA)} />
              <StatCard label="wRC+" value={stat.wRC ?? "-"} />
              <StatCard label="HR" value={stat.homeRuns ?? "-"} />
              <StatCard label="RBI" value={stat.rbi ?? "-"} />
              <StatCard label="BB%" value={formatPct(stat.bbPct)} />
              <StatCard label="K%" value={formatPct(stat.kPct)} />
              <StatCard label="BABIP" value={formatAvg(stat.babip)} />
              <StatCard label="WAR" value={stat.war?.toFixed(1) ?? "-"} highlight />
            </div>
          )}
        </div>

        {/* Monthly chart + career stats */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <PlayerMetricChart
            data={monthlyData}
            label={chartLabel}
            color={team.primaryColor}
            isLowerBetter={isLowerBetter}
            seasonAvg={chartBase}
          />
          <PlayerStatsTable player={player} />
        </div>

        {/* AI Analysis Panel */}
        <AiPlayerAnalysisPanel playerId={playerId} playerName={player.name} />
      </div>
    </div>
  );
}
