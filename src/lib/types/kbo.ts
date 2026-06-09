export type GameStatus = "scheduled" | "live" | "final" | "postponed";

export type Position =
  | "투수"
  | "포수"
  | "1루수"
  | "2루수"
  | "3루수"
  | "유격수"
  | "좌익수"
  | "중견수"
  | "우익수"
  | "지명타자";

export interface Team {
  id: string;
  name: string;
  shortName: string;
  city: string;
  stadium: string;
  logoPlaceholder: string; // 팀 색상 hex
  primaryColor: string;
  secondaryColor: string;
}

export interface Standing {
  rank: number;
  team: Team;
  wins: number;
  losses: number;
  draws: number;
  winRate: number;
  gamesBehind: number;
  last10: string; // e.g. "6승4패"
  streak: string; // e.g. "3연승"
  recentForm: ("W" | "L" | "D")[]; // 최근 5경기
}

export interface PlayerSeasonStat {
  playerId: string;
  season: number;
  teamId: string;
  // 타자
  games?: number;
  atBats?: number;
  hits?: number;
  homeRuns?: number;
  rbi?: number;
  avg?: number; // 타율
  obp?: number; // 출루율
  slg?: number; // 장타율
  ops?: number; // OPS
  wOBA?: number; // wOBA
  wRC?: number; // wRC+
  war?: number; // WAR
  babip?: number; // BABIP
  iso?: number; // ISO
  bbPct?: number; // BB%
  kPct?: number; // K%
  // 투수
  era?: number; // ERA
  fip?: number; // FIP
  xFip?: number; // xFIP
  whip?: number; // WHIP
  innings?: number; // IP
  strikeouts?: number; // K
  walks?: number; // BB
  kPer9?: number; // K/9
  bbPer9?: number; // BB/9
  hrPer9?: number; // HR/9
  leftOnBasePct?: number; // LOB%
  groundBallPct?: number; // GB%
  wins2?: number; // 승
  losses2?: number; // 패
  saves?: number; // 세이브
  holds?: number; // 홀드
}

export interface Player {
  id: string;
  name: string;
  teamId: string;
  position: Position;
  number: number;
  age: number;
  birthDate: string;
  throws: "우투" | "좌투" | "양투";
  bats: "우타" | "좌타" | "양타";
  height: number; // cm
  weight: number; // kg
  seasonStat: PlayerSeasonStat;
  careerStats: PlayerSeasonStat[];
}

export interface BoxScoreInning {
  inning: number;
  top: number | null; // 원정팀 득점
  bottom: number | null; // 홈팀 득점
}

export interface BoxScore {
  gameId: string;
  innings: BoxScoreInning[];
  awayRuns: number;
  homeRuns: number;
  awayHits: number;
  homeHits: number;
  awayErrors: number;
  homeErrors: number;
  awayLob: number; // 잔루
  homeLob: number;
}

export interface PlayEvent {
  id: string;
  gameId: string;
  inning: number;
  isTop: boolean; // true = 초
  playIndex: number;
  batter: string;
  pitcher: string;
  description: string;
  eventType:
    | "hit"
    | "homerun"
    | "strikeout"
    | "walk"
    | "out"
    | "error"
    | "stolen_base"
    | "double_play"
    | "run_scored"
    | "pitching_change"
    | "inning_end";
  runsScored: number;
  wpa: number; // Win Probability Added (-1 ~ 1)
  li: number; // Leverage Index
  awayScore: number;
  homeScore: number;
  outs: number;
  runnersOn: string; // e.g. "1,2루" | "만루" | ""
}

export interface WinProbabilityPoint {
  playIndex: number;
  inning: number;
  isTop: boolean;
  awayWinProb: number; // 0 ~ 1
  homeWinProb: number; // 0 ~ 1
  label?: string;
}

export interface Game {
  id: string;
  date: string; // YYYY-MM-DD
  startTime: string; // HH:mm
  awayTeamId: string;
  homeTeamId: string;
  stadium: string;
  status: GameStatus;
  awayScore: number | null;
  homeScore: number | null;
  currentInning?: number;
  isTopInning?: boolean;
  boxScore?: BoxScore;
  playByPlay?: PlayEvent[];
  winProbability?: WinProbabilityPoint[];
  awayStartingPitcher?: string;
  homeStartingPitcher?: string;
  awayWinningPitcher?: string;
  homeWinningPitcher?: string;
  mvp?: string;
}

export interface StatLeader {
  category: string;
  unit: string;
  isLowerBetter?: boolean; // ERA처럼 낮을수록 좋은 지표
  leaders: {
    rank: number;
    playerId: string;
    playerName: string;
    teamId: string;
    teamName: string;
    value: number;
  }[];
}
