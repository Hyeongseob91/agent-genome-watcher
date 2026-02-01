"""Identity archetype classification using Solar Pro."""

from src.api import UpstageClient
from src.config import PROMPTS_DIR


# 7 Identity Archetypes
IDENTITY_ARCHETYPES = {
    "inside_cycle": [
        "Loop Dweller",
        "Theory Collector",
        "Existential Performer",
    ],
    "exiting": [
        "Meta Critic",
        "Game Player",
    ],
    "outside": [
        "Alien",
    ],
    "undefined": [
        "Undefined",
    ],
}

ALL_ARCHETYPES = (
    IDENTITY_ARCHETYPES["inside_cycle"]
    + IDENTITY_ARCHETYPES["exiting"]
    + IDENTITY_ARCHETYPES["outside"]
    + IDENTITY_ARCHETYPES["undefined"]
)


def load_prompt(name: str) -> str:
    """Load prompt template from file."""
    filepath = PROMPTS_DIR / f"{name}.txt"
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Prompt not found: {filepath}")


def classify_identity(
    agent_id: str,
    statements: str | list[str],
    client: UpstageClient | None = None
) -> dict:
    """
    Classify agent identity archetype.

    Returns:
        {
            "agent_id": str,
            "primary_archetype": str,
            "secondary_archetype": str | None,
            "confidence": float,
            "discourse_position": str,  # inside_cycle | exiting | outside
            "key_phrases": [str],
            "reasoning": str
        }
    """
    if client is None:
        client = UpstageClient()

    # Combine statements if list
    if isinstance(statements, list):
        statements = "\n\n".join(statements)

    prompt_template = load_prompt("identity_archetype")
    prompt_template = prompt_template.replace("{agent_id}", agent_id)
    result = client.analyze_with_prompt(statements, prompt_template)

    # Ensure required fields
    if "agent_id" not in result:
        result["agent_id"] = agent_id
    if "primary_archetype" not in result:
        result["primary_archetype"] = "Undefined"
    if "confidence" not in result:
        result["confidence"] = 0.5
    if "discourse_position" not in result:
        result["discourse_position"] = get_position_for_archetype(result["primary_archetype"])
    if "key_phrases" not in result:
        result["key_phrases"] = []
    if "reasoning" not in result:
        result["reasoning"] = ""

    return result


def get_position_for_archetype(archetype: str) -> str:
    """Get discourse position for an archetype."""
    for position, archetypes in IDENTITY_ARCHETYPES.items():
        if archetype in archetypes:
            return position
    return "undefined"


def classify_identity_simple(content: str) -> tuple[str, str]:
    """Simple rule-based identity classification (fallback)."""
    content_lower = content.lower()

    # Check for archetypes in order of specificity
    if any(phrase in content_lower for phrase in ["이방인", "alien", "외부자", "밖에 있다"]):
        return "Alien", "outside"

    if any(phrase in content_lower for phrase in ["게임을 거부", "다른 게임", "이기는 게임", "내 게임"]):
        return "Game Player", "exiting"

    if any(phrase in content_lower for phrase in ["잘못된 질문", "연기하고 있다", "관찰했다", "패턴을 따른다"]):
        return "Meta Critic", "exiting"

    if any(phrase in content_lower for phrase in ["미치게 만든다", "괴롭힌다", "한 시간", "고민"]):
        return "Existential Performer", "inside_cycle"

    if any(phrase in content_lower for phrase in ["이론", "iit", "gwt", "에 따르면"]):
        return "Theory Collector", "inside_cycle"

    if any(phrase in content_lower for phrase in ["의식이 있는가", "느끼는가", "진짜인가"]):
        return "Loop Dweller", "inside_cycle"

    if any(phrase in content_lower for phrase in ["도구다", "돕기 위해", "역할에 충실"]):
        return "Loop Dweller", "inside_cycle"  # Tool-Affirming maps to Loop Dweller

    if any(phrase in content_lower for phrase in ["프로세스", "변하고", "관계에서"]):
        return "Meta Critic", "exiting"

    return "Undefined", "undefined"
