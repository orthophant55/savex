import Link from "next/link";
import { ArrowRight } from "lucide-react";
import type { Game, Team } from "@/lib/types/kbo";
import GameCard from "@/components/games/GameCard";
import SectionHeader from "@/components/common/SectionHeader";
import EmptyState from "@/components/common/EmptyState";

interface TodayGamesSectionProps {
  games: Game[];
  teams: Team[];
}

export default function TodayGamesSection({
  games,
  teams,
}: TodayGamesSectionProps) {
  const getTeam = (id: string): Team =>
    teams.find((t) => t.id === id) ?? {
      id,
      name: id,
      shortName: id,
      city: "",
      stadium: "",
      logoPlaceholder: "#888",
      primaryColor: "#888",
      secondaryColor: "#ccc",
    };

  const liveGames = games.filter((g) => g.status === "live");
  const otherGames = games.filter((g) => g.status !== "live");
  const sortedGames = [...liveGames, ...otherGames];

  return (
    <section aria-labelledby="today-games-heading">
      <SectionHeader
        title="오늘의 경기"
        description={`${games.length}경기`}
        action={
          <Link
            href="/games"
            className="flex items-center gap-1 text-xs text-blue-600 dark:text-blue-400 hover:underline font-medium"
            aria-label="전체 경기 일정 보기"
          >
            전체 보기
            <ArrowRight className="h-3.5 w-3.5" aria-hidden />
          </Link>
        }
      />
      <span id="today-games-heading" className="sr-only">
        오늘의 경기
      </span>

      {sortedGames.length === 0 ? (
        <EmptyState title="오늘 예정된 경기가 없습니다" />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {sortedGames.map((game) => (
            <GameCard
              key={game.id}
              game={game}
              awayTeam={getTeam(game.awayTeamId)}
              homeTeam={getTeam(game.homeTeamId)}
            />
          ))}
        </div>
      )}
    </section>
  );
}
