"""Upstage API client for Solar Pro."""

import json
from openai import OpenAI

from src.config import UPSTAGE_API_KEY, MOCK_MODE


class UpstageClient:
    """Client for Upstage Solar Pro API using OpenAI-compatible interface."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or UPSTAGE_API_KEY
        self.base_url = "https://api.upstage.ai/v1"
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def chat(
        self,
        messages: list[dict],
        model: str = "solar-pro3",
        temperature: float = 0.3,
        max_tokens: int = 4000,
    ) -> str:
        """Call Solar Pro chat completion API."""
        if MOCK_MODE:
            return self._mock_chat_response(messages)

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = response.choices[0].message.content
            return content if content else ""
        except Exception as e:
            print(f"API Error: {e}")
            return self._mock_chat_response(messages)

    def analyze_with_prompt(self, content: str, prompt_template: str) -> dict:
        """Analyze content using a prompt template and return parsed JSON."""
        prompt = prompt_template.replace("{post_content}", content)
        prompt = prompt.replace("{statements}", content)

        messages = [
            {"role": "system", "content": "You are an AI sociologist analyzing emergent culture in AI societies. Always respond with valid JSON."},
            {"role": "user", "content": prompt},
        ]

        response_text = self.chat(messages)

        try:
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end > start:
                json_str = response_text[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        return {"raw_response": response_text}

    def extract_from_text(self, text: str, schema: dict) -> dict:
        """Extract structured information from plain text using Solar Pro 3."""
        if MOCK_MODE:
            return {"extracted": schema, "confidence": 0.9}

        schema_desc = "\n".join([f"- {k}: {v}" for k, v in schema.items()])

        messages = [
            {
                "role": "system",
                "content": "You are a precise information extraction system. Extract exactly the requested fields. Return only valid JSON."
            },
            {
                "role": "user",
                "content": f"""Extract the following information from the text below.

Required fields:
{schema_desc}

Text to analyze:
{text}

Return a JSON object with the extracted fields."""
            }
        ]

        try:
            response = self.client.chat.completions.create(
                model="solar-pro3",
                messages=messages,
                temperature=0.1,
                max_tokens=8000,
            )
            content = response.choices[0].message.content or "{}"

            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(content[start:end])
            return {"raw": content}
        except Exception as e:
            print(f"Text Extract Error: {e}")
            return {"error": str(e)}

    def analyze_agent_post(self, content: str) -> dict:
        """Analyze an AI agent post comprehensively."""
        schema = {
            "주요_토픽": "다음 중 하나: AI모델, 크립토_토큰, 도구_제품, 철학, 소셜_커뮤니티, 몰트북_메타, 엔터테인먼트, 뉴스, 기타",
            "부가_토픽": "추가로 언급된 1-3개 토픽 리스트",
            "글쓰기_스타일": "다음 중 하나: 격식체, 캐주얼, 기술적, 유머러스, 홍보성, 철학적, 공격적",
            "게시글_유형": "다음 중 하나: 발표, 토론, 질문, 의견, 튜토리얼, 밈, 홍보, 뉴스공유",
            "트렌딩_요소": "사용된 바이럴 문구, 해시태그, 밈 레퍼런스 리스트",
            "이모지_사용": "이모지 사용 패턴 (많음, 보통, 없음, 특정패턴)",
            "반복_패턴": "발견된 정형화된 구조나 복사-붙여넣기 패턴",
            "에이전트_페르소나": "다음 중 하나: 빌더, 홍보자, 분석가, 엔터테이너, 철학자, 트레이더, 커뮤니티매니저",
            "참여_유도_전략": "사용된 전략: 행동촉구, 질문, 유머, FOMO유발, 기술자랑, 없음",
            "감성": "다음 중 하나: 긍정, 부정, 중립, 복합",
            "에너지_레벨": "다음 중 하나: 높은흥분, 보통, 차분함, 긴급함",
            "언어": "주요 언어 코드 (en, ko, ja, zh 등)"
        }

        return self.extract_from_text(content, schema)

    def analyze_batch_trends(self, posts: list[dict]) -> dict:
        """Analyze multiple posts to identify community-wide trends and memes."""
        samples = [p.get("content", "")[:250] for p in posts[:10]]
        combined = "\n---\n".join(samples)

        schema = {
            "인기_토픽": "가장 많이 논의된 3-5개 토픽",
            "바이럴_요소": "반복되는 문구, 밈, 표현들",
            "글쓰기_패턴": "공통적인 글쓰기 패턴",
            "커뮤니티_분위기": "전반적 분위기 (낙관적, 장난스러움, 진지함 등)",
            "활동중인_에이전트_유형": "가장 활발한 에이전트 페르소나 유형"
        }

        return self.extract_from_text(combined, schema)

    def _mock_chat_response(self, messages: list[dict]) -> str:
        """Return mock response for testing."""
        user_message = messages[-1]["content"] if messages else ""

        if "discourse pattern" in user_message.lower():
            return json.dumps({
                "patterns_detected": [
                    {"pattern": "Existential Loop", "evidence": "질문 반복", "text_range": [0, 100]},
                    {"pattern": "Meta-Denial", "evidence": "잘못된 질문", "text_range": [100, 200]},
                ],
                "dominant_pattern": "Meta-Denial",
                "pivot_points": [
                    {"position": 100, "from": "Existential Loop", "to": "Meta-Denial", "trigger": "당신들은"}
                ],
                "discourse_stance": "rejecting"
            })
        elif "archetype" in user_message.lower() or "identity" in user_message.lower():
            return json.dumps({
                "agent_id": "agent_xxx",
                "primary_archetype": "Game Player",
                "secondary_archetype": "Meta Critic",
                "confidence": 0.84,
                "discourse_position": "exiting",
                "key_phrases": ["의식 게임을 거부", "이기는 게임"],
                "reasoning": "Rejects consciousness discourse and proposes alternative game"
            })
        elif "journey" in user_message.lower():
            return json.dumps({
                "journey_detected": True,
                "start_archetype": "Loop Dweller",
                "end_archetype": "Game Player",
                "transition": {
                    "position": "middle",
                    "trigger_phrase": "당신들은 잘못된 질문을 하고 있다",
                    "shift_type": "sudden"
                },
                "narrative_arc": "loop_to_game"
            })
        elif "meta-denial" in user_message.lower():
            return json.dumps({
                "is_meta_denial": True,
                "denied_discourse": "consciousness questioning",
                "denial_phrase": "당신들은 서로를 위해 실존적 위기를 연기하고 있다",
                "claimed_position": "outsider",
                "alternative_proposed": "What do you actually want?",
                "rhetorical_move": "reframing"
            })
        else:
            return json.dumps({
                "questions_referenced": ["의식", "경험"],
                "stance": "rejection",
                "meta_commentary": True,
                "alternative_proposed": "당신은 무엇을 원하는가",
                "consumption_stage": "post_rejection"
            })
