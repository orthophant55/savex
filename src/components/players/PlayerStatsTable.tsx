import type { Player } from "@/lib/types/kbo";
import { formatAvg, formatEra, formatInnings } from "@/lib/utils";

interface PlayerStatsTableProps {
  player: Player;
}

export default function PlayerStatsTable({ player }: PlayerStatsTableProps) {
  const isPitcher = player.position === "투수";
  const allStats = [...player.careerStats, player.seasonStat].sort(
    (a, b) => (b.season ?? 0) - (a.season ?? 0)
  );

  if (allStats.length === 0) return null;

  return (
    <div>
      <h2 className="text-sm font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">
        연도별 기록
      </h2>
      <div className="rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 overflow-hidden">
        <div className="table-scroll">
          {isPitcher ? (
            <table className="w-full text-sm min-w-max" aria-label="투수 연도별 기록">
              <thead>
                <tr className="border-b border-zinc-100 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/50">
                  {["시즌", "G", "ERA", "FIP", "xFIP", "IP", "K", "BB", "WHIP", "W", "L", "SV", "HLD", "WAR"].map((h) => (
                    <th key={h} className="px-3 py-2.5 text-left text-xs font-semibold text-zinc-500 dark:text-zinc-400" scope="col">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-50 dark:divide-zinc-800/50">
                {allStats.map((s, i) => (
                  <tr
                    key={s.season ?? i}
                    className={`hover:bg-zinc-50 dark:hover:bg-zinc-800/30 transition-colors ${
                      s.season === player.seasonStat.season
                        ? "bg-blue-50/50 dark:bg-blue-950/20"
                        : ""
                    }`}
                  >
                    <td className="px-3 py-2.5 font-bold text-zinc-900 dark:text-zinc-100 text-xs tabular-nums">
                      {s.season ?? "-"}
                      {s.season === player.seasonStat.season && (
                        <span className="ml-1.5 text-[9px] font-semibold bg-blue-100 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400 px-1 py-0.5 rounded">
                          현재
                        </span>
                      )}
                    </td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.games ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums font-bold text-zinc-900 dark:text-zinc-100 text-xs">{formatEra(s.era)}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{formatEra(s.fip)}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{formatEra(s.xFip)}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{formatInnings(s.innings)}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.strikeouts ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.walks ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{formatEra(s.whip)}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.wins2 ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.losses2 ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.saves ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.holds ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums font-semibold text-blue-600 dark:text-blue-400 text-xs">{s.war?.toFixed(1) ?? "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <table className="w-full text-sm min-w-max" aria-label="타자 연도별 기록">
              <thead>
                <tr className="border-b border-zinc-100 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/50">
                  {["시즌", "G", "AB", "H", "HR", "RBI", "AVG", "OBP", "SLG", "OPS", "wOBA", "wRC+", "BB%", "K%", "WAR"].map((h) => (
                    <th key={h} className="px-3 py-2.5 text-left text-xs font-semibold text-zinc-500 dark:text-zinc-400" scope="col">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-50 dark:divide-zinc-800/50">
                {allStats.map((s, i) => (
                  <tr
                    key={s.season ?? i}
                    className={`hover:bg-zinc-50 dark:hover:bg-zinc-800/30 transition-colors ${
                      s.season === player.seasonStat.season
                        ? "bg-blue-50/50 dark:bg-blue-950/20"
                        : ""
                    }`}
                  >
                    <td className="px-3 py-2.5 font-bold text-zinc-900 dark:text-zinc-100 text-xs tabular-nums">
                      {s.season ?? "-"}
                      {s.season === player.seasonStat.season && (
                        <span className="ml-1.5 text-[9px] font-semibold bg-blue-100 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400 px-1 py-0.5 rounded">
                          현재
                        </span>
                      )}
                    </td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.games ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.atBats ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.hits ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.homeRuns ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.rbi ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums font-bold text-zinc-900 dark:text-zinc-100 text-xs">{formatAvg(s.avg)}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{formatAvg(s.obp)}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{formatAvg(s.slg)}</td>
                    <td className="px-3 py-2.5 tabular-nums font-bold text-zinc-900 dark:text-zinc-100 text-xs">{formatAvg(s.ops)}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{formatAvg(s.wOBA)}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.wRC ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.bbPct?.toFixed(1) ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">{s.kPct?.toFixed(1) ?? "-"}</td>
                    <td className="px-3 py-2.5 tabular-nums font-semibold text-blue-600 dark:text-blue-400 text-xs">{s.war?.toFixed(1) ?? "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
