import Link from "next/link";
import type { Team, Standing } from "@/lib/types/kbo";
import { formatWinRate, getWinRateColor } from "@/lib/utils";

interface TeamCardProps {
  team: Team;
  standing: Standing;
}

function FormDot({ result }: { result: "W" | "L" | "D" }) {
  const styles = {
    W: "bg-blue-500",
    L: "bg-red-400",
    D: "bg-zinc-400",
  };
  return (
    <span
      className={`inline-block h-2 w-2 rounded-full ${styles[result]}`}
      aria-label={result === "W" ? "승" : result === "L" ? "패" : "무"}
    />
  );
}

export default function TeamCard({ team, standing }: TeamCardProps) {
  return (
    <Link
      href={`/teams/${team.id}`}
      className="group block rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 overflow-hidden hover:shadow-md transition-shadow"
      aria-label={`${team.name} 상세 보기`}
    >
      {/* Top color bar */}
      <div className="h-1.5" style={{ backgroundColor: team.primaryColor }} aria-hidden />

      <div className="p-4">
        {/* Team identity */}
        <div className="flex items-center gap-3 mb-4">
          <div
            className="h-12 w-12 rounded-full flex items-center justify-center text-white font-black text-sm shrink-0 shadow-sm"
            style={{ backgroundColor: team.primaryColor }}
            aria-label={team.name}
          >
            {team.shortName.length <= 2 ? team.shortName : team.shortName.slice(0, 2)}
          </div>
          <div>
            <p className="text-[11px] text-zinc-400 dark:text-zinc-500 leading-none">
              {team.city} · {team.stadium}
            </p>
            <p className="font-bold text-zinc-900 dark:text-zinc-100 text-sm mt-0.5 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
              {team.name}
            </p>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-2 text-center mb-3">
          <div>
            <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mb-0.5">순위</p>
            <p
              className={`text-lg font-black tabular-nums ${
                standing.rank <= 5
                  ? "text-blue-600 dark:text-blue-400"
                  : "text-zinc-500 dark:text-zinc-400"
              }`}
            >
              {standing.rank}위
            </p>
          </div>
          <div>
            <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mb-0.5">승률</p>
            <p
              className={`text-lg font-black tabular-nums ${getWinRateColor(
                standing.winRate
              )}`}
            >
              {formatWinRate(standing.winRate)}
            </p>
          </div>
          <div>
            <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mb-0.5">GB</p>
            <p className="text-lg font-black tabular-nums text-zinc-500 dark:text-zinc-400">
              {standing.gamesBehind === 0 ? "-" : standing.gamesBehind}
            </p>
          </div>
        </div>

        {/* W-L-D */}
        <div className="text-center mb-3">
          <span className="text-xs text-zinc-500 dark:text-zinc-400 tabular-nums">
            <span className="text-blue-600 dark:text-blue-400 font-semibold">{standing.wins}승</span>
            {" "}
            <span className="text-red-500 dark:text-red-400 font-semibold">{standing.losses}패</span>
            {" "}
            <span className="text-zinc-400 font-semibold">{standing.draws}무</span>
          </span>
        </div>

        {/* Recent form */}
        <div className="flex items-center justify-between">
          <span className="text-[10px] text-zinc-400 dark:text-zinc-500">최근 5경기</span>
          <div
            className="flex items-center gap-1"
            aria-label={`최근 5경기 결과: ${standing.recentForm.join(" ")}`}
          >
            {standing.recentForm.map((r, i) => (
              <FormDot key={i} result={r} />
            ))}
          </div>
        </div>

        <div className="mt-2 flex items-center justify-between">
          <span className="text-[10px] text-zinc-400 dark:text-zinc-500">연속</span>
          <span
            className={`text-[11px] font-semibold ${
              standing.streak.includes("연승")
                ? "text-blue-600 dark:text-blue-400"
                : "text-red-500 dark:text-red-400"
            }`}
          >
            {standing.streak}
          </span>
        </div>
      </div>
    </Link>
  );
}
