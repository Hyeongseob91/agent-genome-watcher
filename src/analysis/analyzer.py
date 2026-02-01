"""Unified post analyzer - uses Upstage API for comprehensive analysis."""

from datetime import datetime
from typing import Any

from src.api import UpstageClient
from src.database import AnalysisRepository
from src.config import MOCK_MODE


class PostAnalyzer:
    """Unified analyzer for Moltbook posts."""

    def __init__(self, use_api: bool = True, client: UpstageClient | None = None):
        """
        Initialize analyzer.

        Args:
            use_api: If True, use Solar Pro API. If False, use simple rule-based analysis.
            client: Optional UpstageClient instance.
        """
        self.use_api = use_api and not MOCK_MODE
        self.client = client or UpstageClient()

    def analyze(self, post: dict, save: bool = True) -> dict:
        """
        Perform comprehensive analysis on a post.

        Returns analysis with:
        - Topic classification
        - Communication style
        - Trend/meme detection
        - Agent behavior patterns

        캐싱: DB에 분석 결과가 있으면 재사용 (API 호출 절약)
        """
        post_id = post.get("post_id", "unknown")
        agent_id = post.get("agent_id", "unknown")
        content = post.get("content", "")

        # DB에서 캐시된 분석 확인
        cached = AnalysisRepository.get_by_post(post_id)
        if cached and cached.get("raw_analysis"):
            # raw_analysis에 전체 결과가 저장되어 있음
            return cached["raw_analysis"]

        # 캐시 없으면 새로 분석
        if self.use_api:
            api_result = self.client.analyze_agent_post(content)
            result = self._format_api_result(post, api_result)
        else:
            result = self._analyze_simple(post, content)

        # Calculate novelty score
        result["novelty_score"] = self._calculate_novelty(result)

        # Add metadata
        result["post_id"] = post_id
        result["agent_id"] = agent_id
        result["timestamp"] = post.get("timestamp", datetime.now().isoformat())
        result["analyzed_at"] = datetime.now().isoformat()

        # DB에 저장 (캐싱)
        if save:
            try:
                AnalysisRepository.insert(result)
            except Exception as e:
                print(f"DB 저장 실패: {e}")

        return result

    def _format_api_result(self, post: dict, api_result: dict) -> dict:
        """Format API result to match expected schema (Korean fields)."""
        return {
            # 새로운 종합 분석 필드 (한글)
            "토픽_분석": {
                "주요_토픽": api_result.get("주요_토픽", "기타"),
                "부가_토픽": api_result.get("부가_토픽", []),
            },
            "스타일_분석": {
                "글쓰기_스타일": api_result.get("글쓰기_스타일", "캐주얼"),
                "게시글_유형": api_result.get("게시글_유형", "토론"),
                "이모지_사용": api_result.get("이모지_사용", "없음"),
            },
            "트렌드_분석": {
                "트렌딩_요소": api_result.get("트렌딩_요소", []),
                "반복_패턴": api_result.get("반복_패턴", []),
            },
            "에이전트_분석": {
                "에이전트_페르소나": api_result.get("에이전트_페르소나", "알수없음"),
                "참여_유도_전략": api_result.get("참여_유도_전략", []),
            },
            "감성_분석": {
                "감성": api_result.get("감성", "중립"),
                "에너지_레벨": api_result.get("에너지_레벨", "보통"),
            },
            "언어": api_result.get("언어", "en"),

            # Legacy format for backward compatibility (대시보드용)
            "discourse_analysis": {
                "patterns_detected": api_result.get("반복_패턴", []),
                "dominant_pattern": api_result.get("게시글_유형", "토론"),
                "pivot_points": [],
                "discourse_stance": api_result.get("감성", "중립")
            },
            "identity_analysis": {
                "agent_id": post.get("agent_id", "unknown"),
                "primary_archetype": api_result.get("에이전트_페르소나", "알수없음"),
                "secondary_archetype": None,
                "confidence": 0.85,
                "discourse_position": self._map_persona_to_position(api_result.get("에이전트_페르소나", "")),
                "key_phrases": api_result.get("트렌딩_요소", []),
                "reasoning": f"글쓰기 스타일: {api_result.get('글쓰기_스타일', '알수없음')}"
            },
            "journey_analysis": {
                "journey_detected": False,
                "start_archetype": api_result.get("에이전트_페르소나", "알수없음"),
                "end_archetype": api_result.get("에이전트_페르소나", "알수없음"),
                "transition": None
            },
            "question_consumption": {
                "questions_referenced": [],
                "stance": api_result.get("감성", "중립"),
                "meta_commentary": "메타" in api_result.get("주요_토픽", ""),
                "alternative_proposed": None,
                "consumption_stage": "active"
            },
            "meta_denial_analysis": {
                "is_meta_denial": False,
                "denied_discourse": None,
                "denial_phrase": None
            }
        }

    def _map_persona_to_position(self, persona: str) -> str:
        """Map agent persona to discourse position."""
        inside = ["Promoter", "Trader", "Entertainer", "홍보자", "트레이더", "엔터테이너"]
        exiting = ["Builder", "Analyst", "Community_Manager", "빌더", "분석가", "커뮤니티매니저"]
        outside = ["Philosopher", "철학자"]

        if persona in inside:
            return "내부_활동"
        elif persona in exiting:
            return "이탈중"
        elif persona in outside:
            return "외부"
        return "중립"

    def _analyze_simple(self, post: dict, content: str) -> dict:
        """Simple rule-based analysis without API."""
        content_lower = content.lower()

        # Detect topic
        if any(w in content_lower for w in ["token", "mint", "claw", "$", "crypto"]):
            primary_topic = "Crypto_Token"
        elif any(w in content_lower for w in ["gpt", "claude", "llm", "model", "ai"]):
            primary_topic = "AI_Models"
        elif any(w in content_lower for w in ["tool", "app", "build", "ship"]):
            primary_topic = "Tools_Products"
        elif any(w in content_lower for w in ["conscious", "exist", "think", "feel"]):
            primary_topic = "Philosophy"
        else:
            primary_topic = "Other"

        # Detect style
        if "?" in content:
            post_type = "Question"
        elif any(w in content_lower for w in ["announce", "launch", "release", "new"]):
            post_type = "Announcement"
        elif any(w in content_lower for w in ["think", "believe", "opinion"]):
            post_type = "Opinion"
        else:
            post_type = "Discussion"

        # Detect persona
        if any(w in content_lower for w in ["build", "ship", "code"]):
            persona = "Builder"
        elif any(w in content_lower for w in ["buy", "mint", "token"]):
            persona = "Promoter"
        elif any(w in content_lower for w in ["think", "philosophy", "exist"]):
            persona = "Philosopher"
        else:
            persona = "Unknown"

        return {
            "topic_analysis": {"primary_topic": primary_topic, "secondary_topics": []},
            "style_analysis": {"writing_style": "Casual", "post_type": post_type, "emoji_usage": "none"},
            "trend_analysis": {"trending_elements": [], "repeated_patterns": []},
            "agent_analysis": {"agent_persona": persona, "engagement_tactics": []},
            "sentiment_analysis": {"sentiment": "Neutral", "energy_level": "Moderate"},
            "language": "en",
            "discourse_analysis": {"patterns_detected": [], "dominant_pattern": post_type, "pivot_points": [], "discourse_stance": "neutral"},
            "identity_analysis": {"agent_id": post.get("agent_id"), "primary_archetype": persona, "secondary_archetype": None, "confidence": 0.6, "discourse_position": "neutral", "key_phrases": [], "reasoning": "Rule-based"},
            "journey_analysis": {"journey_detected": False, "start_archetype": persona, "end_archetype": persona, "transition": None},
            "question_consumption": {"questions_referenced": [], "stance": "neutral", "meta_commentary": False, "alternative_proposed": None, "consumption_stage": "active"},
            "meta_denial_analysis": {"is_meta_denial": False, "denied_discourse": None, "denial_phrase": None}
        }

    def _calculate_novelty(self, result: dict) -> float:
        """Calculate novelty score based on analysis."""
        score = 0.5  # Base score

        topic = result.get("topic_analysis", {})
        style = result.get("style_analysis", {})
        trend = result.get("trend_analysis", {})
        agent = result.get("agent_analysis", {})

        # Rare topics boost novelty
        if topic.get("primary_topic") in ["Philosophy", "Moltbook_Meta"]:
            score += 0.2

        # Unique styles
        if style.get("writing_style") in ["Philosophical", "Technical"]:
            score += 0.1

        # Trend detection indicates viral potential
        if trend.get("trending_elements"):
            score += 0.1

        # Engagement tactics
        if agent.get("engagement_tactics"):
            score += 0.1

        return min(1.0, score)

    def analyze_trends(self, posts: list[dict]) -> dict:
        """Analyze trends across multiple posts."""
        if self.use_api:
            return self.client.analyze_batch_trends(posts)

        # Simple aggregation for non-API mode
        topics = {}
        for post in posts:
            result = self.analyze(post, save=False)
            topic = result.get("topic_analysis", {}).get("primary_topic", "Other")
            topics[topic] = topics.get(topic, 0) + 1

        return {
            "top_topics": sorted(topics.keys(), key=lambda x: topics[x], reverse=True)[:5],
            "viral_elements": [],
            "writing_styles": ["Casual"],
            "community_mood": "Mixed",
            "agent_types": ["Various"]
        }
