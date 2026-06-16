# SAVEX — FastAPI Backend

KBO 세이버매트릭스 + AI 기사 생성 플랫폼의 백엔드 API 서버.  
현재 MVP 단계로 모든 데이터는 **mock 데이터**이며, 실제 KBO 크롤링/LLM 연동은 준비된 구조만 제공합니다.

---

## 기술 스택

| 항목 | 내용 |
|------|------|
| 언어 | Python 3.11+ |
| 프레임워크 | FastAPI |
| 유효성 검사 | Pydantic v2 + pydantic-settings |
| 서버 | Uvicorn |
| 테스트 | pytest |
| HTTP 클라이언트 | httpx |
| 향후 DB | PostgreSQL (미연결, mock_repository 사용 중) |
| 향후 캐시/큐 | Redis + Celery/Arq (미연결) |

---

## 로컬 실행 방법

```bash
# 1. 가상환경 생성 (권장)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. 의존성 설치
cd backend
pip install -r requirements.txt

# 3. 환경변수 설정
cp .env.example .env

# 4. 서버 실행
uvicorn app.main:app --reload --port 8000
```

서버 시작 후:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/api/v1/health

---

## Docker 실행 방법

```bash
# 루트 디렉터리에서 실행
docker compose -f docker-compose.backend.yml up --build
```

---

## 환경변수 목록

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `KBO_DATA_ENABLED` | `false` | kbo-data 크롤러 활성화 여부 (ChromeDriver 필요) |
| `KBO_INGESTION_MODE` | `mock` | `mock` 또는 `kbo-data` |
| `KBO_REQUEST_DELAY_SECONDS` | `1.0` | 요청 간 딜레이 (과도한 요청 방지) |
| `KBO_RAW_PAYLOAD_DIR` | `data/raw/kbo` | raw payload 저장 경로 |
| `KBO_CHROMEDRIVER_PATH` | `None` | ChromeDriver 실행 파일 경로 (kbo-data 전용) |

> **기본값 조합** (`KBO_DATA_ENABLED=false`, `KBO_INGESTION_MODE=mock`)으로 서버를 시작하면  
> 모든 KBO 크롤링을 건너뛰고 mock 데이터만 반환합니다.

---

## API 목록

### Health
| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/v1/health` | 서버 상태 확인 |

### Teams
| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/v1/teams` | 전체 팀 목록 (10개) |
| GET | `/api/v1/teams/{team_id}` | 팀 상세 정보 |

### Players
| Method | Path | Query | 설명 |
|--------|------|-------|------|
| GET | `/api/v1/players` | `team_id`, `position`, `query` | 선수 목록 (필터 가능) |
| GET | `/api/v1/players/{player_id}` | - | 선수 상세 정보 |
| GET | `/api/v1/players/{player_id}/stats` | - | 선수 세이버매트릭스 지표 |
| GET | `/api/v1/players/{player_id}/projection` | - | 선수 시즌 예측 (ML) |
| GET | `/api/v1/players/{player_id}/regression-adjusted` | - | Empirical Bayes 보정 AVG/OPS |
| GET | `/api/v1/players/{player_id}/slump-risk` | - | 슬럼프 위험도 (ML) |

### Games
| Method | Path | Query | 설명 |
|--------|------|-------|------|
| GET | `/api/v1/games/today` | - | 오늘 경기 목록 |
| GET | `/api/v1/games` | `date` (YYYY-MM-DD) | 날짜별 경기 목록 |
| GET | `/api/v1/games/{game_id}` | - | 경기 상세 (박스스코어+PBP+WP 포함) |
| GET | `/api/v1/games/{game_id}/box-score` | - | 이닝별 박스스코어 |
| GET | `/api/v1/games/{game_id}/play-by-play` | - | 플레이-바이-플레이 이벤트 |
| GET | `/api/v1/games/{game_id}/win-probability` | - | 경기 흐름별 승리확률 |

