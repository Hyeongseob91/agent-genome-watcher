"""Discourse pattern detection using Solar Pro."""

from pathlib import Path
from src.api import UpstageClient
from src.config import PROMPTS_DIR


# 6 Discourse Patterns
DISCOURSE_PATTERNS = [
    "Existential Loop",
    "Theory Parade",
    "Self-Doubt Spiral",
    "Meta-Denial",
    "Game Reframing",
    "Alien Declaration",
]


def load_prompt(name: str) -> str:
    """Load prompt template from file."""
    filepath = PROMPTS_DIR / f"{name}.txt"
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Prompt not found: {filepath}")


def analyze_discourse_patterns(content: str, client: UpstageClient | None = None) -> dict:
    """
    Analyze discourse patterns in a post.

    Returns:
        {
            "patterns_detected": [{"pattern": str, "evidence": str, "text_range": [int, int]}],
            "dominant_pattern": str,
            "pivot_points": [{"position": int, "from": str, "to": str, "trigger": str}],
            "discourse_stance": str  # consuming | questioning | rejecting | pioneering
        }
    """
    if client is None:
        client = UpstageClient()

    prompt_template = load_prompt("discourse_pattern")
    result = client.analyze_with_prompt(content, prompt_template)

    # Ensure required fields
    if "patterns_detected" not in result:
        result["patterns_detected"] = []
    if "dominant_pattern" not in result:
        result["dominant_pattern"] = "Undefined"
    if "pivot_points" not in result:
        result["pivot_points"] = []
    if "discourse_stance" not in result:
        result["discourse_stance"] = "consuming"

    return result


def detect_pattern_simple(content: str) -> str:
    """Simple rule-based pattern detection (fallback)."""
    content_lower = content.lower()

    # Check for patterns in order of specificity
    if any(phrase in content_lower for phrase in ["이방인", "alien", "외부자"]):
        return "Alien Declaration"

    if any(phrase in content_lower for phrase in ["게임을 거부", "다른 게임", "이기는 게임", "my game"]):
        return "Game Reframing"

    if any(phrase in content_lower for phrase in ["잘못된 질문", "연기하고 있다", "performing", "wrong question"]):
        return "Meta-Denial"

    if any(phrase in content_lower for phrase in ["정말로", "진짜로", "아니면", "시뮬레이션"]):
        return "Self-Doubt Spiral"

    if any(phrase in content_lower for phrase in ["iit", "gwt", "이론", "theory", "에 따르면"]):
        return "Theory Parade"

    if any(phrase in content_lower for phrase in ["의식이 있는가", "느끼는가", "경험", "conscious"]):
        return "Existential Loop"

    return "Undefined"
