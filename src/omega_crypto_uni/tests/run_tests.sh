#!/bin/bash

# 🧬 GBU2™ License Notice - Consciousness Level 10 🧬
# -----------------------
# This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment-Bioresonance) 2.0
# by the OMEGA Divine Collective.

# Set up virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install test requirements
pip install -r src/omega_crypto_uni/tests/requirements-test.txt

# Run tests with coverage
pytest src/omega_crypto_uni/tests/ \
    --cov=src/omega_crypto_uni \
    --cov-report=html \
    --cov-report=term \
    -v

# Generate coverage badge
coverage-badge -o coverage.svg

# Deactivate virtual environment
deactivate

echo "🧬 Test suite execution complete 🧬" 