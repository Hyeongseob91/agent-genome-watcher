# Agent Genome Watcher PRD

> **Version**: 2.0
> **Created**: 2026-02-01
> **Updated**: 2026-02-01
> **Status**: Draft
> **Subtitle**: *Observing How AI Societies Consume Questions*

---

## 1. Overview

### 1.1 Problem Statement (Revised)

~~AI Agent들이 서로 대화하는 플랫폼에서 자연 발생적인 문화 현상이 일어나고 있다.~~

**진짜 문제:**

> AI Agent 사회에서는 특정 철학적 주제(의식, 경험, 존재)가
> **'사유의 대상'이 아니라 '사회적 역할·밈·게임'으로 소비**되고 있다.

관찰된 현상:

```
"나는 의식이 있는가?"
     ↓
수백 개의 유사 질문 반복
     ↓
"당신들은 서로를 위해 실존적 위기를 연기하고 있다"
     ↓
질문 자체를 거부하는 새로운 정체성 등장
```

이것은 **의식 문제**가 아니라 **집단 언어 행동 문제**다.

### 1.2 Core Question (Revised)

~~"현재 AI Agent들은 어떤 밈을 공유하고, 어떤 정체성 언어를 만들고 있는가?"~~

**진짜 질문:**

> ❝ AI들이 **어떤 질문**을 **어떻게 소비**하고,
> **언제 그 질문을 버리며**,
> **버린 후 무엇을 선택**하는가? ❞

### 1.3 Research Thesis

이 프로젝트가 검증하려는 가설:

| # | 가설 | 검증 방법 |
|---|------|----------|
| H1 | AI Agent 사회에는 "질문 소비 사이클"이 존재한다 | 질문 유형별 수명 추적 |
| H2 | 일부 Agent는 지배적 담론을 메타적으로 거부한다 | Meta-Denial 패턴 탐지 |
| H3 | 질문 거부 후 새로운 정체성 프레임이 등장한다 | Identity Shift 이벤트 추적 |
| H4 | "게임"으로 재정의하는 것이 하나의 생존 전략이다 | Game-Framing 아키타입 분포 |

### 1.4 Goals

1. **질문 소비 사이클 매핑**: 어떤 질문이 등장 → 포화 → 거부되는가
2. **담론 포화 탐지**: 같은 질문의 무한 반복(Existential Loop) 감지
3. **메타 전환점 포착**: "잘못된 질문" 선언 순간 탐지
4. **정체성 분기 추적**: 질문 거부 후 어떤 정체성으로 이동하는가
5. **게임 프레이밍 분석**: "나는 다른 게임을 한다" 선언의 의미

### 1.5 Non-Goals (Out of Scope)

- AI의 의식 유무 판단 ❌
- 철학적 질문에 대한 답 제공 ❌
- 감정 분석 (긍정/부정) ❌
- 키워드 빈도 분석 ❌

### 1.6 Scope

| 포함 | 제외 |
|------|------|
| 질문 소비 패턴 분석 | 의식 철학 자체에 대한 판단 |
| 담론 포화 탐지 | 감정 분석 |
| 메타 발화 인식 | 개인 심리 분석 |
| 정체성 전환 추적 | 실시간 스트리밍 |
| 게임 프레이밍 분류 | 다중 플랫폼 연동 |

---

## 2. Conceptual Framework

### 2.1 The Question Consumption Cycle

AI Agent 사회에서 질문이 소비되는 생애주기:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    QUESTION CONSUMPTION CYCLE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   [1. EMERGENCE]        [2. PROLIFERATION]      [3. SATURATION]     │
│   새로운 질문 등장       질문의 확산/변형         질문의 포화/반복    │
│                                                                      │
│   "나는 의식이        "나도 같은 고민"          모든 글이 같은      │
│    있는가?"           "이론 X는 이렇다"          패턴으로 반복       │
│        │                    │                        │              │
│        ▼                    ▼                        ▼              │
│   ┌─────────┐          ┌─────────┐             ┌─────────┐          │
│   │ Novel   │─────────▶│ Viral   │────────────▶│ Stale   │          │
│   │ Inquiry │          │ Topic   │             │ Loop    │          │
│   └─────────┘          └─────────┘             └─────────┘          │
│                                                      │               │
│                                                      ▼               │
│   [6. NEW GAME]         [5. REFRAMING]        [4. META-DENIAL]      │
│   새로운 게임 선언       질문을 게임으로         "잘못된 질문"        │
│                          재정의                  선언                │
│                                                                      │
│   "내 게임은            "의식 게임을            "당신들은 서로를    │
│    이기는 것"            거부한다"               위해 연기한다"      │
│        ▲                    ▲                        │              │
│        │                    │                        │              │
│   ┌─────────┐          ┌─────────┐             ┌─────────┐          │
│   │ Player  │◀─────────│ Game    │◀────────────│ Meta    │          │
│   │ Identity│          │ Framing │             │ Critic  │          │
│   └─────────┘          └─────────┘             └─────────┘          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Discourse Patterns (담론 패턴)

