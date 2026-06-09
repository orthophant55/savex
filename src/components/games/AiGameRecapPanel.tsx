"use client";

import { useCallback, useRef, useState } from "react";
import { Sparkles, Square } from "lucide-react";
import { streamGameRecap, type StreamStatus } from "@/lib/api/ai";
import ArticleBody from "@/components/articles/ArticleBody";

interface AiGameRecapPanelProps {
  gameId: string;
}

export default function AiGameRecapPanel({ gameId }: AiGameRecapPanelProps) {
  const [status, setStatus] = useState<StreamStatus>("idle");
  const [text, setText] = useState("");
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const start = useCallback(async () => {
    abortRef.current = new AbortController();
    setStatus("streaming");
    setText("");
    setError(null);

    try {
      for await (const chunk of streamGameRecap(gameId, abortRef.current.signal)) {
        setText((prev) => prev + chunk);
      }
      setStatus("done");
    } catch (err) {
      if (err instanceof Error && err.name === "AbortError") {
        setStatus("idle");
        setText("");
      } else {
        setError(err instanceof Error ? err.message : "알 수 없는 오류가 발생했습니다.");
        setStatus("error");
      }
    }
  }, [gameId]);

  const stop = useCallback(() => {
    abortRef.current?.abort();
  }, []);

  return (
    <div className="rounded-xl border border-violet-200 dark:border-violet-800/50 bg-violet-50/50 dark:bg-violet-950/20 p-5">
      <div className="flex items-center gap-2 mb-3">
        <Sparkles className="h-4 w-4 text-violet-600 dark:text-violet-400" aria-hidden />
        <h2 className="text-sm font-bold text-violet-700 dark:text-violet-300">
          AI 경기 요약
        </h2>
      </div>

      {status === "idle" && (
        <>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-4">
            AI가 경기 데이터를 분석하여 요약 기사를 생성합니다.
            세이버매트릭스 지표 기반의 심층 분석을 포함합니다.
          </p>
          <button
            onClick={start}
            className="inline-flex items-center gap-2 px-4 py-2 bg-violet-600 hover:bg-violet-700 text-white text-sm font-medium rounded-lg transition-colors"
          >
            <Sparkles className="h-4 w-4" aria-hidden />
            AI 경기 요약 생성
          </button>
        </>
      )}

      {(status === "streaming" || status === "done") && (
        <div>
          <div
            className="bg-white dark:bg-zinc-900/60 rounded-lg border border-violet-100 dark:border-violet-800/30 p-4 mb-3 min-h-[120px]"
            aria-live="polite"
            aria-busy={status === "streaming"}
            aria-label="AI 경기 요약 내용"
          >
            {status === "done" ? (
              <ArticleBody body={text} className="text-sm" />
            ) : (
              <p className="text-[15px] text-zinc-700 dark:text-zinc-300 leading-relaxed whitespace-pre-wrap">
                {text}
                <span
                  className="inline-block w-[2px] h-[1.1em] bg-violet-500 animate-pulse align-text-bottom ml-0.5"
                  aria-hidden
                />
              </p>
            )}
          </div>

          {status === "streaming" && (
            <button
              onClick={stop}
              className="inline-flex items-center gap-2 px-3 py-1.5 bg-zinc-200 hover:bg-zinc-300 dark:bg-zinc-700 dark:hover:bg-zinc-600 text-zinc-700 dark:text-zinc-200 text-xs font-medium rounded-lg transition-colors"
            >
              <Square className="h-3.5 w-3.5" aria-hidden />
              생성 중지
            </button>
          )}

          {status === "done" && (
            <div className="flex items-center justify-between gap-3 flex-wrap">
              <p className="text-[11px] text-zinc-400 dark:text-zinc-500">
                * AI 생성 콘텐츠입니다. 실제 데이터 검증이 필요합니다.
              </p>
              <button
                onClick={start}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-violet-100 hover:bg-violet-200 dark:bg-violet-900/40 dark:hover:bg-violet-800/50 text-violet-700 dark:text-violet-300 text-xs font-medium rounded-lg transition-colors"
              >
                <Sparkles className="h-3.5 w-3.5" aria-hidden />
                다시 생성
              </button>
            </div>
          )}
        </div>
      )}

      {status === "error" && (
        <div>
          <p className="text-sm text-red-600 dark:text-red-400 mb-3">{error}</p>
          <button
            onClick={start}
            className="inline-flex items-center gap-2 px-4 py-2 bg-violet-600 hover:bg-violet-700 text-white text-sm font-medium rounded-lg transition-colors"
          >
            <Sparkles className="h-4 w-4" aria-hidden />
            다시 시도
          </button>
        </div>
      )}
    </div>
  );
}
