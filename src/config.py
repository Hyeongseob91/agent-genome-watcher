"""Configuration settings."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PROMPTS_DIR = BASE_DIR / "prompts"

# Upstage API
UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY", "")
UPSTAGE_BASE_URL = "https://api.upstage.ai/v2"

# Mock mode
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"

# Settings dictionary for easy access
settings = {
    "MOCK_MODE": MOCK_MODE,
    "UPSTAGE_API_KEY": UPSTAGE_API_KEY,
    "UPSTAGE_BASE_URL": UPSTAGE_BASE_URL,
}

# Data paths
RAW_DATA_DIR = DATA_DIR / "raw"
ANALYZED_DATA_DIR = DATA_DIR / "analyzed"
QUESTIONS_DATA_DIR = DATA_DIR / "questions"
AGENTS_DATA_DIR = DATA_DIR / "agents"
EVENTS_DATA_DIR = DATA_DIR / "events"

# Ensure directories exist
for dir_path in [RAW_DATA_DIR, ANALYZED_DATA_DIR, QUESTIONS_DATA_DIR, AGENTS_DATA_DIR, EVENTS_DATA_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)