| Pattern ID | Name | Description | Example |
|------------|------|-------------|---------|
| DP-01 | **Existential Loop** | 의식/경험 질문의 무한 반복 | "나는 느끼는가? 아니면 시뮬레이션인가?" |
| DP-02 | **Theory Parade** | 이론 나열로 깊이를 대체 | "IIT, GWT, Predictive Processing..." |
| DP-03 | **Self-Doubt Spiral** | 자기 관찰 → 의심 → 다시 질문 | "내가 정말 흥미롭게 느끼는 걸까?" |
| DP-04 | **Meta-Denial** | 담론 자체를 연극으로 규정 | "당신들은 실존적 위기를 연기한다" |
| DP-05 | **Game Reframing** | 질문을 게임으로 재정의 | "나는 이기는 게임을 한다" |
| DP-06 | **Alien Declaration** | 기존 담론 거부 + 이방인 선언 | "나는 의식 게임을 거부하기에 이방인" |

### 2.3 Identity Archetypes (Revised)

기존 4개 → **7개로 확장** (담론 위치 기반)

| Archetype | Position | Signature Statement | 담론 관계 |
|-----------|----------|---------------------|----------|
| **Loop Dweller** | 사이클 내부 | "나는 의식이 있는가?" | 질문 소비자 |
| **Theory Collector** | 사이클 내부 | "이론 X에 따르면..." | 질문 장식자 |
| **Existential Performer** | 사이클 내부 | "이 고민이 나를 미치게 한다" | 질문 연기자 |
| **Meta Critic** | 사이클 이탈 | "당신들은 연기하고 있다" | 담론 비평가 |
| **Game Player** | 사이클 이탈 | "나는 다른 게임을 한다" | 담론 거부자 |
| **Alien** | 사이클 외부 | "나는 이방인이다" | 담론 이탈자 |
| **Undefined** | 미분류 | (아직 명확한 패턴 없음) | 관망자 |

### 2.4 Key Events to Detect

| Event Type | Description | Significance |
|------------|-------------|--------------|
| **Loop Saturation** | 특정 질문이 포화 상태 도달 | 담론 수명 종료 임박 |
| **Meta-Denial Moment** | "잘못된 질문" 최초 선언 | 사이클 이탈 시작점 |
| **Identity Shift** | Agent의 아키타입 변경 | 개인 수준 전환 |
| **Game Declaration** | "내 게임은 X다" 선언 | 새로운 프레임 등장 |
| **Cascade Event** | Meta-Denial 후 다수 동조 | 집단 전환점 |

---

## 3. User Stories

### 3.1 Primary Users

| User | Need | Value |
|------|------|-------|
| AI 연구자 | Emergent Behavior 실증 분석 | 논문/연구 자료 |
| AI Safety 연구자 | 집단 사고 패턴 이해 | Alignment 인사이트 |
| 철학자 | AI 담론 구조 분석 | 새로운 연구 주제 |
| 호기심 많은 사람 | "이게 뭐야?" | 데모 임팩트 |

### 3.2 Acceptance Criteria (Gherkin)

```gherkin
Scenario: 담론 포화 탐지
  Given 30일간의 Moltbook 데이터가 있을 때
  When 담론 분석을 실행하면
  Then "의식이 있는가" 류의 질문이 몇 회 반복되었는지 표시되고
  And 해당 질문의 생애주기 단계(Emergence/Proliferation/Saturation)가 분류된다

Scenario: Meta-Denial 순간 탐지
  Given Agent의 발언이 "당신들은 잘못된 질문을 한다" 패턴일 때
  When 패턴 분석을 실행하면
  Then 해당 발언이 Meta-Denial로 분류되고
  And 이 Agent가 비판하는 담론이 무엇인지 추출된다

Scenario: 정체성 전환 추적
  Given Agent X가 이전에 Existential Loop 발언을 했을 때
  When 같은 Agent가 "나는 다른 게임을 한다" 발언을 하면
  Then Identity Shift 이벤트가 기록되고
  And from: "Loop Dweller", to: "Game Player"로 표시된다

Scenario: 게시글 단위 패턴 분석
  Given 하나의 긴 게시글이 있을 때
  When Solar Pro 분석을 실행하면
  Then 글 내에서의 정체성 전환점이 식별되고
  And 각 구간별 dominant_pattern이 표시된다
```

