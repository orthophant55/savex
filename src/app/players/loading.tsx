import { TableSkeleton } from "@/components/common/LoadingSkeleton";

export default function PlayersLoading() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="h-8 w-24 animate-pulse rounded bg-zinc-200 dark:bg-zinc-800 mb-6" />
      <div className="h-10 w-64 animate-pulse rounded-lg bg-zinc-200 dark:bg-zinc-800 mb-4" />
      <div className="h-8 w-full animate-pulse rounded-lg bg-zinc-200 dark:bg-zinc-800 mb-6" />
      <TableSkeleton rows={10} />
    </div>
  );
}
