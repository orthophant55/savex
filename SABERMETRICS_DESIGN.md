# SAVEX Sabermetrics Design

> 이 문서는 SAVEX의 세이버매트릭스 설계 철학, 구현 우선순위, KBO 적용 시 주의사항을 정리한 것이다.

## 1. 핵심 설계 철학

SAVEX는 KBO 기록을 단순히 보여주는 사이트가 아니라, **득점가치·승리기여·예측값**으로 변환해주는 플랫폼이다.

야구 지표를 다루는 5가지 방식:

| 계층 | 개념 | 예시 |
|------|------|------|
| 1. 관측값 | 기록된 결과 | AVG, ERA, OPS |
| 2. 잠재 실력의 noisy observation | 관측 성적 = 잠재 실력 + 표본오차 + 운 | 보정 AVG, 표본 안정성 점수 |
| 3. 득점가치 | 이벤트를 run value로 변환 | wOBA, FIP, RE24 |
| 4. 승리기여 | 득점을 승리 단위로 변환 | WAR, WPA, Pythagorean Wins |
| 5. 의사결정 기준 | 전략 판단 | 번트/도루/교체 기대득점 변화 |

---

## 2. 핵심 참고 문헌

### 2-1. 표본 신뢰성 / Regression to the Mean

- **Efron & Morris (1975)** — Stein Estimator, Empirical Bayes  
  - "타자의 현재 타율은 잠재 실력의 noisy estimate다"  
  - 표본이 작을수록 리그 평균 쪽으로 shrinkage  
  - 구현: `regression_adjustment.py` → `calculate_regression_adjusted_avg()`

- **Brown (2008)** — "In-Season Predictions of Batting Averages"  
  - naive AVG는 표본이 적을 때 리그 평균보다 예측력이 낮다  
  - empirical Bayes 방식이 낫다

- **Jensen, McShane, Wyner** — Hierarchical Bayesian hitting model  
  - age, position, past performance를 함께 반영하는 구조  
  - 구현: `regression_adjusted_batting_model.py` → TODO로 확장 예정

### 2-2. 기대득점 / Run Expectancy

- **Bukiet, Harold, Palacios (1997)** — Markov chain 기반 base-out state 기대득점  
  - 24개 base-out state (8 base × 3 out)  
  - RE24: 플레이 전후 기대득점 변화  
  - 구현: `run_expectancy.py`

- **Tango, Lichtman, Dolphin — The Book (2007)**  
  - 번트/도루/대타/불펜/플래툰의 기대득점/기대승률 영향 분석  
  - Leverage Index 정의  
  - 구현: `wpa.py`, `win_expectancy.py`

### 2-3. Linear Weights / wOBA

- **FanGraphs Linear Weights** — 단타/2루타/홈런/볼넷의 run value를 실증 측정  
  - 단타가 0.47, 홈런이 1.40인 것은 단순 counting이 아님  
  - wOBA weight = linear weight를 OBP 스케일로 환산  
  - 구현: `linear_weights.py`, `woba.py`

### 2-4. Fielding Independent Pitching

- **FIP** — HR, BB, HBP, K처럼 투수가 직접 통제하는 이벤트 중심  
  - ERA는 수비·운의 영향을 받음. FIP가 더 예측 가능한 투수 능력 측정치  
  - xFIP: HR을 리그 평균 HR/FB로 대체 (구현 예정)  
  - SIERA: 타구 유형 추가 반영 (구현 예정)  
  - 구현: `fip.py`

### 2-5. WAR (Wins Above Replacement)

- **Baumer, Jensen, Matthews — openWAR (2015)**  
  - "WAR는 단일 정답이 아니라 불확실성을 가진 추정치다"  
  - 타격/투구/주루/수비 기여를 대체수준 대비 승리로 환산  
  - 수비 기여는 데이터 한계로 측정 오차가 크다  
  - 구현: `war_lite.py` (skeleton, placeholder)

### 2-6. Pythagorean Expectation

