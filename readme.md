# SAVEX

KBO 전용 세이버메트릭스 기반 야구 인사이트 플랫폼입니다.

SAVEX는 단순한 야구 기록 조회 사이트가 아니라, KBO 경기 데이터와 세이버메트릭스 지표를 기반으로 경기 리뷰, 선수 분석, 팀 분석, AI 생성 칼럼을 제공하는 것을 목표로 합니다.

현재는 프론트엔드 중심의 MVP 단계이며, 이후 FastAPI 백엔드, KBO 데이터 수집 파이프라인, 세이버메트릭스 계산 엔진, 자체 ML 모델, LLM 기반 기사 생성 시스템을 단계적으로 붙이는 구조로 개발합니다.

---

## 핵심 목표

- KBO 경기 일정, 스코어, 팀 순위, 선수 기록 제공
- 선수/팀별 세이버메트릭스 지표 시각화
- 경기별 승리확률, WPA, LI 등 고급 지표 제공
- LLM을 활용한 경기 리뷰 기사 자동 생성
- LLM을 활용한 선수/팀/세이버메트릭스 칼럼 생성
- 향후 자체 ML 모델을 통한 승리확률 예측, 선수 성과 예측, 기사 소재 랭킹 제공

---

## 현재 개발 단계

현재 저장소는 Next.js 기반 프론트엔드 프로젝트를 중심으로 구성되어 있습니다.

백엔드는 아직 실제 운영 서버로 붙어 있지 않으며, 향후 backend/ 디렉터리에 FastAPI 기반 백엔드를 추가할 예정입니다.

현재 단계의 목표는 다음과 같습니다.

text 1. 프론트엔드 mock MVP 완성 2. FastAPI mock backend 추가 3. 프론트엔드와 백엔드 API 연동 4. 세이버메트릭스 계산 모듈 추가 5. ML model skeleton 추가 6. AI 기사 생성 mock streaming 추가 7. 실제 KBO 데이터 수집기 연결 8. 실제 LLM 또는 fine-tuned LLM 연결 

---

## 기술 스택

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Vitest
- ESLint

### Backend 예정

- FastAPI
- Pydantic
- Uvicorn
- pytest
- PostgreSQL
- Redis
- Celery 또는 RQ
- Python 기반 analytics / ML module

### AI / ML 예정

- LLM 기반 기사 생성
- Fine-tuned LLM 또는 외부 LLM API
- 자체 Python ML 모델
- 승리확률 예측 모델
- 선수 성과 예측 모델
- 기사 소재 랭킹 모델

---

## 로컬 실행 방법

### 1. 의존성 설치

bash npm install 

### 2. 개발 서버 실행

bash npm run dev 

실행 후 아래 주소에서 확인합니다.

bash http://localhost:3000 

### 3. 린트 실행

bash npm run lint 

### 4. 테스트 실행

bash npm run test 

만약 test 스크립트가 없다면 package.json에 아래 스크립트를 추가합니다.

json {   "scripts": {     "test": "vitest"   } } 

### 5. 타입 체크

bash npm run typecheck 

만약 typecheck 스크립트가 없다면 package.json에 아래 스크립트를 추가합니다.

json {   "scripts": {     "typecheck": "tsc --noEmit"   } } 

---

## 환경 변수

향후 백엔드 API를 붙이면 프론트엔드에서 아래 환경 변수를 사용합니다.

bash NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1 

예시:

ts const API_BASE_URL =   process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1"; 

---

## 예정 백엔드 구조

향후 루트에 backend/ 디렉터리를 추가합니다.

text backend/   app/     main.py      core/       config.py       logging.py       exceptions.py      api/       routes/         health.py         teams.py         players.py         games.py         articles.py         ai.py         stats.py      schemas/       kbo.py       article.py       ai.py      mock/       data.py      repositories/       mock_repository.py      domain/       teams/         service.py       players/         service.py       games/         service.py       articles/         service.py      analytics/       sabermetrics/         batting.py         pitching.py         wpa.py       features/         game_state.py      ml/       contracts.py       registry.py       models/         win_probability_model.py         player_projection_model.py         article_topic_model.py      ai/       prompt_builder.py       mock_generator.py       generation_service.py      workers/       ingest_games.py       compute_sabermetrics.py       generate_articles.py      tests/       test_api.py       test_sabermetrics.py    requirements.txt   README.md   .env.example 

