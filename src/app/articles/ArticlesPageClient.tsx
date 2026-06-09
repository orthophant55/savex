"use client";

import { useState, useMemo } from "react";
import type { Article, ArticleCategory } from "@/lib/types/article";
import ArticleCard from "@/components/articles/ArticleCard";

const CATEGORIES: { value: "all" | ArticleCategory; label: string }[] = [
  { value: "all", label: "전체" },
  { value: "game_review", label: "경기 리뷰" },
  { value: "player_analysis", label: "선수 분석" },
  { value: "team_analysis", label: "팀 분석" },
  { value: "sabermetrics", label: "세이버 칼럼" },
];

interface ArticlesPageClientProps {
  articles: Article[];
}

export default function ArticlesPageClient({ articles }: ArticlesPageClientProps) {
  const [category, setCategory] = useState<"all" | ArticleCategory>("all");

  const filtered = useMemo(() => {
    if (category === "all") return articles;
    return articles.filter((a) => a.category === category);
  }, [articles, category]);

  return (
    <>
      {/* Category filter */}
      <div className="flex flex-wrap gap-2 mb-6" role="group" aria-label="카테고리 필터">
        {CATEGORIES.map(({ value, label }) => (
          <button
            key={value}
            onClick={() => setCategory(value)}
            className={`px-4 py-1.5 text-sm font-semibold rounded-full border transition-colors ${
              category === value
                ? "bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 border-zinc-900 dark:border-zinc-100"
                : "border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 hover:border-zinc-300 dark:hover:border-zinc-600"
            }`}
            aria-pressed={category === value}
          >
            {label}
            {value !== "all" && (
              <span className="ml-1.5 text-xs opacity-60">
                ({articles.filter((a) => a.category === value).length})
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Count */}
      <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-4">
        {filtered.length}건
      </p>

      {/* Articles grid */}
      {filtered.length === 0 ? (
        <div className="py-16 text-center text-zinc-400 dark:text-zinc-500 text-sm">
          해당 카테고리의 기사가 없습니다.
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((article) => (
            <ArticleCard key={article.id} article={article} />
          ))}
        </div>
      )}
    </>
  );
}
