import { notFound } from "next/navigation";
import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import {
  getTeamById,
  getTeamStanding,
  getPlayersByTeam,
} from "@/lib/api/kbo";
import TeamHeader from "@/components/teams/TeamHeader";
import TeamStatsTabs from "@/components/teams/TeamStatsTabs";
import TeamTrendChart from "@/components/teams/TeamTrendChart";

interface Props {
  params: Promise<{ teamId: string }>;
}

// 결정론적 월별 트렌드 데이터 생성 (수치는 예시)
function getTeamTrendData(teamId: string, winRate: number) {
  const seed = teamId.split("").reduce((a, c) => a + c.charCodeAt(0), 0);
  const months = ["3월", "4월", "5월", "6월"];
  let cumWins = 0;
  let cumGames = 0;

  return months.map((period, i) => {
    const variation = ((seed * (i + 1) * 17) % 100 - 50) / 400;
    const monthRate = Math.max(0.2, Math.min(0.85, winRate + variation));
    const gamesThisMonth = 20;
    const winsThisMonth = Math.round(monthRate * gamesThisMonth);
    cumWins += winsThisMonth;
    cumGames += gamesThisMonth;

    const runs = Math.round(4.5 + ((seed * (i + 3) * 7) % 40 - 20) / 10);
    const runsAllowed = Math.round(4.2 + ((seed * (i + 5) * 11) % 40 - 20) / 10);

    return {
      period,
      winRate: parseFloat((cumWins / cumGames).toFixed(3)),
      runs: Math.max(2, runs),
      runsAllowed: Math.max(2, runsAllowed),
    };
  });
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { teamId } = await params;
  const team = await getTeamById(teamId);
  if (!team) return { title: "팀을 찾을 수 없습니다" };
  return { title: team.name };
}

export default async function TeamDetailPage({ params }: Props) {
  const { teamId } = await params;

  const [team, standing, players] = await Promise.all([
    getTeamById(teamId),
    getTeamStanding(teamId),
    getPlayersByTeam(teamId),
  ]);

  if (!team || !standing) notFound();

  const trendData = getTeamTrendData(teamId, standing.winRate);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Back */}
      <Link
        href="/teams"
        className="inline-flex items-center gap-1.5 text-sm text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 mb-6 transition-colors"
        aria-label="팀 목록으로"
      >
        <ArrowLeft className="h-4 w-4" aria-hidden />
        팀 목록
      </Link>

      <div className="space-y-8">
        {/* Team header */}
        <TeamHeader team={team} standing={standing} />

        {/* Trend chart */}
        <TeamTrendChart
          data={trendData}
          primaryColor={team.primaryColor}
          teamName={team.name}
        />

        {/* Stats tabs */}
        <div>
          <h2 className="text-sm font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-4">
            팀 스탯 & 로스터
          </h2>
          <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-5">
            <TeamStatsTabs players={players} standing={standing} />
          </div>
        </div>

        {/* AI Team analysis placeholder */}
        <div className="rounded-xl border border-violet-200 dark:border-violet-800/50 bg-violet-50/50 dark:bg-violet-950/20 p-5">
          <p className="text-sm font-bold text-violet-700 dark:text-violet-300 mb-1">
            ✨ AI 팀 분석
          </p>
          <p className="text-xs text-zinc-500 dark:text-zinc-400">
            팀 전력 심층 분석 기능은 준비 중입니다.
          </p>
        </div>
      </div>
    </div>
  );
}
