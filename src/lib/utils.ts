import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(dateStr: string): string {
  const d = new Date(dateStr);
  return d.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

export function formatShortDate(dateStr: string): string {
  const d = new Date(dateStr);
  return d.toLocaleDateString("ko-KR", { month: "numeric", day: "numeric" });
}

export function formatDateTime(isoStr: string): string {
  const d = new Date(isoStr);
  return d.toLocaleString("ko-KR", {
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function formatRelativeTime(isoStr: string): string {
  const diff = Date.now() - new Date(isoStr).getTime();
  const minutes = Math.floor(diff / 60000);
  if (minutes < 60) return `${minutes}분 전`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}시간 전`;
  const days = Math.floor(hours / 24);
  return `${days}일 전`;
}

export function formatStat(value: number | undefined, decimals = 3): string {
  if (value === undefined || value === null) return "-";
  return value.toFixed(decimals);
}

export function formatAvg(value: number | undefined): string {
  if (value === undefined || value === null) return "-";
  return value.toFixed(3).replace("0.", ".");
}

export function formatEra(value: number | undefined): string {
  if (value === undefined || value === null) return "-";
  return value.toFixed(2);
}

export function formatPct(value: number | undefined): string {
  if (value === undefined || value === null) return "-";
  return `${value.toFixed(1)}%`;
}

export function formatInnings(value: number | undefined): string {
  if (value === undefined || value === null) return "-";
  const full = Math.floor(value);
  const frac = Math.round((value - full) * 10);
  if (frac === 0) return `${full}.0`;
  return `${full}.${frac}`;
}

export function formatWinRate(value: number): string {
  return value.toFixed(3).replace("0.", ".");
}

export function formatReadingTime(minutes: number): string {
  return `${minutes}분 읽기`;
}

export function getWinRateColor(winRate: number): string {
  if (winRate >= 0.6) return "text-green-600 dark:text-green-400";
  if (winRate >= 0.5) return "text-blue-600 dark:text-blue-400";
  if (winRate >= 0.4) return "text-orange-500 dark:text-orange-400";
  return "text-red-600 dark:text-red-400";
}

export function getStatColor(value: number, high: number, low: number): string {
  if (value >= high) return "text-green-600 dark:text-green-400 font-semibold";
  if (value <= low) return "text-red-600 dark:text-red-400";
  return "";
}

export function getGameStatusLabel(status: string): string {
  switch (status) {
    case "scheduled":
      return "예정";
    case "live":
      return "진행중";
    case "final":
      return "종료";
    case "postponed":
      return "취소";
    default:
      return status;
  }
}

export function getGameStatusColor(status: string): string {
  switch (status) {
    case "live":
      return "bg-red-500 text-white";
    case "final":
      return "bg-zinc-200 text-zinc-700 dark:bg-zinc-700 dark:text-zinc-200";
    case "scheduled":
      return "bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-200";
    case "postponed":
      return "bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-200";
    default:
      return "bg-zinc-100 text-zinc-700";
  }
}

export function getPositionAbbr(position: string): string {
  const map: Record<string, string> = {
    투수: "P",
    포수: "C",
    "1루수": "1B",
    "2루수": "2B",
    "3루수": "3B",
    유격수: "SS",
    좌익수: "LF",
    중견수: "CF",
    우익수: "RF",
    지명타자: "DH",
  };
  return map[position] ?? position;
}

export function TODAY(): string {
  return new Date().toISOString().slice(0, 10);
}
