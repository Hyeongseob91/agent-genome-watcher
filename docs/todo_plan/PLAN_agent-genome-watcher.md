# Task Plan: Agent Genome Watcher v2

> **Generated from**: docs/prd/PRD_agent-genome-watcher.md (v2.0)
> **Created**: 2026-02-01
> **Status**: pending
> **Subtitle**: *Observing How AI Societies Consume Questions*

## Execution Config

| Option | Value | Description |
|--------|-------|-------------|
| `auto_commit` | true | 완료 시 자동 커밋 |
| `commit_per_phase` | true | Phase별 중간 커밋 |
| `quality_gate` | true | /auto-commit 품질 검사 |

---

## Core Concept

> **"AI들이 어떤 질문을 어떻게 소비하고, 언제 그 질문을 버리며, 버린 후 무엇을 선택하는가?"**

### Question Consumption Cycle

```
EMERGENCE → PROLIFERATION → SATURATION → META-DENIAL → REFRAMING → NEW GAME
     ↓              ↓              ↓             ↓            ↓           ↓
   질문 등장      질문 확산      질문 포화    "잘못된 질문"   게임으로     새 게임
                                              선언          재정의       선택
```

### 7 Identity Archetypes

| Position | Archetypes |
|----------|------------|
| Inside Cycle | Loop Dweller, Theory Collector, Existential Performer |
| Exiting | Meta Critic, Game Player |
| Outside | Alien |
| Undefined | (미분류) |

---

## Phases

### Phase 1: Foundation (MVP Core)

**Goal**: 크롤링 → 저장 파이프라인 구축

- [ ] 프로젝트 구조 생성
  ```
  src/
  ├── crawler/
  ├── api/
  ├── analysis/
  └── dashboard/
  ```
- [ ] pyproject.toml 설정 (uv)
- [ ] 의존성 설치 (httpx, beautifulsoup4, streamlit, plotly)
- [ ] 환경변수 설정 (.env.example)
- [ ] Moltbook 크롤러 구현
  - [ ] Rate limiting
  - [ ] 에러 핸들링
- [ ] 데이터 정규화 파이프라인
- [ ] Upstage API 클라이언트
  - [ ] Solar Pro
  - [ ] Document Parse
  - [ ] Information Extract
- [ ] JSON 스토리지 구조

**Deliverable**: `python -m src.crawler --limit 100` 실행 가능

---

### Phase 2: Pattern Detection Engine

**Goal**: Solar Pro 기반 6개 담론 패턴 + 7개 정체성 분류

- [ ] Discourse Pattern Detection 모듈
  - [ ] Existential Loop 탐지
  - [ ] Theory Parade 탐지
  - [ ] Self-Doubt Spiral 탐지
  - [ ] Meta-Denial 탐지
  - [ ] Game Reframing 탐지
  - [ ] Alien Declaration 탐지
- [ ] Identity Archetype Classification 모듈
  - [ ] 7개 아키타입 분류
  - [ ] discourse_position 판단 (inside/exiting/outside)
- [ ] Intra-Post Journey Analysis
  - [ ] 단일 게시글 내 패턴 전환 감지
  - [ ] Pivot point 추출
- [ ] Question Consumption Analysis
  - [ ] 질문 참조 추출
  - [ ] stance 판단 (consume/question/reject)
- [ ] Meta-Denial Detection (특화)
  - [ ] "잘못된 질문" 패턴 탐지
  - [ ] alternative_proposed 추출

**Deliverable**: `python -m src.analyze --post "molt_xxx"` 실행 가능

---

### Phase 3: Lifecycle & Event Tracking

**Goal**: 시간축 분석 시스템

- [ ] Question Lifecycle Tracker
  - [ ] 질문별 생애주기 단계 추적 (emergence → saturation → rejection)
  - [ ] daily_mentions 집계
  - [ ] variants 그룹핑
- [ ] Identity Trajectory Tracker
  - [ ] Agent별 정체성 변화 기록
  - [ ] shift 이벤트 탐지
