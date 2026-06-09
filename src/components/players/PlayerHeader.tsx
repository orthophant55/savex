import type { Player, Team } from "@/lib/types/kbo";
import { getPositionAbbr } from "@/lib/utils";

interface PlayerHeaderProps {
  player: Player;
  team: Team;
}

export default function PlayerHeader({ player, team }: PlayerHeaderProps) {
  const isPitcher = player.position === "투수";

  return (
    <div
      className="rounded-xl overflow-hidden"
      style={{
        background: `linear-gradient(135deg, ${team.primaryColor}ee, ${team.primaryColor}88)`,
      }}
    >
      <div className="px-6 py-8">
        <div className="flex flex-col sm:flex-row items-center sm:items-start gap-5">
          {/* Number placeholder */}
          <div
            className="h-20 w-20 rounded-full flex items-center justify-center text-white font-black text-2xl shrink-0 border-2 border-white/30 shadow-lg"
            style={{ backgroundColor: `${team.primaryColor}cc` }}
            aria-label={`등번호 ${player.number}`}
          >
            {player.number}
          </div>

          {/* Info */}
          <div className="flex-1 text-center sm:text-left">
            {/* Name & badges */}
            <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2 mb-1">
              <span className="bg-white/20 text-white text-xs font-semibold px-2.5 py-0.5 rounded-full">
                {team.shortName}
              </span>
              <span className="bg-white/20 text-white text-xs font-semibold px-2.5 py-0.5 rounded-full">
                {getPositionAbbr(player.position)} · {player.position}
              </span>
            </div>
            <h1 className="text-white text-3xl font-black">{player.name}</h1>

            {/* Physical info */}
            <div className="flex flex-wrap items-center justify-center sm:justify-start gap-4 mt-4 text-white/80 text-sm">
              <span>{player.age}세 ({player.birthDate})</span>
              <span aria-hidden>·</span>
              <span>{player.height}cm / {player.weight}kg</span>
              <span aria-hidden>·</span>
              <span>{player.throws} / {player.bats}</span>
            </div>

            {/* Key stats quick view */}
            <div className="flex flex-wrap gap-3 mt-4">
              {isPitcher ? (
                <>
                  {player.seasonStat.era !== undefined && (
                    <div className="bg-white/15 rounded-lg px-3 py-2 text-center min-w-[56px]">
                      <p className="text-white/70 text-[10px] uppercase tracking-wide">ERA</p>
                      <p className="text-white font-black text-lg tabular-nums">
                        {player.seasonStat.era.toFixed(2)}
                      </p>
                    </div>
                  )}
                  {player.seasonStat.fip !== undefined && (
                    <div className="bg-white/15 rounded-lg px-3 py-2 text-center min-w-[56px]">
                      <p className="text-white/70 text-[10px] uppercase tracking-wide">FIP</p>
                      <p className="text-white font-black text-lg tabular-nums">
                        {player.seasonStat.fip.toFixed(2)}
                      </p>
                    </div>
                  )}
                  {player.seasonStat.whip !== undefined && (
                    <div className="bg-white/15 rounded-lg px-3 py-2 text-center min-w-[56px]">
                      <p className="text-white/70 text-[10px] uppercase tracking-wide">WHIP</p>
                      <p className="text-white font-black text-lg tabular-nums">
                        {player.seasonStat.whip.toFixed(2)}
                      </p>
                    </div>
                  )}
                </>
              ) : (
                <>
                  {player.seasonStat.avg !== undefined && (
                    <div className="bg-white/15 rounded-lg px-3 py-2 text-center min-w-[56px]">
                      <p className="text-white/70 text-[10px] uppercase tracking-wide">AVG</p>
                      <p className="text-white font-black text-lg tabular-nums">
                        {player.seasonStat.avg.toFixed(3).replace("0.", ".")}
                      </p>
                    </div>
                  )}
                  {player.seasonStat.ops !== undefined && (
                    <div className="bg-white/15 rounded-lg px-3 py-2 text-center min-w-[56px]">
                      <p className="text-white/70 text-[10px] uppercase tracking-wide">OPS</p>
                      <p className="text-white font-black text-lg tabular-nums">
                        {player.seasonStat.ops.toFixed(3).replace("0.", ".")}
                      </p>
                    </div>
                  )}
                  {player.seasonStat.homeRuns !== undefined && (
                    <div className="bg-white/15 rounded-lg px-3 py-2 text-center min-w-[56px]">
                      <p className="text-white/70 text-[10px] uppercase tracking-wide">HR</p>
                      <p className="text-white font-black text-lg tabular-nums">
                        {player.seasonStat.homeRuns}
                      </p>
                    </div>
                  )}
                </>
              )}
              {player.seasonStat.war !== undefined && (
                <div className="bg-white/15 rounded-lg px-3 py-2 text-center min-w-[56px]">
                  <p className="text-white/70 text-[10px] uppercase tracking-wide">WAR</p>
                  <p className="text-white font-black text-lg tabular-nums">
                    {player.seasonStat.war.toFixed(1)}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
