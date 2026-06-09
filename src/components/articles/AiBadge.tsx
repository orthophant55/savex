import { Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

interface AiBadgeProps {
  label?: string;
  size?: "sm" | "md";
  className?: string;
}

export default function AiBadge({
  label = "AI 생성",
  size = "sm",
  className,
}: AiBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full font-medium bg-violet-100 text-violet-700 dark:bg-violet-900/40 dark:text-violet-300",
        size === "sm" && "text-[10px] px-2 py-0.5",
        size === "md" && "text-xs px-2.5 py-1",
        className
      )}
      aria-label="AI가 생성한 콘텐츠"
    >
      <Sparkles className={cn(size === "sm" ? "h-2.5 w-2.5" : "h-3 w-3")} aria-hidden />
      {label}
    </span>
  );
}
