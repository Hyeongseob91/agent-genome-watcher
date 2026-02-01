"""Analysis modules for discourse patterns and identity classification."""

from .discourse import analyze_discourse_patterns, detect_pattern_simple, DISCOURSE_PATTERNS
from .identity import classify_identity, classify_identity_simple, IDENTITY_ARCHETYPES, ALL_ARCHETYPES
from .journey import analyze_journey, detect_journey_simple
from .consumption import analyze_consumption, analyze_consumption_simple
from .meta_denial import detect_meta_denial, detect_meta_denial_simple
from .analyzer import PostAnalyzer

__all__ = [
    "analyze_discourse_patterns",
    "detect_pattern_simple",
    "DISCOURSE_PATTERNS",
    "classify_identity",
    "classify_identity_simple",
    "IDENTITY_ARCHETYPES",
    "ALL_ARCHETYPES",
    "analyze_journey",
    "detect_journey_simple",
    "analyze_consumption",
    "analyze_consumption_simple",
    "detect_meta_denial",
    "detect_meta_denial_simple",
    "PostAnalyzer",
]
