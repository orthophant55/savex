import Link from "next/link";
import { ChevronRight } from "lucide-react";
import {
  getTodayGames,
  getTeams,
  getStandings,
  getStatLeaders,
  getArticles,
} from "@/lib/api/kbo";
import TodayGamesSection from "@/components/home/TodayGamesSection";
import StandingsSection from "@/components/home/StandingsSection";
import StatLeadersSection from "@/components/home/StatLeadersSection";
import FeaturedArticlesSection from "@/components/home/FeaturedArticlesSection";

export default async function HomePage() {
  const [todayGames, teams, standings, statLeaders, articles] =
    await Promise.all([
      getTodayGames(),
      getTeams(),
      getStandings(),
      getStatLeaders(),
      getArticles({ limit: 4 }),
    ]);

  const liveCount = todayGames.filter((g) => g.status === "live").length;
  const heroSubtext =
    liveCount > 0
      ? `현재 ${liveCount}경기 진행 중`
      : `오늘 ${todayGames.length}경기 예정`;

  return (
    <>
      {/* Hero */}
      <section
        className="bg-gradient-to-br from-zinc-900 via-blue-950 to-zinc-900 text-white"
        aria-label="메인 히어로"
      >
        <div className="max-w-6xl mx-auto px-4 py-14 md:py-20">
          <div className="max-w-2xl">
            <p className="text-blue-400 text-xs font-semibold tracking-widest uppercase mb-3">
              2026 KBO Season
            </p>
            <h1 className="text-3xl md:text-4xl font-black tracking-tight leading-tight text-white">
              KBO 세이버매트릭스
              <br />
              <span className="text-blue-400">인사이트</span>
            </h1>
            <p className="mt-4 text-zinc-400 text-sm md:text-base leading-relaxed">
              WAR, FIP, wOBA, WPA — 숫자가 말해주는 야구의 진실.
              <br />
              <span className="text-zinc-300 font-medium">{heroSubtext}</span>
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <Link
                href="/games"
                className="inline-flex items-center gap-1.5 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded-lg transition-colors"
                aria-label="오늘 경기 보기"
              >
                오늘 경기 보기
                <ChevronRight className="h-4 w-4" aria-hidden />
              </Link>
              <Link
                href="/articles"
                className="inline-flex items-center gap-1.5 px-5 py-2.5 bg-white/10 hover:bg-white/20 text-white text-sm font-semibold rounded-lg transition-colors border border-white/20"
                aria-label="AI 칼럼 보기"
              >
                AI 칼럼 보기
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-4 py-8 space-y-12">
        <TodayGamesSection games={todayGames} teams={teams} />
        <StandingsSection standings={standings} />
        <StatLeadersSection leaders={statLeaders} />
        <FeaturedArticlesSection articles={articles} />
      </div>
    </>
  );
}