---

## 백엔드 실행 예정 방식

백엔드가 추가된 뒤에는 아래 방식으로 실행합니다.

### 1. 백엔드 디렉터리로 이동

bash cd backend 

### 2. Python 가상환경 생성

bash python -m venv .venv 

macOS / Linux:

bash source .venv/bin/activate 

Windows PowerShell:

bash .venv\Scripts\Activate.ps1 

### 3. 의존성 설치

bash pip install -r requirements.txt 

### 4. FastAPI 서버 실행

bash uvicorn app.main:app --reload --port 8000 

### 5. Swagger 문서 확인

bash http://localhost:8000/docs 

### 6. 백엔드 테스트 실행

bash pytest 

---

## 예정 API

### Health

http GET /api/v1/health 

### Teams

http GET /api/v1/teams GET /api/v1/teams/{team_id} 

### Players

http GET /api/v1/players GET /api/v1/players/{player_id} GET /api/v1/players?team_id=kt&position=IF&query=강백호 

### Games

http GET /api/v1/games/today GET /api/v1/games GET /api/v1/games?date=2026-06-09 GET /api/v1/games/{game_id} GET /api/v1/games/{game_id}/box-score GET /api/v1/games/{game_id}/play-by-play GET /api/v1/games/{game_id}/win-probability 

### Stats

http GET /api/v1/standings GET /api/v1/stat-leaders 

### Articles

http GET /api/v1/articles GET /api/v1/articles/{article_id} GET /api/v1/articles?category=game_recap 

### AI Mock Streaming

http POST /api/v1/ai/game-recap POST /api/v1/ai/player-analysis 

초기에는 실제 LLM을 호출하지 않고 mock streaming response만 반환합니다.

---

## KBO Mock Data 기준

초기 mock data에는 KBO 10개 팀을 모두 포함합니다.

text LG 트윈스 KT 위즈 SSG 랜더스 NC 다이노스 두산 베어스 KIA 타이거즈 롯데 자이언츠 삼성 라이온즈 한화 이글스 키움 히어로즈 

초기 mock data에 포함할 항목은 다음과 같습니다.

text 팀별 선수 최소 3명 오늘 경기 5개 경기별 box score 대표 경기 play-by-play 최소 12개 대표 경기 win probability point 최소 12개 팀 순위 10개 스탯 리더 AI 기사 mock 5개 이상 

주의 사항:

text mock data는 실제 경기 기록이 아닙니다. 실제 KBO 데이터를 사용하는 것처럼 표시하지 않습니다. 실제 KBO 사이트 크롤링은 추후 별도 단계에서 진행합니다. 

---

## 세이버메트릭스 개발 계획

초기에는 수식 기반 지표부터 구현합니다.

### 타자 지표

text AVG OBP SLG OPS ISO BABIP wOBA wRC+ WAR-lite 

예정 파일:

text backend/app/analytics/sabermetrics/batting.py 

필수 함수:

python calculate_avg(h, ab) calculate_obp(h, bb, hbp, ab, sf) calculate_slg(singles, doubles, triples, hr, ab) calculate_ops(obp, slg) calculate_iso(slg, avg) calculate_babip(h, hr, ab, so, sf) 

### 투수 지표

text ERA WHIP K% BB% K-BB% HR/9 FIP ERA+ WAR-lite 

예정 파일:

text backend/app/analytics/sabermetrics/pitching.py 

필수 함수:

python calculate_era(er, innings_pitched) calculate_whip(bb, h, innings_pitched) calculate_k_rate(so, batters_faced) calculate_bb_rate(bb, batters_faced) calculate_fip(hr, bb, hbp, so, innings_pitched, constant=3.10) 

### 경기 지표

