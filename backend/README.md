# KBO Insight — FastAPI Backend

KBO 세이버매트릭스 + AI 기사 생성 플랫폼의 백엔드 API 서버.  
현재 MVP 단계로 모든 데이터는 **mock 데이터**이며, 실제 KBO API/LLM 연동은 준비됩니다.

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

# 3. 환경변수 설정 (옵션)
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
| GET | `/api/v1/standings` | 팀 순위표 |
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

> AI 엔드포인트는 현재 mock 스트리밍입니다. 실제 LLM을 호출하지 않습니다.

---

## Mock 데이터 교체 방법

### 1. KBO 실제 데이터 수집기 연결
`backend/app/workers/ingest_games.py`의 `main()` 함수에 실제 KBO 데이터 소스 연동 코드를 추가한다.

```python
# 예: KBO 공식 데이터 API 연동
async def main():
    games = await kbo_client.fetch_today_games()
    for game in games:
        await real_repo.upsert_game(game)
```

### 2. PostgreSQL Repository 연결
`backend/app/repositories/` 아래 `postgres_repository.py`를 추가하고,  
`MockRepository`와 동일한 메서드 시그니처를 구현한다.  
각 domain service에서 `mock_repo` 대신 `pg_repo`를 주입하면 된다.

```python
# backend/app/domain/teams/service.py
from app.repositories.postgres_repository import pg_repo  # 교체

class TeamsService:
    def list_teams(self):
        return pg_repo.list_teams()
```

### 3. 세이버매트릭스 배치 계산
`backend/app/workers/compute_sabermetrics.py`에서  
`analytics.sabermetrics.batting` / `pitching` 함수를 호출하고 결과를 DB에 저장한다.

---

## ML 모델 연결 방법

`backend/app/ml/registry.py`에 실제 모델을 등록하면 된다:

```python
from your_module import RealWinProbModel  # joblib, lightgbm, sklearn, torch 등

registry.register("win_probability", "1.0.0-lgbm", RealWinProbModel.load("model.pkl"))
```

모든 ML 계약(I/O 스키마)은 `backend/app/ml/contracts.py`에 정의돼 있다.  
API route는 registry를 통해 모델을 사용하므로 코드 변경 없이 모델을 교체할 수 있다.

---

## 실제 LLM 연결 방법

`backend/app/ai/generation_service.py`의 `GenerationService`에 LLM provider 분기를 추가한다:

```python
if settings.LLM_PROVIDER == "anthropic":
    from app.ai.anthropic_client import stream_game_recap_real
    async for chunk in stream_game_recap_real(game, prompt):
        yield chunk
```

`backend/app/ai/prompt_builder.py`에 실제 LLM prompt가 이미 skeleton으로 준비돼 있다.  
`.env`에서 `LLM_PROVIDER=anthropic`과 `LLM_API_KEY=sk-ant-...`를 설정하면 된다.

---

## 테스트 실행 방법

```bash
cd backend
pytest -v
```

총 56개 테스트 (API 통합 테스트 23개 + 세이버매트릭스 유닛 테스트 33개).
