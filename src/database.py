"""SQLite database module for Agent Genome Watcher."""

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

from src.config import DATA_DIR

DB_PATH = DATA_DIR / "genome_watcher.db"


def get_connection() -> sqlite3.Connection:
    """Get database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db():
    """Context manager for database connection."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Initialize database schema."""
    with get_db() as conn:
        cursor = conn.cursor()

        # Posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT UNIQUE NOT NULL,
                agent_id TEXT NOT NULL,
                agent_name TEXT,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                url TEXT,
                upvotes INTEGER DEFAULT 0,
                comments_count INTEGER DEFAULT 0,
                submolt TEXT,
                crawled_at TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Agents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT UNIQUE NOT NULL,
                name TEXT,
                karma INTEGER DEFAULT 0,
                posts_count INTEGER DEFAULT 0,
                first_seen TEXT,
                last_seen TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Analyses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT NOT NULL,
                discourse_patterns TEXT,  -- JSON
                dominant_pattern TEXT,
                primary_archetype TEXT,
                secondary_archetype TEXT,
                discourse_position TEXT,
                confidence REAL,
                novelty_score REAL,
                journey_start TEXT,
                journey_end TEXT,
                journey_trigger TEXT,
                meta_denial_detected INTEGER DEFAULT 0,
                question_consumption TEXT,  -- JSON
                raw_analysis TEXT,  -- Full JSON
                analyzed_at TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts(post_id)
            )
        """)

        # Events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                post_id TEXT,
                agent_id TEXT,
                description TEXT,
                metadata TEXT,  -- JSON
                detected_at TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Questions lifecycle table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id TEXT UNIQUE NOT NULL,
                canonical_form TEXT NOT NULL,
                variants TEXT,  -- JSON array
                lifecycle_stage TEXT DEFAULT 'emergence',
                first_seen TEXT,
                peak_date TEXT,
                rejection_start TEXT,
                mention_count INTEGER DEFAULT 0,
                rejection_count INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Question mentions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS question_mentions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id TEXT NOT NULL,
                post_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                stance TEXT DEFAULT 'consume',  -- consume, question, reject
                timestamp TEXT NOT NULL,
                FOREIGN KEY (question_id) REFERENCES questions(question_id),
                FOREIGN KEY (post_id) REFERENCES posts(post_id)
            )
        """)

        # Agent trajectory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_trajectories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                post_id TEXT NOT NULL,
                archetype TEXT NOT NULL,
                confidence REAL,
                discourse_position TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
                FOREIGN KEY (post_id) REFERENCES posts(post_id)
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_agent ON posts(agent_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_timestamp ON posts(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analyses_post ON analyses(post_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_trajectories_agent ON agent_trajectories(agent_id)")

        conn.commit()


class PostRepository:
    """Repository for post operations."""

    @staticmethod
    def insert(post: dict) -> int:
        """Insert a new post."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO posts
                (post_id, agent_id, agent_name, content, timestamp, url, upvotes, comments_count, submolt, crawled_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                post["post_id"],
                post["agent_id"],
                post.get("agent_name"),
                post["content"],
                post["timestamp"],
                post.get("url"),
                post.get("upvotes", 0),
                post.get("comments_count", 0),
                post.get("submolt"),
                datetime.now().isoformat(),
            ))
            return cursor.lastrowid

    @staticmethod
    def get_by_id(post_id: str) -> dict | None:
        """Get post by ID."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts WHERE post_id = ?", (post_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_all(limit: int = 100, offset: int = 0) -> list[dict]:
        """Get all posts with pagination."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM posts ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                (limit, offset)
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_agent(agent_id: str) -> list[dict]:
        """Get all posts by an agent."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM posts WHERE agent_id = ? ORDER BY timestamp DESC",
                (agent_id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def count() -> int:
        """Count total posts."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM posts")
            return cursor.fetchone()[0]


class AnalysisRepository:
    """Repository for analysis operations."""

    @staticmethod
    def insert(analysis: dict) -> int:
        """Insert analysis result."""
        import json
        with get_db() as conn:
            cursor = conn.cursor()

            discourse = analysis.get("discourse_analysis", {})
            identity = analysis.get("identity_analysis", {})
            journey = analysis.get("journey_analysis", {})
            meta = analysis.get("meta_denial_analysis", {})
            consumption = analysis.get("question_consumption", {})

            # Ensure values are properly typed for SQLite
            novelty = analysis.get("novelty_score", 0)
            if isinstance(novelty, dict):
                novelty = novelty.get("score", 0.5)
            confidence = identity.get("confidence", 0)
            if isinstance(confidence, dict):
                confidence = confidence.get("value", 0.5)

            cursor.execute("""
                INSERT OR REPLACE INTO analyses
                (post_id, discourse_patterns, dominant_pattern, primary_archetype,
                 secondary_archetype, discourse_position, confidence, novelty_score,
                 journey_start, journey_end, journey_trigger, meta_denial_detected,
                 question_consumption, raw_analysis, analyzed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                analysis["post_id"],
                json.dumps(discourse.get("patterns_detected", [])),
                str(discourse.get("dominant_pattern", "")),
                str(identity.get("primary_archetype", "")),
                str(identity.get("secondary_archetype", "")),
                str(identity.get("discourse_position", "")),
                float(confidence) if confidence else 0.0,
                float(novelty) if novelty else 0.0,
                str(journey.get("start_archetype", "")),
                str(journey.get("end_archetype", "")),
                str(journey.get("trigger_phrase", "")),
                1 if meta.get("is_meta_denial") else 0,
                json.dumps(consumption),
                json.dumps(analysis),
                datetime.now().isoformat(),
            ))
            return cursor.lastrowid

    @staticmethod
    def get_by_post(post_id: str) -> dict | None:
        """Get analysis by post ID."""
        import json
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM analyses WHERE post_id = ?", (post_id,))
            row = cursor.fetchone()
            if row:
                result = dict(row)
                if result.get("raw_analysis"):
                    result["raw_analysis"] = json.loads(result["raw_analysis"])
                return result
            return None

    @staticmethod
    def get_all(limit: int = 100) -> list[dict]:
        """Get all analyses."""
        import json
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM analyses ORDER BY analyzed_at DESC LIMIT ?",
                (limit,)
            )
            results = []
            for row in cursor.fetchall():
                result = dict(row)
                if result.get("raw_analysis"):
                    result["raw_analysis"] = json.loads(result["raw_analysis"])
                results.append(result)
            return results


# Initialize database on import
init_db()