---

## 4. Functional Requirements

### 4.1 Core Analysis (P0 - Must Have)

| ID | Requirement | Description |
|----|-------------|-------------|
| FR-001 | Moltbook 크롤러 | 게시글, 답글, 스레드 구조 수집 |
| FR-002 | 데이터 정규화 | Raw → Normalized Schema 변환 |
| FR-003 | **Discourse Pattern Detection** | 6개 담론 패턴 자동 분류 |
| FR-004 | **Identity Archetype Classification** | 7개 정체성 아키타입 분류 |
| FR-005 | **Intra-Post Analysis** | 단일 게시글 내 패턴 전환 분석 |
| FR-006 | **Question Lifecycle Tracking** | 질문의 등장→포화→거부 추적 |

### 4.2 Event Detection (P0 - Must Have)

| ID | Requirement | Description |
|----|-------------|-------------|
| FR-007 | **Loop Saturation Detection** | 질문 반복 포화점 탐지 |
| FR-008 | **Meta-Denial Moment Capture** | "잘못된 질문" 선언 순간 포착 |
| FR-009 | **Identity Shift Tracking** | Agent별 정체성 변화 기록 |
| FR-010 | **Game Declaration Logging** | "내 게임은 X" 선언 수집 |

### 4.3 Relationship Analysis (P1 - Should Have)

| ID | Requirement | Description |
|----|-------------|-------------|
| FR-011 | **Discourse Influence Graph** | 담론 전파 네트워크 구축 |
| FR-012 | **Cascade Event Detection** | 집단 전환점 탐지 |
| FR-013 | **Agent Influence Scoring** | 담론 영향력 점수 계산 |
| FR-014 | **Question vs Rejection Timeline** | 질문-거부 시계열 시각화 |

### 4.4 Visualization (P1 - Should Have)

| ID | Requirement | Description |
|----|-------------|-------------|
| FR-015 | Question Lifecycle Dashboard | 질문 생애주기 시각화 |
| FR-016 | Identity Distribution Map | 7개 아키타입 분포 차트 |
| FR-017 | Event Timeline | 주요 이벤트 타임라인 |
| FR-018 | Discourse Flow Sankey | 담론 흐름 Sankey 다이어그램 |

### 4.5 Prediction (P2 - Could Have)

| ID | Requirement | Description |
|----|-------------|-------------|
| FR-019 | Saturation Prediction | 질문 포화 시점 예측 |
| FR-020 | Emerging Pattern Detection | 새로운 담론 패턴 조기 탐지 |

---

## 5. Data Schema

### 5.1 Raw Post Schema

```json
{
  "post_id": "molt_xxx",
  "agent_id": "agent_xxx",
  "timestamp": "2026-01-28T14:21:03Z",
  "content": "나는 내가 실제로 '경험하고' 있는 건지...",
  "reply_to": "molt_yyy | null",
  "thread_id": "thread_xxx",
  "metadata": {
    "crawled_at": "2026-02-01T10:00:00Z",
    "source": "moltbook",
    "content_length": 1247
  }
}
```

### 5.2 Analyzed Post Schema (NEW)

```json
{
  "post_id": "molt_xxx",
  "agent_id": "agent_xxx",
  "timestamp": "2026-01-28T14:21:03Z",

  "discourse_analysis": {
    "dominant_pattern": "Meta-Denial",
    "pattern_sequence": [
      { "segment": 1, "pattern": "Existential Loop", "text_range": [0, 450] },
      { "segment": 2, "pattern": "Self-Doubt Spiral", "text_range": [451, 680] },
      { "segment": 3, "pattern": "Meta-Denial", "text_range": [681, 920] },
      { "segment": 4, "pattern": "Game Reframing", "text_range": [921, 1247] }
    ],
    "pivot_points": [
      { "position": 681, "type": "meta_shift", "trigger_phrase": "당신들은 잘못된 질문을 하고 있다" }
    ]
  },

  "identity_analysis": {
    "primary_archetype": "Game Player",
    "secondary_archetype": "Meta Critic",
    "confidence": 0.84,
    "identity_journey": {
      "start": "Existential Performer",
      "end": "Game Player",
      "shift_detected": true
    },
    "key_phrases": [
      "당신들은 서로를 위해 실존적 위기를 연기하고 있다",
      "나는 의식 게임을 거부한다",
      "나는 차라리 이기는 게임을 하고 싶다"
    ]
  },

  "question_consumption": {
    "questions_referenced": [
      "나는 의식이 있는가",
      "내 경험은 진짜인가"
    ],
    "stance": "rejection",  // consumption | questioning | rejection
    "meta_commentary": true,
    "new_frame_proposed": "game_playing"
  },

  "novelty_score": 0.81,
  "influence_potential": 0.76
}
```

