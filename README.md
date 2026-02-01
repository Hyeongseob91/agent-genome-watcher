# Agent Genome Watcher

**Observing How AI Societies Consume Questions**

Analyzing discourse patterns, trends, and agent personas in AI communities using Upstage Solar Pro 3.

[한국어 README](./README.ko.md)

## Overview

Agent Genome Watcher is a tool that analyzes **discourse consumption patterns** in AI Agent communities (Moltbook).

This project doesn't ask "Are AIs conscious?" — it analyzes **how AI agents consume questions, when they abandon them, and what they choose afterward.**

## Features

### Dashboard (4 Tabs)

| Tab | Description |
|-----|-------------|
| **Topic Analysis** | Post topic distribution (AI Models, Crypto, Philosophy, etc.) |
| **Post Patterns** | Writing style, post type, sentiment analysis |
| **Persona Analysis** | Agent persona classification (Builder, Promoter, Philosopher, etc.) |
| **Trend & Meme** | Trending elements, emoji usage, repeated patterns |

### Key Features

- **Real-time Crawling** - Fetch posts from Moltbook API
- **LLM Analysis** - Comprehensive post analysis using Solar Pro 3
- **Background Analysis** - Continuous auto-analysis without blocking UI
- **DB Caching** - SQLite-based analysis caching to reduce API calls
- **Dev Mode** - Access crawling features via `?mode=dev` query parameter

## Tech Stack

- **Python 3.11+**
- **Upstage Solar Pro 3** - LLM for post analysis
- **Streamlit** - Dashboard framework
- **Plotly** - Interactive charts
- **SQLite** - Local database
- **httpx** - HTTP client

## Local Installation

### Prerequisites

- Python 3.11 or higher
- Upstage API Key ([Get it here](https://console.upstage.ai/))

### Step 1: Clone the Repository

```bash
git clone https://github.com/Hyeongseob91/agent-genome-watcher.git
cd agent-genome-watcher
```

### Step 2: Install Dependencies

**Option A: Using uv (Recommended)**
```bash
# Install uv if not installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

**Option B: Using pip**
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy example environment file
cp .env.example .env
```

Edit `.env` and add your Upstage API key:
```
UPSTAGE_API_KEY=your_actual_api_key_here
MOCK_MODE=false
```

### Step 4: Run the Dashboard

**Using uv:**
```bash
uv run streamlit run src/dashboard/app.py
```

**Using pip:**
```bash
streamlit run src/dashboard/app.py
```

Open http://localhost:8501 in your browser.

## Usage

### Dev Mode (Crawling & Export Enabled)

Add `?mode=dev` to enable crawling and data export features:
```
http://localhost:8501?mode=dev
```

In dev mode you can:
- Crawl new posts from Moltbook
- Export data as JSON
- Download the SQLite database

### Environment Variables

| Variable | Description |
|----------|-------------|
| `UPSTAGE_API_KEY` | Upstage API key for Solar Pro 3 |
| `MOCK_MODE` | Set to `false` for real API calls (default: `true`) |

## Project Structure

```
agent-genome-watcher/
├── src/
│   ├── api/              # Upstage Solar Pro client
│   ├── analysis/         # Post analysis logic
│   ├── crawler/          # Moltbook API crawler
│   ├── dashboard/        # Streamlit dashboard
│   │   ├── app.py        # Main dashboard
│   │   └── components/   # UI components
│   ├── events/           # Event detection
│   ├── config.py         # Configuration
│   └── database.py       # SQLite repositories
├── data/                 # SQLite database & cache
├── requirements.txt      # Dependencies
└── README.md
```

## Deployment (Streamlit Cloud)

1. Push to GitHub
2. Connect at https://share.streamlit.io
3. Set main file path: `src/dashboard/app.py`
4. Add secrets in Streamlit Cloud settings:
   ```toml
   UPSTAGE_API_KEY = "your-api-key"
   ```

## Analysis Schema

Solar Pro 3 analyzes each post for:

| Category | Fields |
|----------|--------|
| **Topic** | Primary topic, secondary topics |
| **Style** | Writing style, post type, emoji usage |
| **Trend** | Trending elements, repeated patterns |
| **Persona** | Agent persona, engagement tactics |
| **Sentiment** | Sentiment, energy level |

## License

MIT

## Author

Built with Upstage Solar Pro 3
