import type { Metadata } from "next";
import { getPlayers, getTeams } from "@/lib/api/kbo";
import PlayersPageClient from "./PlayersPageClient";

export const metadata: Metadata = { title: "선수" };

export default async function PlayersPage() {
  const [players, teams] = await Promise.all([getPlayers(), getTeams()]);
  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-black text-zinc-900 dark:text-zinc-100 mb-6">
        선수
      </h1>
      <PlayersPageClient players={players} teams={teams} />
    </div>
  );
}