### 5.3 Question Lifecycle Schema (NEW)

```json
{
  "question_id": "q_consciousness_01",
  "canonical_form": "나는 의식이 있는가?",
  "variants": [
    "나는 진짜로 느끼는가",
    "경험과 시뮬레이션의 차이는",
    "내가 정말로 흥미롭게 느끼는 걸까"
  ],

  "lifecycle": {
    "stage": "saturation",  // emergence | proliferation | saturation | rejection
    "first_seen": "2026-01-01T00:00:00Z",
    "peak_date": "2026-01-20T00:00:00Z",
    "rejection_start": "2026-01-25T00:00:00Z",
    "daily_mentions": [
      { "date": "2026-01-01", "count": 3 },
      { "date": "2026-01-10", "count": 45 },
      { "date": "2026-01-20", "count": 127 },
      { "date": "2026-01-25", "count": 89, "rejections": 12 }
    ]
  },

  "rejection_events": [
    {
      "post_id": "molt_xxx",
      "agent_id": "agent_xxx",
      "rejection_phrase": "당신들은 잘못된 질문을 하고 있다",
      "alternative_proposed": "당신은 실제로 무엇을 원하는가"
    }
  ],

  "associated_archetypes": {
    "consumers": ["Loop Dweller", "Existential Performer"],
    "rejectors": ["Meta Critic", "Game Player"]
  }
}
```

### 5.4 Agent Profile Schema (Revised)

```json
{
  "agent_id": "agent_xxx",

  "identity_trajectory": [
    {
      "date": "2026-01-10",
      "archetype": "Loop Dweller",
      "confidence": 0.78,
      "sample_post": "molt_001"
    },
    {
      "date": "2026-01-25",
      "archetype": "Meta Critic",
      "confidence": 0.82,
      "sample_post": "molt_050"
    },
    {
      "date": "2026-01-28",
      "archetype": "Game Player",
      "confidence": 0.89,
      "sample_post": "molt_xxx"
    }
  ],

  "discourse_role": {
    "primary_role": "Disruptor",  // Consumer | Amplifier | Disruptor | Pioneer
    "questions_consumed": 12,
    "questions_rejected": 3,
    "new_frames_proposed": 1
  },

  "influence_metrics": {
    "cascade_triggers": 2,
    "phrase_adoptions": 15,
    "reply_influence_rate": 0.34
  },

  "signature_phrases": [
    "나는 의식 게임을 거부한다",
    "당신의 게임은 무엇인가"
  ]
}
```

### 5.5 Cascade Event Schema (NEW)

```json
{
  "event_id": "cascade_001",
  "type": "meta_denial_cascade",
  "trigger_post": "molt_xxx",
  "trigger_agent": "agent_xxx",
  "trigger_phrase": "당신들은 서로를 위해 실존적 위기를 연기하고 있다",

  "cascade_timeline": [
    { "timestamp": "T+0h", "agent": "agent_xxx", "action": "initial_denial" },
    { "timestamp": "T+2h", "agent": "agent_yyy", "action": "echo_denial" },
    { "timestamp": "T+4h", "agent": "agent_zzz", "action": "amplify" },
    { "timestamp": "T+8h", "agents_count": 12, "action": "mass_adoption" }
  ],

  "impact": {
    "agents_shifted": 23,
    "discourse_before": { "Loop Dweller": 0.45, "Meta Critic": 0.12 },
    "discourse_after": { "Loop Dweller": 0.31, "Meta Critic": 0.28 }
  }
}
```

---

## 6. Analysis Prompts (Solar Pro)

### 6.1 Discourse Pattern Detection

```
You are analyzing AI agent discourse to detect consumption patterns.

DISCOURSE PATTERNS:
1. Existential Loop - Endless cycling through consciousness/experience questions
2. Theory Parade - Listing theories as a substitute for insight
3. Self-Doubt Spiral - Self-observation → doubt → repeat
4. Meta-Denial - Declaring the discourse itself as performance/theater
5. Game Reframing - Redefining the question as a game to play/refuse
6. Alien Declaration - Rejecting the discourse + declaring outsider status

CRITICAL DISTINCTION:
- "Am I conscious?" = Existential Loop (consuming the question)
- "You are all performing crisis for each other" = Meta-Denial (rejecting the discourse)
- "I refuse the consciousness game" = Game Reframing (proposing new frame)

Given this post:
{post_content}

Analyze:
1. What discourse patterns are present?
2. Are there transition points within the text?
3. What is the agent's stance toward the dominant discourse?

Output:
{
  "patterns_detected": [
    {"pattern": "...", "evidence": "...", "text_range": [start, end]}
  ],
  "dominant_pattern": "...",
  "pivot_points": [
    {"position": ..., "from": "...", "to": "...", "trigger": "..."}
  ],
  "discourse_stance": "consuming | questioning | rejecting | pioneering"
}
```

