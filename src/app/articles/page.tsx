import type { Metadata } from "next";
import { getArticles } from "@/lib/api/kbo";
import ArticlesPageClient from "./ArticlesPageClient";

export const metadata: Metadata = { title: "기사" };

export default async function ArticlesPage() {
  const articles = await getArticles();
  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-black text-zinc-900 dark:text-zinc-100 mb-6">
        기사 & 칼럼
      </h1>
      <ArticlesPageClient articles={articles} />
    </div>
  );
}
