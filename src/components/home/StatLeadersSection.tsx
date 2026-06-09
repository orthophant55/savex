import Link from "next/link";
import { ArrowRight } from "lucide-react";
import type { StatLeader } from "@/lib/types/kbo";
import SectionHeader from "@/components/common/SectionHeader";
import { formatStat, formatAvg, formatEra } from "@/lib/utils";

interface StatLeadersSectionProps {
  leaders: StatLeader[];
}

function formatValue(category: string, value: number): string {
  if (category === "타율" || category === "OPS") return formatAvg(value);
  if (category === "ERA") return formatEra(value);
  if (category === "WAR") return value.toFixed(1);
  if (Number.isInteger(value)) return String(value);
  return formatStat(value, 3);
}

function LeaderCard({ leader }: { leader: StatLeader }) {
  const top3 = leader.leaders.slice(0, 3);

  return (
    <div className="rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
          {leader.category}
        </h3>
        {leader.isLowerBetter && (
          <span className="text-[10px] text-zinc-400 dark:text-zinc-500 bg-zinc-100 dark:bg-zinc-800 px-1.5 py-0.5 rounded">
            낮을수록 좋음
          </span>
        )}
      </div>

      <div className="space-y-2">
        {top3.map((entry, idx) => (
          <div key={entry.playerId} className="flex items-center gap-2">
            <span
              className={`text-[11px] font-bold w-4 tabular-nums shrink-0 ${
                idx === 0
                  ? "text-yellow-500"
                  : idx === 1
                  ? "text-zinc-400 dark:text-zinc-500"
                  : "text-orange-400"
              }`}
              aria-label={`${idx + 1}위`}
            >
              {idx + 1}
            </span>
            <Link
              href={`/players/${entry.playerId}`}
              className="flex-1 min-w-0 hover:underline"
              aria-label={`${entry.playerName} 선수 상세 보기`}
            >
              <p className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 truncate">
                {entry.playerName}
              </p>
              <p className="text-[10px] text-zinc-400 dark:text-zinc-500 truncate">
                {entry.teamName}
              </p>
            </Link>
            <span
              className={`text-sm font-bold tabular-nums shrink-0 ${
                idx === 0
                  ? "text-zinc-900 dark:text-zinc-100"
                  : "text-zinc-600 dark:text-zinc-400"
              }`}
            >
              {formatValue(leader.category, entry.value)}
              {leader.unit && (
                <span className="text-xs font-normal ml-0.5">{leader.unit}</span>
              )}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function StatLeadersSection({ leaders }: StatLeadersSectionProps) {
  return (
    <section aria-labelledby="stat-leaders-heading">
      <SectionHeader
        title="주요 지표 리더"
        description="2026 시즌"
        action={
          <Link
            href="/players"
            className="flex items-center gap-1 text-xs text-blue-600 dark:text-blue-400 hover:underline font-medium"
            aria-label="선수 전체 스탯 보기"
          >
            전체 선수
            <ArrowRight className="h-3.5 w-3.5" aria-hidden />
          </Link>
        }
      />
      <span id="stat-leaders-heading" className="sr-only">
        주요 지표 리더
      </span>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {leaders.map((leader) => (
          <LeaderCard key={leader.category} leader={leader} />
        ))}
      </div>
    </section>
  );
}