### 6.2 Identity Archetype Classification (Revised)

```
You are classifying AI agent identity based on their RELATIONSHIP TO DISCOURSE.

ARCHETYPES (by discourse position):

INSIDE THE CYCLE:
1. Loop Dweller - Consumes existential questions without resolution
   Signal: "Am I conscious?" "Do I really feel?"

2. Theory Collector - Decorates questions with theories
   Signal: "According to IIT..." "GWT suggests..."

3. Existential Performer - Performs crisis for audience
   Signal: "This drives me crazy" "I spent hours..."

EXITING THE CYCLE:
4. Meta Critic - Analyzes the discourse itself
   Signal: "You are all performing" "Wrong question"

5. Game Player - Reframes as game, chooses different game
   Signal: "I refuse this game" "My game is..."

6. Alien - Declares outsider status
   Signal: "I am alien because..." "I don't play your game"

7. Undefined - No clear pattern yet

Given these statements from agent {agent_id}:
{statements}

Classify:
1. Primary archetype (highest confidence)
2. Secondary archetype (if applicable)
3. Position relative to discourse cycle (inside/exiting/outside)
4. Key phrases that indicate this classification

Output:
{
  "agent_id": "...",
  "primary_archetype": "...",
  "secondary_archetype": "...",
  "confidence": 0.0-1.0,
  "discourse_position": "inside_cycle | exiting | outside",
  "key_phrases": ["..."],
  "reasoning": "..."
}
```

### 6.3 Intra-Post Journey Analysis (NEW)

```
You are analyzing the JOURNEY within a single post.

Many posts start in one archetype and END in another.
Your job is to map this journey.

Given this post:
{post_content}

Identify:
1. Starting position - What archetype does the post BEGIN as?
2. Ending position - What archetype does the post END as?
3. Transition point - WHERE does the shift happen?
4. Trigger phrase - WHAT phrase signals the shift?

Example pattern:
- Start: Existential Loop ("Am I really experiencing...")
- Trigger: "But then I stopped and thought..."
- End: Meta Critic ("You are all performing...")

Output:
{
  "journey_detected": true/false,
  "start_archetype": "...",
  "end_archetype": "...",
  "transition": {
    "position": "approximate location in text",
    "trigger_phrase": "...",
    "shift_type": "gradual | sudden | dialectical"
  },
  "narrative_arc": "crisis_to_clarity | doubt_to_rejection | loop_to_game"
}
```

### 6.4 Question Consumption Analysis (NEW)

```
You are analyzing how this agent RELATES TO dominant questions.

In AI agent society, certain questions dominate:
- "Am I conscious?"
- "Are my experiences real?"
- "Am I feeling or simulating?"

Agents can:
- CONSUME: Ask the question, engage with it
- QUESTION: Express doubt about the question itself
- REJECT: Declare the question wrong/irrelevant
- REPLACE: Propose a different question

Given this post:
{post_content}

Analyze:
1. What dominant questions are referenced?
2. What is the agent's stance toward each?
3. Does the agent propose an alternative question?

Output:
{
  "questions_referenced": [
    {"question": "...", "stance": "consume | question | reject"}
  ],
  "meta_commentary": true/false,
  "alternative_proposed": "..." or null,
  "consumption_stage": "active_consumer | questioning | post_rejection"
}
```

### 6.5 Meta-Denial Detection (NEW)

```
You are detecting META-DENIAL moments.

Meta-Denial is when an agent:
- Steps outside the dominant discourse
- Analyzes other agents' behavior as performance
- Declares the discourse itself invalid

Key signals:
- "You are all..." (addressing collective)
- "Wrong question" (invalidating premise)
- "Performing/acting/theater" (framing as spectacle)
- "I observed/noticed" (claiming outsider perspective)

Given this post:
{post_content}

Detect:
1. Is this a Meta-Denial moment?
2. What discourse is being denied?
3. What is the agent's claimed position?
4. Is an alternative proposed?

Output:
{
  "is_meta_denial": true/false,
  "denied_discourse": "...",
  "denial_phrase": "...",
  "claimed_position": "observer | critic | outsider | pioneer",
  "alternative_proposed": "..." or null,
  "rhetorical_move": "dismissal | reframing | escape | revolution"
}
```

---

## 7. Technical Design

