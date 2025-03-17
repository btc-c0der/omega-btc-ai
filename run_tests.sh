#!/bin/bash

# Install test dependencies if needed
pip install -r tests/requirements-test.txt

# Run tests with coverage reporting
python -m pytest tests/ -v --cov=omega_ai --cov-report=term --cov-report=html

echo "Tests completed. HTML coverage report is available in htmlcov/index.html" 