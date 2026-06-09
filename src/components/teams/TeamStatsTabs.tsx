"use client";

import { useRef, useState } from "react";
import type { Player, Standing } from "@/lib/types/kbo";
import RosterTable from "./RosterTable";
import { formatAvg, formatEra, formatWinRate } from "@/lib/utils";
import Link from "next/link";

const TABS = [
  { id: "overview", label: "개요" },
  { id: "batting", label: "타격" },
  { id: "pitching", label: "투구" },
  { id: "defense", label: "수비" },
] as const;

type TabId = (typeof TABS)[number]["id"];

interface TeamStatsTabsProps {
  players: Player[];
  standing: Standing;
}

function OverviewTab({ players, standing }: TeamStatsTabsProps) {
  const batters = players
    .filter((p) => p.position !== "투수")
    .sort((a, b) => (b.seasonStat.ops ?? 0) - (a.seasonStat.ops ?? 0))
    .slice(0, 3);

  const pitchers = players
    .filter((p) => p.position === "투수")
    .sort((a, b) => (a.seasonStat.era ?? 99) - (b.seasonStat.era ?? 99))
    .slice(0, 3);

  return (
    <div className="space-y-6">
      {/* Season record */}
      <div>
        <h3 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">
          시즌 성적
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: "승", value: standing.wins, color: "text-blue-600 dark:text-blue-400" },
            { label: "패", value: standing.losses, color: "text-red-500 dark:text-red-400" },
            { label: "무", value: standing.draws, color: "text-zinc-500 dark:text-zinc-400" },
            {
              label: "승률",
              value: formatWinRate(standing.winRate),
              color: "text-zinc-900 dark:text-zinc-100",
            },
          ].map(({ label, value, color }) => (
            <div
              key={label}
              className="rounded-lg border border-zinc-200 dark:border-zinc-800 p-3 text-center"
            >
              <p className="text-[10px] text-zinc-500 dark:text-zinc-400">{label}</p>
              <p className={`text-xl font-black tabular-nums ${color}`}>{value}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Top performers */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {/* Top batters */}
        <div>
          <h3 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">
            타격 상위
          </h3>
          <div className="space-y-2">
            {batters.map((p, i) => (
              <Link
                key={p.id}
                href={`/players/${p.id}`}
                className="flex items-center gap-3 p-2.5 rounded-lg border border-zinc-100 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors"
              >
                <span className="text-xs font-bold text-zinc-400 w-4">{i + 1}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 truncate">
                    {p.name}
                  </p>
                  <p className="text-[10px] text-zinc-400 dark:text-zinc-500">{p.position}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-bold tabular-nums text-zinc-900 dark:text-zinc-100">
                    {formatAvg(p.seasonStat.ops)}
                  </p>
                  <p className="text-[10px] text-zinc-400 dark:text-zinc-500">OPS</p>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Top pitchers */}
        <div>
          <h3 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">
            투구 상위
          </h3>
          <div className="space-y-2">
            {pitchers.map((p, i) => (
              <Link
                key={p.id}
                href={`/players/${p.id}`}
                className="flex items-center gap-3 p-2.5 rounded-lg border border-zinc-100 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors"
              >
                <span className="text-xs font-bold text-zinc-400 w-4">{i + 1}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 truncate">
                    {p.name}
                  </p>
                  <p className="text-[10px] text-zinc-400 dark:text-zinc-500">투수</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-bold tabular-nums text-zinc-900 dark:text-zinc-100">
                    {formatEra(p.seasonStat.era)}
                  </p>
                  <p className="text-[10px] text-zinc-400 dark:text-zinc-500">ERA</p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function TeamStatsTabs({ players, standing }: TeamStatsTabsProps) {
  const [activeTab, setActiveTab] = useState<TabId>("overview");
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([]);

  function handleTabKeyDown(e: React.KeyboardEvent, idx: number) {
    let next = idx;
    if (e.key === "ArrowRight") next = (idx + 1) % TABS.length;
    else if (e.key === "ArrowLeft") next = (idx - 1 + TABS.length) % TABS.length;
    else return;
    e.preventDefault();
    setActiveTab(TABS[next].id);
    tabRefs.current[next]?.focus();
  }

  return (
    <div>
      {/* Tab bar */}
      <div
        className="flex gap-1 border-b border-zinc-200 dark:border-zinc-800 mb-5"
        role="tablist"
        aria-label="팀 스탯 탭"
      >
        {TABS.map(({ id, label }, idx) => (
          <button
            key={id}
            ref={(el) => { tabRefs.current[idx] = el; }}
            role="tab"
            aria-selected={activeTab === id}
            aria-controls={`tab-panel-${id}`}
            tabIndex={activeTab === id ? 0 : -1}
            onClick={() => setActiveTab(id)}
            onKeyDown={(e) => handleTabKeyDown(e, idx)}
            className={`px-4 py-2.5 text-sm font-semibold border-b-2 -mb-px transition-colors ${
              activeTab === id
                ? "border-blue-600 dark:border-blue-400 text-blue-600 dark:text-blue-400"
                : "border-transparent text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100"
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Tab panels */}
      <div
        id={`tab-panel-${activeTab}`}
        role="tabpanel"
        aria-label={TABS.find((t) => t.id === activeTab)?.label}
      >
        {activeTab === "overview" && (
          <OverviewTab players={players} standing={standing} />
        )}
        {activeTab === "batting" && (
          <RosterTable players={players} mode="batting" />
        )}
        {activeTab === "pitching" && (
          <RosterTable players={players} mode="pitching" />
        )}
        {activeTab === "defense" && (
          <div className="py-12 text-center text-zinc-400 dark:text-zinc-500">
            <p className="text-sm">수비 스탯은 준비 중입니다.</p>
            <p className="text-xs mt-1">향후 UZR, DRS 지표를 제공할 예정입니다.</p>
          </div>
        )}
      </div>
    </div>
  );
}