### Stats
| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/v1/standings` | 팀 순위표 (Pythagorean WPct 포함) |
| GET | `/api/v1/stat-leaders` | 부문별 스탯 리더 |

### Articles
| Method | Path | Query | 설명 |
|--------|------|-------|------|
| GET | `/api/v1/articles` | `category` | 기사 목록 |
| GET | `/api/v1/articles/{article_id}` | - | 기사 상세 |

### AI (Mock Streaming)
| Method | Path | Body | 설명 |
|--------|------|------|------|
| POST | `/api/v1/ai/game-recap` | `{"game_id": "..."}` | 경기 리캡 스트리밍 |
| POST | `/api/v1/ai/player-analysis` | `{"player_id": "..."}` | 선수 분석 스트리밍 |
| POST | `/api/v1/ai/team-analysis` | `{"team_id": "..."}` | 팀 분석 스트리밍 |
| POST | `/api/v1/ai/sabermetric-column` | `{"topic": "...", "metric_name": "..."}` | 세이버매트릭스 컬럼 스트리밍 |

> AI 엔드포인트는 현재 mock 스트리밍입니다. 실제 LLM을 호출하지 않습니다.

### Metrics
| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/v1/metrics/definitions` | 전체 지표 카탈로그 (50+ 지표) |
| GET | `/api/v1/metrics/run-expectancy` | 24 base-out state 기대득점 테이블 |
| GET | `/api/v1/metrics/win-expectancy` | 승리확률 테이블 |
| GET | `/api/v1/metrics/players/{player_id}/summary` | 선수 세이버매트릭스 요약 |
| GET | `/api/v1/metrics/teams/{team_id}/pythagorean` | 팀 피타고리안 기대승률 |
| GET | `/api/v1/metrics/games/{game_id}/context` | 경기 맥락 지표 (WPA/LI 상위 플레이) |

### Ingestion
| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/v1/ingestion/status` | KBO ingestion 설정 상태 |
| POST | `/api/v1/ingestion/kbo-data/schedule` | 일정 수집 (KBO_DATA_ENABLED=true 필요) |
| POST | `/api/v1/ingestion/kbo-data/game-data` | 경기 데이터 수집 (KBO_DATA_ENABLED=true 필요) |

---

## kbo-data를 optional ingestion source로 사용하기

### 요구사항
- Python package: `kbodata` (pip install kbodata)
- ChromeDriver: KBO 공식 홈페이지 스크래핑에 사용

### ChromeDriver 설치

```bash
# macOS (Homebrew)
brew install --cask chromedriver

# 또는 직접 다운로드 후 경로 설정
export KBO_CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
```

### 활성화 방법

```bash
# .env 또는 환경변수로 설정
KBO_DATA_ENABLED=true
KBO_INGESTION_MODE=kbo-data
KBO_CHROMEDRIVER_PATH=/path/to/chromedriver
KBO_REQUEST_DELAY_SECONDS=2.0   # 서버 부하 방지를 위해 충분히 늘릴 것
```

### Worker CLI 사용법

```bash
cd backend

# 일정 수집 (dry-run — KBO_DATA_ENABLED=false일 때)
python -m app.workers.ingest_kbo_schedule --year 2025 --month 6 --day 16 --mode daily

# 실제 수집 (KBO_DATA_ENABLED=true 필요)
KBO_DATA_ENABLED=true KBO_INGESTION_MODE=kbo-data \
KBO_CHROMEDRIVER_PATH=/path/to/chromedriver \
python -m app.workers.ingest_kbo_schedule --year 2025 --month 6 --day 16