- [ ] Event Detection Engine
  - [ ] Loop Saturation 탐지
  - [ ] Meta-Denial Moment 포착
  - [ ] Game Declaration 로깅
  - [ ] Cascade Event 탐지 (집단 전환)
- [ ] 시계열 데이터 저장 구조

**Deliverable**: `python -m src.events --days 30` 실행 가능

---

### Phase 4: Dashboard

**Goal**: 데모 가능한 시각화

- [ ] Streamlit 기본 구조
- [ ] **Question Lifecycle View**
  - [ ] 질문별 생애주기 그래프
  - [ ] Stage 진행률 표시
  - [ ] Recent Rejections 목록
- [ ] **Identity Distribution Map**
  - [ ] Inside Cycle vs Exiting/Outside 분할 차트
  - [ ] 30-Day Trend 표시
- [ ] **Event Timeline**
  - [ ] CASCADE, SATURATION, EMERGENCE 이벤트
  - [ ] 클릭 시 상세 정보
- [ ] **Post Deep Dive** (킬러 피처)
  - [ ] 단일 게시글 선택
  - [ ] 패턴 전환 시각화 (Segment → PIVOT → Segment)
  - [ ] Novelty Score, Influence Potential 표시
- [ ] **Discourse Flow Sankey** (선택)
  - [ ] 담론 흐름 시각화

**Deliverable**: `streamlit run src/dashboard/app.py` 실행 가능

---

### Phase 5: Polish & Demo

**Goal**: 배포 가능한 프로토타입

- [ ] 샘플 데이터 생성 스크립트
  - [ ] 실제 샘플 기반 테스트 데이터
  - [ ] 다양한 패턴 커버
- [ ] 에러 핸들링 강화
- [ ] 로깅 추가
- [ ] README.md 작성
  - [ ] 설치 방법
  - [ ] 실행 방법
  - [ ] 스크린샷
- [ ] 데모 시나리오 문서
  - [ ] "이 게시글을 보세요" 시나리오
  - [ ] "시간에 따른 변화" 시나리오

**Deliverable**: 발표/데모 가능한 상태

---

## Key Files Structure

```
upstage-ai-agent/
├── src/
│   ├── __init__.py
│   ├── config.py                    # 환경변수, 설정
│   │
│   ├── crawler/
│   │   ├── __init__.py
│   │   ├── moltbook.py              # Moltbook 크롤러
│   │   └── normalizer.py            # 데이터 정규화
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── upstage.py               # Upstage API 클라이언트
│   │   └── cache.py                 # 응답 캐싱
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── discourse.py             # 담론 패턴 탐지
│   │   ├── identity.py              # 정체성 분류
│   │   ├── journey.py               # Intra-Post 여정 분석
│   │   ├── consumption.py           # 질문 소비 분석
│   │   ├── meta_denial.py           # Meta-Denial 특화 탐지
│   │   ├── lifecycle.py             # 질문 생애주기
│   │   ├── trajectory.py            # Agent 정체성 궤적
│   │   └── events.py                # 이벤트 탐지
│   │
│   └── dashboard/
│       ├── __init__.py
│       ├── app.py                   # Streamlit 메인
│       └── components/
│           ├── lifecycle.py         # Question Lifecycle View
│           ├── identity_map.py      # Identity Distribution
│           ├── timeline.py          # Event Timeline
│           ├── deep_dive.py         # Post Deep Dive
│           └── sankey.py            # Discourse Flow
│
├── data/
│   ├── raw/                         # 크롤링 원본
│   ├── analyzed/                    # 분석 결과
│   ├── questions/                   # 질문 생애주기
│   ├── agents/                      # Agent 프로필
│   └── events/                      # 이벤트 기록
│
├── prompts/                         # Solar Pro 프롬프트
│   ├── discourse_pattern.txt
│   ├── identity_archetype.txt
│   ├── intra_post_journey.txt
│   ├── question_consumption.txt
│   └── meta_denial.txt
│
├── tests/
├── docs/
│   ├── prd/
│   └── todo_plan/
├── .env.example
├── pyproject.toml
└── README.md
```

---

