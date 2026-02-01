"""Agent identity trajectory tracking - tracking how agents change over time."""

from datetime import datetime
from typing import Any

from src.config import AGENTS_DATA_DIR
from src.storage import save_json, load_json, save_agent_profile, load_agent_profile


class IdentityTrajectoryTracker:
    """Track identity changes for agents over time."""

    def __init__(self):
        self.agents = {}  # agent_id -> profile data
        self.load_data()

    def load_data(self) -> None:
        """Load existing agent data."""
        for filepath in AGENTS_DATA_DIR.glob("*.json"):
            data = load_json(filepath)
            if data:
                self.agents[data.get("agent_id", filepath.stem)] = data

    def save_data(self) -> None:
        """Save all agent data."""
        for agent_id, data in self.agents.items():
            save_agent_profile(agent_id, data)

    def record_analysis(
        self,
        agent_id: str,
        post_id: str,
        timestamp: str,
        archetype: str,
        confidence: float,
        discourse_position: str,
        key_phrases: list[str] | None = None
    ) -> dict | None:
        """
        Record an analysis result for an agent.

        Returns shift event if identity changed, None otherwise.
        """
        if agent_id not in self.agents:
            self.agents[agent_id] = {
                "agent_id": agent_id,
                "identity_trajectory": [],
                "discourse_role": {
                    "primary_role": "Consumer",
                    "questions_consumed": 0,
                    "questions_rejected": 0,
                    "new_frames_proposed": 0,
                },
                "influence_metrics": {
                    "cascade_triggers": 0,
                    "phrase_adoptions": 0,
                },
                "signature_phrases": [],
            }

        agent = self.agents[agent_id]

        # Get previous archetype
        trajectory = agent["identity_trajectory"]
        prev_archetype = trajectory[-1]["archetype"] if trajectory else None

        # Add new trajectory point
        trajectory.append({
            "date": timestamp[:10],  # YYYY-MM-DD
            "archetype": archetype,
            "confidence": confidence,
            "discourse_position": discourse_position,
            "sample_post": post_id,
        })

        # Keep only last 100 points
        agent["identity_trajectory"] = trajectory[-100:]

        # Add signature phrases
        if key_phrases:
            for phrase in key_phrases:
                if phrase not in agent["signature_phrases"]:
                    agent["signature_phrases"].append(phrase)
            # Keep only last 10
            agent["signature_phrases"] = agent["signature_phrases"][-10:]

        # Update discourse role based on position
        if discourse_position in ["exiting", "outside"]:
            agent["discourse_role"]["primary_role"] = "Disruptor"
        elif discourse_position == "inside_cycle":
            agent["discourse_role"]["primary_role"] = "Consumer"

        # Detect shift
        shift_event = None
        if prev_archetype and prev_archetype != archetype:
            shift_event = {
                "agent_id": agent_id,
                "timestamp": timestamp,
                "from_archetype": prev_archetype,
                "to_archetype": archetype,
                "trigger_post": post_id,
            }

        return shift_event

    def get_trajectory(self, agent_id: str) -> list[dict]:
        """Get identity trajectory for an agent."""
        agent = self.agents.get(agent_id, {})
        return agent.get("identity_trajectory", [])

    def get_profile(self, agent_id: str) -> dict | None:
        """Get full profile for an agent."""
        return self.agents.get(agent_id)

    def get_agents_by_archetype(self, archetype: str) -> list[str]:
        """Get list of agent IDs with current archetype."""
        result = []
        for agent_id, data in self.agents.items():
            trajectory = data.get("identity_trajectory", [])
            if trajectory and trajectory[-1].get("archetype") == archetype:
                result.append(agent_id)
        return result

    def get_agents_by_position(self, position: str) -> list[str]:
        """Get list of agent IDs at discourse position."""
        result = []
        for agent_id, data in self.agents.items():
            trajectory = data.get("identity_trajectory", [])
            if trajectory and trajectory[-1].get("discourse_position") == position:
                result.append(agent_id)
        return result

    def compute_distribution(self) -> dict:
        """Compute current archetype distribution."""
        distribution = {}
        total = 0

        for data in self.agents.values():
            trajectory = data.get("identity_trajectory", [])
            if trajectory:
                archetype = trajectory[-1].get("archetype", "Undefined")
                distribution[archetype] = distribution.get(archetype, 0) + 1
                total += 1

        # Convert to ratios
        if total > 0:
            for archetype in distribution:
                distribution[archetype] = distribution[archetype] / total

        return distribution

    def get_all_shift_events(self) -> list[dict]:
        """Get all identity shift events across agents."""
        events = []

        for agent_id, data in self.agents.items():
            trajectory = data.get("identity_trajectory", [])
            for i in range(1, len(trajectory)):
                prev = trajectory[i-1]
                curr = trajectory[i]
                if prev["archetype"] != curr["archetype"]:
                    events.append({
                        "agent_id": agent_id,
                        "date": curr["date"],
                        "from": prev["archetype"],
                        "to": curr["archetype"],
                        "post_id": curr.get("sample_post"),
                    })

        # Sort by date
        events.sort(key=lambda x: x["date"])
        return events
