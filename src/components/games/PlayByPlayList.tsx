import type { PlayEvent, Team } from "@/lib/types/kbo";
import { cn } from "@/lib/utils";

interface PlayByPlayListProps {
  events: PlayEvent[];
  awayTeam: Team;
  homeTeam: Team;
}

function getEventIcon(eventType: PlayEvent["eventType"]): string {
  const icons: Record<PlayEvent["eventType"], string> = {
    homerun: "💥",
    hit: "🎯",
    strikeout: "K",
    walk: "BB",
    out: "○",
    error: "E",
    stolen_base: "SB",
    double_play: "DP",
    run_scored: "R",
    pitching_change: "🔄",
    inning_end: "▪",
  };
  return icons[eventType] ?? "•";
}

function getEventStyle(eventType: PlayEvent["eventType"]): string {
  switch (eventType) {
    case "homerun":
      return "bg-orange-50 dark:bg-orange-950/30 border-l-4 border-orange-400";
    case "hit":
      return "bg-blue-50 dark:bg-blue-950/30 border-l-4 border-blue-300";
    case "run_scored":
      return "bg-green-50 dark:bg-green-950/30 border-l-4 border-green-400";
    case "pitching_change":
      return "bg-zinc-50 dark:bg-zinc-800/50 border-l-4 border-zinc-300 dark:border-zinc-600";
    case "inning_end":
      return "bg-zinc-50 dark:bg-zinc-800/50 border-l-4 border-zinc-200 dark:border-zinc-700";
    default:
      return "border-l-4 border-transparent";
  }
}

function WpaBadge({ wpa }: { wpa: number }) {
  const isPositive = wpa > 0;
  const abs = Math.abs(wpa);
  if (abs < 0.03) return null;
  return (
    <span
      className={cn(
        "text-[10px] font-mono font-semibold tabular-nums px-1.5 py-0.5 rounded",
        isPositive
          ? "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300"
          : "bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300"
      )}
      title={`WPA: ${wpa > 0 ? "+" : ""}${wpa.toFixed(3)}`}
      aria-label={`승리확률 기여 ${wpa > 0 ? "+" : ""}${wpa.toFixed(3)}`}
    >
      {wpa > 0 ? "+" : ""}
      {wpa.toFixed(2)}
    </span>
  );
}

function LiBadge({ li }: { li: number }) {
  if (li < 1.5) return null;
  return (
    <span
      className="text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded bg-yellow-100 text-yellow-700 dark:bg-yellow-900/40 dark:text-yellow-300"
      title={`Leverage Index: ${li.toFixed(2)}`}
      aria-label={`레버리지 인덱스 ${li.toFixed(2)}`}
    >
      LI {li.toFixed(1)}
    </span>
  );
}

export default function PlayByPlayList({
  events,
  awayTeam,
  homeTeam,
}: PlayByPlayListProps) {
  // 이닝별 그룹화
  const grouped = events.reduce<Record<string, PlayEvent[]>>((acc, e) => {
    const key = `${e.inning}-${e.isTop ? "top" : "bot"}`;
    if (!acc[key]) acc[key] = [];
    acc[key].push(e);
    return acc;
  }, {});

  const groupKeys = Object.keys(grouped).sort((a, b) => {
    const [inA, hA] = a.split("-");
    const [inB, hB] = b.split("-");
    const innA = parseInt(inA), innB = parseInt(inB);
    if (innA !== innB) return innA - innB;
    return hA === "top" ? -1 : 1;
  });

  return (
    <div>
      <h2 className="text-sm font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">
        플레이 바이 플레이
      </h2>
      <div className="space-y-4" aria-label="이닝별 경기 진행">
        {groupKeys.map((key) => {
          const [inningStr, half] = key.split("-");
          const inning = parseInt(inningStr);
          const isTop = half === "top";
          const battingTeam = isTop ? awayTeam : homeTeam;

          return (
            <div key={key} className="rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 overflow-hidden">
              {/* Inning header */}
              <div
                className="px-4 py-2 flex items-center gap-2 border-b border-zinc-100 dark:border-zinc-800"
                style={{ borderLeftWidth: 4, borderLeftColor: battingTeam.primaryColor }}
              >
                <span className="text-xs font-bold text-zinc-600 dark:text-zinc-300">
                  {inning}회 {isTop ? "초" : "말"}
                </span>
                <div
                  className="h-4 w-4 rounded-full flex items-center justify-center text-white text-[8px] font-bold"
                  style={{ backgroundColor: battingTeam.primaryColor }}
                  aria-hidden
                />
                <span className="text-xs text-zinc-500 dark:text-zinc-400">
                  {battingTeam.shortName} 공격
                </span>
              </div>

              {/* Events */}
              <div className="divide-y divide-zinc-50 dark:divide-zinc-800/50">
                {grouped[key].map((event) => (
                  <div
                    key={event.id}
                    className={cn(
                      "px-4 py-2.5 text-sm",
                      getEventStyle(event.eventType)
                    )}
                  >
                    <div className="flex items-start gap-2">
                      <span
                        className="shrink-0 mt-0.5 text-xs font-mono w-6 text-center"
                        aria-hidden
                      >
                        {getEventIcon(event.eventType)}
                      </span>
                      <div className="flex-1 min-w-0">
                        <p className="text-zinc-800 dark:text-zinc-200 leading-snug text-[13px]">
                          {event.description}
                        </p>
                        <div className="mt-1 flex items-center gap-2 flex-wrap">
                          {/* Score */}
                          <span className="text-[11px] font-semibold text-zinc-500 dark:text-zinc-400 tabular-nums">
                            {awayTeam.shortName} {event.awayScore} :{" "}
                            {event.homeScore} {homeTeam.shortName}
                          </span>
                          {event.runnersOn && (
                            <span className="text-[10px] text-zinc-400 dark:text-zinc-500">
                              {event.runnersOn}
                            </span>
                          )}
                          <WpaBadge wpa={event.wpa} />
                          <LiBadge li={event.li} />
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