text Win Expectancy WPA Leverage Index Run Expectancy 중요 플레이 순위 

예정 파일:

text backend/app/analytics/sabermetrics/wpa.py 

필수 함수:

python clamp_probability(value) calculate_wpa(before_home_wp, after_home_wp) calculate_leverage_index(abs_wp_change, avg_abs_wp_change) 

---

## 자체 ML 모델 개발 계획

LLM과 자체 ML 모델은 역할이 다릅니다.

자체 ML 모델은 판단과 예측을 담당합니다.

text 승리확률 예측 선수 성과 예측 기사 소재 랭킹 이상치 탐지 팀 전력 예측 

LLM은 표현과 서술을 담당합니다.

text 경기 기사 작성 선수 분석 칼럼 작성 팀 분석 칼럼 작성 세이버메트릭스 해설 생성 문체 변환 요약 

초기 ML 구조는 다음과 같습니다.

text backend/app/ml/   contracts.py   registry.py   models/     win_probability_model.py     player_projection_model.py     article_topic_model.py 

ML 설계 원칙:

text API route에서 ML 모델을 직접 import하지 않습니다. service layer가 model registry를 통해 모델을 가져옵니다. 모델 입출력은 Pydantic contract로 고정합니다. 모델 결과에는 model_name, model_version, confidence를 포함합니다. 나중에 sklearn, LightGBM, XGBoost, PyTorch 모델로 교체 가능해야 합니다. 

예상 발전 흐름:

text v0: rule-based placeholder v1: lookup table v2: sklearn / logistic regression v3: LightGBM / XGBoost v4: sequence / deep learning model 

---

## LLM / Fine-tuned LLM 통합 계획

초기에는 실제 LLM을 호출하지 않습니다.

초기 구조:

text backend/app/ai/   prompt_builder.py   mock_generator.py   generation_service.py 

향후 실제 LLM이 들어오면 다음 흐름으로 확장합니다.

text game_id 또는 player_id 입력 ↓ DB에서 경기/선수/세이버 지표 조회 ↓ 자체 ML 모델로 중요도/소재 랭킹 계산 ↓ article context JSON 생성 ↓ prompt_builder가 프롬프트 생성 ↓ fine-tuned LLM 또는 외부 LLM 호출 ↓ 초안 생성 ↓ fact check ↓ 검수 대기 ↓ 발행 

LLM에는 자연어보다 구조화된 JSON context를 우선 전달합니다.

json {   "game": {     "homeTeam": "KT 위즈",     "awayTeam": "삼성 라이온즈",     "homeScore": 4,     "awayScore": 3,     "stadium": "수원 KT위즈파크",     "status": "final"   },   "topPlaysByWpa": [     {       "inning": 8,       "half": "bottom",       "description": "2사 1,2루에서 좌전 적시타",       "wpa": 0.312,       "li": 3.1     }   ] } 

---

## 향후 DB 설계

초기에는 mock repository를 사용합니다.

이후 PostgreSQL을 붙일 때 필요한 핵심 테이블은 다음과 같습니다.

text teams players seasons games game_teams box_scores play_events player_game_stats team_game_stats player_season_stats team_season_stats standings sabermetric_snapshots articles article_generation_jobs article_fact_checks ml_models ml_predictions raw_kbo_payloads data_quality_issues 

DB 설계 원칙:

text 원본 데이터와 정제 데이터를 분리합니다. 세이버 지표는 계산 버전을 남깁니다. ML 예측 결과는 model_version과 함께 저장합니다. AI 콘텐츠는 생성과 발행을 분리합니다. 실시간 데이터와 경기 종료 후 확정 데이터를 분리합니다. 

---

## 데이터 수집기 개발 계획

초기에는 실제 수집기를 구현하지 않습니다.

향후 worker를 통해 수집과 계산을 분리합니다.

text backend/app/workers/ingest_games.py backend/app/workers/compute_sabermetrics.py backend/app/workers/generate_articles.py 

예상 수집 주기:

