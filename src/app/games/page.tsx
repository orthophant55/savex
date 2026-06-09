import type { Metadata } from "next";
import { getGamesByDate, getTeams } from "@/lib/api/kbo";
import GamesPageClient from "./GamesPageClient";

export const metadata: Metadata = { title: "경기 일정" };

export default async function GamesPage() {
  const today = new Date().toISOString().slice(0, 10);
  const [games, teams] = await Promise.all([
    getGamesByDate(today),
    getTeams(),
  ]);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-black text-zinc-900 dark:text-zinc-100 mb-6">
        경기 일정
      </h1>
      <GamesPageClient initialGames={games} teams={teams} initialDate={today} />
    </div>
  );
}
