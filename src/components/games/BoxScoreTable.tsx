import type { Game, Team } from "@/lib/types/kbo";

interface BoxScoreTableProps {
  game: Game;
  awayTeam: Team;
  homeTeam: Team;
}

export default function BoxScoreTable({
  game,
  awayTeam,
  homeTeam,
}: BoxScoreTableProps) {
  if (!game.boxScore) return null;

  const { innings, awayRuns, homeRuns, awayHits, homeHits, awayErrors, homeErrors } =
    game.boxScore;

  const awayByInning = innings.map((i) => i.top);
  const homeByInning = innings.map((i) => i.bottom);
  const inningNumbers = innings.map((i) => i.inning);

  return (
    <div>
      <h2 className="text-sm font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">
        박스스코어
      </h2>
      <div className="table-scroll rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900">
        <table
          className="w-full text-sm min-w-max"
          aria-label="이닝별 득점 박스스코어"
        >
          <thead>
            <tr className="border-b border-zinc-100 dark:border-zinc-800">
              <th className="text-left px-4 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 text-xs w-24">
                팀
              </th>
              {inningNumbers.map((n) => (
                <th
                  key={n}
                  className="text-center px-2 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 text-xs w-9"
                  scope="col"
                >
                  {n}
                </th>
              ))}
              <th className="text-center px-3 py-2.5 font-bold text-zinc-700 dark:text-zinc-300 text-xs border-l border-zinc-100 dark:border-zinc-800 w-9">
                R
              </th>
              <th className="text-center px-3 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 text-xs w-9">
                H
              </th>
              <th className="text-center px-3 py-2.5 font-semibold text-zinc-500 dark:text-zinc-400 text-xs w-9">
                E
              </th>
            </tr>
          </thead>
          <tbody>
            {/* Away team row */}
            <tr className="border-b border-zinc-50 dark:border-zinc-800/50">
              <td className="px-4 py-2.5">
                <div className="flex items-center gap-2">
                  <div
                    className="h-5 w-5 rounded-full flex items-center justify-center text-white text-[9px] font-bold shrink-0"
                    style={{ backgroundColor: awayTeam.primaryColor }}
                    aria-hidden
                  />
                  <span className="font-semibold text-zinc-900 dark:text-zinc-100 text-xs">
                    {awayTeam.shortName}
                  </span>
                </div>
              </td>
              {awayByInning.map((score, i) => (
                <td
                  key={i}
                  className="text-center px-2 py-2.5 text-sm tabular-nums text-zinc-700 dark:text-zinc-300"
                >
                  {score !== null ? (
                    score > 0 ? (
                      <span className="font-bold text-zinc-900 dark:text-zinc-100">
                        {score}
                      </span>
                    ) : (
                      score
                    )
                  ) : (
                    <span className="text-zinc-300 dark:text-zinc-600">—</span>
                  )}
                </td>
              ))}
              <td className="text-center px-3 py-2.5 font-bold text-zinc-900 dark:text-zinc-100 border-l border-zinc-100 dark:border-zinc-800 tabular-nums">
                {awayRuns}
              </td>
              <td className="text-center px-3 py-2.5 text-zinc-600 dark:text-zinc-400 tabular-nums text-sm">
                {awayHits}
              </td>
              <td className="text-center px-3 py-2.5 text-zinc-600 dark:text-zinc-400 tabular-nums text-sm">
                {awayErrors}
              </td>
            </tr>

            {/* Home team row */}
            <tr>
              <td className="px-4 py-2.5">
                <div className="flex items-center gap-2">
                  <div
                    className="h-5 w-5 rounded-full flex items-center justify-center text-white text-[9px] font-bold shrink-0"
                    style={{ backgroundColor: homeTeam.primaryColor }}
                    aria-hidden
                  />
                  <span className="font-semibold text-zinc-900 dark:text-zinc-100 text-xs">
                    {homeTeam.shortName}
                  </span>
                </div>
              </td>
              {homeByInning.map((score, i) => (
                <td
                  key={i}
                  className="text-center px-2 py-2.5 text-sm tabular-nums text-zinc-700 dark:text-zinc-300"
                >
                  {score !== null ? (
                    score > 0 ? (
                      <span className="font-bold text-zinc-900 dark:text-zinc-100">
                        {score}
                      </span>
                    ) : (
                      score
                    )
                  ) : (
                    <span className="text-zinc-300 dark:text-zinc-600">—</span>
                  )}
                </td>
              ))}
              <td className="text-center px-3 py-2.5 font-bold text-zinc-900 dark:text-zinc-100 border-l border-zinc-100 dark:border-zinc-800 tabular-nums">
                {homeRuns}
              </td>
              <td className="text-center px-3 py-2.5 text-zinc-600 dark:text-zinc-400 tabular-nums text-sm">
                {homeHits}
              </td>
              <td className="text-center px-3 py-2.5 text-zinc-600 dark:text-zinc-400 tabular-nums text-sm">
                {homeErrors}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
