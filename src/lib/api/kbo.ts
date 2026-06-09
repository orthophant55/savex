/**
 * KBO 데이터 접근 레이어
 *
 * 현재는 mock 데이터를 반환합니다.
 * 실제 API로 교체 시 각 함수 내부의 mock import를 fetch 호출로 교체하세요.
 * 함수 시그니처는 변경하지 않아도 됩니다.
 *
 * 교체 예시:
 *   // Before (mock)
 *   return MOCK_GAMES.filter(...);
 *
 *   // After (real API)
 *   const res = await fetch(`${API_BASE}/games?date=${date}`);
 *   return res.json();
 */

import type { Game, Team, Player, Standing, StatLeader } from "@/lib/types/kbo";
import type { Article } from "@/lib/types/article";

import { MOCK_GAMES } from "@/lib/mock/games";
import { MOCK_TEAMS } from "@/lib/mock/teams";
import { MOCK_PLAYERS } from "@/lib/mock/players";
import { MOCK_STANDINGS } from "@/lib/mock/standings";
import { MOCK_STAT_LEADERS } from "@/lib/mock/stat-leaders";
import { MOCK_ARTICLES } from "@/lib/mock/articles";

// 실제 API 교체 시 이 상수를 환경변수로 변경
// const API_BASE = process.env.KBO_API_BASE_URL;

// ─── 경기 ────────────────────────────────────

export async function getTodayGames(): Promise<Game[]> {
  const today = new Date().toISOString().slice(0, 10);
  // 오늘 날짜 게임이 없으면 mock 전체 반환 (개발 편의)
  const todayGames = MOCK_GAMES.filter((g) => g.date === today);
  return todayGames.length > 0 ? todayGames : MOCK_GAMES;
}

export async function getGamesByDate(date: string): Promise<Game[]> {
  const games = MOCK_GAMES.filter((g) => g.date === date);
  return games.length > 0 ? games : MOCK_GAMES;
}

export async function getGameById(gameId: string): Promise<Game | null> {
  return MOCK_GAMES.find((g) => g.id === gameId) ?? null;
}

// ─── 팀 ─────────────────────────────────────

export async function getTeams(): Promise<Team[]> {
  return MOCK_TEAMS;
}

export async function getTeamById(teamId: string): Promise<Team | null> {
  return MOCK_TEAMS.find((t) => t.id === teamId) ?? null;
}

// ─── 순위 ────────────────────────────────────

export async function getStandings(): Promise<Standing[]> {
  return MOCK_STANDINGS;
}

// ─── 선수 ────────────────────────────────────

export interface GetPlayersParams {
  teamId?: string;
  position?: string;
  query?: string;
}

export async function getPlayers(params?: GetPlayersParams): Promise<Player[]> {
  let players = [...MOCK_PLAYERS];

  if (params?.teamId) {
    players = players.filter((p) => p.teamId === params.teamId);
  }
  if (params?.position) {
    players = players.filter((p) => p.position === params.position);
  }
  if (params?.query) {
    const q = params.query.toLowerCase();
    players = players.filter(
      (p) =>
        p.name.toLowerCase().includes(q) ||
        p.teamId.toLowerCase().includes(q)
    );
  }

  return players;
}

export async function getPlayerById(playerId: string): Promise<Player | null> {
  return MOCK_PLAYERS.find((p) => p.id === playerId) ?? null;
}

// ─── 통계 리더 ───────────────────────────────

export async function getStatLeaders(): Promise<StatLeader[]> {
  return MOCK_STAT_LEADERS;
}

// ─── 기사 ────────────────────────────────────

export interface GetArticlesParams {
  category?: string;
  limit?: number;
}

export async function getArticles(params?: GetArticlesParams): Promise<Article[]> {
  let articles = [...MOCK_ARTICLES];

  if (params?.category) {
    articles = articles.filter((a) => a.category === params.category);
  }

  // 최신순 정렬
  articles.sort(
    (a, b) =>
      new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime()
  );

  if (params?.limit) {
    articles = articles.slice(0, params.limit);
  }

  return articles;
}

export async function getArticleById(articleId: string): Promise<Article | null> {
  return MOCK_ARTICLES.find((a) => a.id === articleId) ?? null;
}

// ─── 팀 관련 선수/경기 편의 함수 ─────────────

export async function getPlayersByTeam(teamId: string): Promise<Player[]> {
  return getPlayers({ teamId });
}

export async function getTeamStanding(teamId: string): Promise<Standing | null> {
  const standings = await getStandings();
  return standings.find((s) => s.team.id === teamId) ?? null;
}

export async function getRelatedArticles(
  gameId?: string,
  teamIds?: string[],
  playerIds?: string[]
): Promise<Article[]> {
  return MOCK_ARTICLES.filter((a) => {
    if (gameId && a.related.gameId === gameId) return true;
    if (teamIds?.some((id) => a.related.teamIds?.includes(id))) return true;
    if (playerIds?.some((id) => a.related.playerIds?.includes(id))) return true;
    return false;
  });
}
