import Link from "next/link";
import type { Player } from "@/lib/types/kbo";
import { formatAvg, formatEra, formatPct, formatInnings, getPositionAbbr } from "@/lib/utils";

interface RosterTableProps {
  players: Player[];
  mode: "batting" | "pitching";
}

export default function RosterTable({ players, mode }: RosterTableProps) {
  if (mode === "batting") {
    const batters = players.filter((p) => p.position !== "투수").sort(
      (a, b) => (b.seasonStat.ops ?? 0) - (a.seasonStat.ops ?? 0)
    );

    if (batters.length === 0) {
      return (
        <p className="text-sm text-zinc-500 dark:text-zinc-400 py-8 text-center">
          타자 데이터가 없습니다.
        </p>
      );
    }

    return (
      <div className="table-scroll">
        <table className="w-full text-sm min-w-max" aria-label="팀 타격 스탯">
          <thead>
            <tr className="border-b border-zinc-100 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/50">
              {["이름", "포지션", "G", "AVG", "OBP", "SLG", "OPS", "HR", "RBI", "WAR"].map(
                (h) => (
                  <th
                    key={h}
                    className="px-3 py-2.5 text-left text-xs font-semibold text-zinc-500 dark:text-zinc-400 first:sticky first:left-0 first:bg-zinc-50 dark:first:bg-zinc-800/50"
                    scope="col"
                  >
                    {h}
                  </th>
                )
              )}
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-50 dark:divide-zinc-800/50">
            {batters.map((p) => (
              <tr
                key={p.id}
                className="hover:bg-zinc-50 dark:hover:bg-zinc-800/30 transition-colors"
              >
                <td className="px-3 py-2.5 sticky left-0 bg-white dark:bg-zinc-900 hover:bg-zinc-50 dark:hover:bg-zinc-800/30">
                  <Link
                    href={`/players/${p.id}`}
                    className="font-semibold text-zinc-900 dark:text-zinc-100 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                  >
                    {p.name}
                  </Link>
                </td>
                <td className="px-3 py-2.5 text-xs text-zinc-500 dark:text-zinc-400">
                  {getPositionAbbr(p.position)}
                </td>
                <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">
                  {p.seasonStat.games ?? "-"}
                </td>
                <td className="px-3 py-2.5 tabular-nums font-medium text-zinc-900 dark:text-zinc-100 text-xs">
                  {formatAvg(p.seasonStat.avg)}
                </td>
                <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">
                  {formatAvg(p.seasonStat.obp)}
                </td>
                <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">
                  {formatAvg(p.seasonStat.slg)}
                </td>
                <td className="px-3 py-2.5 tabular-nums font-bold text-zinc-900 dark:text-zinc-100 text-xs">
                  {formatAvg(p.seasonStat.ops)}
                </td>
                <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">
                  {p.seasonStat.homeRuns ?? "-"}
                </td>
                <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">
                  {p.seasonStat.rbi ?? "-"}
                </td>
                <td className="px-3 py-2.5 tabular-nums font-semibold text-blue-600 dark:text-blue-400 text-xs">
                  {p.seasonStat.war?.toFixed(1) ?? "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  // Pitching mode
  const pitchers = players.filter((p) => p.position === "투수").sort(
    (a, b) => (a.seasonStat.era ?? 99) - (b.seasonStat.era ?? 99)
  );

  if (pitchers.length === 0) {
    return (
      <p className="text-sm text-zinc-500 dark:text-zinc-400 py-8 text-center">
        투수 데이터가 없습니다.
      </p>
    );
  }

  return (
    <div className="table-scroll">
      <table className="w-full text-sm min-w-max" aria-label="팀 투구 스탯">
        <thead>
          <tr className="border-b border-zinc-100 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/50">
            {["이름", "G", "ERA", "FIP", "IP", "K", "BB", "WHIP", "W", "L", "WAR"].map(
              (h) => (
                <th
                  key={h}
                  className="px-3 py-2.5 text-left text-xs font-semibold text-zinc-500 dark:text-zinc-400 first:sticky first:left-0 first:bg-zinc-50 dark:first:bg-zinc-800/50"
                  scope="col"
                >
                  {h}
                </th>
              )
            )}
          </tr>
        </thead>
        <tbody className="divide-y divide-zinc-50 dark:divide-zinc-800/50">
          {pitchers.map((p) => (
            <tr
              key={p.id}
              className="hover:bg-zinc-50 dark:hover:bg-zinc-800/30 transition-colors"
            >
              <td className="px-3 py-2.5 sticky left-0 bg-white dark:bg-zinc-900">
                <Link
                  href={`/players/${p.id}`}
                  className="font-semibold text-zinc-900 dark:text-zinc-100 hover:text-blue-600 dark:hover:text-blue-400"
                >
                  {p.name}
                </Link>
              </td>
              <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">
                {p.seasonStat.games ?? "-"}
              </td>
              <td className="px-3 py-2.5 tabular-nums font-bold text-zinc-900 dark:text-zinc-100 text-xs">
                {formatEra(p.seasonStat.era)}
              </td>
              <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">
                {formatEra(p.seasonStat.fip)}
              </td>
              <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">
                {formatInnings(p.seasonStat.innings)}
              </td>
              <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">
                {p.seasonStat.strikeouts ?? "-"}
              </td>
              <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">
                {p.seasonStat.walks ?? "-"}
              </td>
              <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">
                {formatEra(p.seasonStat.whip)}
              </td>
              <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">
                {p.seasonStat.wins2 ?? "-"}
              </td>
              <td className="px-3 py-2.5 tabular-nums text-zinc-600 dark:text-zinc-400 text-xs">
                {p.seasonStat.losses2 ?? "-"}
              </td>
              <td className="px-3 py-2.5 tabular-nums font-semibold text-blue-600 dark:text-blue-400 text-xs">
                {p.seasonStat.war?.toFixed(1) ?? "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
