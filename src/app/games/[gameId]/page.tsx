import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getGameById, getTeamById } from "@/lib/api/kbo";
import GameHeader from "@/components/games/GameHeader";
import BoxScoreTable from "@/components/games/BoxScoreTable";
import PlayByPlayList from "@/components/games/PlayByPlayList";
import WinProbabilityChart from "@/components/games/WinProbabilityChart";
import AiGameRecapPanel from "@/components/games/AiGameRecapPanel";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";

interface Props {
  params: Promise<{ gameId: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { gameId } = await params;
  const game = await getGameById(gameId);
  if (!game) return { title: "경기를 찾을 수 없습니다" };
  return {
    title: `${game.awayTeamId} vs ${game.homeTeamId} — ${game.date}`,
  };
}

export default async function GameDetailPage({ params }: Props) {
  const { gameId } = await params;

  const game = await getGameById(gameId);
  if (!game) notFound();

  const [awayTeam, homeTeam] = await Promise.all([
    getTeamById(game.awayTeamId),
    getTeamById(game.homeTeamId),
  ]);

  if (!awayTeam || !homeTeam) notFound();

  // WPA 상위 플레이 (|wpa| 기준 내림차순)
  const topWpaPlays = (game.playByPlay ?? [])
    .filter((e) => Math.abs(e.wpa) >= 0.05)
    .sort((a, b) => Math.abs(b.wpa) - Math.abs(a.wpa))
    .slice(0, 5);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Back */}
      <Link
        href="/games"
        className="inline-flex items-center gap-1.5 text-sm text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 mb-6 transition-colors"
        aria-label="경기 목록으로 돌아가기"
      >
        <ArrowLeft className="h-4 w-4" aria-hidden />
        경기 목록
      </Link>

      <div className="space-y-8">
        {/* Game header */}
        <GameHeader game={game} awayTeam={awayTeam} homeTeam={homeTeam} />

        {/* Box score */}
        {game.boxScore && (
          <BoxScoreTable
            game={game}
            awayTeam={awayTeam}
            homeTeam={homeTeam}
          />
        )}

        {/* WPA top plays */}
        {topWpaPlays.length > 0 && (
          <div>
            <h2 className="text-sm font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">
              승부의 분기점 (WPA 상위)
            </h2>
            <div className="rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 divide-y divide-zinc-100 dark:divide-zinc-800">
              {topWpaPlays.map((play, i) => (
                <div key={play.id} className="px-4 py-3 flex items-start gap-3">
                  <span className="text-xs font-bold text-zinc-400 dark:text-zinc-500 w-4 tabular-nums mt-0.5">
                    {i + 1}
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-zinc-800 dark:text-zinc-200">
                      {play.description}
                    </p>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
                      {play.inning}회 {play.isTop ? "초" : "말"} · {awayTeam.shortName}{" "}
                      {play.awayScore} : {play.homeScore} {homeTeam.shortName}
                    </p>
                  </div>
                  <div className="shrink-0 flex flex-col items-end gap-1">
                    <span
                      className={`text-xs font-bold tabular-nums px-2 py-0.5 rounded ${
                        play.wpa > 0
                          ? "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300"
                          : "bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300"
                      }`}
                      aria-label={`승리확률 변화: ${play.wpa > 0 ? "+" : ""}${play.wpa.toFixed(3)}`}
                    >
                      WPA {play.wpa > 0 ? "+" : ""}
                      {play.wpa.toFixed(3)}
                    </span>
                    {play.li >= 1.5 && (
                      <span
                        className="text-[10px] font-semibold tabular-nums px-1.5 py-0.5 rounded bg-yellow-100 text-yellow-700 dark:bg-yellow-900/40 dark:text-yellow-300"
                        aria-label={`레버리지 인덱스 ${play.li.toFixed(2)}`}
                      >
                        LI {play.li.toFixed(1)}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Win probability + play-by-play: 데스크탑 2열 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Win probability chart */}
          {game.winProbability && game.winProbability.length > 0 && (
            <WinProbabilityChart
              data={game.winProbability}
              awayTeam={awayTeam}
              homeTeam={homeTeam}
            />
          )}

          {/* Play-by-play */}
          {game.playByPlay && game.playByPlay.length > 0 && (
            <PlayByPlayList
              events={game.playByPlay}
              awayTeam={awayTeam}
              homeTeam={homeTeam}
            />
          )}
        </div>

        {/* AI recap panel */}
        <AiGameRecapPanel gameId={gameId} />
      </div>
    </div>
  );
}
