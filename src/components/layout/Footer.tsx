export default function Footer() {
  return (
    <footer className="border-t border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 mt-16">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <p className="text-sm font-bold text-zinc-900 dark:text-zinc-100">
              ⚾ KBO Insight
            </p>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
              세이버매트릭스 기반 KBO 분석 플랫폼
            </p>
          </div>
          <div className="text-xs text-zinc-400 dark:text-zinc-500 text-center md:text-right space-y-1">
            <p>
              본 사이트의 데이터는 실제 KBO 데이터가 아닌 예시 데이터입니다.
            </p>
            <p>
              AI 생성 콘텐츠는 자동 생성된 초안이며 공개 전 검수가 필요합니다.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
