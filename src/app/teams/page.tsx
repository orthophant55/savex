import type { Metadata } from "next";
import { getTeams, getStandings } from "@/lib/api/kbo";
import TeamCard from "@/components/teams/TeamCard";
import SectionHeader from "@/components/common/SectionHeader";

export const metadata: Metadata = { title: "팀" };

export default async function TeamsPage() {
  const [teams, standings] = await Promise.all([getTeams(), getStandings()]);

  const standingMap = Object.fromEntries(standings.map((s) => [s.team.id, s]));

  // 순위순 정렬
  const sortedTeams = [...teams].sort(
    (a, b) => (standingMap[a.id]?.rank ?? 99) - (standingMap[b.id]?.rank ?? 99)
  );

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <SectionHeader
        title="KBO 팀"
        description="2026 시즌 순위 기준"
        className="mb-6"
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {sortedTeams.map((team) => {
          const standing = standingMap[team.id];
          if (!standing) return null;
          return (
            <TeamCard key={team.id} team={team} standing={standing} />
          );
        })}
      </div>
    </div>
  );
}
