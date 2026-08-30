#!/usr/bin/env bash
# Shared CASE/UCO MCP listener for Cursor, Hermes, Claude Desktop, and others.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="$ROOT/.venv/bin:${PATH:-/usr/local/bin:/usr/bin:/bin}"
export PYTHONPATH="$ROOT/python:$ROOT/mcp_server${PYTHONPATH:+:$PYTHONPATH}"
export CASE_UCO_EXTENSIONS="${CASE_UCO_EXTENSIONS:-cac,legalproc,solveit,cryptoinv,rico,weapons,drugs}"
export CASE_UCO_MCP_TRANSPORT="${CASE_UCO_MCP_TRANSPORT:-sse}"
export CASE_UCO_MCP_HOST="${CASE_UCO_MCP_HOST:-127.0.0.1}"
export CASE_UCO_MCP_PORT="${CASE_UCO_MCP_PORT:-8765}"
exec "$ROOT/.venv/bin/python" "$ROOT/mcp_server/server.py" \
  --transport "$CASE_UCO_MCP_TRANSPORT" \
  --host "$CASE_UCO_MCP_HOST" \
  --port "$CASE_UCO_MCP_PORT"
