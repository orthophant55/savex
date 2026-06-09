import { Calendar, MapPin, Trophy } from "lucide-react";
import type { Game, Team } from "@/lib/types/kbo";
import { getGameStatusLabel, getGameStatusColor } from "@/lib/utils";

interface GameHeaderProps {
  game: Game;
  awayTeam: Team;
  homeTeam: Team;
}

function TeamScore({
  team,
  score,
  isWinner,
  pitcher,
  side,
}: {
  team: Team;
  score: number | null;
  isWinner: boolean;
  pitcher?: string;
  side: "away" | "home";
}) {
  return (
    <div
      className={`flex flex-col items-center gap-2 flex-1 ${
        side === "away" ? "md:items-start" : "md:items-end"
      }`}
    >
      <div
        className="h-14 w-14 rounded-full flex items-center justify-center text-white text-lg font-bold shadow-md"
        style={{ backgroundColor: team.primaryColor }}
        aria-label={team.name}
      >
        {team.shortName.slice(0, 2)}
      </div>
      <div className={`text-center ${side === "home" ? "md:text-right" : "md:text-left"}`}>
        <p className="text-xs text-zinc-500 dark:text-zinc-400">{team.city}</p>
        <p className="font-bold text-zinc-900 dark:text-zinc-100">{team.name}</p>
        {pitcher && (
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
            선발: {pitcher}
          </p>
        )}
      </div>
      {score !== null && (
        <p
          className={`text-5xl font-black tabular-nums ${
            isWinner
              ? "text-zinc-900 dark:text-zinc-100"
              : "text-zinc-400 dark:text-zinc-500"
          }`}
          aria-label={`${team.name} ${score}점`}
        >
          {score}
        </p>
      )}
    </div>
  );
}

export default function GameHeader({ game, awayTeam, homeTeam }: GameHeaderProps) {
  const isFinal = game.status === "final";
  const awayWins =
    isFinal &&
    game.awayScore !== null &&
    game.homeScore !== null &&
    game.awayScore > game.homeScore;
  const homeWins =
    isFinal &&
    game.awayScore !== null &&
    game.homeScore !== null &&
    game.homeScore > game.awayScore;

  return (
    <div className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-6">
      {/* Status */}
      <div className="flex items-center justify-center gap-2 mb-6">
        <span
          className={`text-xs font-semibold px-3 py-1 rounded-full ${getGameStatusColor(
            game.status
          )}`}
          aria-label={`경기 상태: ${getGameStatusLabel(game.status)}`}
        >
          {game.status === "live" && game.currentInning
            ? `${game.currentInning}회 ${game.isTopInning ? "초" : "말"} 진행 중`
            : getGameStatusLabel(game.status)}
        </span>
        {game.status === "live" && (
          <span className="inline-flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500" />
          </span>
        )}
      </div>

      {/* Teams */}
      <div className="flex items-center justify-between gap-4">
        <TeamScore
          team={awayTeam}
          score={game.awayScore}
          isWinner={awayWins}
          pitcher={game.awayStartingPitcher}
          side="away"
        />

        <div className="flex flex-col items-center gap-2 shrink-0">
          {game.status === "scheduled" ? (
            <span className="text-2xl font-bold text-zinc-400 dark:text-zinc-500">
              {game.startTime}
            </span>
          ) : (
            <span className="text-xl font-bold text-zinc-300 dark:text-zinc-600">
              :
            </span>
          )}
        </div>

        <TeamScore
          team={homeTeam}
          score={game.homeScore}
          isWinner={homeWins}
          pitcher={game.homeStartingPitcher}
          side="home"
        />
      </div>

      {/* Meta */}
      <div className="mt-6 pt-4 border-t border-zinc-100 dark:border-zinc-800 flex flex-wrap items-center justify-center gap-x-4 gap-y-1 text-xs text-zinc-500 dark:text-zinc-400">
        <span className="flex items-center gap-1">
          <Calendar className="h-3 w-3" aria-hidden />
          {game.date} {game.startTime}
        </span>
        <span className="flex items-center gap-1">
          <MapPin className="h-3 w-3" aria-hidden />
          {game.stadium}
        </span>
        {game.mvp && (
          <span className="flex items-center gap-1">
            <Trophy className="h-3 w-3" aria-hidden />
            MVP: {game.mvp}
          </span>
        )}
      </div>

      {isFinal && (game.awayWinningPitcher || game.homeWinningPitcher) && (
        <div className="mt-2 flex items-center justify-center gap-4 text-xs text-zinc-400 dark:text-zinc-500">
          {game.awayWinningPitcher && (
            <span>승리: {game.awayWinningPitcher}</span>
          )}
          {game.homeWinningPitcher && (
            <span>승리: {game.homeWinningPitcher}</span>
          )}
        </div>
      )}
    </div>
  );
}
