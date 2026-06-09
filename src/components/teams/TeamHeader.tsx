import type { Team, Standing } from "@/lib/types/kbo";
import { formatWinRate, getWinRateColor } from "@/lib/utils";

interface TeamHeaderProps {
  team: Team;
  standing: Standing;
}

export default function TeamHeader({ team, standing }: TeamHeaderProps) {
  return (
    <div
      className="rounded-xl overflow-hidden"
      style={{
        background: `linear-gradient(135deg, ${team.primaryColor}dd, ${team.primaryColor}88)`,
      }}
    >
      <div className="px-6 py-8">
        <div className="flex flex-col sm:flex-row items-center sm:items-start gap-5">
          {/* Logo */}
          <div
            className="h-20 w-20 rounded-full flex items-center justify-center text-white font-black text-2xl shrink-0 shadow-lg border-2 border-white/30"
            style={{ backgroundColor: team.primaryColor }}
            aria-label={team.name}
          >
            {team.shortName.slice(0, 2)}
          </div>

          {/* Info */}
          <div className="flex-1 text-center sm:text-left">
            <p className="text-white/70 text-sm">{team.city} · {team.stadium}</p>
            <h1 className="text-white text-2xl font-black mt-1">{team.name}</h1>

            {/* Stats row */}
            <div className="flex flex-wrap items-center justify-center sm:justify-start gap-4 mt-4">
              <div className="text-center sm:text-left">
                <p className="text-white/60 text-[10px] uppercase tracking-wide">순위</p>
                <p className="text-white text-xl font-black">{standing.rank}위</p>
              </div>
              <div className="h-8 w-px bg-white/20 hidden sm:block" aria-hidden />
              <div className="text-center sm:text-left">
                <p className="text-white/60 text-[10px] uppercase tracking-wide">승률</p>
                <p className="text-white text-xl font-black tabular-nums">
                  {formatWinRate(standing.winRate)}
                </p>
              </div>
              <div className="h-8 w-px bg-white/20 hidden sm:block" aria-hidden />
              <div className="text-center sm:text-left">
                <p className="text-white/60 text-[10px] uppercase tracking-wide">성적</p>
                <p className="text-white text-xl font-black tabular-nums">
                  {standing.wins}승 {standing.losses}패 {standing.draws}무
                </p>
              </div>
              <div className="h-8 w-px bg-white/20 hidden sm:block" aria-hidden />
              <div className="text-center sm:text-left">
                <p className="text-white/60 text-[10px] uppercase tracking-wide">최근 10경기</p>
                <p className="text-white text-xl font-black">{standing.last10}</p>
              </div>
              <div className="h-8 w-px bg-white/20 hidden sm:block" aria-hidden />
              <div className="text-center sm:text-left">
                <p className="text-white/60 text-[10px] uppercase tracking-wide">연속</p>
                <p className="text-white text-xl font-black">{standing.streak}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
