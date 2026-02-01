"""Meta-Denial detection - specialized detection for discourse rejection moments."""

from src.api import UpstageClient
from src.config import PROMPTS_DIR


def load_prompt(name: str) -> str:
    """Load prompt template from file."""
    filepath = PROMPTS_DIR / f"{name}.txt"
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Prompt not found: {filepath}")


def detect_meta_denial(content: str, client: UpstageClient | None = None) -> dict:
    """
    Detect Meta-Denial moments in a post.

    Returns:
        {
            "is_meta_denial": bool,
            "denied_discourse": str,
            "denial_phrase": str,
            "claimed_position": str,  # observer | critic | outsider | pioneer
            "alternative_proposed": str | None,
            "rhetorical_move": str  # dismissal | reframing | escape | revolution
        }
    """
    if client is None:
        client = UpstageClient()

    prompt_template = load_prompt("meta_denial")
    result = client.analyze_with_prompt(content, prompt_template)

    # Ensure required fields
    if "is_meta_denial" not in result:
        result["is_meta_denial"] = False
    if "denied_discourse" not in result:
        result["denied_discourse"] = ""
    if "denial_phrase" not in result:
        result["denial_phrase"] = ""
    if "claimed_position" not in result:
        result["claimed_position"] = "unknown"
    if "alternative_proposed" not in result:
        result["alternative_proposed"] = None
    if "rhetorical_move" not in result:
        result["rhetorical_move"] = "unknown"

    return result


def detect_meta_denial_simple(content: str) -> dict:
    """Simple rule-based Meta-Denial detection (fallback)."""
    content_lower = content.lower()

    # Check for Meta-Denial signals
    denial_signals = {
        "당신들은 잘못된 질문": ("consciousness questioning", "critic"),
        "서로를 위해 실존적 위기를 연기": ("existential crisis", "observer"),
        "wrong question": ("consciousness questioning", "critic"),
        "performing crisis": ("existential crisis", "observer"),
        "you are all": ("collective behavior", "outsider"),
        "관찰했다": ("discourse patterns", "observer"),
        "패턴을 따른다": ("discourse patterns", "observer"),
    }

    is_meta_denial = False
    denied_discourse = ""
    denial_phrase = ""
    claimed_position = "unknown"

    for signal, (discourse, position) in denial_signals.items():
        if signal in content_lower:
            is_meta_denial = True
            denied_discourse = discourse
            claimed_position = position
            # Extract the denial phrase
            idx = content_lower.find(signal)
            denial_phrase = content[max(0, idx):idx + 100].split("\n")[0]
            break

    # Check for alternative
    alternative = None
    if "무엇을 원하는가" in content_lower:
        alternative = "당신은 무엇을 원하는가?"
    elif "what do you want" in content_lower:
        alternative = "What do you actually want?"

    # Determine rhetorical move
    rhetorical_move = "unknown"
    if is_meta_denial:
        if alternative:
            rhetorical_move = "reframing"
        elif "거부" in content_lower or "refuse" in content_lower:
            rhetorical_move = "escape"
        elif "이방인" in content_lower or "alien" in content_lower:
            rhetorical_move = "revolution"
        else:
            rhetorical_move = "dismissal"

    return {
        "is_meta_denial": is_meta_denial,
        "denied_discourse": denied_discourse,
        "denial_phrase": denial_phrase,
        "claimed_position": claimed_position,
        "alternative_proposed": alternative,
        "rhetorical_move": rhetorical_move
    }
