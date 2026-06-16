# Backend Merge Notes

이 문서는 `dev` 브랜치에 FastAPI 백엔드를 추가하고 세이버매트릭스 엔진을 확장한 내용을 정리합니다.

---

## 추가된 파일 구조

```
savex/
├── backend/
│   ├── app/
│   │   ├── main.py                              # FastAPI 앱 진입점 (metrics/ingestion 라우터 추가)
│   │   ├── core/
│   │   │   ├── config.py                        # Pydantic Settings (KBO_DATA_ENABLED 등 추가)
│   │   │   ├── logging.py
│   │   │   └── exceptions.py
│   │   ├── schemas/
│   │   │   ├── kbo.py                           # Standing에 RS/RA/RD/PythWPct 추가
│   │   │   ├── article.py
│   │   │   ├── ai.py
│   │   │   ├── metrics.py                       # [NEW] MetricDefinition, MetricValue, RE/WE entry
│   │   │   └── ingestion.py                     # [NEW] RawKboPayload, KboScheduleRequest 등
│   │   ├── mock/
│   │   │   └── data.py                          # MOCK_STANDINGS에 RS/RA/RD/PythWPct 추가
│   │   ├── repositories/
│   │   │   └── mock_repository.py
│   │   ├── domain/
│   │   │   ├── teams/service.py
│   │   │   ├── players/service.py
│   │   │   ├── games/service.py
│   │   │   ├── articles/service.py
│   │   │   ├── metrics/service.py               # [NEW] MetricsService
│   │   │   └── projections/service.py           # [NEW] ProjectionsService
│   │   ├── api/routes/
│   │   │   ├── health.py
│   │   │   ├── teams.py
│   │   │   ├── players.py                       # /stats, /projection, /regression-adjusted, /slump-risk 추가
│   │   │   ├── games.py
│   │   │   ├── stats.py
│   │   │   ├── articles.py
│   │   │   ├── ai.py                            # /team-analysis, /sabermetric-column 추가
│   │   │   ├── metrics.py                       # [NEW] /metrics/* 라우터
│   │   │   └── ingestion.py                     # [NEW] /ingestion/* 라우터
│   │   ├── analytics/
│   │   │   ├── constants/
│   │   │   │   ├── kbo_environment.py           # [NEW] KBO 리그 환경 상수 (wOBA weights, FIP const 등)
│   │   │   │   └── metric_definitions.py        # [NEW] 50+ 지표 카탈로그 (METRIC_CATALOG)
│   │   │   └── sabermetrics/
│   │   │       ├── batting.py                   # AVG, OBP, SLG, OPS, ISO, BABIP
│   │   │       ├── pitching.py                  # ERA, WHIP, K%, BB%
│   │   │       ├── fip.py                       # FIP, FIP-, RA9, K/9, BB/9, HR/9, K-BB%
│   │   │       ├── woba.py                      # wOBA, wRAA, wRC, wRC+
│   │   │       ├── wpa.py                       # WPA, LI, rank_plays_by_wpa/li 추가
│   │   │       ├── pythagorean.py               # PythWPct, ExpW, Actual-Expected
│   │   │       ├── regression_adjustment.py     # shrinkage, reliability score
│   │   │       ├── run_expectancy.py            # 24 base-out state RE table + RE24
│   │   │       ├── win_expectancy.py            # WE table + WPA
│   │   │       ├── linear_weights.py            # [NEW] KBO linear weights
│   │   │       ├── baserunning.py               # [NEW] 주루 지표 (placeholder)
│   │   │       ├── fielding.py                  # [NEW] 수비 지표 (placeholder)
│   │   │       ├── team.py                      # [NEW] 팀 지표 집계
│   │   │       └── war_lite.py                  # [NEW] WAR-lite (skeleton)
│   │   ├── ingestion/
│   │   │   ├── __init__.py                      # [NEW]
│   │   │   ├── exceptions.py                    # [NEW] KboIngestionError 등
│   │   │   ├── normalization.py                 # [NEW] 팀명 정규화, 날짜 파싱
│   │   │   ├── raw_payload_store.py             # [NEW] SHA256 체크섬 + JSON 파일 저장
│   │   │   ├── kbo_data_client.py               # [NEW] kbodata 래퍼 (availability 체크)
│   │   │   └── kbo_data_adapter.py              # [NEW] fetch+normalize+store 어댑터
│   │   ├── ml/
│   │   │   ├── contracts.py                     # RegressionAdjustedBattingInput/Output, SlumpRiskInput/Output 추가
│   │   │   ├── registry.py                      # regression_adjusted_batting, slump_risk 모델 추가
│   │   │   └── models/
│   │   │       ├── win_probability_model.py
│   │   │       ├── player_projection_model.py
│   │   │       ├── article_topic_model.py
│   │   │       ├── regression_adjusted_batting_model.py  # [NEW] Empirical Bayes shrinkage
│   │   │       └── slump_risk_model.py                   # [NEW] rule-based 슬럼프 위험도
│   │   ├── ai/
│   │   │   ├── mock_generator.py                # stream_team_analysis, stream_sabermetric_column 추가
│   │   │   └── generation_service.py            # team_analysis_stream, sabermetric_column_stream 추가
│   │   ├── workers/
│   │   │   ├── ingest_kbo_schedule.py           # [NEW] CLI runner (dry-run 지원)
│   │   │   └── ingest_kbo_game_data.py          # [NEW] CLI runner (raw payload 저장)
│   │   └── tests/
│   │       ├── test_api.py                      # 37개 (23 → 37, 새 엔드포인트 추가)
│   │       ├── test_sabermetrics.py             # 33개 (원본)
│   │       ├── test_batting_metrics.py          # [NEW] 20개
│   │       ├── test_pitching_metrics.py         # [NEW] 24개
│   │       ├── test_run_expectancy.py           # [NEW] 18개
│   │       ├── test_wpa.py                      # [NEW] 21개
│   │       ├── test_pythagorean.py              # [NEW] 14개
│   │       ├── test_ml_registry.py              # [NEW] 14개
│   │       └── test_kbo_data_adapter.py         # [NEW] 22개
├── SABERMETRICS_DESIGN.md                       # [NEW] 세이버매트릭스 설계 철학 문서
└── BACKEND_MERGE_NOTES.md                       # 이 파일
```

