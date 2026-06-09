import { notFound } from "next/navigation";
import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, Clock, User, Calendar, AlertCircle } from "lucide-react";
import { getArticleById, getTeamById, getPlayerById } from "@/lib/api/kbo";
import AiBadge from "@/components/articles/AiBadge";
import ArticleBody from "@/components/articles/ArticleBody";
import { formatDateTime, formatReadingTime } from "@/lib/utils";
import type { ArticleCategory } from "@/lib/types/article";

interface Props {
  params: Promise<{ articleId: string }>;
}

const CATEGORY_LABELS: Record<ArticleCategory, string> = {
  game_review: "경기 리뷰",
  player_analysis: "선수 분석",
  team_analysis: "팀 분석",
  sabermetrics: "세이버 칼럼",
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { articleId } = await params;
  const article = await getArticleById(articleId);
  if (!article) return { title: "기사를 찾을 수 없습니다" };
  return {
    title: article.title,
    description: article.summary,
  };
}

export default async function ArticleDetailPage({ params }: Props) {
  const { articleId } = await params;

  const article = await getArticleById(articleId);
  if (!article) notFound();

  // 관련 팀/선수 데이터 (병렬로)
  const [relatedTeams, relatedPlayers] = await Promise.all([
    Promise.all((article.related.teamIds ?? []).map((id) => getTeamById(id))),
    Promise.all((article.related.playerIds ?? []).map((id) => getPlayerById(id))),
  ]);

  const validTeams = relatedTeams.filter(Boolean);
  const validPlayers = relatedPlayers.filter(Boolean);

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <Link
        href="/articles"
        className="inline-flex items-center gap-1.5 text-sm text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 mb-6 transition-colors"
        aria-label="기사 목록으로"
      >
        <ArrowLeft className="h-4 w-4" aria-hidden />
        기사 목록
      </Link>

      <article>
        {/* Category + AI badge */}
        <div className="flex flex-wrap items-center gap-2 mb-3">
          <span
            className="text-xs font-semibold px-2.5 py-0.5 rounded-full"
            style={{
              backgroundColor: `${article.thumbnailColor ?? "#6366f1"}20`,
              color: article.thumbnailColor ?? "#6366f1",
            }}
          >
            {CATEGORY_LABELS[article.category]}
          </span>
          {article.sourceType === "ai_generated" && <AiBadge size="md" />}
          {article.sourceType === "hybrid" && (
            <AiBadge label="AI + 편집" size="md" />
          )}
        </div>

        {/* Title */}
        <h1 className="text-2xl font-black text-zinc-900 dark:text-zinc-100 leading-snug mb-4">
          {article.title}
        </h1>

        {/* Summary */}
        <p className="text-base text-zinc-500 dark:text-zinc-400 leading-relaxed mb-5 border-l-4 pl-4 border-zinc-200 dark:border-zinc-700">
          {article.summary}
        </p>

        {/* Meta */}
        <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 text-xs text-zinc-400 dark:text-zinc-500 pb-5 mb-5 border-b border-zinc-100 dark:border-zinc-800">
          {article.author && (
            <span className="flex items-center gap-1">
              <User className="h-3 w-3" aria-hidden />
              {article.author}
            </span>
          )}
          <span className="flex items-center gap-1">
            <Calendar className="h-3 w-3" aria-hidden />
            {formatDateTime(article.publishedAt)}
          </span>
          <span className="flex items-center gap-1">
            <Clock className="h-3 w-3" aria-hidden />
            {formatReadingTime(article.readingTimeMinutes)}
          </span>
        </div>

        {/* Related links */}
        {(validTeams.length > 0 || validPlayers.length > 0 || article.related.gameId) && (
          <div className="mb-6 p-4 rounded-lg bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-100 dark:border-zinc-800">
            <p className="text-xs font-semibold text-zinc-500 dark:text-zinc-400 mb-2">
              관련 링크
            </p>
            <div className="flex flex-wrap gap-2">
              {article.related.gameId && (
                <Link
                  href={`/games/${article.related.gameId}`}
                  className="text-xs px-2.5 py-1 rounded-full border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 hover:border-blue-500 hover:text-blue-600 transition-colors"
                >
                  경기 상세 →
                </Link>
              )}
              {validTeams.map((team) => team && (
                <Link
                  key={team.id}
                  href={`/teams/${team.id}`}
                  className="text-xs px-2.5 py-1 rounded-full text-white"
                  style={{ backgroundColor: team.primaryColor }}
                >
                  {team.shortName}
                </Link>
              ))}
              {validPlayers.map((player) => player && (
                <Link
                  key={player.id}
                  href={`/players/${player.id}`}
                  className="text-xs px-2.5 py-1 rounded-full border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 hover:border-blue-500 hover:text-blue-600 transition-colors"
                >
                  {player.name}
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Tags */}
        {article.tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-6">
            {article.tags.map((tag) => (
              <span
                key={tag}
                className="text-[11px] px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}

        {/* Body */}
        <ArticleBody body={article.body} className="mb-10" />

        {/* Disclaimer for AI-generated articles */}
        {(article.sourceType === "ai_generated" || article.sourceType === "hybrid") && (
          <div className="flex items-start gap-2 p-4 rounded-lg bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800/50">
            <AlertCircle className="h-4 w-4 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" aria-hidden />
            <p className="text-xs text-amber-700 dark:text-amber-300">
              이 글은 자동 생성 초안이며, 공개 전 검수가 필요합니다.
              수치 및 사실 관계는 실제 데이터와 다를 수 있습니다.
            </p>
          </div>
        )}
      </article>
    </div>
  );
}