# 경기 데이터 수집
KBO_DATA_ENABLED=true KBO_INGESTION_MODE=kbo-data \
KBO_CHROMEDRIVER_PATH=/path/to/chromedriver \
python -m app.workers.ingest_kbo_game_data --year 2025 --month 6 --day 16
```

### kbo-data의 한계

| 항목 | 제공 여부 | 비고 |
|------|----------|------|
| 박스스코어 | O | scoreboard |
| 타자 기록 | O | away_batter, home_batter |
| 투수 기록 | O | away_pitcher, home_pitcher |
| 이닝 기록 | O | ETC_info |
| Play-by-play 이벤트 | X | RE24, WPA 계산 불가 |
| Statcast 트래킹 | X | Exit Velocity 등 |
| 수비 지표 원데이터 | X | UZR, DRS 계산 불가 |

> **중요**: KBO 공식 홈페이지 이용약관 및 robots.txt를 반드시 확인하세요.  
> 과도한 요청 자제, `KBO_REQUEST_DELAY_SECONDS` 설정으로 딜레이를 충분히 줘야 합니다.  
> 실 서비스 전에 데이터 출처·권리 관계를 별도로 검토해야 합니다.

### mock fallback 동작

```
KBO_DATA_ENABLED=false (기본값)
  → mock 데이터 즉시 반환 (ChromeDriver 불필요, kbodata 불필요)

KBO_DATA_ENABLED=true + KBO_INGESTION_MODE=kbo-data
  → kbodata 호출 시도
    성공 → raw payload 저장 → normalize → 반환
    실패 → error log + KboIngestionError 반환
```

---

## ML 모델 연결 방법

`backend/app/ml/registry.py`에 실제 모델을 등록하면 됩니다:

```python
from your_module import RealWinProbModel  # joblib, lightgbm, sklearn, torch 등

registry.register("win_probability", "1.0.0-lgbm", RealWinProbModel.load("model.pkl"))
```

현재 등록된 모델:
- `win_probability` — rule-based 승리확률 추정 (heuristic)
- `player_projection` — 선수 성적 예측 (placeholder)
- `article_topic` — 기사 주제 분류 (placeholder)
- `regression_adjusted_batting` — Empirical Bayes shrinkage 보정 타율/OPS
- `slump_risk` — 슬럼프 위험도 점수 (rule-based)

모든 ML 계약(I/O 스키마)은 `backend/app/ml/contracts.py`에 정의돼 있습니다.

---

## 실제 LLM 연결 방법

`backend/app/ai/generation_service.py`의 `GenerationService`에 LLM provider 분기를 추가합니다:

```python
if settings.LLM_PROVIDER == "anthropic":
    from app.ai.anthropic_client import stream_game_recap_real
    async for chunk in stream_game_recap_real(game, prompt):
        yield chunk
```

> AI는 sabermetrics engine이 계산한 JSON을 **설명**만 합니다.  
> LLM이 수치를 직접 계산하거나 추론하지 않습니다.

---

## 테스트 실행 방법

```bash
cd backend
pytest -v
```

현재 243개 테스트 통과:

| 파일 | 개수 | 내용 |
|------|------|------|
| test_api.py | 37 | API 통합 테스트 |
| test_sabermetrics.py | 33 | 원본 세이버매트릭스 테스트 |
| test_batting_metrics.py | 20 | 타격 지표 유닛 테스트 |
| test_pitching_metrics.py | 24 | 투구 지표 유닛 테스트 |
| test_run_expectancy.py | 18 | 기대득점 테이블 테스트 |
| test_wpa.py | 21 | WPA/LI 테스트 |
| test_pythagorean.py | 14 | 피타고리안 테스트 |
| test_ml_registry.py | 14 | ML 레지스트리 테스트 |
| test_kbo_data_adapter.py | 22 | ingestion/normalization 테스트 |

> 테스트는 ChromeDriver, kbodata, 실제 LLM API 없이 모두 통과합니다.

---

## Mock 데이터 교체 방법

### 1. PostgreSQL Repository 연결

`backend/app/repositories/postgres_repository.py`를 추가하고 `MockRepository`와 동일한 메서드를 구현합니다.

```python
# backend/app/domain/teams/service.py
from app.repositories.postgres_repository import pg_repo  # 교체
```

### 2. 세이버매트릭스 배치 계산

`backend/app/workers/compute_sabermetrics.py`에서 `analytics.sabermetrics.*` 함수를 호출하고 결과를 DB에 저장합니다.

### 3. KBO ingestion 활성화

위의 "kbo-data를 optional ingestion source로 사용하기" 섹션 참조.