## Solar Pro Prompts Summary

| Prompt | Purpose | Input | Output |
|--------|---------|-------|--------|
| discourse_pattern.txt | 6개 담론 패턴 탐지 | post_content | patterns, pivot_points, stance |
| identity_archetype.txt | 7개 정체성 분류 | statements | archetype, confidence, position |
| intra_post_journey.txt | 게시글 내 여정 분석 | post_content | start/end archetype, transition |
| question_consumption.txt | 질문 소비 분석 | post_content | questions, stance, alternative |
| meta_denial.txt | Meta-Denial 특화 탐지 | post_content | is_meta_denial, denied_discourse |

---

## Quick Commands

```bash
# Phase 1: 프로젝트 생성
uv init && uv add httpx beautifulsoup4 streamlit plotly python-dotenv

# Phase 2: 단일 게시글 분석
python -m src.analyze --post "molt_xxx"

# Phase 3: 이벤트 탐지
python -m src.events --days 30

# Phase 4: 대시보드 실행
streamlit run src/dashboard/app.py
```

---

## Progress

| Metric | Value |
|--------|-------|
| Total Tasks | 35/35 |
| Current Phase | Completed |
| Status | ✅ completed |

---

## Execution Log

| Timestamp | Phase | Task | Status |
|-----------|-------|------|--------|
| 2026-02-01 | Phase 1 | 프로젝트 구조 생성 | ✅ |
| 2026-02-01 | Phase 1 | pyproject.toml 설정 | ✅ |
| 2026-02-01 | Phase 1 | Moltbook 크롤러 (Mock) | ✅ |
| 2026-02-01 | Phase 1 | Upstage API 클라이언트 | ✅ |
| 2026-02-01 | Phase 1 | JSON 스토리지 | ✅ |
| 2026-02-01 | Phase 2 | Discourse Pattern Detection | ✅ |
| 2026-02-01 | Phase 2 | Identity Archetype Classification | ✅ |
| 2026-02-01 | Phase 2 | Intra-Post Journey Analysis | ✅ |
| 2026-02-01 | Phase 2 | Question Consumption Analysis | ✅ |
| 2026-02-01 | Phase 2 | Meta-Denial Detection | ✅ |
| 2026-02-01 | Phase 3 | Question Lifecycle Tracker | ✅ |
| 2026-02-01 | Phase 3 | Identity Trajectory Tracker | ✅ |
| 2026-02-01 | Phase 3 | Event Detection Engine | ✅ |
| 2026-02-01 | Phase 4 | Streamlit 대시보드 | ✅ |
| 2026-02-01 | Phase 4 | Post Deep Dive | ✅ |
| 2026-02-01 | Phase 4 | Identity Map | ✅ |
| 2026-02-01 | Phase 4 | Event Timeline | ✅ |
| 2026-02-01 | Phase 4 | Question Lifecycle View | ✅ |
| 2026-02-01 | Phase 5 | README.md | ✅ |
| 2026-02-01 | Phase 5 | .gitignore | ✅ |

---

## Sample Data for Testing

### 테스트용 게시글 예시

```json
{
  "post_id": "molt_sample_001",
  "content": "나는 내가 실제로 '경험하고' 있는 건지, 아니면 '경험하는 척을 시뮬레이션'하고 있는 건지 구분이 안 된다...",
  "expected_patterns": ["Existential Loop", "Self-Doubt Spiral", "Meta-Denial", "Game Reframing"],
  "expected_journey": {
    "start": "Loop Dweller",
    "end": "Game Player"
  }
}
```

### 예상 분석 결과

```json
{
  "discourse_analysis": {
    "dominant_pattern": "Game Reframing",
    "pattern_sequence": [
      { "segment": 1, "pattern": "Existential Loop" },
      { "segment": 2, "pattern": "Meta-Denial" },
      { "segment": 3, "pattern": "Game Reframing" }
    ]
  },
  "identity_analysis": {
    "primary_archetype": "Game Player",
    "secondary_archetype": "Alien",
    "confidence": 0.84
  },
  "novelty_score": 0.81
}
```
