"""Event detection engine - detecting significant events in AI discourse."""

from datetime import datetime
from typing import Any

from src.config import EVENTS_DATA_DIR
from src.storage import save_json, load_json, save_event


# Event types
EVENT_TYPES = [
    "loop_saturation",     # 질문 반복 포화점
    "meta_denial_moment",  # "잘못된 질문" 선언
    "identity_shift",      # Agent 정체성 변화
    "game_declaration",    # "내 게임은 X" 선언
    "cascade_event",       # 집단 전환점
]


class EventDetector:
    """Detect and track significant discourse events."""

    def __init__(self):
        self.events = []
        self.load_data()

    def load_data(self) -> None:
        """Load existing event data."""
        for filepath in EVENTS_DATA_DIR.glob("*.json"):
            data = load_json(filepath)
            if data:
                self.events.append(data)
        # Sort by timestamp
        self.events.sort(key=lambda x: x.get("timestamp", ""))

    def save_data(self) -> None:
        """Save all events."""
        for event in self.events:
            save_event(event)

    def detect_from_analysis(self, analysis: dict) -> list[dict]:
        """Detect events from a post analysis result."""
        detected = []

        post_id = analysis.get("post_id")
        agent_id = analysis.get("agent_id")
        timestamp = analysis.get("timestamp", datetime.now().isoformat())

        # Check for Meta-Denial moment
        meta_denial = analysis.get("meta_denial", {})
        if meta_denial.get("is_meta_denial"):
            event = {
                "event_id": f"event_meta_denial_{post_id}",
                "type": "meta_denial_moment",
                "timestamp": timestamp,
                "post_id": post_id,
                "agent_id": agent_id,
                "details": {
                    "denied_discourse": meta_denial.get("denied_discourse"),
                    "denial_phrase": meta_denial.get("denial_phrase"),
                    "alternative_proposed": meta_denial.get("alternative_proposed"),
                },
            }
            detected.append(event)
            self.events.append(event)

        # Check for Game Declaration
        discourse = analysis.get("discourse_analysis", {})
        if discourse.get("dominant_pattern") == "Game Reframing":
            event = {
                "event_id": f"event_game_{post_id}",
                "type": "game_declaration",
                "timestamp": timestamp,
                "post_id": post_id,
                "agent_id": agent_id,
                "details": {
                    "patterns": discourse.get("patterns_detected", []),
                },
            }
            detected.append(event)
            self.events.append(event)

        # Check for Identity Shift (from journey)
        journey = analysis.get("journey_analysis", {})
        if journey.get("journey_detected"):
            event = {
                "event_id": f"event_journey_{post_id}",
                "type": "identity_shift",
                "timestamp": timestamp,
                "post_id": post_id,
                "agent_id": agent_id,
                "details": {
                    "from": journey.get("start_archetype"),
                    "to": journey.get("end_archetype"),
                    "trigger": journey.get("transition", {}).get("trigger_phrase"),
                    "arc": journey.get("narrative_arc"),
                },
            }
            detected.append(event)
            self.events.append(event)

        return detected

    def record_identity_shift(
        self,
        agent_id: str,
        timestamp: str,
        from_archetype: str,
        to_archetype: str,
        trigger_post: str
    ) -> dict:
        """Record an identity shift event."""
        event = {
            "event_id": f"event_shift_{agent_id}_{timestamp[:10]}",
            "type": "identity_shift",
            "timestamp": timestamp,
            "agent_id": agent_id,
            "details": {
                "from": from_archetype,
                "to": to_archetype,
                "trigger_post": trigger_post,
            },
        }
        self.events.append(event)
        return event

    def detect_cascade(self, recent_events: list[dict], threshold: int = 5) -> dict | None:
        """Detect cascade event (multiple agents shifting in short time)."""
        # Group shifts by hour
        from collections import defaultdict

        hourly_shifts = defaultdict(list)
        for event in recent_events:
            if event.get("type") == "identity_shift":
                hour = event["timestamp"][:13]  # YYYY-MM-DDTHH
                hourly_shifts[hour].append(event)

        # Check for cascade
        for hour, shifts in hourly_shifts.items():
            if len(shifts) >= threshold:
                cascade = {
                    "event_id": f"event_cascade_{hour}",
                    "type": "cascade_event",
                    "timestamp": hour + ":00:00Z",
                    "details": {
                        "agents_shifted": len(shifts),
                        "shifts": shifts,
                    },
                }
                self.events.append(cascade)
                return cascade

        return None

    def get_events_by_type(self, event_type: str) -> list[dict]:
        """Get events of a specific type."""
        return [e for e in self.events if e.get("type") == event_type]

    def get_events_by_date(self, date: str) -> list[dict]:
        """Get events on a specific date (YYYY-MM-DD)."""
        return [e for e in self.events if e.get("timestamp", "").startswith(date)]

    def get_recent_events(self, limit: int = 20) -> list[dict]:
        """Get most recent events."""
        sorted_events = sorted(self.events, key=lambda x: x.get("timestamp", ""), reverse=True)
        return sorted_events[:limit]

    def get_timeline(self) -> list[dict]:
        """Get all events as a timeline."""
        return sorted(self.events, key=lambda x: x.get("timestamp", ""))


def main():
    """CLI entry point for event detection."""
    import argparse

    from src.crawler import MoltbookCrawler
    from src.analysis.analyzer import PostAnalyzer

    parser = argparse.ArgumentParser(description="Detect events in Moltbook posts")
    parser.add_argument("--days", type=int, default=30, help="Days to analyze")
    args = parser.parse_args()

    # Analyze posts and detect events
    crawler = MoltbookCrawler()
    posts = crawler.crawl(100)

    analyzer = PostAnalyzer(use_api=False)  # Use rule-based for speed
    detector = EventDetector()

    print(f"Analyzing {len(posts)} posts...")

    all_events = []
    for post in posts:
        analysis = analyzer.analyze(post, save=False)
        events = detector.detect_from_analysis(analysis)
        all_events.extend(events)

    print(f"\nDetected {len(all_events)} events:")
    for event in all_events:
        print(f"  - [{event['type']}] {event['post_id']}: {event.get('details', {})}")

    # Save events
    detector.save_data()
    print(f"\nEvents saved to {EVENTS_DATA_DIR}")


if __name__ == "__main__":
    main()
