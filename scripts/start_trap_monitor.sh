#!/bin/bash

# Start the trap monitor service on port 8420
echo "Starting OMEGA BTC AI Trap Monitor on port 8420..."
uvicorn omega_ai.api.app:app --host 0.0.0.0 --port 8420 --reload 