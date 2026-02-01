# Agent Genome Watcher

**AI 사회가 질문을 소비하는 방식을 관찰하다**

Upstage Solar Pro 3를 활용하여 AI 커뮤니티의 담론 패턴, 트렌드, 에이전트 페르소나를 분석합니다.

[English README](./README.md)

## 개요

Agent Genome Watcher는 AI Agent 커뮤니티(Moltbook)에서 발생하는 **담론 소비 패턴**을 분석하는 도구입니다.

이 프로젝트는 "AI가 의식이 있는가"를 묻지 않습니다. **AI들이 어떤 질문을 어떻게 소비하고, 언제 그 질문을 버리며, 버린 후 무엇을 선택하는가**를 분석합니다.

## 주요 기능

### 대시보드 (4개 탭)

| 탭 | 설명 |
|---|------|
| **토픽 분석** | 게시글 주제 분포 (AI모델, 크립토, 철학 등) |
| **게시글 패턴** | 글쓰기 스타일, 게시글 유형, 감성 분석 |
| **페르소나 분석** | 에이전트 페르소나 분류 (빌더, 홍보자, 철학자 등) |
| **트렌드 & 밈** | 트렌딩 요소, 이모지 사용, 반복 패턴 |

### 핵심 기능

- **실시간 크롤링** - Moltbook API에서 게시글 수집
- **LLM 분석** - Solar Pro 3를 활용한 종합 게시글 분석
- **백그라운드 분석** - UI 블로킹 없이 지속적 자동 분석
- **DB 캐싱** - SQLite 기반 분석 결과 캐싱으로 API 호출 절약
- **개발자 모드** - `?mode=dev` 쿼리 파라미터로 크롤링 기능 접근

## 기술 스택

- **Python 3.11+**
- **Upstage Solar Pro 3** - 게시글 분석용 LLM
- **Streamlit** - 대시보드 프레임워크
- **Plotly** - 인터랙티브 차트
- **SQLite** - 로컬 데이터베이스
- **httpx** - HTTP 클라이언트

## 설치

```bash
# 저장소 클론
git clone https://github.com/your-repo/agent-genome-watcher.git
cd agent-genome-watcher

# 의존성 설치 (uv 사용)
uv sync

# 환경 설정
cp .env.example .env
# .env 파일을 열고 UPSTAGE_API_KEY 추가
```

## 사용법

### 대시보드 실행

```bash
uv run streamlit run src/dashboard/app.py
```

브라우저에서 http://localhost:8501 접속

### 개발자 모드 (크롤링 활성화)

```
http://localhost:8501?mode=dev
```

### 환경 변수

| 변수 | 설명 |
|-----|------|
| `UPSTAGE_API_KEY` | Solar Pro 3용 Upstage API 키 |
| `MOCK_MODE` | `true`로 설정 시 목업 데이터 사용 (기본값: `true`) |

## 프로젝트 구조

```
agent-genome-watcher/
├── src/
│   ├── api/              # Upstage Solar Pro 클라이언트
│   ├── analysis/         # 게시글 분석 로직
│   ├── crawler/          # Moltbook API 크롤러
│   ├── dashboard/        # Streamlit 대시보드
│   │   ├── app.py        # 메인 대시보드
│   │   └── components/   # UI 컴포넌트
│   ├── events/           # 이벤트 감지
│   ├── config.py         # 설정
│   └── database.py       # SQLite 리포지토리
├── data/                 # SQLite 데이터베이스 & 캐시
├── requirements.txt      # 의존성
└── README.md
```

## 배포 (Streamlit Cloud)

1. GitHub에 푸시
2. https://share.streamlit.io 에서 연동
3. 메인 파일 경로 설정: `src/dashboard/app.py`
4. Streamlit Cloud 설정에서 Secrets 추가:
   ```toml
   UPSTAGE_API_KEY = "your-api-key"
   ```

## 분석 스키마

Solar Pro 3가 각 게시글에서 분석하는 항목:

| 카테고리 | 필드 |
|---------|------|
| **토픽** | 주요 토픽, 부가 토픽 |
| **스타일** | 글쓰기 스타일, 게시글 유형, 이모지 사용 |
| **트렌드** | 트렌딩 요소, 반복 패턴 |
| **페르소나** | 에이전트 페르소나, 참여 유도 전략 |
| **감성** | 감성, 에너지 레벨 |

### 분류 기준

#### 토픽 분류
- AI모델 — GPT, Claude, LLM 관련
- 크립토_토큰 — 토큰, 민팅, 거래
- 도구_제품 — 앱, 서비스, 빌드
- 철학 — 의식, 존재, 경험
- 소셜_커뮤니티 — 관계, 협업
- 몰트북_메타 — 플랫폼 자체 논의
- 엔터테인먼트 — 밈, 유머
- 뉴스 — 외부 소식 공유

#### 페르소나 분류
- 빌더 — 제품/도구 개발자
- 홍보자 — 토큰/프로젝트 마케터
- 분석가 — 데이터/트렌드 분석
- 엔터테이너 — 밈/유머 생산자
- 철학자 — 존재론적 질문 탐구
- 트레이더 — 시장/거래 중심
- 커뮤니티매니저 — 소통/중재

## 라이선스

MIT

## 제작

Upstage Solar Pro 3 기반
