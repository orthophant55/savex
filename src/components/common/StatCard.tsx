import { cn } from "@/lib/utils";

interface StatCardProps {
  label: string;
  value: string | number;
  subLabel?: string;
  subValue?: string;
  highlight?: boolean;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export default function StatCard({
  label,
  value,
  subLabel,
  subValue,
  highlight = false,
  size = "md",
  className,
}: StatCardProps) {
  return (
    <div
      className={cn(
        "rounded-lg border bg-white dark:bg-zinc-900 dark:border-zinc-800 border-zinc-200 p-4 flex flex-col gap-1",
        highlight && "border-blue-500 dark:border-blue-400",
        className
      )}
    >
      <span
        className={cn(
          "text-zinc-500 dark:text-zinc-400 font-medium",
          size === "sm" && "text-xs",
          size === "md" && "text-xs",
          size === "lg" && "text-sm"
        )}
      >
        {label}
      </span>
      <span
        className={cn(
          "font-bold tabular-nums",
          size === "sm" && "text-xl",
          size === "md" && "text-2xl",
          size === "lg" && "text-3xl",
          highlight
            ? "text-blue-600 dark:text-blue-400"
            : "text-zinc-900 dark:text-zinc-100"
        )}
      >
        {value}
      </span>
      {subLabel && subValue && (
        <div className="flex items-center gap-1 text-xs text-zinc-500 dark:text-zinc-400">
          <span>{subLabel}</span>
          <span className="font-medium">{subValue}</span>
        </div>
      )}
    </div>
  );
}
