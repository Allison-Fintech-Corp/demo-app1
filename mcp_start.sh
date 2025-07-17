#!/usr/bin/env bash
# Spin up the fake core and wrap it as an MCP server

# 1) launch FastAPI stub
uvicorn bank_stub:app --port 8001 --reload &
STUB_PID=$!
sleep 2               # <-- give Uvicorn time to bind

# 2) wrap with MCP so agents can call `jack_core.<tool>`
python -m mcp.cli wrap http://localhost:8001 --name jack_core

echo "Jack‑Henry stub running    PID=$STUB_PID"
echo "Press Ctrl‑C to stop everything."
wait $STUB_PID          # keep script alive