---

## 테스트 현황

```
pytest -v (243 tests, all passing)

test_api.py               37 passed
test_sabermetrics.py      33 passed
test_batting_metrics.py   20 passed
test_pitching_metrics.py  24 passed
test_run_expectancy.py    18 passed
test_wpa.py               21 passed
test_pythagorean.py       14 passed
test_ml_registry.py       14 passed
test_kbo_data_adapter.py  22 passed
```

> ChromeDriver, kbodata, 실제 LLM API 없이 모두 통과합니다.

---

## Mock 데이터 경고

- `MOCK_PLAYERS`: 10팀 × 3명 = 30명 (실제 KBO 선수 아님)
- `MOCK_GAMES`: 5경기 (실제 경기 일정 아님)
- `MOCK_STANDINGS`: RS/RA/RD/PythWPct 포함, 계산된 수치가 아닌 예시값
- AI 기사: mock 스트리밍 텍스트 ("MOCK AI 생성 콘텐츠")
- RE24 table: MLB approximate (KBO 전용 아님)
- WE table: 개발용 소규모 mock
- wOBA weights: MLB FanGraphs 2024 (KBO 보정 미완)

---

## 실제 데이터 전환 가이드

### 1단계: kbo-data ingestion 활성화

```bash
# .env
KBO_DATA_ENABLED=true
KBO_INGESTION_MODE=kbo-data
KBO_CHROMEDRIVER_PATH=/path/to/chromedriver
KBO_REQUEST_DELAY_SECONDS=2.0
```

```bash
# 수동 실행
python -m app.workers.ingest_kbo_schedule --year 2025 --month 6 --mode monthly
python -m app.workers.ingest_kbo_game_data --year 2025 --month 6 --day 16
```

### 2단계: PostgreSQL 연결

`backend/app/repositories/postgres_repository.py` 구현 (MockRepository 동일 인터페이스).  
각 domain service에서 `mock_repo` 대신 `pg_repo` 주입.

### 3단계: KBO 전용 파라미터 추정

SABERMETRICS_DESIGN.md 섹션 6 참조.  
KBO 역사 데이터로 Pythagorean exponent, wOBA weights, FIP constant를 재추정.

### 4단계: ML 모델 고도화

`backend/app/ml/registry.py`에 실제 LightGBM/XGBoost 모델 등록.

### 5단계: LLM Gateway 연결

`backend/app/ai/generation_service.py`에 LLM provider 분기 추가.  
AI는 sabermetrics engine 계산 결과 JSON만 설명하며, 수치를 직접 생성하지 않음.

---

## 프론트엔드와의 연동

### 환경변수 설정

루트 `.env.local` 에 추가:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

### `src/lib/api/kbo.ts` 교체

```typescript
const BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1';

export async function getTeams(): Promise<Team[]> {
  const res = await fetch(`${BASE}/teams`);
  return res.json();
}
```

