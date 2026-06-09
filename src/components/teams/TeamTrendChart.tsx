"use client";

import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

interface TrendDataPoint {
  period: string;
  winRate: number;
  runs: number;
  runsAllowed: number;
}

interface TeamTrendChartProps {
  data: TrendDataPoint[];
  primaryColor: string;
  teamName: string;
}

export default function TeamTrendChart({
  data,
  primaryColor,
  teamName,
}: TeamTrendChartProps) {
  return (
    <div>
      <h2 className="text-sm font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">
        월별 트렌드
      </h2>
      <div className="rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-4">
        <p className="sr-only">
          {teamName} 월별 승률 및 득·실점 추이 차트
        </p>
        <div style={{ height: 240 }}>
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={data} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e4e4e7" strokeOpacity={0.5} />
              <XAxis
                dataKey="period"
                tick={{ fontSize: 11, fill: "#a1a1aa" }}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                yAxisId="rate"
                orientation="right"
                domain={[0.2, 0.8]}
                tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
                tick={{ fontSize: 10, fill: "#a1a1aa" }}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                yAxisId="runs"
                orientation="left"
                domain={[0, 12]}
                tick={{ fontSize: 10, fill: "#a1a1aa" }}
                tickLine={false}
                axisLine={false}
              />
              <Tooltip
                formatter={(value, name) => {
                  const v = typeof value === "number" ? value : 0;
                  if (name === "승률") return [`${(v * 100).toFixed(1)}%`, name as string];
                  return [v, name as string];
                }}
                contentStyle={{
                  fontSize: 12,
                  borderRadius: 8,
                  border: "1px solid #e4e4e7",
                }}
              />
              <Legend
                wrapperStyle={{ fontSize: 11, paddingTop: 8 }}
              />
              <Bar yAxisId="runs" dataKey="runs" name="득점" fill="#93c5fd" opacity={0.7} radius={[3, 3, 0, 0]} />
              <Bar yAxisId="runs" dataKey="runsAllowed" name="실점" fill="#fca5a5" opacity={0.7} radius={[3, 3, 0, 0]} />
              <Line
                yAxisId="rate"
                type="monotone"
                dataKey="winRate"
                name="승률"
                stroke={primaryColor}
                strokeWidth={2.5}
                dot={{ r: 4, fill: primaryColor, strokeWidth: 0 }}
                activeDot={{ r: 6 }}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
        <p className="text-[10px] text-zinc-400 dark:text-zinc-500 text-center mt-1">
          * 예시 데이터입니다
        </p>
      </div>
    </div>
  );
}
