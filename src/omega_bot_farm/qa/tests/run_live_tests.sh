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

# Script to run live tests for the CyBer1t4L QA Bot
# This script automatically generates HTML coverage reports for review

# Display fancy cool box
cat << "EOF"
=====================================================================
=                                                                   =
=   █▀▀ █ █ █▀▄ █▀▀ █▀█ ▄▄ ▀█ ▀█▀ █ █ █    ▄▀█  █▀▄ █▀█ ▀█▀       =
=   █▄▄ ▀▄▀ █▀▄ ██▄ █▀▄    █  █  ▀▄▀ █▄▄   █▀█  █▄▀ █▄█  █        =
=                                                                   =
=                      LIVE DISCORD INTEGRATION TESTS               =
=                                                                   =
=====================================================================
EOF

# Set the current directory to the project root
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "/Users/fsiqueira/Desktop/GitHub/omega-btc-ai")
cd "$PROJECT_ROOT"

# Set up the report directory
REPORT_DIR="$PROJECT_ROOT/src/omega_bot_farm/qa/tests/reports/html"
mkdir -p "$REPORT_DIR"

# Run the tests with coverage reporting
echo "Running live tests with CyBer1t4L QA Bot..."
echo "Writing coverage HTML reports to: $REPORT_DIR"

# Execute pytest with coverage, ensuring HTML reports are generated
python -m pytest -xs \
    src/omega_bot_farm/qa/tests/test_discord_interactions.py \
    src/omega_bot_farm/qa/tests/test_discord_basic.py \
    src/omega_bot_farm/qa/tests/test_discord_connection.py \
    src/omega_bot_farm/qa/tests/test_discord_integration.py \
    --cov=src.omega_bot_farm.qa.cyber1t4l_qa_bot \
    --cov-report=term \
    --cov-report=html:"$REPORT_DIR"

# Celebrate the completion
echo -e "\n✨ Live tests complete! ✨\n" 