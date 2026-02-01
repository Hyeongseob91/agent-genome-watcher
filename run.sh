#!/bin/bash
# Run Agent Genome Watcher Dashboard

cd "$(dirname "$0")"
PYTHONPATH=. uv run streamlit run src/dashboard/app.py "$@"