- **Bill James (1980s)** — RS^x / (RS^x + RA^x)  
  - 득실점으로 기대승률 추정  
  - KBO 최적 exponent x는 역사적 KBO 데이터로 회귀 추정 필요  
  - 구현: `pythagorean.py`

### 2-7. WPA / Win Expectancy

- **Win Expectancy** — inning, half, score_diff, outs, base_state를 key로 홈팀 승리확률 lookup  
- **WPA (Win Probability Added)** — 플레이 전후 홈팀 승리확률 변화  
  - 클러치한 홈런 > 블로우아웃 홈런 (맥락 반영)  
- 구현: `win_expectancy.py`, `wpa.py`

---

## 3. 지표 범주

| 범주 | 주요 지표 |
|------|----------|
| 타격 기본 | PA, AB, H, 1B, 2B, 3B, HR, BB, IBB, HBP, SO, SF, SH, GDP |
| 타격 비율 | AVG, OBP, SLG, OPS, ISO, BB%, K%, BABIP, wOBA, wRAA, wRC, wRC+ |
| 투수 기본 | IP, ER, R, H, HR, BB, HBP, K, BF |
| 투수 세이버 | ERA, RA9, WHIP, K/9, BB/9, HR/9, K%, BB%, K-BB%, FIP, xFIP*, SIERA* |
| 주루 | SB, CS, SB%*, wSB*, BsR* |
| 수비 | E, FPct*, UZR*, DRS*, OAA* |
| 팀 | W, L, WPct, RS, RA, RD, PythWPct, ExpW, Actual-Expected |
| 상황/맥락 | RE24, WPA, WE, LI, Clutch* |
| Statcast/트래킹 | ExitVelo†, LaunchAngle†, HardHit%†, Barrel%†, xBA†, xwOBA†, SprintSpeed† |

`*` = placeholder (구조만 있음, 실제 계산 미구현)  
`†` = future (KBO 공개 데이터에 현재 미제공)

---

## 4. 구현 우선순위

### 1단계 (완료)
- AVG, OBP, SLG, OPS, ISO, BB%, K%, BABIP
- ERA, RA9, WHIP, K/9, BB/9, HR/9, K%, BB%, K-BB%
- FIP, FIP-

### 2단계 (완료)
- wOBA, wRAA, wRC, wRC+
- RE24 (24 base-out state)
- WPA, LI, WE

### 3단계 (완료)
- Pythagorean WPct, Expected Wins, Actual-Expected

### 4단계 (완료)
- Regression-adjusted AVG, OPS (shrinkage/empirical Bayes)
- Projected player stats (placeholder)
- Sample reliability score
- Confidence interval placeholder

### 5단계 (미구현 - TODO)
- xFIP, SIERA
- WAR-lite (본격 계산)
- 번트/도루 손익분기점 시뮬레이터
- 플래툰 효과
- 불펜 교체 의사결정 지원

---

## 5. context-neutral vs context-dependent 구분

| 구분 | 의미 | 예시 |
|------|------|------|
| context-neutral | 상황과 무관한 절대 가치 | RE24, wOBA, FIP |
| context-dependent | 상황에 따라 가치가 달라짐 | WPA, LI, IBB |

**중요**: AI 기사는 지표의 context를 함께 설명해야 한다.  
- 9회 동점 역전 홈런의 WPA >> 10:0 리드 홈런의 WPA  
- 단, 두 홈런의 wOBA 기여는 동일  

---

## 6. KBO 전용 파라미터 추정 필요 사항

아래 파라미터는 현재 MLB 데이터 또는 임의값을 placeholder로 사용 중이다.
KBO 역사적 데이터가 확보되면 실제 값으로 교체해야 한다.

