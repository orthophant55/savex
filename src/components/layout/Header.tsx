import Link from "next/link";
import MainNav from "./MainNav";
import MobileNav from "./MobileNav";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white/95 dark:bg-zinc-950/95 backdrop-blur-sm border-b border-zinc-200 dark:border-zinc-800">
      <div className="relative max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        {/* Logo */}
        <Link
          href="/"
          className="flex items-center gap-2 font-bold text-zinc-900 dark:text-zinc-100 hover:opacity-80 transition-opacity"
          aria-label="KBO Insight 홈으로"
        >
          <span className="text-xl" aria-hidden>
            ⚾
          </span>
          <span className="text-base tracking-tight">KBO Insight</span>
        </Link>

        {/* Desktop nav */}
        <div className="hidden md:block">
          <MainNav />
        </div>

        {/* Mobile nav */}
        <MobileNav />
      </div>
    </header>
  );
}
