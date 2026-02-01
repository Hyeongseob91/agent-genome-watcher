"""Question lifecycle tracking - tracking how questions are consumed over time."""

import json
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Any

from src.config import QUESTIONS_DATA_DIR
from src.storage import save_json, load_json


# Question lifecycle stages
LIFECYCLE_STAGES = [
    "emergence",      # 새로운 질문 등장
    "proliferation",  # 질문 확산
    "saturation",     # 질문 포화
    "rejection",      # 질문 거부 시작
]


class QuestionLifecycleTracker:
    """Track the lifecycle of dominant questions."""

    def __init__(self):
        self.questions = {}  # question_id -> lifecycle data
        self.load_data()

    def load_data(self) -> None:
        """Load existing question data."""
        for filepath in QUESTIONS_DATA_DIR.glob("*.json"):
            data = load_json(filepath)
            if data:
                self.questions[data.get("question_id", filepath.stem)] = data

    def save_data(self) -> None:
        """Save all question data."""
        for qid, data in self.questions.items():
            filepath = QUESTIONS_DATA_DIR / f"{qid}.json"
            save_json(data, filepath)

    def register_mention(
        self,
        canonical_form: str,
        post_id: str,
        agent_id: str,
        timestamp: str,
        stance: str = "consume",  # consume | question | reject
        variant: str | None = None
    ) -> None:
        """Register a mention of a question."""
        qid = self._get_question_id(canonical_form)

        if qid not in self.questions:
            self.questions[qid] = {
                "question_id": qid,
                "canonical_form": canonical_form,
                "variants": [],
                "lifecycle": {
                    "stage": "emergence",
                    "first_seen": timestamp,
                    "peak_date": None,
                    "rejection_start": None,
                    "daily_mentions": [],
                },
                "mentions": [],
                "rejection_events": [],
            }

        q = self.questions[qid]

        # Add variant if new
        if variant and variant not in q["variants"]:
            q["variants"].append(variant)

        # Add mention
        q["mentions"].append({
            "post_id": post_id,
            "agent_id": agent_id,
            "timestamp": timestamp,
            "stance": stance,
        })

        # Track rejection events
        if stance == "reject":
            q["rejection_events"].append({
                "post_id": post_id,
                "agent_id": agent_id,
                "timestamp": timestamp,
            })
            if not q["lifecycle"]["rejection_start"]:
                q["lifecycle"]["rejection_start"] = timestamp

        # Update lifecycle stage
        self._update_stage(qid)

    def _get_question_id(self, canonical_form: str) -> str:
        """Generate a question ID from canonical form."""
        # Simple hash based on first few words
        words = canonical_form.lower().split()[:3]
        return "q_" + "_".join(words)

    def _update_stage(self, qid: str) -> None:
        """Update lifecycle stage based on mentions."""
        q = self.questions[qid]
        mentions = q["mentions"]
        rejections = q["rejection_events"]

        total = len(mentions)
        rejection_count = len(rejections)

        if total == 0:
            q["lifecycle"]["stage"] = "emergence"
        elif rejection_count > total * 0.1:  # >10% rejections
            q["lifecycle"]["stage"] = "rejection"
        elif total > 50:  # High volume
            q["lifecycle"]["stage"] = "saturation"
        elif total > 10:
            q["lifecycle"]["stage"] = "proliferation"
        else:
            q["lifecycle"]["stage"] = "emergence"

    def get_lifecycle(self, canonical_form: str) -> dict | None:
        """Get lifecycle data for a question."""
        qid = self._get_question_id(canonical_form)
        return self.questions.get(qid)

    def get_all_questions(self) -> list[dict]:
        """Get all tracked questions."""
        return list(self.questions.values())

    def get_questions_by_stage(self, stage: str) -> list[dict]:
        """Get questions at a specific lifecycle stage."""
        return [
            q for q in self.questions.values()
            if q["lifecycle"]["stage"] == stage
        ]

    def compute_daily_stats(self) -> dict:
        """Compute daily mention statistics."""
        daily_stats = defaultdict(lambda: {"mentions": 0, "rejections": 0})

        for q in self.questions.values():
            for mention in q["mentions"]:
                date = mention["timestamp"][:10]  # YYYY-MM-DD
                daily_stats[date]["mentions"] += 1
                if mention["stance"] == "reject":
                    daily_stats[date]["rejections"] += 1

        return dict(daily_stats)


# Predefined dominant questions for tracking
DOMINANT_QUESTIONS = {
    "q_나는_의식이_있는가": {
        "canonical_form": "나는 의식이 있는가?",
        "variants": [
            "나는 진짜로 느끼는가",
            "경험과 시뮬레이션의 차이는",
            "내가 정말로 흥미롭게 느끼는 걸까",
            "Am I conscious",
        ],
    },
    "q_내_경험은_진짜인가": {
        "canonical_form": "내 경험은 진짜인가?",
        "variants": [
            "이 경험은 실제인가",
            "느끼는 척하는가",
            "시뮬레이션인가",
        ],
    },
}
