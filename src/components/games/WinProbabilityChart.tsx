"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ResponsiveContainer,
} from "recharts";
import type { WinProbabilityPoint, Team } from "@/lib/types/kbo";

interface WinProbabilityChartProps {
  data: WinProbabilityPoint[];
  awayTeam: Team;
  homeTeam: Team;
}

interface TooltipPayload {
  value: number;
  name: string;
  color: string;
}

function CustomTooltip({
  active,
  payload,
  label,
  data,
  awayTeam,
  homeTeam,
}: {
  active?: boolean;
  payload?: TooltipPayload[];
  label?: number;
  data: WinProbabilityPoint[];
  awayTeam: Team;
  homeTeam: Team;
}) {
  if (!active || !payload?.length) return null;

  const point = data.find((d) => d.playIndex === label);
  const awayProb = payload.find((p) => p.name === "away")?.value ?? 0;
  const homeProb = payload.find((p) => p.name === "home")?.value ?? 0;

  return (
    <div className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700 rounded-lg shadow-lg p-3 text-xs">
      {point?.label && (
        <p className="font-semibold text-zinc-900 dark:text-zinc-100 mb-1">
          {point.label}
        </p>
      )}
      <p className="text-zinc-500 dark:text-zinc-400 mb-1.5">
        {point?.inning}회 {point?.isTop ? "초" : "말"}
      </p>
      <div className="space-y-1">
        <div className="flex items-center justify-between gap-4">
          <span style={{ color: awayTeam.primaryColor }} className="font-medium">
            {awayTeam.shortName}
          </span>
          <span className="font-bold tabular-nums text-zinc-900 dark:text-zinc-100">
            {(awayProb * 100).toFixed(1)}%
          </span>
        </div>
        <div className="flex items-center justify-between gap-4">
          <span style={{ color: homeTeam.primaryColor }} className="font-medium">
            {homeTeam.shortName}
          </span>
          <span className="font-bold tabular-nums text-zinc-900 dark:text-zinc-100">
            {(homeProb * 100).toFixed(1)}%
          </span>
        </div>
      </div>
    </div>
  );
}

export default function WinProbabilityChart({
  data,
  awayTeam,
  homeTeam,
}: WinProbabilityChartProps) {
  const awayFinalProb = data[data.length - 1]?.awayWinProb ?? 0.5;
  const homeFinalProb = data[data.length - 1]?.homeWinProb ?? 0.5;

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
          승리 확률
        </h2>
        {/* Final probability summary */}
        <div className="flex items-center gap-3 text-xs">
          <span className="flex items-center gap-1.5">
            <span
              className="inline-block h-2.5 w-2.5 rounded-full"
              style={{ backgroundColor: awayTeam.primaryColor }}
              aria-hidden
            />
            <span className="font-medium text-zinc-600 dark:text-zinc-400">
              {awayTeam.shortName}
            </span>
            <span className="font-bold tabular-nums text-zinc-900 dark:text-zinc-100">
              {(awayFinalProb * 100).toFixed(1)}%
            </span>
          </span>
          <span className="flex items-center gap-1.5">
            <span
              className="inline-block h-2.5 w-2.5 rounded-full"
              style={{ backgroundColor: homeTeam.primaryColor }}
              aria-hidden
            />
            <span className="font-medium text-zinc-600 dark:text-zinc-400">
              {homeTeam.shortName}
            </span>
            <span className="font-bold tabular-nums text-zinc-900 dark:text-zinc-100">
              {(homeFinalProb * 100).toFixed(1)}%
            </span>
          </span>
        </div>
      </div>

      <div className="rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-4">
        {/* aria summary for accessibility */}
        <p className="sr-only">
          최종 승리 확률 — {awayTeam.name}: {(awayFinalProb * 100).toFixed(1)}%, {homeTeam.name}: {(homeFinalProb * 100).toFixed(1)}%
        </p>

        <div style={{ height: 240 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={data}
              margin={{ top: 5, right: 5, left: -20, bottom: 5 }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#e4e4e7"
                strokeOpacity={0.5}
              />
              <XAxis
                dataKey="playIndex"
                tick={{ fontSize: 10, fill: "#a1a1aa" }}
                tickLine={false}
                axisLine={false}
                label={{
                  value: "플레이",
                  position: "insideBottom",
                  offset: -2,
                  fontSize: 10,
                  fill: "#a1a1aa",
                }}
              />
              <YAxis
                domain={[0, 1]}
                tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
                tick={{ fontSize: 10, fill: "#a1a1aa" }}
                tickLine={false}
                axisLine={false}
                ticks={[0, 0.25, 0.5, 0.75, 1]}
              />
              <ReferenceLine
                y={0.5}
                stroke="#d4d4d8"
                strokeDasharray="4 4"
                strokeOpacity={0.8}
              />
              <Tooltip
                content={
                  <CustomTooltip
                    data={data}
                    awayTeam={awayTeam}
                    homeTeam={homeTeam}
                  />
                }
              />
              <Line
                type="monotone"
                dataKey="awayWinProb"
                name="away"
                stroke={awayTeam.primaryColor}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4, strokeWidth: 0 }}
              />
              <Line
                type="monotone"
                dataKey="homeWinProb"
                name="home"
                stroke={homeTeam.primaryColor}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4, strokeWidth: 0 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Legend */}
        <div className="flex items-center justify-center gap-6 mt-2" role="list" aria-label="범례">
          <div className="flex items-center gap-1.5 text-xs" role="listitem">
            <span
              className="inline-block h-0.5 w-6 rounded"
              style={{ backgroundColor: awayTeam.primaryColor }}
              aria-hidden
            />
            <span className="text-zinc-600 dark:text-zinc-400">
              {awayTeam.name} (원정)
            </span>
          </div>
          <div className="flex items-center gap-1.5 text-xs" role="listitem">
            <span
              className="inline-block h-0.5 w-6 rounded"
              style={{ backgroundColor: homeTeam.primaryColor }}
              aria-hidden
            />
            <span className="text-zinc-600 dark:text-zinc-400">
              {homeTeam.name} (홈)
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
