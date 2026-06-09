import Link from "next/link";
import { ArrowRight } from "lucide-react";
import type { Article } from "@/lib/types/article";
import ArticleCard from "@/components/articles/ArticleCard";
import SectionHeader from "@/components/common/SectionHeader";

interface FeaturedArticlesSectionProps {
  articles: Article[];
}

export default function FeaturedArticlesSection({
  articles,
}: FeaturedArticlesSectionProps) {
  return (
    <section aria-labelledby="articles-heading">
      <SectionHeader
        title="AI 추천 기사"
        description="세이버매트릭스 분석 · AI 생성 콘텐츠"
        action={
          <Link
            href="/articles"
            className="flex items-center gap-1 text-xs text-blue-600 dark:text-blue-400 hover:underline font-medium"
            aria-label="전체 기사 목록 보기"
          >
            전체 기사
            <ArrowRight className="h-3.5 w-3.5" aria-hidden />
          </Link>
        }
      />
      <span id="articles-heading" className="sr-only">
        AI 추천 기사
      </span>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {articles.map((article) => (
          <ArticleCard key={article.id} article={article} />
        ))}
      </div>
    </section>
  );
}
