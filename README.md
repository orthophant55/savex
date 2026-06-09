# KBO Insight

KBO 세이버매트릭스 기반 경기 분석 + AI 생성 기사 플랫폼 MVP.

WAR, FIP, wOBA, WPA 등 고급 지표를 제공하고, AI가 경기 요약 및 선수 분석 리포트를 스트리밍으로 생성합니다.

---

## 실행 방법

```bash
npm install
npm run dev      # http://localhost:3000
```

기타 명령어:

```bash
npm run build    # 프로덕션 빌드
npm run lint     # ESLint
npm test         # 단위 테스트 (vitest)
npm run test:watch  # 워치 모드
```

---

## 프로젝트 구조

```
src/
├── app/                        # Next.js App Router 페이지
│   ├── page.tsx                # 홈 (순위표, 오늘 경기, 스탯 리더, 기사)
│   ├── games/
│   │   ├── page.tsx            # 경기 목록 (날짜 필터)
│   │   └── [gameId]/page.tsx   # 경기 상세 (박스스코어, WPA, AI 요약)
│   ├── teams/
│   │   ├── page.tsx            # 팀 목록
│   │   └── [teamId]/page.tsx   # 팀 상세 (순위, 로스터, 트렌드 차트)
│   ├── players/
│   │   ├── page.tsx            # 선수 목록 (검색, 팀/포지션 필터)
│   │   └── [playerId]/page.tsx # 선수 상세 (세이버 지표, AI 분석)
│   ├── articles/
│   │   ├── page.tsx            # 기사 목록
│   │   └── [articleId]/page.tsx # 기사 상세
│   └── api/
│       └── ai/
│           ├── game-recap/route.ts      # AI 경기 요약 스트리밍 API
│           └── player-analysis/route.ts # AI 선수 분석 스트리밍 API
│
├── components/
│   ├── layout/                 # Header, Footer, Nav
│   ├── home/                   # 홈 섹션 컴포넌트
│   ├── games/                  # 경기 관련 컴포넌트
│   ├── teams/                  # 팀 관련 컴포넌트
│   ├── players/                # 선수 관련 컴포넌트
│   ├── articles/               # 기사 관련 컴포넌트
│   └── common/                 # 공용 컴포넌트 (StatCard, EmptyState 등)
│
└── lib/
    ├── types/kbo.ts            # 도메인 타입 정의
    ├── utils.ts                # 포맷 유틸리티
    ├── mock/                   # Mock 데이터
    │   ├── teams.ts
    │   ├── players.ts
    │   ├── games.ts
    │   ├── standings.ts
    │   ├── articles.ts
    │   └── stat-leaders.ts
    └── api/
        ├── kbo.ts              # 데이터 접근 레이어 (mock → 실제 API 교체 포인트)
        └── ai.ts               # AI 스트림 클라이언트 헬퍼
```

---

## Mock 데이터 교체 가이드

### 1. KBO 데이터 API 연동

`src/lib/api/kbo.ts` 내 각 함수는 `Promise<T>`를 반환하므로, 함수 내부만 `fetch` 호출로 교체하면 됩니다.

```ts
// 변경 전 (mock)
export async function getGameById(id: string): Promise<Game | null> {
  return MOCK_GAMES.find((g) => g.id === id) ?? null;
}

// 변경 후 (실제 API)
export async function getGameById(id: string): Promise<Game | null> {
  const res = await fetch(`https://api.example.com/games/${id}`);
  if (!res.ok) return null;
  return res.json();
}
```

### 2. Mock 데이터 파일

`src/lib/mock/` 디렉터리의 각 파일에 실제 데이터를 교체하거나, 위 API 레이어를 교체하면 자동으로 반영됩니다.

---

## AI API 교체 가이드

현재 AI API는 실제 LLM 없이 경기/선수 데이터를 기반으로 텍스트를 생성하여 스트리밍합니다.

### 실제 LLM(Anthropic Claude 등)으로 교체하는 방법

**교체 파일:** `src/app/api/ai/game-recap/route.ts`, `src/app/api/ai/player-analysis/route.ts`

**교체 포인트:**

```ts
// 1. generateGameRecapText() 함수를 LLM API 호출로 교체
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // process.env.ANTHROPIC_API_KEY 자동 참조

async function generateGameRecapText(game: Game): Promise<ReadableStream> {
  const stream = await client.messages.stream({
    model: "claude-opus-4-7",
    max_tokens: 1024,
    messages: [{ role: "user", content: `경기 데이터: ${JSON.stringify(game)}` }],
  });
  return stream.toReadableStream();
}
```

**중요 원칙:**
- API 키(`ANTHROPIC_API_KEY` 등)는 반드시 서버 환경변수로만 관리
- 브라우저(클라이언트 컴포넌트)에 절대 노출 금지
- 클라이언트 측 `src/lib/api/ai.ts`는 수정 불필요 — 스트림 소비 방식은 동일

---

## 기술 스택

| 분류 | 기술 |
|------|------|
| 프레임워크 | Next.js 16 (App Router) |
| 언어 | TypeScript 5 |
| 스타일 | Tailwind CSS v4 |
| 차트 | Recharts v3 |
| 아이콘 | lucide-react |
| 테스트 | Vitest |

---

## 접근성

- 본문 바로가기 스킵 링크 (`본문으로 바로가기`)
- 모바일 메뉴 Escape 키 닫기
- 탭 컴포넌트 키보드 화살표 내비게이션 (←/→)
- AI 스트리밍 영역 `aria-live="polite"` 적용
- 모든 상호작용 요소 `aria-label` 명시
- 다크 모드 지원 (`prefers-color-scheme`)
