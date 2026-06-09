/**
 * AI API 클라이언트 헬퍼 (브라우저 전용)
 *
 * 실제 LLM 호출은 서버 사이드 API route에서만 처리합니다.
 * 이 파일은 'use client' 컴포넌트에서 스트림을 소비하는 헬퍼입니다.
 *
 * 실제 LLM 연동 시 /api/ai/game-recap/route.ts 와
 * /api/ai/player-analysis/route.ts 내부만 수정하면 됩니다.
 */

export type StreamStatus = "idle" | "streaming" | "done" | "error";

/**
 * 경기 요약 스트림 — AsyncGenerator로 텍스트 청크를 yield합니다.
 */
export async function* streamGameRecap(
  gameId: string,
  signal?: AbortSignal
): AsyncGenerator<string, void, unknown> {
  const response = await fetch("/api/ai/game-recap", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gameId }),
    signal,
  });

  if (!response.ok) {
    throw new Error(`요약 생성 실패: ${response.status}`);
  }

  if (!response.body) {
    throw new Error("스트림을 받을 수 없습니다.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      yield decoder.decode(value, { stream: true });
    }
  } finally {
    reader.releaseLock();
  }
}

/**
 * 선수 분석 스트림 — AsyncGenerator로 텍스트 청크를 yield합니다.
 */
export async function* streamPlayerAnalysis(
  playerId: string,
  signal?: AbortSignal
): AsyncGenerator<string, void, unknown> {
  const response = await fetch("/api/ai/player-analysis", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ playerId }),
    signal,
  });

  if (!response.ok) {
    throw new Error(`분석 생성 실패: ${response.status}`);
  }

  if (!response.body) {
    throw new Error("스트림을 받을 수 없습니다.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      yield decoder.decode(value, { stream: true });
    }
  } finally {
    reader.releaseLock();
  }
}
