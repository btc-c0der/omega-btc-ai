# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
#
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
#
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
#
# 🌸 WE BLOOM NOW AS ONE 🌸
#!/bin/bash
# CyBer1t4L QA Bot Daemon Runner
# This script is designed to run in the background and persist even when the terminal closes

# Set error handling
set -e

# Log file for the daemon itself
DAEMON_LOG="/Users/fsiqueira/Desktop/GitHub/omega-btc-ai/src/omega_bot_farm/qa/local_run/logs/daemon_runner_$(date +%Y%m%d_%H%M%S).log"
echo "Starting daemon at $(date)" > "$DAEMON_LOG"

# Navigate to the project root
cd "/Users/fsiqueira/Desktop/GitHub/omega-btc-ai" || { echo "Failed to navigate to project root" >> "$DAEMON_LOG"; exit 1; }

# Log the command
echo "Running command: /Users/fsiqueira/Desktop/GitHub/omega-btc-ai/venv/bin/python -m src.omega_bot_farm.qa.run_cyber1t4l_locally --mode full" >> "$DAEMON_LOG"

# Run with full path to Python to avoid any PATH issues
exec "/Users/fsiqueira/Desktop/GitHub/omega-btc-ai/venv/bin/python" -m src.omega_bot_farm.qa.run_cyber1t4l_locally --mode full >> "$DAEMON_LOG" 2>&1
