# Backend Merge Notes

이 문서는 `dev` 브랜치에 FastAPI 백엔드를 추가한 내용을 정리합니다.

---

## 추가된 파일 구조

```
savex/
├── backend/
│   ├── app/
│   │   ├── main.py                        # FastAPI 앱 진입점
│   │   ├── core/
│   │   │   ├── config.py                  # Pydantic Settings
│   │   │   ├── logging.py                 # 로거 헬퍼
│   │   │   └── exceptions.py              # NotFoundError, AppValidationError
│   │   ├── schemas/
│   │   │   ├── kbo.py                     # Team, Player, Game, PlayEvent, Standing 등
│   │   │   ├── article.py                 # Article, ArticleCategory, AiGenerationStatus 등
│   │   │   └── ai.py                      # GameRecapRequest, PlayerAnalysisRequest
│   │   ├── mock/
│   │   │   └── data.py                    # 10팀, 30선수, 5경기, PBP, WP, standings, articles
│   │   ├── repositories/
│   │   │   └── mock_repository.py         # MockRepository (나중에 PostgreSQL로 교체)
│   │   ├── domain/
│   │   │   ├── teams/service.py           # TeamsService
│   │   │   ├── players/service.py         # PlayersService
│   │   │   ├── games/service.py           # GamesService
│   │   │   └── articles/service.py        # ArticlesService
│   │   ├── api/routes/
│   │   │   ├── health.py                  # GET /api/v1/health
│   │   │   ├── teams.py                   # GET /api/v1/teams[/{id}]
│   │   │   ├── players.py                 # GET /api/v1/players[/{id}]
│   │   │   ├── games.py                   # GET /api/v1/games/...
│   │   │   ├── stats.py                   # GET /api/v1/standings, /stat-leaders
│   │   │   ├── articles.py                # GET /api/v1/articles[/{id}]
│   │   │   └── ai.py                      # POST /api/v1/ai/game-recap, /player-analysis
│   │   ├── analytics/sabermetrics/
│   │   │   ├── batting.py                 # AVG, OBP, SLG, OPS, ISO, BABIP
│   │   │   ├── pitching.py                # ERA, WHIP, K%, BB%, FIP
│   │   │   └── wpa.py                     # WPA, Leverage Index
│   │   ├── analytics/features/
│   │   │   └── game_state.py              # GameState dataclass
│   │   ├── ml/
│   │   │   ├── contracts.py               # ML I/O schemas
│   │   │   ├── registry.py                # ModelRegistry
│   │   │   └── models/
│   │   │       ├── win_probability_model.py
│   │   │       ├── player_projection_model.py
│   │   │       └── article_topic_model.py
│   │   ├── ai/
│   │   │   ├── prompt_builder.py          # LLM prompt skeleton
│   │   │   ├── mock_generator.py          # Mock streaming generator
│   │   │   └── generation_service.py      # LLM_PROVIDER 분기 서비스
│   │   ├── workers/
│   │   │   ├── ingest_games.py            # KBO 데이터 수집 (TODO)
│   │   │   ├── compute_sabermetrics.py    # 배치 계산 (TODO)
│   │   │   └── generate_articles.py       # 기사 생성 배치 (TODO)
│   │   └── tests/
│   │       ├── test_api.py                # API 통합 테스트 23개
│   │       └── test_sabermetrics.py       # 세이버매트릭스 유닛 테스트 33개
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── README.md
├── docker-compose.backend.yml             # 백엔드 전용 Docker Compose
├── .env.example                           # 프론트엔드 환경변수 예시 추가
└── BACKEND_MERGE_NOTES.md                 # 이 파일
```

---

## 프론트엔드와의 연동 방법

### 환경변수 설정

루트 `.env.local` 에 추가:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

### `src/lib/api/kbo.ts` 교체 방법

현재 `src/lib/api/kbo.ts`는 mock 데이터를 직접 import한다.  
백엔드 API로 교체 시 다음과 같이 수정한다:

```typescript
const BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1';

export async function getTeams(): Promise<Team[]> {
  const res = await fetch(`${BASE}/teams`);
  return res.json();
}

export async function getTodayGames(): Promise<Game[]> {
  const res = await fetch(`${BASE}/games/today`);
  return res.json();
}
// ... 나머지도 동일 패턴으로 교체
```

### `src/lib/api/ai.ts` 교체 방법

현재 `/api/ai/game-recap` (Next.js route)를 호출 중이다.  
백엔드로 교체 시:

```typescript
export async function* streamGameRecap(gameId: string, signal?: AbortSignal) {
  const BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1';
  const res = await fetch(`${BASE}/ai/game-recap`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ game_id: gameId }),
    signal,
  });
  // ... 기존 스트리밍 로직 유지
}
```

---

## 프론트엔드 타입 ↔ 백엔드 스키마 매핑

| 항목 | 프론트엔드 (`src/lib/types/`) | 백엔드 (`backend/app/schemas/`) |
|------|-------------------------------|----------------------------------|
| GameStatus | `"scheduled" \| "live" \| "final" \| "postponed"` | + `pre_game`, `delayed`, `suspended`, `cancelled` 추가 (superset) |
| ArticleCategory | `"game_review"` | `"game_recap"` (동의어) |
| ArticleSourceType | `"editorial"` | `"human_written"` (동의어) |
| AiGenerationStatus | `"pending"`, `"completed"` | `"draft"`, `"generated"` (동의어) |

프론트엔드 타입을 백엔드 스키마와 완전히 맞추려면 `src/lib/types/` 파일을 소폭 수정하거나,  
백엔드 API 응답에서 값을 매핑하는 어댑터 함수를 `src/lib/api/kbo.ts`에 추가한다.

---

## dev 브랜치 병합 체크리스트

- [ ] `cd backend && pip install -r requirements.txt` 성공
- [ ] `cd backend && uvicorn app.main:app --reload --port 8000` 실행 가능
- [ ] `cd backend && pytest -v` → 56개 모두 통과
- [ ] `http://localhost:8000/docs` Swagger UI 정상 표시
- [ ] `/api/v1/ai/game-recap` streaming 응답 확인 (`curl -X POST ... -d '{"game_id":"game_1"}'`)
- [ ] 기존 프론트엔드 `npm run build` 성공 (백엔드 변경 영향 없음)
- [ ] `.env.example`에 `NEXT_PUBLIC_API_BASE_URL` 추가 확인
- [ ] `BACKEND_MERGE_NOTES.md` README.md 링크 추가

---

## 향후 작업 (TODO)

| 항목 | 파일 | 우선순위 |
|------|------|---------|
| PostgreSQL 연결 | `backend/app/repositories/postgres_repository.py` | High |
| 실제 KBO 데이터 수집 | `backend/app/workers/ingest_games.py` | High |
| 세이버매트릭스 배치 | `backend/app/workers/compute_sabermetrics.py` | High |
| ML 모델 아티팩트 로딩 | `backend/app/ml/registry.py` | Medium |
| 실제 LLM Gateway | `backend/app/ai/generation_service.py` | Medium |
| 기사 생성 배치 | `backend/app/workers/generate_articles.py` | Medium |
| 에디터 검토 UI | 새 프론트엔드 페이지 | Low |
| Redis 캐시 레이어 | `backend/app/core/cache.py` | Low |
| Celery 큐 연동 | `backend/app/workers/` 전반 | Low |
| JWT 인증 | `backend/app/core/auth.py` | Low |