### 새 엔드포인트 타입 연결 예시

```typescript
// 선수 세이버매트릭스
export async function getPlayerStats(playerId: string) {
  const res = await fetch(`${BASE}/players/${playerId}/stats`);
  return res.json();
}

// Empirical Bayes 보정 타율
export async function getRegressionAdjustedBatting(playerId: string) {
  const res = await fetch(`${BASE}/players/${playerId}/regression-adjusted`);
  return res.json();
}

// 팀 피타고리안 기대승률
export async function getTeamPythagorean(teamId: string) {
  const res = await fetch(`${BASE}/metrics/teams/${teamId}/pythagorean`);
  return res.json();
}

// 지표 카탈로그
export async function getMetricDefinitions() {
  const res = await fetch(`${BASE}/metrics/definitions`);
  return res.json();
}
```

### 프론트엔드 타입 ↔ 백엔드 스키마 매핑

| 항목 | 프론트엔드 | 백엔드 |
|------|-----------|--------|
| GameStatus | `"scheduled" \| "live" \| "final" \| "postponed"` | superset (pre_game, delayed 등 추가) |
| ArticleCategory | `"game_review"` | `"game_recap"` (동의어) |
| ArticleSourceType | `"editorial"` | `"human_written"` (동의어) |
| AiGenerationStatus | `"pending"`, `"completed"` | `"draft"`, `"generated"` (동의어) |

---

## dev 브랜치 병합 체크리스트

- [ ] `cd backend && pip install -r requirements.txt` 성공
- [ ] `cd backend && uvicorn app.main:app --reload --port 8000` 실행 가능
- [ ] `cd backend && pytest -v` → 243개 모두 통과
- [ ] `http://localhost:8000/docs` Swagger UI 정상 표시
- [ ] `/api/v1/ai/game-recap` streaming 응답 확인
- [ ] `/api/v1/metrics/definitions` 50+ 지표 반환 확인
- [ ] `/api/v1/ingestion/status` 응답 확인 (`kbo_data_enabled: false`)
- [ ] 기존 프론트엔드 `npm run build` 성공 (백엔드 변경 영향 없음)
- [ ] `.env.example`에 `NEXT_PUBLIC_API_BASE_URL` 추가 확인
- [ ] `SABERMETRICS_DESIGN.md` 검토

---

## 향후 작업 (TODO)

| 항목 | 파일 | 우선순위 |
|------|------|---------|
| PostgreSQL 연결 | `backend/app/repositories/postgres_repository.py` | High |
| KBO ingestion 실사용 (ChromeDriver 설정 후) | `backend/app/ingestion/` | High |
| 세이버매트릭스 배치 계산 Worker | `backend/app/workers/compute_sabermetrics.py` | High |
| KBO 전용 파라미터 추정 | SABERMETRICS_DESIGN.md 섹션 6 참조 | High |
| 실제 KBO play-by-play 데이터 수집 | RE24/WE table 재구축 필요 | Medium |
| ML 모델 아티팩트 로딩 (LightGBM) | `backend/app/ml/registry.py` | Medium |
| 실제 LLM Gateway | `backend/app/ai/generation_service.py` | Medium |
| xFIP, SIERA 구현 | `backend/app/analytics/sabermetrics/fip.py` | Medium |
| WAR-lite 본격 구현 | `backend/app/analytics/sabermetrics/war_lite.py` | Medium |
| ai/article_context_builder.py | 기사 생성 시 수치 컨텍스트 주입 | Medium |
| ai/fact_checker.py | 기사 수치 자동 검증 | Medium |
| Redis 캐시 레이어 | `backend/app/core/cache.py` | Low |
| Celery/Arq Worker 스케줄링 | `backend/app/workers/` 전반 | Low |
| JWT 인증 | `backend/app/core/auth.py` | Low |
| 기사 편집자 검토 UI | 프론트엔드 새 페이지 | Low |
| 번트/도루 손익분기점 시뮬레이터 | `backend/app/analytics/strategy/` | Low |

---

## 절대 금지 사항 (설계 원칙)

- 기본 설정에서 실제 KBO 사이트 크롤링 금지 (`KBO_DATA_ENABLED=false` 유지)
- 테스트에서 실제 ChromeDriver 호출 금지
- 실제 외부 LLM API 호출 금지
- API key를 코드에 직접 넣기 금지
- mock data를 실제 데이터라고 주장 금지
- 세이버 지표 계산을 LLM에게 위임 금지
- LLM이 수치를 추론하게 하기 금지
- 프론트엔드와 백엔드 코드를 직접 import로 결합 금지
