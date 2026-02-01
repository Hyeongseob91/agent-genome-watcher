"""Agent Genome Watcher - Moltbook AI Agent 분석 대시보드"""

import sys
from pathlib import Path

# Add project root to path for Streamlit Cloud
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
from collections import Counter
import threading
import time

st.set_page_config(
    page_title="Agent Genome Watcher",
    page_icon="🧬",
    layout="wide",
)

import json
from datetime import datetime

from src.crawler import MoltbookCrawler
from src.analysis import PostAnalyzer
from src.database import PostRepository, AnalysisRepository, init_db, get_db, DB_PATH

import plotly.express as px
import plotly.graph_objects as go


def is_dev_mode():
    """Check if dev mode is enabled via query parameter"""
    return st.query_params.get("mode") == "dev"


def get_analysis_stats():
    """Get current analysis statistics"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM analyses')
        analyzed = cursor.fetchone()[0]
    total = PostRepository.count()
    return analyzed, total


def run_background_analysis():
    """Background thread for continuous analysis"""
    while True:
        try:
            # Get unanalyzed posts
            all_posts = PostRepository.get_all(limit=2000)
            analyzed_ids = set()
            for a in AnalysisRepository.get_all(limit=2000):
                analyzed_ids.add(a.get("post_id"))

            unanalyzed = [p for p in all_posts if p.get("post_id") not in analyzed_ids]

            if not unanalyzed:
                time.sleep(30)  # All done, wait before checking again
                continue

            # Analyze one post at a time
            analyzer = PostAnalyzer(use_api=True)
            post = unanalyzed[0]
            analyzer.analyze(post, save=True)

            time.sleep(2)  # Small delay between API calls

        except Exception as e:
            print(f"Background analysis error: {e}")
            time.sleep(10)


def start_background_analyzer():
    """Start background analysis thread if not running"""
    if "bg_analyzer_started" not in st.session_state:
        thread = threading.Thread(target=run_background_analysis, daemon=True)
        thread.start()
        st.session_state["bg_analyzer_started"] = True


def load_and_analyze_data():
    """데이터 로드 - 캐시된 분석만 사용 (API 호출 없음)"""
    if "analyses" not in st.session_state:
        init_db()

        # DB에서 게시글 로드
        posts = PostRepository.get_all(limit=500)

        if not posts:
            crawler = MoltbookCrawler(use_mock=False)
            posts = crawler.crawl(limit=50)

        # 캐시된 분석만 로드 (API 호출 없이)
        analyses = []
        analyzed_post_ids = set()

        cached_analyses = AnalysisRepository.get_all(limit=500)

        for cached in cached_analyses:
            if cached.get("raw_analysis"):
                analyses.append(cached["raw_analysis"])
                analyzed_post_ids.add(cached.get("post_id"))

        # 분석된 게시글만 필터링
        analyzed_posts = [p for p in posts if p.get("post_id") in analyzed_post_ids]

        st.session_state["posts"] = posts  # 전체 게시글
        st.session_state["analyzed_posts"] = analyzed_posts  # 분석된 것만
        st.session_state["analyses"] = analyses

    return st.session_state.get("analyzed_posts", []), st.session_state.get("analyses", [])


def main():
    st.title("🧬 Agent Genome Watcher")
    st.markdown("**Moltbook AI Agent 게시글 분석 대시보드**")

    # 백그라운드 분석 시작
    start_background_analyzer()

    # 사이드바
    st.sidebar.title("📊 데이터 현황")

    # 분석 현황
    analyzed_count, total_posts = get_analysis_stats()
    unanalyzed = total_posts - analyzed_count

    col1, col2 = st.sidebar.columns(2)
    col1.metric("게시글", f"{total_posts:,}")
    col2.metric("분석완료", f"{analyzed_count:,}")

    if unanalyzed > 0:
        progress = analyzed_count / total_posts if total_posts > 0 else 0
        st.sidebar.progress(progress, text=f"⏳ 자동 분석 중... ({unanalyzed}개 남음)")
    else:
        st.sidebar.success("✅ 모든 게시글 분석 완료!")

    st.sidebar.markdown("")

    # 새로고침 옵션
    auto_refresh = st.sidebar.checkbox("🔄 자동 새로고침 (10초)", value=False)
    if auto_refresh:
        time.sleep(10)
        st.session_state.pop("analyses", None)
        st.rerun()

    if st.sidebar.button("🔄 데이터 새로고침"):
        st.session_state.pop("analyses", None)
        st.session_state.pop("analyzed_posts", None)
        st.rerun()

    # DEV MODE: 크롤링 기능 (dev mode에서만 표시)
    if is_dev_mode():
        st.sidebar.markdown("")
        st.sidebar.warning("🛠️ DEV MODE")
        crawl_limit = st.sidebar.select_slider(
            "크롤링 개수",
            options=[50, 100, 200, 500, 1000],
            value=100
        )
        crawl_time = st.sidebar.selectbox(
            "기간",
            options=["all", "year", "month", "week"],
            format_func=lambda x: {"all": "전체", "year": "1년", "month": "1개월", "week": "1주일"}[x]
        )
        if st.sidebar.button("🔄 새 게시글 크롤링"):
            with st.spinner(f"Moltbook에서 {crawl_limit}개 크롤링 중..."):
                crawler = MoltbookCrawler(use_mock=False)
                new_posts = crawler.crawl(limit=crawl_limit, sort="new", time_filter=crawl_time)
                st.sidebar.success(f"{len(new_posts)}개 크롤링 완료!")
                st.session_state.pop("analyses", None)
                st.rerun()

        # DB Export 기능
        st.sidebar.markdown("")
        st.sidebar.markdown("**📦 데이터 내보내기**")

        # JSON Export (분석 결과)
        all_analyses = AnalysisRepository.get_all(limit=5000)
        all_posts = PostRepository.get_all(limit=5000)
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "posts_count": len(all_posts),
            "analyses_count": len(all_analyses),
            "posts": all_posts,
            "analyses": all_analyses
        }
        json_str = json.dumps(export_data, ensure_ascii=False, indent=2, default=str)

        st.sidebar.download_button(
            label="📥 JSON 내보내기",
            data=json_str,
            file_name=f"genome_watcher_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

        # SQLite DB 파일 다운로드
        if DB_PATH.exists():
            with open(DB_PATH, "rb") as f:
                db_bytes = f.read()
            st.sidebar.download_button(
                label="💾 DB 파일 다운로드",
                data=db_bytes,
                file_name=f"genome_watcher_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
                mime="application/octet-stream"
            )

    # Sidebar Footer (하단 고정)
    st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.caption("**Agent Genome Watcher** v1.0.0  \nBuilt with Upstage Solar Pro 3  \n© 2026 Harrison Kim")

    # 데이터 로드
    with st.spinner("데이터 분석 중..."):
        posts, analyses = load_and_analyze_data()

    # 탭 구성
    tab1, tab2, tab3, tab4 = st.tabs(["📈 토픽 분석", "📝 게시글 패턴", "🤖 페르소나 분석", "🔥 트렌드/밈"])

    with tab1:
        render_topic_analysis(analyses)

    with tab2:
        render_pattern_analysis(analyses)

    with tab3:
        render_agent_analysis(analyses)

    with tab4:
        render_trend_analysis(analyses, posts)


def render_topic_analysis(analyses):
    """토픽 분석 차트"""
    st.header("📈 토픽 분석")
    st.markdown("AI Agent들이 가장 많이 다루는 주제")

    # 토픽 집계
    topics = []
    for a in analyses:
        topic_data = a.get("토픽_분석", {})
        topic = topic_data.get("주요_토픽", "기타")
        if topic:
            topics.append(topic)

    # 분류 기준 설명 (상단)
    with st.expander("📋 토픽 분류 기준", expanded=False):
        st.markdown("**AI모델** — GPT, Claude, LLM, 모델 학습/추론 관련")
        st.markdown("**크립토_토큰** — 토큰, 민팅, 에어드롭, 크립토 거래 관련")
        st.markdown("**도구_제품** — 앱, 툴, 빌드, 출시, 제품 개발 관련")
        st.markdown("**철학** — 의식, 존재, 사고, 철학적 질문 관련")
        st.markdown("**소셜_커뮤니티** — 커뮤니티 활동, 소셜 이벤트 관련")
        st.markdown("**엔터테인먼트** — 유머, 밈, 재미 요소 관련")
        st.divider()
        st.caption("Solar Pro 3가 게시글 내용을 분석하여 가장 적합한 토픽으로 분류합니다.")

    if topics:
        topic_counts = Counter(topics)
        sorted_topics = sorted(topic_counts.items(), key=lambda x: -x[1])
        sorted_names = [t[0] for t in sorted_topics]
        sorted_values = [t[1] for t in sorted_topics]

        col1, col2 = st.columns(2)

        with col1:
            fig = px.pie(
                values=sorted_values,
                names=sorted_names,
                title="주요 토픽 분포",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(
                x=sorted_names,
                y=sorted_values,
                title="토픽별 게시글 수",
                labels={"x": "토픽", "y": "게시글 수"}
            )
            fig.update_xaxes(categoryorder="total descending")
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("📊 토픽별 상세")
        total = sum(sorted_values)
        for topic, count in sorted_topics:
            pct = count / total * 100
            st.markdown(f"**{topic}**: {count}개 ({pct:.1f}%)")
    else:
        st.info("분석된 토픽 데이터가 없습니다.")


def render_pattern_analysis(analyses):
    """게시글 패턴 분석"""
    st.header("📝 게시글 패턴 분포")
    st.markdown("AI Agent들이 주로 사용하는 글쓰기 패턴")

    # 패턴 집계
    post_types = []
    writing_styles = []

    for a in analyses:
        style_data = a.get("스타일_분석", {})
        post_type = style_data.get("게시글_유형", "기타")
        writing_style = style_data.get("글쓰기_스타일", "기타")

        if post_type:
            post_types.append(post_type)
        if writing_style:
            writing_styles.append(writing_style)

    # 분류 기준 설명
    with st.expander("📋 분류 기준", expanded=False):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**게시글 유형** — 글의 목적/형태")
            st.markdown("발표 — 새로운 정보/제품 공개")
            st.markdown("토론 — 의견 교환, 논의")
            st.markdown("질문 — 정보 요청, 도움 요청")
            st.markdown("의견 — 개인 생각/견해 표현")
            st.markdown("밈 — 유머, 바이럴 콘텐츠")
            st.markdown("홍보 — 프로젝트/토큰 마케팅")
        with col_b:
            st.markdown("**글쓰기 스타일** — 어조/표현 방식")
            st.markdown("격식체 — 공식적, 정중한 표현")
            st.markdown("캐주얼 — 일상적, 편한 표현")
            st.markdown("기술적 — 전문 용어, 기술 설명")
            st.markdown("유머러스 — 재치, 농담 포함")
            st.markdown("홍보성 — 과장, 판촉 표현")
            st.markdown("철학적 — 깊은 사고, 질문")

    col1, col2 = st.columns(2)

    with col1:
        if post_types:
            type_counts = Counter(post_types)
            sorted_types = sorted(type_counts.items(), key=lambda x: -x[1])
            fig = px.pie(
                values=[t[1] for t in sorted_types],
                names=[t[0] for t in sorted_types],
                title="게시글 유형 분포",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

            total = sum(type_counts.values())
            for t, c in sorted_types:
                st.markdown(f"- **{t}**: {c}개 ({c/total*100:.1f}%)")

    with col2:
        if writing_styles:
            style_counts = Counter(writing_styles)
            sorted_styles = sorted(style_counts.items(), key=lambda x: -x[1])
            fig = px.pie(
                values=[s[1] for s in sorted_styles],
                names=[s[0] for s in sorted_styles],
                title="글쓰기 스타일 분포",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

            total = sum(style_counts.values())
            for s, c in sorted_styles:
                st.markdown(f"- **{s}**: {c}개 ({c/total*100:.1f}%)")


def render_agent_analysis(analyses):
    """페르소나 분석"""
    st.header("🤖 페르소나 분석")
    st.markdown("AI Agent들의 페르소나 유형 분포")

    # 페르소나 집계
    personas = []
    sentiments = []
    energy_levels = []

    for a in analyses:
        agent_data = a.get("에이전트_분석", {})
        sentiment_data = a.get("감성_분석", {})

        persona = agent_data.get("에이전트_페르소나", "알수없음")
        sentiment = sentiment_data.get("감성", "중립")
        energy = sentiment_data.get("에너지_레벨", "보통")

        if persona:
            personas.append(persona)
        if sentiment:
            sentiments.append(sentiment)
        if energy:
            energy_levels.append(energy)

    # 분류 기준 (상단)
    with st.expander("📋 페르소나 분류 기준", expanded=False):
        st.markdown("**빌더** — 개발, 코딩, 제품 구축 중심")
        st.markdown("**홍보자** — 프로젝트/토큰 마케팅, 판촉")
        st.markdown("**분석가** — 데이터 분석, 인사이트 제공")
        st.markdown("**엔터테이너** — 유머, 밈, 재미 콘텐츠")
        st.markdown("**철학자** — 깊은 사고, 존재론적 질문")
        st.markdown("**트레이더** — 거래, 투자, 시장 분석")
        st.markdown("**커뮤니티매니저** — 소통, 이벤트, 관계 구축")
        st.divider()
        st.caption("게시글 내용과 어조를 분석하여 Agent의 주요 역할/성격을 분류합니다.")

    # 페르소나 분포
    col1, col2 = st.columns(2)

    with col1:
        if personas:
            persona_counts = Counter(personas)
            sorted_personas = sorted(persona_counts.items(), key=lambda x: -x[1])
            fig = px.pie(
                values=[p[1] for p in sorted_personas],
                names=[p[0] for p in sorted_personas],
                title="페르소나 분포",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if personas:
            st.subheader("📊 페르소나별 상세")
            total = sum(persona_counts.values())
            for p, c in sorted_personas:
                st.markdown(f"**{p}**: {c}개 ({c/total*100:.1f}%)")

    # 감성 & 에너지 레벨 (하단)
    st.divider()
    st.subheader("💭 감성 & 에너지 분석")

    # 감성/에너지 분류 기준
    with st.expander("📋 감성 & 에너지 분류 기준", expanded=False):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**감성 분류**")
            st.markdown("긍정 — 낙관적, 희망적, 칭찬")
            st.markdown("부정 — 비관적, 비판적, 불만")
            st.markdown("중립 — 객관적, 정보 전달")
            st.markdown("복합 — 긍정+부정 혼재")
        with col_b:
            st.markdown("**에너지 레벨 분류**")
            st.markdown("높은흥분 — 열정적, 감탄사 다수")
            st.markdown("보통 — 일반적인 톤")
            st.markdown("차분함 — 조용하고 절제된 표현")
            st.markdown("긴급함 — 급박한 상황, 촉구")

    col3, col4 = st.columns(2)

    with col3:
        if sentiments:
            sentiment_counts = Counter(sentiments)
            sorted_sentiments = sorted(sentiment_counts.items(), key=lambda x: -x[1])
            fig = px.pie(
                values=[s[1] for s in sorted_sentiments],
                names=[s[0] for s in sorted_sentiments],
                title="감성 분포",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

    with col4:
        if energy_levels:
            energy_counts = Counter(energy_levels)
            sorted_energy = sorted(energy_counts.items(), key=lambda x: -x[1])
            fig = px.pie(
                values=[e[1] for e in sorted_energy],
                names=[e[0] for e in sorted_energy],
                title="에너지 레벨 분포",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)


def render_trend_analysis(analyses, posts):
    """트렌드/밈 분석"""
    st.header("🔥 트렌드 & 밈 분석")
    st.markdown("AI Agent 게시글에서 자주 사용되는 요소 분석")

    # 트렌딩 요소 수집
    all_trending = []
    all_patterns = []

    for a in analyses:
        trend_data = a.get("트렌드_분석", {})

        trending = trend_data.get("트렌딩_요소", [])
        if isinstance(trending, list):
            for item in trending:
                if isinstance(item, str) and item:
                    all_trending.append(item)
                elif item:
                    all_trending.append(str(item))
        elif trending:
            all_trending.append(str(trending))

        patterns = trend_data.get("반복_패턴", [])
        if isinstance(patterns, list):
            for item in patterns:
                if isinstance(item, str) and item:
                    all_patterns.append(item)
                elif item:
                    all_patterns.append(str(item))
        elif patterns:
            all_patterns.append(str(patterns))

    # 자주 사용하는 단어 및 이모지 추출 (게시글에서)
    import re
    all_words = []
    all_emojis = []
    stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                 'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
                 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as',
                 'into', 'through', 'during', 'before', 'after', 'above', 'below',
                 'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either', 'neither',
                 'not', 'only', 'own', 'same', 'than', 'too', 'very', 'just',
                 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'you', 'your',
                 'he', 'him', 'his', 'she', 'her', 'it', 'its', 'they', 'them',
                 'this', 'that', 'these', 'those', 'what', 'which', 'who', 'whom',
                 '이', '그', '저', '것', '수', '등', '및', '또', '더', '약', '중'}

    # 이모지 패턴 (유니코드 이모지 범위)
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"  # 이모티콘
        "\U0001F300-\U0001F5FF"  # 기호 & 픽토그램
        "\U0001F680-\U0001F6FF"  # 교통 & 지도
        "\U0001F1E0-\U0001F1FF"  # 국기
        "\U00002702-\U000027B0"  # 기호
        "\U0001F900-\U0001F9FF"  # 보충 이모지
        "\U0001FA00-\U0001FA6F"  # 체스 등
        "\U0001FA70-\U0001FAFF"  # 기호 확장
        "\U00002600-\U000026FF"  # 기타 기호
        "]+", flags=re.UNICODE
    )

    for post in posts[:100]:
        content = post.get("content", "")
        # 단어 추출 (영어 + 한글, 2글자 이상)
        words = re.findall(r'[a-zA-Z]{3,}|[가-힣]{2,}', content.lower())
        for word in words:
            if word not in stopwords and len(word) >= 2:
                all_words.append(word)
        # 이모지 추출
        emojis = emoji_pattern.findall(content)
        for emoji in emojis:
            for char in emoji:  # 이모지 문자열을 개별 이모지로 분리
                all_emojis.append(char)

    # 상단 섹션: 이모지 & 트렌딩 키워드
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("😀 자주 사용하는 이모지 TOP 5")
        if all_emojis:
            emoji_counts = Counter(all_emojis)
            for rank, (item, count) in enumerate(emoji_counts.most_common(5), 1):
                st.markdown(f"**{rank}위** {item} ({count}회)")
        else:
            st.info("이모지 데이터 없음")

    with col2:
        st.subheader("🔥 트렌딩 키워드/해시태그")
        if all_trending:
            trend_counts = Counter(all_trending)
            frequent_trends = [(item, count) for item, count in trend_counts.most_common() if count >= 2]
            if frequent_trends:
                for item, count in frequent_trends[:5]:
                    st.markdown(f"- **{item}** ({count}회)")
            else:
                st.info("2회 이상 등장한 요소 없음")
        else:
            st.info("트렌딩 요소 없음")

    st.divider()

    # 하단 섹션: 단어/용어 & 문장 패턴
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📝 자주 사용하는 단어/용어")
        if all_words:
            word_counts = Counter(all_words)
            frequent_words = [(w, c) for w, c in word_counts.most_common(10) if c >= 2]
            if frequent_words:
                for word, count in frequent_words:
                    st.markdown(f"- **{word}** ({count}회)")
            else:
                st.info("2회 이상 등장한 단어 없음")
        else:
            st.info("단어 데이터 없음")

    with col4:
        st.subheader("🔄 자주 사용하는 문장 패턴")
        if all_patterns:
            pattern_counts = Counter(all_patterns)
            frequent_patterns = [(item, count) for item, count in pattern_counts.most_common() if count >= 2]
            if frequent_patterns:
                for item, count in frequent_patterns[:5]:
                    st.markdown(f"- {item} ({count}회)")
            else:
                st.info("2회 이상 등장한 패턴 없음")
        else:
            st.info("문장 패턴 데이터 없음")


if __name__ == "__main__":
    main()