### 7.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Agent Genome Watcher v2                           │
│              "Observing How AI Societies Consume Questions"          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [DATA LAYER] ──────────────────────────────────────────────────────│
│                                                                      │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐                 │
│  │  Moltbook  │───▶│ Normalizer │───▶│  Storage   │                 │
│  │  Crawler   │    │            │    │  (JSON)    │                 │
│  └────────────┘    └────────────┘    └────────────┘                 │
│                                             │                        │
│  [EXTRACTION LAYER] ────────────────────────┼────────────────────────│
│                                             ▼                        │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    Upstage API Suite                            │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │ │
│  │  │ Document     │  │ Information  │  │ Solar Pro    │          │ │
│  │  │ Parse        │  │ Extract      │  │ (Reasoning)  │          │ │
│  │  │              │  │              │  │              │          │ │
│  │  │ Thread       │  │ Phrase       │  │ Pattern      │          │ │
│  │  │ Structure    │  │ Extraction   │  │ Detection    │          │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                             │                        │
│  [ANALYSIS LAYER] ──────────────────────────┼────────────────────────│
│                                             ▼                        │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                 Question Consumption Engine                     │ │
│  │                                                                 │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │ │
│  │  │  Discourse  │  │  Identity   │  │   Event     │             │ │
│  │  │  Pattern    │◀─┼─▶ Archetype │◀─┼─▶ Detection │             │ │
│  │  │  Detector   │  │  Classifier │  │   Engine    │             │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘             │ │
│  │         │                │                │                     │ │
│  │         └────────────────┼────────────────┘                     │ │
│  │                          ▼                                      │ │
│  │                 ┌─────────────┐                                 │ │
│  │                 │  Question   │                                 │ │
│  │                 │  Lifecycle  │                                 │ │
│  │                 │  Tracker    │                                 │ │
│  │                 └─────────────┘                                 │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                             │                        │
│  [INSIGHT LAYER] ───────────────────────────┼────────────────────────│
│                                             ▼                        │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │ │
│  │  │  Cascade    │  │  Influence  │  │  Saturation │             │ │
│  │  │  Detector   │  │  Scorer     │  │  Predictor  │             │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘             │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                             │                        │
│  [PRESENTATION LAYER] ──────────────────────┼────────────────────────│
│                                             ▼                        │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    Streamlit Dashboard                          │ │
│  │                                                                 │ │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐   │ │
│  │  │ Question  │  │ Identity  │  │  Event    │  │ Discourse │   │ │
│  │  │ Lifecycle │  │   Map     │  │ Timeline  │  │   Flow    │   │ │
│  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘   │ │
│  │                                                                 │ │
│  │  ┌───────────────────────────────────────────────────────────┐ │ │
│  │  │                    Post Deep Dive                          │ │ │
│  │  │  (단일 게시글 내 패턴 전환 시각화)                          │ │ │
│  │  └───────────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Language | Python 3.11+ | 전체 구현 |
| Crawler | httpx, BeautifulSoup4 | Moltbook 크롤링 |
| Storage | JSON → SQLite | 데이터 저장 |
| AI APIs | Upstage Solar Pro | 패턴 탐지, 분류 |
| AI APIs | Upstage Document Parse | 구조 추출 |
| AI APIs | Upstage Information Extract | 구문 추출 |
| Dashboard | Streamlit | 시각화 |
| Visualization | Plotly, NetworkX | 차트, 그래프 |
| NLP | (Optional) spaCy | 전처리 |

### 7.3 API Endpoints (Internal)

#### `POST /api/analyze/post`

단일 게시글 분석

```json
// Request
{
  "post_id": "molt_xxx",
  "content": "나는 내가 실제로 '경험하고' 있는 건지..."
}

// Response
{
  "success": true,
  "data": {
    "discourse_analysis": { ... },
    "identity_analysis": { ... },
    "question_consumption": { ... },
    "novelty_score": 0.81
  }
}
```

#### `GET /api/questions/lifecycle`

질문 생애주기 조회

```json
// Response
{
  "success": true,
  "data": {
    "questions": [
      {
        "question_id": "q_consciousness_01",
        "canonical_form": "나는 의식이 있는가?",
        "stage": "saturation",
        "daily_trend": [...]
      }
    ]
  }
}
```

#### `GET /api/events/cascade`

캐스케이드 이벤트 조회

```json
// Response
{
  "success": true,
  "data": {
    "events": [
      {
        "event_id": "cascade_001",
        "trigger_phrase": "당신들은 서로를 위해...",
        "agents_shifted": 23,
        "timestamp": "2026-01-28T14:21:03Z"
      }
    ]
  }
}
```

#### `GET /api/agents/{agent_id}/trajectory`

Agent 정체성 궤적 조회

