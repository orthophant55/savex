import Link from "next/link";
import { Clock } from "lucide-react";
import type { Article, ArticleCategory } from "@/lib/types/article";
import AiBadge from "./AiBadge";
import { formatRelativeTime, formatReadingTime } from "@/lib/utils";

const CATEGORY_LABELS: Record<ArticleCategory, string> = {
  game_review: "경기 리뷰",
  player_analysis: "선수 분석",
  team_analysis: "팀 분석",
  sabermetrics: "세이버 칼럼",
};

const CATEGORY_COLORS: Record<ArticleCategory, string> = {
  game_review: "bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300",
  player_analysis: "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300",
  team_analysis: "bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300",
  sabermetrics: "bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-300",
};

interface ArticleCardProps {
  article: Article;
  compact?: boolean;
}

export default function ArticleCard({ article, compact = false }: ArticleCardProps) {
  return (
    <Link
      href={`/articles/${article.id}`}
      className="group block rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 overflow-hidden hover:border-zinc-300 dark:hover:border-zinc-700 transition-colors"
      aria-label={`기사: ${article.title}`}
    >
      {/* Color bar */}
      <div
        className="h-1 w-full"
        style={{ backgroundColor: article.thumbnailColor ?? "#6366f1" }}
        aria-hidden
      />
      <div className="p-4">
        {/* badges */}
        <div className="flex items-center gap-2 mb-2 flex-wrap">
          <span
            className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${CATEGORY_COLORS[article.category]}`}
          >
            {CATEGORY_LABELS[article.category]}
          </span>
          {article.sourceType === "ai_generated" && <AiBadge />}
        </div>

        {/* title */}
        <h3 className="font-semibold text-zinc-900 dark:text-zinc-100 leading-snug group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors line-clamp-2 text-sm">
          {article.title}
        </h3>

        {!compact && (
          <p className="mt-1.5 text-xs text-zinc-500 dark:text-zinc-400 line-clamp-2 leading-relaxed">
            {article.summary}
          </p>
        )}

        {/* meta */}
        <div className="mt-3 flex items-center gap-3 text-[11px] text-zinc-400 dark:text-zinc-500">
          <span>{formatRelativeTime(article.publishedAt)}</span>
          <span aria-hidden>·</span>
          <span className="flex items-center gap-1">
            <Clock className="h-3 w-3" aria-hidden />
            {formatReadingTime(article.readingTimeMinutes)}
          </span>
          {article.author && (
            <>
              <span aria-hidden>·</span>
              <span>{article.author}</span>
            </>
          )}
        </div>
      </div>
    </Link>
  );
}
