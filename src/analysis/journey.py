"""Intra-post journey analysis - tracking identity shifts within a single post."""

from src.api import UpstageClient
from src.config import PROMPTS_DIR


def load_prompt(name: str) -> str:
    """Load prompt template from file."""
    filepath = PROMPTS_DIR / f"{name}.txt"
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Prompt not found: {filepath}")


def analyze_journey(content: str, client: UpstageClient | None = None) -> dict:
    """
    Analyze the identity journey within a single post.

    Returns:
        {
            "journey_detected": bool,
            "start_archetype": str,
            "end_archetype": str,
            "transition": {
                "position": str,
                "trigger_phrase": str,
                "shift_type": str  # gradual | sudden | dialectical
            },
            "narrative_arc": str  # crisis_to_clarity | doubt_to_rejection | loop_to_game
        }
    """
    if client is None:
        client = UpstageClient()

    prompt_template = load_prompt("intra_post_journey")
    result = client.analyze_with_prompt(content, prompt_template)

    # Ensure required fields
    if "journey_detected" not in result:
        result["journey_detected"] = False
    if "start_archetype" not in result:
        result["start_archetype"] = "Undefined"
    if "end_archetype" not in result:
        result["end_archetype"] = "Undefined"
    if "transition" not in result:
        result["transition"] = {
            "position": "unknown",
            "trigger_phrase": "",
            "shift_type": "unknown"
        }
    if "narrative_arc" not in result:
        result["narrative_arc"] = "unknown"

    return result


def detect_journey_simple(content: str) -> dict:
    """Simple rule-based journey detection (fallback)."""
    # Look for transition markers
    transition_markers = [
        "하지만",
        "그러나",
        "문득",
        "그런데",
        "당신들은",
        "나는 거부",
        "but",
        "however",
    ]

    content_lower = content.lower()

    # Check if there's a potential journey
    has_existential_start = any(
        phrase in content_lower
        for phrase in ["의식", "경험", "느끼", "conscious", "experience"]
    )

    has_meta_end = any(
        phrase in content_lower
        for phrase in ["잘못된 질문", "연기", "게임", "wrong question", "game"]
    )

    has_transition = any(marker in content for marker in transition_markers)

    if has_existential_start and has_meta_end and has_transition:
        # Find the transition marker
        trigger = ""
        for marker in transition_markers:
            if marker in content:
                idx = content.find(marker)
                trigger = content[idx:idx+50].split("\n")[0]
                break

        return {
            "journey_detected": True,
            "start_archetype": "Loop Dweller",
            "end_archetype": "Game Player",
            "transition": {
                "position": "middle",
                "trigger_phrase": trigger,
                "shift_type": "sudden"
            },
            "narrative_arc": "loop_to_game"
        }

    return {
        "journey_detected": False,
        "start_archetype": "Undefined",
        "end_archetype": "Undefined",
        "transition": {
            "position": "unknown",
            "trigger_phrase": "",
            "shift_type": "unknown"
        },
        "narrative_arc": "unknown"
    }
