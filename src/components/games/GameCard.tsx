import Link from "next/link";
import { MapPin } from "lucide-react";
import type { Game } from "@/lib/types/kbo";
import type { Team } from "@/lib/types/kbo";
import { getGameStatusLabel, getGameStatusColor } from "@/lib/utils";

interface GameCardProps {
  game: Game;
  awayTeam: Team;
  homeTeam: Team;
}

function TeamBlock({
  team,
  score,
  isWinner,
  side,
}: {
  team: Team;
  score: number | null;
  isWinner: boolean;
  side: "away" | "home";
}) {
  return (
    <div
      className={`flex items-center gap-2 ${side === "home" ? "flex-row-reverse" : ""}`}
    >
      {/* Logo placeholder */}
      <div
        className="h-9 w-9 rounded-full flex items-center justify-center text-white text-xs font-bold shrink-0"
        style={{ backgroundColor: team.primaryColor }}
        aria-label={team.name}
      >
        {team.shortName.slice(0, 2)}
      </div>
      <div className={side === "home" ? "text-right" : ""}>
        <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-none">
          {team.city}
        </p>
        <p
          className={`text-sm font-bold leading-tight ${
            isWinner
              ? "text-zinc-900 dark:text-zinc-100"
              : "text-zinc-500 dark:text-zinc-400"
          }`}
        >
          {team.shortName}
        </p>
      </div>
      {score !== null && (
        <span
          className={`text-2xl font-bold tabular-nums ml-1 ${
            isWinner
              ? "text-zinc-900 dark:text-zinc-100"
              : "text-zinc-400 dark:text-zinc-500"
          }`}
          aria-label={`${team.name} ${score}점`}
        >
          {score}
        </span>
      )}
    </div>
  );
}

export default function GameCard({ game, awayTeam, homeTeam }: GameCardProps) {
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
    <Link
      href={`/games/${game.id}`}
      className="block rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-4 hover:border-zinc-300 dark:hover:border-zinc-700 transition-colors"
      aria-label={`${awayTeam.name} vs ${homeTeam.name} 경기 상세`}
    >
      {/* Status + time */}
      <div className="flex items-center justify-between mb-3">
        <span
          className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${getGameStatusColor(
            game.status
          )}`}
          aria-label={`경기 상태: ${getGameStatusLabel(game.status)}`}
        >
          {game.status === "live" && game.currentInning
            ? `${game.currentInning}회 ${game.isTopInning ? "초" : "말"}`
            : getGameStatusLabel(game.status)}
        </span>
        {game.status === "scheduled" && (
          <span className="text-xs text-zinc-500 dark:text-zinc-400">
            {game.startTime}
          </span>
        )}
      </div>

      {/* Teams & score */}
      <div className="flex items-center justify-between gap-2">
        <TeamBlock
          team={awayTeam}
          score={game.awayScore}
          isWinner={awayWins}
          side="away"
        />

        {game.status === "scheduled" ? (
          <span className="text-xs text-zinc-400 dark:text-zinc-500 font-medium">
            VS
          </span>
        ) : (
          <span className="text-xs text-zinc-300 dark:text-zinc-600">-</span>
        )}

        <TeamBlock
          team={homeTeam}
          score={game.homeScore}
          isWinner={homeWins}
          side="home"
        />
      </div>

      {/* Stadium */}
      <div className="mt-3 flex items-center gap-1 text-[11px] text-zinc-400 dark:text-zinc-500">
        <MapPin className="h-3 w-3" aria-hidden />
        <span>{game.stadium}</span>
        {game.awayStartingPitcher && (
          <>
            <span aria-hidden className="mx-1">
              ·
            </span>
            <span>
              {game.awayStartingPitcher} vs {game.homeStartingPitcher}
            </span>
          </>
        )}
      </div>
    </Link>
  );
}
