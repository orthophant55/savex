"use client";

import { useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import type { Game, Team } from "@/lib/types/kbo";
import GameCard from "@/components/games/GameCard";
import EmptyState from "@/components/common/EmptyState";
import { getGameStatusLabel, getGameStatusColor } from "@/lib/utils";

const STATUS_FILTERS = [
  { value: "all", label: "전체" },
  { value: "live", label: "진행중" },
  { value: "final", label: "종료" },
  { value: "scheduled", label: "예정" },
] as const;

type StatusFilter = (typeof STATUS_FILTERS)[number]["value"];

interface GamesPageClientProps {
  initialGames: Game[];
  teams: Team[];
  initialDate: string;
}

function addDays(dateStr: string, days: number): string {
  const d = new Date(dateStr);
  d.setDate(d.getDate() + days);
  return d.toISOString().slice(0, 10);
}

function formatDisplayDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("ko-KR", {
    month: "long",
    day: "numeric",
    weekday: "short",
  });
}

export default function GamesPageClient({
  initialGames,
  teams,
  initialDate,
}: GamesPageClientProps) {
  const [selectedDate, setSelectedDate] = useState(initialDate);
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");

  const getTeam = (id: string): Team =>
    teams.find((t) => t.id === id) ?? {
      id,
      name: id,
      shortName: id,
      city: "",
      stadium: "",
      logoPlaceholder: "#888",
      primaryColor: "#888",
      secondaryColor: "#ccc",
    };

  // 날짜가 바뀌면 실제로는 API 호출하겠지만 현재는 mock
  // 모든 날짜에서 initialGames를 보여줌 (mock data는 today 고정)
  const filteredGames =
    statusFilter === "all"
      ? initialGames
      : initialGames.filter((g) => g.status === statusFilter);

  const liveCount = initialGames.filter((g) => g.status === "live").length;

  return (
    <>
      {/* Date navigation */}
      <div className="flex items-center gap-3 mb-6">
        <button
          onClick={() => setSelectedDate((d) => addDays(d, -1))}
          className="p-2 rounded-lg border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          aria-label="이전 날짜"
        >
          <ChevronLeft className="h-4 w-4 text-zinc-600 dark:text-zinc-400" />
        </button>

        <div className="flex-1 text-center">
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 bg-transparent border-none outline-none cursor-pointer"
            aria-label="경기 날짜 선택"
          />
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
            {formatDisplayDate(selectedDate)}
          </p>
        </div>

        <button
          onClick={() => setSelectedDate((d) => addDays(d, 1))}
          className="p-2 rounded-lg border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          aria-label="다음 날짜"
        >
          <ChevronRight className="h-4 w-4 text-zinc-600 dark:text-zinc-400" />
        </button>
      </div>

      {/* Status filter */}
      <div
        className="flex gap-2 mb-6 flex-wrap"
        role="group"
        aria-label="경기 상태 필터"
      >
        {STATUS_FILTERS.map(({ value, label }) => (
          <button
            key={value}
            onClick={() => setStatusFilter(value)}
            className={`px-3 py-1.5 text-xs font-semibold rounded-full border transition-colors ${
              statusFilter === value
                ? "bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 border-zinc-900 dark:border-zinc-100"
                : "border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 hover:border-zinc-300 dark:hover:border-zinc-600"
            }`}
            aria-pressed={statusFilter === value}
          >
            {label}
            {value === "live" && liveCount > 0 && (
              <span className="ml-1.5 inline-flex items-center justify-center h-4 w-4 rounded-full bg-red-500 text-white text-[10px] font-bold">
                {liveCount}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Games grid */}
      {filteredGames.length === 0 ? (
        <EmptyState
          title="조건에 맞는 경기가 없습니다"
          description="날짜 또는 필터를 변경해 보세요."
        />
      ) : (
        <div className="space-y-3">
          {filteredGames.map((game) => (
            <div key={game.id} className="flex items-start gap-2">
              {/* Status pill */}
              <div className="pt-3.5 shrink-0 hidden sm:block">
                <span
                  className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${getGameStatusColor(
                    game.status
                  )}`}
                >
                  {getGameStatusLabel(game.status)}
                </span>
              </div>
              <div className="flex-1">
                <GameCard
                  game={game}
                  awayTeam={getTeam(game.awayTeamId)}
                  homeTeam={getTeam(game.homeTeamId)}
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </>
  );
}