text 시즌 일정: 하루 1회 팀/선수 기본 정보: 하루 1회 오늘 경기 상태: 경기일 1~5분 간격 진행 중 경기 스코어: 15~30초 간격 플레이바이플레이: 15~30초 간격 경기 종료 후 박스스코어: 종료 직후 + 30분 후 재확인 시즌 누적 스탯: 경기 종료 후 배치 

데이터 수집 시 원본 payload를 반드시 저장합니다.

예상 테이블:

text raw_kbo_payloads - id - source - source_url - payload_type - payload_json - payload_text - fetched_at - checksum - parser_version 

---

## Admin / CMS 개발 계획

AI 콘텐츠는 바로 자동 발행하지 않고, 초기에는 검수 기반으로 운영합니다.

추가 예정 admin 기능:

text /admin/articles - AI 생성 기사 목록 - 상태 필터 - 미리보기 - 수정 - 승인 - 반려 - 발행  /admin/jobs - 데이터 수집 job 상태 - 기사 생성 job 상태 - 실패 원인  /admin/data-quality - 선수 매핑 오류 - 경기 데이터 누락 - 중복 이벤트 - 기록 정정 필요 항목 

기사 상태:

text draft generating generated fact_checking needs_review approved published failed 

---

## 개발 로드맵

### Phase 1. Frontend Mock MVP

text [ ] 홈 페이지 mock data 렌더링 [ ] 경기 목록 페이지 [ ] 경기 상세 페이지 [ ] 팀 목록 페이지 [ ] 팀 상세 페이지 [ ] 선수 목록 페이지 [ ] 선수 상세 페이지 [ ] 기사 목록 페이지 [ ] 기사 상세 페이지 [ ] AI mock streaming UI [ ] 모바일 반응형 정리 

### Phase 2. Backend Mock API

text [ ] FastAPI backend 추가 [ ] /api/v1/health 구현 [ ] /api/v1/teams 구현 [ ] /api/v1/games/today 구현 [ ] /api/v1/games/{id} 구현 [ ] /api/v1/players/{id} 구현 [ ] /api/v1/articles 구현 [ ] /api/v1/ai/game-recap streaming 구현 [ ] /api/v1/ai/player-analysis streaming 구현 [ ] pytest 작성 

### Phase 3. Frontend ↔ Backend 연동

text [ ] NEXT_PUBLIC_API_BASE_URL 추가 [ ] frontend API client 정리 [ ] 홈의 오늘 경기 API 연동 [ ] 팀 목록 API 연동 [ ] 경기 상세 API 연동 [ ] 선수 상세 API 연동 [ ] 기사 목록 API 연동 [ ] 로딩 상태 처리 [ ] 에러 상태 처리 

### Phase 4. Sabermetrics Engine

text [ ] AVG/OBP/SLG/OPS 계산 [ ] ERA/WHIP/FIP 계산 [ ] WPA/LI 계산 [ ] Run Expectancy 설계 [ ] WAR-lite 설계 [ ] 계산 함수 테스트 작성 [ ] 계산 버전 관리 방식 설계 

### Phase 5. ML Skeleton

text [ ] ml/contracts.py 작성 [ ] ModelRegistry 작성 [ ] WinProbabilityModel placeholder 작성 [ ] PlayerProjectionModel placeholder 작성 [ ] ArticleTopicModel placeholder 작성 [ ] model_name/model_version/confidence 반환 [ ] 서비스 계층에서 registry를 통해 모델 사용 

### Phase 6. Real KBO Data Ingestion

text [ ] 데이터 소스 조사 [ ] 이용약관 및 robots.txt 확인 [ ] raw payload 저장 구조 구현 [ ] 팀/선수 매핑 로직 구현 [ ] 경기 일정 수집 [ ] 경기 결과 수집 [ ] 플레이바이플레이 수집 [ ] 데이터 품질 이슈 저장 

### Phase 7. Database / Cache / Queue

text [ ] PostgreSQL schema 작성 [ ] migration 도구 도입 [ ] mock repository를 DB repository로 교체 [ ] Redis cache 도입 [ ] Celery/RQ/Arq 중 하나로 worker queue 도입 [ ] 수집 job retry 정책 작성 [ ] 기사 생성 job 비동기화 

