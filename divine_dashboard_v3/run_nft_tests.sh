#!/bin/bash

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


# Set environment variables for testing
export PYTHONPATH="$(pwd)/.."
export NFT_API_KEY="test_api_key"
export NFT_CONTRACT_ADDRESS="0xTESTCONTRACT"

# Create output directory if it doesn't exist
mkdir -p nft_output

# Run tests with coverage
python -m pytest components/nft/test_nft_components.py -v --cov=components.nft --cov-report=term --cov-report=html:coverage_report

# Print summary
echo ""
echo "✨ NFT Component Tests Complete ✨"
echo "Coverage report saved to coverage_report/index.html"

# Target coverage check
COVERAGE=$(python -c "import xml.etree.ElementTree as ET; tree = ET.parse('coverage.xml'); root = tree.getroot(); print(root.attrib['line-rate'])")
TARGET=0.9

if (( $(echo "$COVERAGE >= $TARGET" | bc -l) )); then
    echo "🎉 Target coverage of ${TARGET}% achieved! Current coverage: $(echo "$COVERAGE * 100" | bc -l)%"
else
    echo "⚠️ Coverage below target. Current: $(echo "$COVERAGE * 100" | bc -l)%, Target: $(echo "$TARGET * 100" | bc -l)%"
fi 