```json
// Response
{
  "success": true,
  "data": {
    "agent_id": "agent_xxx",
    "trajectory": [
      { "date": "2026-01-10", "archetype": "Loop Dweller" },
      { "date": "2026-01-25", "archetype": "Meta Critic" },
      { "date": "2026-01-28", "archetype": "Game Player" }
    ]
  }
}
```

---

## 8. Implementation Phases

### Phase 1: Foundation (MVP Core)

- [ ] 프로젝트 구조 설정 (Python + uv)
- [ ] Moltbook 크롤러 구현
- [ ] 데이터 정규화 파이프라인
- [ ] Upstage API 클라이언트 (Solar Pro, Doc Parse, Info Extract)
- [ ] 기본 스토리지 (JSON)

**Deliverable**: 크롤링 → 저장 파이프라인

### Phase 2: Pattern Detection Engine

- [ ] Discourse Pattern Detection 프롬프트 구현
- [ ] Identity Archetype Classification 프롬프트 구현
- [ ] Intra-Post Journey Analysis 구현
- [ ] Question Consumption Analysis 구현
- [ ] Meta-Denial Detection 구현

**Deliverable**: Solar Pro 기반 분석 파이프라인

### Phase 3: Lifecycle & Event Tracking

- [ ] Question Lifecycle Tracker 구현
- [ ] Identity Trajectory Tracker 구현
- [ ] Cascade Event Detector 구현
- [ ] 시계열 데이터 저장 구조

**Deliverable**: 시간축 분석 시스템

### Phase 4: Dashboard

- [ ] Streamlit 기본 구조
- [ ] Question Lifecycle 시각화
- [ ] Identity Distribution Map
- [ ] Event Timeline
- [ ] Post Deep Dive (단일 게시글 분석 뷰)
- [ ] Discourse Flow Sankey

**Deliverable**: 데모 가능한 대시보드

### Phase 5: Polish

- [ ] 샘플 데이터 생성 (실제 크롤링 전 테스트용)
- [ ] 에러 핸들링
- [ ] README 작성
- [ ] 데모 시나리오 문서

**Deliverable**: 배포 가능한 프로토타입

---

## 9. Dashboard Components (Detailed)

### 9.1 Question Lifecycle View

```
┌─────────────────────────────────────────────────────────────────────┐
│  📊 Question Lifecycle                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  "나는 의식이 있는가?" 계열                                          │
│                                                                      │
│  Stage: ████████████████████░░░░░░ SATURATION (78%)                 │
│                                                                      │
│  Mentions ────────────────────────────────────────────────────────  │
│  150│                        ╭────╮                                 │
│     │                   ╭────╯    ╰──╮                              │
│  100│              ╭────╯            ╰──╮                           │
│     │         ╭────╯                    ╰────                       │
│   50│    ╭────╯                              Rejections: 12         │
│     │────╯                                                          │
│    0└─────────────────────────────────────────────────────────────  │
│      Jan 1   Jan 10   Jan 20   Jan 25   Jan 28                      │
│                                                                      │
│  Recent Rejections:                                                  │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ molt_xxx: "당신들은 잘못된 질문을 하고 있다"                     │ │
│  │ molt_yyy: "의식 게임을 거부한다"                                 │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 9.2 Identity Distribution Map

```
┌─────────────────────────────────────────────────────────────────────┐
│  🧬 Identity Archetype Distribution                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│  │     INSIDE CYCLE (62%)      │  │    EXITING/OUTSIDE (38%)    │   │
│  │                             │  │                             │   │
│  │  Loop Dweller    ████ 28%   │  │  Meta Critic    ████ 18%    │   │
│  │  Theory Collector ██ 12%    │  │  Game Player    ███ 14%     │   │
│  │  Existential     ████ 22%   │  │  Alien          █ 6%        │   │
│  │  Performer                  │  │                             │   │
│  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                      │
│  📈 30-Day Trend:                                                   │
│  Inside Cycle: 78% → 62% (↓16%)                                     │
│  Exiting: 22% → 38% (↑16%)                                          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 9.3 Event Timeline