### Phase 8. Real LLM Integration

text [ ] LLM provider gateway 작성 [ ] prompt_builder 구현 [ ] article context JSON 생성 [ ] game recap 생성 [ ] player analysis 생성 [ ] team analysis 생성 [ ] sabermetric column 생성 [ ] fact check 최소 구현 [ ] admin review flow 연결 

### Phase 9. Admin CMS

text [ ] /admin/articles [ ] /admin/jobs [ ] /admin/data-quality [ ] 기사 preview [ ] 기사 수정 [ ] 승인/반려 [ ] 발행 

### Phase 10. Production Readiness

text [ ] Sentry 연동 [ ] API rate limit [ ] 캐싱 정책 [ ] Docker 배포 [ ] staging/prod 환경 분리 [ ] CI/CD [ ] 로그/알림 체계 [ ] 백업 전략 

---

## Claude Code 작업 권장 순서

Claude Code에는 한 번에 모든 작업을 요청하지 않고 단계별로 요청합니다.

### 1차 작업

text 현재 repo 구조를 확인하고 backend/ 디렉터리에 FastAPI 스캐폴딩, schemas, mock data, repository, 기본 API routes를 추가해라. 실제 외부 API 호출은 하지 마라. pytest로 health, teams, games, articles API 테스트를 추가해라. 

### 2차 작업

text backend/app/analytics와 backend/app/ml 구조를 추가해라. batting, pitching, wpa 계산 함수와 테스트를 작성하고, ml/contracts.py, registry.py, win_probability_model.py, player_projection_model.py, article_topic_model.py skeleton을 구현해라. 

### 3차 작업

text backend/app/ai에 mock streaming generation 구조를 추가해라. /api/v1/ai/game-recap, /api/v1/ai/player-analysis 엔드포인트에서 StreamingResponse를 반환하게 하고, 프론트엔드에서 연동 가능한 형식으로 문서를 작성해라. 

### 4차 작업

text 프론트엔드의 mock data 접근 구조를 확인하고, NEXT_PUBLIC_API_BASE_URL 기반 API client를 추가해라. 우선 홈의 오늘 경기, 팀 목록, 경기 상세부터 백엔드 API로 교체해라. 로딩과 에러 상태를 추가해라. 

### 5차 작업

text README, BACKEND_MERGE_NOTES, .env.example, docker-compose.backend.yml을 정리하고, 로컬 실행 방법과 앞으로의 개발 로드맵을 문서화해라. npm lint/test와 pytest 실행 결과를 확인하고 문제를 수정해라. 

---

## 주의사항

text 실제 KBO 크롤링은 아직 하지 않습니다. 실제 LLM API 호출은 아직 하지 않습니다. API key를 코드에 넣지 않습니다. mock data를 실제 데이터처럼 표현하지 않습니다. AI 생성 문구에는 AI-generated 또는 mock 표시를 남깁니다. 프론트엔드와 백엔드는 HTTP API로만 연결합니다. 세이버메트릭스 계산 로직과 LLM 기사 생성 로직을 섞지 않습니다. ML 모델은 API route에 직접 붙이지 않고 registry/service layer를 통해 호출합니다. 

---

## 최종 목표 아키텍처

text Next.js Frontend   ↓ FastAPI Backend API   ↓ PostgreSQL   ↓ Redis Cache / Queue   ↓ Worker Layer   ├─ KBO Data Ingestion   ├─ Sabermetrics Calculation   ├─ ML Prediction   └─ LLM Article Generation   ↓ Admin Review / CMS   ↓ Published Articles & Analytics Pages 

---

## 프로젝트 방향

SAVEX의 최종 방향은 다음과 같습니다.

text KBO 데이터 파이프라인 + 세이버메트릭스 분석 엔진 + 자체 ML 예측 모델 + LLM 기반 기사/칼럼 생성 CMS 

초기에는 mock으로 빠르게 MVP를 만들고, 이후 실제 데이터와 모델을 단계적으로 붙입니다.