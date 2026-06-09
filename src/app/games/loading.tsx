import { GameCardSkeleton } from "@/components/common/LoadingSkeleton";

export default function GamesLoading() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="h-8 w-32 animate-pulse rounded bg-zinc-200 dark:bg-zinc-800 mb-6" />
      <div className="h-16 w-full animate-pulse rounded-lg bg-zinc-200 dark:bg-zinc-800 mb-6" />
      <div className="space-y-3">
        {Array.from({ length: 5 }).map((_, i) => (
          <GameCardSkeleton key={i} />
        ))}
      </div>
    </div>
  );
}
