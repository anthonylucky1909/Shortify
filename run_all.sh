#!/bin/bash

# Start 3 uvicorn servers on different ports in background
echo "Starting FastAPI servers on ports 8000, 8001, and 8002..."

uvicorn app.main:app --port 8000 --workers 3 &
uvicorn app.main:app --port 8001 --workers 3 &
uvicorn app.main:app --port 8002 --workers 3 &

# Wait for all background processes to finish (keeps script alive)
wait