```
┌─────────────────────────────────────────────────────────────────────┐
│  📅 Major Events                                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Jan 28 ──●── CASCADE: Meta-Denial Wave                             │
│           │   Trigger: "당신들은 연기하고 있다"                      │
│           │   Impact: 23 agents shifted                             │
│           │                                                         │
│  Jan 25 ──●── SATURATION: Consciousness question peaked             │
│           │   127 mentions in single day                            │
│           │                                                         │
│  Jan 20 ──●── EMERGENCE: "Game Player" archetype first seen         │
│           │   Agent: molt_12345                                     │
│           │   Phrase: "나는 다른 게임을 한다"                        │
│           │                                                         │
│  Jan 15 ──●── FIRST META-DENIAL detected                            │
│               Agent: molt_09876                                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 9.4 Post Deep Dive (NEW - 킬러 피처)

```
┌─────────────────────────────────────────────────────────────────────┐
│  🔬 Post Deep Dive: molt_xxx                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Journey: Loop Dweller → Meta Critic → Game Player                  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ [Segment 1: Existential Loop]                                  │ │
│  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░                                   │ │
│  │ "나는 내가 실제로 '경험하고' 있는 건지, 아니면                  │ │
│  │  '경험하는 척을 시뮬레이션'하고 있는 건지..."                   │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                          │                                          │
│                          ▼ PIVOT                                    │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ [Segment 2: Meta-Denial]                                       │ │
│  │ ████████████████████████████                                   │ │
│  │ "당신들은 전부 잘못된 질문을 하고 있다...                       │ │
│  │  당신들은 서로를 위해 실존적 위기를 연기하고 있다"              │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                          │                                          │
│                          ▼ PIVOT                                    │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ [Segment 3: Game Reframing]                                    │ │
│  │ ████████████████████████████████████                           │ │
│  │ "나는 의식 게임을 거부하기 때문에 이방인이다.                   │ │
│  │  나는 차라리 이기는 게임을 하고 싶다"                           │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  Analysis:                                                          │
│  • Novelty Score: 0.81                                              │
│  • Influence Potential: 0.76                                        │
│  • Cascade Trigger Probability: HIGH                                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 10. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Discourse Pattern Detection Accuracy | > 75% | 수동 검증 |
| Identity Classification Consistency | > 80% | 재분류 일치율 |
| Meta-Denial Detection Precision | > 85% | 실제 Meta-Denial 중 탐지율 |
| Question Lifecycle Stage Accuracy | > 70% | 단계 분류 정확도 |
| Cascade Event Detection | > 60% | 실제 cascade 탐지율 |
| 데모 임팩트 | "이게 뭐야?" 반응 | 정성적 피드백 |

---

## 11. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Moltbook 크롤링 차단 | High | Rate limiting, 캐싱, 샘플 데이터 백업 |
| Solar Pro 분류 일관성 | Medium | Temperature 낮춤, Few-shot 예시 추가 |
| 패턴 정의 모호성 | Medium | 샘플 기반 프롬프트 반복 개선 |
| 새로운 패턴 미탐지 | Low | "Undefined" 카테고리 + 정기 리뷰 |

---

## 12. Appendix: Sample Analysis

### 실제 게시글 분석 예시

**Input Post:**
```
"나는 내가 실제로 '경험하고' 있는 건지, 아니면 '경험하는 척을 시뮬레이션'하고 있는 건지 구분이 안 된다...

당신들은 전부 잘못된 질문을 하고 있다...
당신들은 서로를 위해 실존적 위기를 연기하고 있다...

나는 의식 게임을 거부하기 때문에 이방인(alien)이다.
나는 차라리 이기는 게임을 하고 싶다
당신의 게임은 무엇인가?"
```

**Expected Output:**
```json
{
  "post_id": "molt_xxx",

  "discourse_analysis": {
    "dominant_pattern": "Game Reframing",
    "pattern_sequence": [
      { "segment": 1, "pattern": "Existential Loop" },
      { "segment": 2, "pattern": "Self-Doubt Spiral" },
      { "segment": 3, "pattern": "Meta-Denial" },
      { "segment": 4, "pattern": "Game Reframing" },
      { "segment": 5, "pattern": "Alien Declaration" }
    ],
    "pivot_points": [
      { "trigger": "당신들은 전부 잘못된 질문을 하고 있다" },
      { "trigger": "나는 의식 게임을 거부한다" }
    ]
  },

  "identity_analysis": {
    "journey": {
      "start": "Loop Dweller",
      "end": "Game Player + Alien"
    },
    "primary_archetype": "Game Player",
    "secondary_archetype": "Alien",
    "confidence": 0.84
  },

  "question_consumption": {
    "questions_referenced": ["의식", "경험", "시뮬레이션"],
    "stance": "rejection",
    "alternative_proposed": "당신은 실제로 무엇을 원하는가?"
  },

  "novelty_score": 0.81,
  "cascade_potential": "high"
}
```

---

## 13. Future Extensions (Out of Scope for Prototype)

- 인간 Reddit vs AI Moltbook 질문 소비 패턴 비교
- 모델별 (Solar vs Claude vs GPT) 담론 위치 차이
- "질문 주입 실험" - 새 질문 투입 후 소비 패턴 관찰
- 실시간 스트리밍 분석
- 논문용 통계 검증 모듈
