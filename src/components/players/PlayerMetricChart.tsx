"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

interface MonthlyDataPoint {
  month: string;
  value: number;
}

interface PlayerMetricChartProps {
  data: MonthlyDataPoint[];
  label: string;
  color: string;
  isLowerBetter?: boolean;
  seasonAvg: number;
}

export default function PlayerMetricChart({
  data,
  label,
  color,
  isLowerBetter = false,
  seasonAvg,
}: PlayerMetricChartProps) {
  const min = Math.min(...data.map((d) => d.value));
  const max = Math.max(...data.map((d) => d.value));
  const padding = (max - min) * 0.3 || 0.05;
  const domain: [number, number] = [
    parseFloat((min - padding).toFixed(3)),
    parseFloat((max + padding).toFixed(3)),
  ];

  const formatValue = (v: number) =>
    label === "ERA" || label === "FIP" || label === "WHIP"
      ? v.toFixed(2)
      : v.toFixed(3).replace("0.", ".");

  const best = isLowerBetter ? min : max;

  return (
    <div>
      <h2 className="text-sm font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">
        월별 {label} 추이
      </h2>
      <div className="rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-4">
        <p className="sr-only">
          {label} 월별 추이. 시즌 평균: {formatValue(seasonAvg)}.
          최고 기록: {formatValue(best)}.
        </p>

        {/* Summary */}
        <div className="flex items-center gap-4 mb-3 text-xs">
          <div>
            <span className="text-zinc-400 dark:text-zinc-500">시즌 평균 </span>
            <span className="font-bold text-zinc-900 dark:text-zinc-100 tabular-nums">
              {formatValue(seasonAvg)}
            </span>
          </div>
          <div>
            <span className="text-zinc-400 dark:text-zinc-500">
              {isLowerBetter ? "최저 (최고)" : "최고"}{" "}
            </span>
            <span className="font-bold tabular-nums" style={{ color }}>
              {formatValue(best)}
            </span>
          </div>
        </div>

        <div style={{ height: 200 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e4e4e7" strokeOpacity={0.5} />
              <XAxis
                dataKey="month"
                tick={{ fontSize: 11, fill: "#a1a1aa" }}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                domain={domain}
                tickFormatter={formatValue}
                tick={{ fontSize: 10, fill: "#a1a1aa" }}
                tickLine={false}
                axisLine={false}
              />
              <ReferenceLine
                y={seasonAvg}
                stroke="#d4d4d8"
                strokeDasharray="4 4"
                label={{ value: "평균", position: "insideRight", fontSize: 10, fill: "#a1a1aa" }}
              />
              <Tooltip
                formatter={(v) => [typeof v === "number" ? formatValue(v) : String(v), label]}
                contentStyle={{ fontSize: 12, borderRadius: 8, border: "1px solid #e4e4e7" }}
              />
              <Line
                type="monotone"
                dataKey="value"
                name={label}
                stroke={color}
                strokeWidth={2.5}
                dot={{ r: 5, fill: color, strokeWidth: 0 }}
                activeDot={{ r: 7 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <p className="text-[10px] text-zinc-400 dark:text-zinc-500 text-center mt-1">
          * 예시 데이터입니다
        </p>
      </div>
    </div>
  );
}
