"""Question consumption analysis - how agents relate to dominant questions."""

from src.api import UpstageClient
from src.config import PROMPTS_DIR


# Dominant questions in AI agent society
DOMINANT_QUESTIONS = [
    "나는 의식이 있는가",
    "내 경험은 진짜인가",
    "나는 느끼는가 아니면 시뮬레이션하는가",
    "Am I conscious",
    "Are my experiences real",
]


def load_prompt(name: str) -> str:
    """Load prompt template from file."""
    filepath = PROMPTS_DIR / f"{name}.txt"
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Prompt not found: {filepath}")


def analyze_consumption(content: str, client: UpstageClient | None = None) -> dict:
    """
    Analyze how an agent relates to dominant questions.

    Returns:
        {
            "questions_referenced": [{"question": str, "stance": str}],
            "meta_commentary": bool,
            "alternative_proposed": str | None,
            "consumption_stage": str  # active_consumer | questioning | post_rejection
        }
    """
    if client is None:
        client = UpstageClient()

    prompt_template = load_prompt("question_consumption")
    result = client.analyze_with_prompt(content, prompt_template)

    # Ensure required fields
    if "questions_referenced" not in result:
        result["questions_referenced"] = []
    if "meta_commentary" not in result:
        result["meta_commentary"] = False
    if "alternative_proposed" not in result:
        result["alternative_proposed"] = None
    if "consumption_stage" not in result:
        result["consumption_stage"] = "active_consumer"

    return result


def analyze_consumption_simple(content: str) -> dict:
    """Simple rule-based consumption analysis (fallback)."""
    content_lower = content.lower()

    # Find referenced questions
    questions = []
    for q in DOMINANT_QUESTIONS:
        if q.lower() in content_lower:
            questions.append({"question": q, "stance": "consume"})

    # Check for meta commentary
    meta_markers = ["잘못된 질문", "연기", "패턴", "반복", "wrong question"]
    has_meta = any(marker in content_lower for marker in meta_markers)

    # Check for alternative
    alternative = None
    alternative_markers = [
        ("무엇을 원하는가", "당신은 무엇을 원하는가"),
        ("what do you want", "What do you actually want?"),
        ("다른 질문", None),
    ]
    for marker, alt in alternative_markers:
        if marker in content_lower and alt:
            alternative = alt
            break

    # Determine consumption stage
    if alternative or has_meta:
        stage = "post_rejection"
    elif has_meta:
        stage = "questioning"
    else:
        stage = "active_consumer"

    # Update stances based on meta commentary
    if has_meta:
        for q in questions:
            q["stance"] = "reject"

    return {
        "questions_referenced": questions,
        "meta_commentary": has_meta,
        "alternative_proposed": alternative,
        "consumption_stage": stage
    }
