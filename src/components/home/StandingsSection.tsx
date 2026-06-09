import Link from "next/link";
import { ArrowRight } from "lucide-react";
import type { Standing } from "@/lib/types/kbo";
import SectionHeader from "@/components/common/SectionHeader";
import { formatWinRate, getWinRateColor } from "@/lib/utils";

interface StandingsSectionProps {
  standings: Standing[];
}

function FormDot({ result }: { result: "W" | "L" | "D" }) {
  const colors = {
    W: "bg-blue-500",
    L: "bg-red-400",
    D: "bg-zinc-400",
  };
  const labels = { W: "승", L: "패", D: "무" };
  return (
    <span
      className={`inline-block h-2 w-2 rounded-full ${colors[result]}`}
      aria-label={labels[result]}
      title={labels[result]}
    />
  );
}

export default function StandingsSection({ standings }: StandingsSectionProps) {
  return (
    <section aria-labelledby="standings-heading">
      <SectionHeader
        title="팀 순위"
        action={
          <Link
            href="/teams"
            className="flex items-center gap-1 text-xs text-blue-600 dark:text-blue-400 hover:underline font-medium"
            aria-label="팀 상세 보기"
          >
            팀 상세
            <ArrowRight className="h-3.5 w-3.5" aria-hidden />
          </Link>
        }
      />
      <span id="standings-heading" className="sr-only">
        팀 순위
      </span>

      <div className="rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 overflow-hidden">
        <div className="table-scroll">
          <table
            className="w-full text-sm"
            aria-label="KBO 팀 순위표"
          >
            <thead>
              <tr className="border-b border-zinc-100 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/50">
                <th className="text-left px-4 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 text-xs w-8">
                  순위
                </th>
                <th className="text-left px-3 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 text-xs">
                  팀
                </th>
                <th className="text-center px-3 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 text-xs w-10">
                  승
                </th>
                <th className="text-center px-3 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 text-xs w-10">
                  패
                </th>
                <th className="text-center px-3 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 text-xs w-10">
                  무
                </th>
                <th className="text-center px-3 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 text-xs w-16">
                  승률
                </th>
                <th className="text-center px-3 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 text-xs w-12">
                  GB
                </th>
                <th className="text-center px-3 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 text-xs hidden md:table-cell">
                  연속
                </th>
                <th className="text-center px-3 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 text-xs hidden sm:table-cell w-24">
                  최근 5경기
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-50 dark:divide-zinc-800/50">
              {standings.map((s) => (
                <tr
                  key={s.team.id}
                  className="hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors"
                >
                  <td className="px-4 py-2.5">
                    <span
                      className={`text-xs font-bold tabular-nums ${
                        s.rank <= 5
                          ? "text-blue-600 dark:text-blue-400"
                          : "text-zinc-500 dark:text-zinc-400"
                      }`}
                    >
                      {s.rank}
                    </span>
                  </td>
                  <td className="px-3 py-2.5">
                    <Link
                      href={`/teams/${s.team.id}`}
                      className="flex items-center gap-2 hover:underline"
                      aria-label={`${s.team.name} 상세 보기`}
                    >
                      <div
                        className="h-5 w-5 rounded-full flex items-center justify-center text-white text-[8px] font-bold shrink-0"
                        style={{ backgroundColor: s.team.primaryColor }}
                        aria-hidden
                      />
                      <span className="font-semibold text-zinc-900 dark:text-zinc-100 text-xs">
                        {s.team.shortName}
                      </span>
                    </Link>
                  </td>
                  <td className="text-center px-3 py-2.5 text-xs tabular-nums text-zinc-700 dark:text-zinc-300">
                    {s.wins}
                  </td>
                  <td className="text-center px-3 py-2.5 text-xs tabular-nums text-zinc-700 dark:text-zinc-300">
                    {s.losses}
                  </td>
                  <td className="text-center px-3 py-2.5 text-xs tabular-nums text-zinc-700 dark:text-zinc-300">
                    {s.draws}
                  </td>
                  <td className="text-center px-3 py-2.5 text-xs">
                    <span
                      className={`font-bold tabular-nums ${getWinRateColor(
                        s.winRate
                      )}`}
                    >
                      {formatWinRate(s.winRate)}
                    </span>
                  </td>
                  <td className="text-center px-3 py-2.5 text-xs tabular-nums text-zinc-500 dark:text-zinc-400">
                    {s.gamesBehind === 0 ? "-" : s.gamesBehind}
                  </td>
                  <td className="text-center px-3 py-2.5 text-xs text-zinc-500 dark:text-zinc-400 hidden md:table-cell">
                    <span
                      className={
                        s.streak.includes("연승")
                          ? "text-blue-600 dark:text-blue-400 font-medium"
                          : "text-red-500 dark:text-red-400 font-medium"
                      }
                    >
                      {s.streak}
                    </span>
                  </td>
                  <td className="text-center px-3 py-2.5 hidden sm:table-cell">
                    <div
                      className="flex items-center justify-center gap-1"
                      aria-label={`최근 5경기: ${s.recentForm.join(", ")}`}
                    >
                      {s.recentForm.map((r, i) => (
                        <FormDot key={i} result={r} />
                      ))}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