| 파라미터 | 현재값 | 추정 방법 |
|---------|--------|----------|
| Pythagorean exponent x | 1.83 | log(W/L) / log(RS/RA) 회귀 |
| FIP constant | 3.10 | lgERA - (13×lgHR + 3×(lgBB+lgHBP) - 2×lgK) / lgIP |
| wOBA weights | MLB FanGraphs 2024 | KBO RE table 기반 linear weights 회귀 |
| wOBA scale | 1.15 | wOBA를 run value로 환산 비율 |
| League avg | 0.269 | 실제 KBO 시즌 집계 |
| Stabilization points | MLB estimate | KBO career split-half reliability 분석 |
| Park factors | 1.0 (중립) | 구장별 멀티시즌 득점환경 비교 |
| RE24 table | MLB approximate | KBO play-by-play 데이터 집계 필요 |
| WE table | 개발용 소규모 mock | KBO 역사 game state → logistic regression |

---

## 7. kbo-data 기반 ingestion 한계 및 주의사항

### kbo-data가 제공하는 데이터
- 박스스코어 (scoreboard)
- 타자 기록 (away_batter, home_batter)
- 투수 기록 (away_pitcher, home_pitcher)
- ETC_info (경기 부가 정보)

### kbo-data의 한계
- **play-by-play 이벤트 미제공**: RE24, WPA 계산에 필요한 공 하나하나 이벤트는 포함되지 않을 수 있다.
- **Statcast 수준 트래킹 미제공**: Exit Velocity, Launch Angle, Sprint Speed 불가
- **수비 지표 미제공**: UZR, DRS, OAA 계산 불가
- **ChromeDriver 필요**: 웹 스크래핑 방식
- **KBO 공식 홈페이지 변경 시 파싱 깨질 수 있음**

### 사용 시 주의사항
- KBO 공식 홈페이지 robots.txt / 이용약관 반드시 확인
- 과도한 요청 금지 (`KBO_REQUEST_DELAY_SECONDS` 설정)
- 실제 서비스 전 데이터 출처·권리 검토 필요
- 개발/연구 목적으로만 사용

### mock fallback 전략
```python
if KBO_DATA_ENABLED and KBO_INGESTION_MODE == "kbo-data":
    try:
        raw = kbo_data_client.fetch(...)
        save raw payload
        normalize
        return normalized
    except:
        log error
        if MOCK_MODE: return mock data
else:
    return mock data
```

---

## 8. WAR 불확실성 관점

openWAR (Baumer et al., 2015)의 관점에서:
- WAR는 단일 숫자가 아니라 **불확실성을 가진 추정치**
- 수비 기여는 측정 오차가 매우 크므로 보수적으로 표시
- KBO 수비 데이터 한계로 `war_lite.py`는 현재 skeleton/placeholder
- WAR-lite를 공식 WAR처럼 표시하지 않는다

---

## 9. AI 기사 생성 정책

- AI는 지표를 **계산하지 않는다**. 계산된 지표를 **설명**만 한다.
- LLM에게 수치 추론을 맡기지 않는다.
- 모든 수치는 sabermetrics engine이 제공한 JSON에서만 온다.
- 기사는 draft 상태로 생성되며, fact_checker → review → publish 단계를 거친다.
- mock data로 생성된 기사는 명확히 "MOCK AI 생성 콘텐츠"로 표시된다.

---

## 10. 향후 확장 방향

1. **KBO 역사적 play-by-play 데이터 확보** → 실제 RE24/WE table 구축
2. **KBO 전용 파라미터 회귀 추정** → wOBA weights, FIP constant, Pythagorean x
3. **PostgreSQL 저장** → 팀/선수/경기/플레이 이벤트 정규화
4. **Redis Cache** → 자주 접근하는 지표 캐싱
5. **Celery/Arq Worker** → 자동 수집 스케줄링
6. **ML 모델 고도화** → LightGBM/XGBoost 승리확률 모델, hierarchical Bayesian 타자 예측
7. **Fine-tuned LLM** → 세이버매트릭스 어휘/지표 정의 학습된 기사 생성 모델
8. **KBO 구장 효과 추정** → 파크팩터 계산으로 wRC+/FIP- 보정 개선
