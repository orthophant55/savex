"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import { Search } from "lucide-react";
import type { Player, Team } from "@/lib/types/kbo";
import { formatAvg, formatEra, getPositionAbbr } from "@/lib/utils";

const POSITIONS = ["전체", "투수", "포수", "1루수", "2루수", "3루수", "유격수", "좌익수", "중견수", "우익수", "지명타자"] as const;
const PLAYER_TABS = [
  { id: "batter", label: "타자" },
  { id: "pitcher", label: "투수" },
] as const;
type PlayerTab = (typeof PLAYER_TABS)[number]["id"];

interface PlayersPageClientProps {
  players: Player[];
  teams: Team[];
}

export default function PlayersPageClient({ players, teams }: PlayersPageClientProps) {
  const [query, setQuery] = useState("");
  const [teamFilter, setTeamFilter] = useState("all");
  const [tab, setTab] = useState<PlayerTab>("batter");

  const filtered = useMemo(() => {
    return players.filter((p) => {
      const isPitcher = p.position === "투수";
      if (tab === "batter" && isPitcher) return false;
      if (tab === "pitcher" && !isPitcher) return false;
      if (teamFilter !== "all" && p.teamId !== teamFilter) return false;
      if (query) {
        const q = query.toLowerCase();
        return p.name.toLowerCase().includes(q);
      }
      return true;
    });
  }, [players, query, teamFilter, tab]);

  const sorted = useMemo(() => {
    return [...filtered].sort((a, b) => {
      if (tab === "batter") return (b.seasonStat.ops ?? 0) - (a.seasonStat.ops ?? 0);
      return (a.seasonStat.era ?? 99) - (b.seasonStat.era ?? 99);
    });
  }, [filtered, tab]);

  const getTeam = (id: string) => teams.find((t) => t.id === id);

  return (
    <>
      {/* Filters */}
      <div className="space-y-3 mb-6">
        {/* Search */}
        <div className="relative max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-400" aria-hidden />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="선수 이름 검색..."
            className="w-full pl-9 pr-4 py-2.5 text-sm rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500"
            aria-label="선수 검색"
          />
        </div>

        {/* Team filter */}
        <div className="flex flex-wrap gap-2" role="group" aria-label="팀 필터">
          <button
            onClick={() => setTeamFilter("all")}
            className={`px-3 py-1 text-xs font-semibold rounded-full border transition-colors ${
              teamFilter === "all"
                ? "bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 border-zinc-900 dark:border-zinc-100"
                : "border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 hover:border-zinc-300"
            }`}
            aria-pressed={teamFilter === "all"}
          >
            전체
          </button>
          {teams.map((t) => (
            <button
              key={t.id}
              onClick={() => setTeamFilter(t.id)}
              className={`px-3 py-1 text-xs font-semibold rounded-full border transition-colors ${
                teamFilter === t.id
                  ? "text-white border-transparent"
                  : "border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 hover:border-zinc-300"
              }`}
              style={teamFilter === t.id ? { backgroundColor: t.primaryColor } : {}}
              aria-pressed={teamFilter === t.id}
            >
              {t.shortName}
            </button>
          ))}
        </div>
      </div>

      {/* Batter/Pitcher tab */}
      <div className="flex gap-1 border-b border-zinc-200 dark:border-zinc-800 mb-5" role="tablist" aria-label="타자/투수 전환">
        {PLAYER_TABS.map(({ id, label }) => (
          <button
            key={id}
            role="tab"
            aria-selected={tab === id}
            onClick={() => setTab(id)}
            className={`px-4 py-2.5 text-sm font-semibold border-b-2 -mb-px transition-colors ${
              tab === id
                ? "border-blue-600 dark:border-blue-400 text-blue-600 dark:text-blue-400"
                : "border-transparent text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100"
            }`}
          >
            {label}
            <span className="ml-1.5 text-xs text-zinc-400 dark:text-zinc-500">
              ({players.filter((p) => (id === "batter") !== (p.position === "투수")).length})
            </span>
          </button>
        ))}
      </div>

      {/* Count */}
      <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-3">
        {sorted.length}명
      </p>

      {/* Table */}
      {sorted.length === 0 ? (
        <div className="py-16 text-center text-zinc-400 dark:text-zinc-500 text-sm">
          검색 조건에 맞는 선수가 없습니다.
        </div>
      ) : (
        <div className="rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 overflow-hidden">
          <div className="table-scroll">
            {tab === "batter" ? (
              <table className="w-full text-sm min-w-max" aria-label="타자 목록">
                <thead>
                  <tr className="border-b border-zinc-100 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/50">
                    {["이름", "팀", "포지션", "G", "AVG", "OBP", "SLG", "OPS", "HR", "RBI", "WAR"].map((h) => (
                      <th key={h} className="px-3 py-2.5 text-left text-xs font-semibold text-zinc-500 dark:text-zinc-400" scope="col">
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-50 dark:divide-zinc-800/50">
                  {sorted.map((p) => {
                    const team = getTeam(p.teamId);
                    return (
                      <tr key={p.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/30 transition-colors">
                        <td className="px-3 py-2.5">
                          <Link href={`/players/${p.id}`} className="font-semibold text-zinc-900 dark:text-zinc-100 hover:text-blue-600 dark:hover:text-blue-400">
                            {p.name}
                          </Link>
                        </td>
                        <td className="px-3 py-2.5">
                          {team && (
                            <Link href={`/teams/${team.id}`}>
                              <span
                                className="inline-block text-[10px] font-bold px-1.5 py-0.5 rounded text-white"
                                style={{ backgroundColor: team.primaryColor }}
                              >
                                {team.shortName}
                              </span>
                            </Link>
                          )}
                        </td>
                        <td className="px-3 py-2.5 text-xs text-zinc-500 dark:text-zinc-400">{getPositionAbbr(p.position)}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs text-zinc-600 dark:text-zinc-400">{p.seasonStat.games ?? "-"}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs font-medium text-zinc-900 dark:text-zinc-100">{formatAvg(p.seasonStat.avg)}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs text-zinc-600 dark:text-zinc-400">{formatAvg(p.seasonStat.obp)}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs text-zinc-600 dark:text-zinc-400">{formatAvg(p.seasonStat.slg)}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs font-bold text-zinc-900 dark:text-zinc-100">{formatAvg(p.seasonStat.ops)}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs text-zinc-600 dark:text-zinc-400">{p.seasonStat.homeRuns ?? "-"}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs text-zinc-600 dark:text-zinc-400">{p.seasonStat.rbi ?? "-"}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs font-semibold text-blue-600 dark:text-blue-400">{p.seasonStat.war?.toFixed(1) ?? "-"}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            ) : (
              <table className="w-full text-sm min-w-max" aria-label="투수 목록">
                <thead>
                  <tr className="border-b border-zinc-100 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/50">
                    {["이름", "팀", "G", "ERA", "FIP", "WHIP", "K", "BB", "W", "L", "WAR"].map((h) => (
                      <th key={h} className="px-3 py-2.5 text-left text-xs font-semibold text-zinc-500 dark:text-zinc-400" scope="col">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-50 dark:divide-zinc-800/50">
                  {sorted.map((p) => {
                    const team = getTeam(p.teamId);
                    return (
                      <tr key={p.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/30 transition-colors">
                        <td className="px-3 py-2.5">
                          <Link href={`/players/${p.id}`} className="font-semibold text-zinc-900 dark:text-zinc-100 hover:text-blue-600 dark:hover:text-blue-400">{p.name}</Link>
                        </td>
                        <td className="px-3 py-2.5">
                          {team && (
                            <Link href={`/teams/${team.id}`}>
                              <span className="inline-block text-[10px] font-bold px-1.5 py-0.5 rounded text-white" style={{ backgroundColor: team.primaryColor }}>{team.shortName}</span>
                            </Link>
                          )}
                        </td>
                        <td className="px-3 py-2.5 tabular-nums text-xs text-zinc-600 dark:text-zinc-400">{p.seasonStat.games ?? "-"}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs font-bold text-zinc-900 dark:text-zinc-100">{formatEra(p.seasonStat.era)}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs text-zinc-600 dark:text-zinc-400">{formatEra(p.seasonStat.fip)}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs text-zinc-600 dark:text-zinc-400">{formatEra(p.seasonStat.whip)}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs text-zinc-600 dark:text-zinc-400">{p.seasonStat.strikeouts ?? "-"}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs text-zinc-600 dark:text-zinc-400">{p.seasonStat.walks ?? "-"}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs text-zinc-600 dark:text-zinc-400">{p.seasonStat.wins2 ?? "-"}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs text-zinc-600 dark:text-zinc-400">{p.seasonStat.losses2 ?? "-"}</td>
                        <td className="px-3 py-2.5 tabular-nums text-xs font-semibold text-blue-600 dark:text-blue-400">{p.seasonStat.war?.toFixed(1) ?? "-"}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            )}
          </div>
        </div>
      )}
    </>
  );
}
