#!/bin/bash
# Install dependencies for Discord bot testing
# This script installs all required and optional packages for testing Discord bot interactions

echo "🧪 Installing Test Dependencies for CyBer1t4L QA Bot 🧪"
echo "=============================================="

# Core testing packages
echo "📦 Installing core testing packages..."
pip install pytest pytest-asyncio pytest-cov pytest-depends

# Discord extension for testing
echo "📦 Installing discord.ext.test..."
pip install -U discord.ext.test

# Make sure discord.py is installed and up-to-date
echo "📦 Ensuring discord.py is installed and up-to-date..."
pip install -U "discord.py>=2.1.0"

# HTTP testing packages (required for live testing)
echo "📦 Installing HTTP testing packages..."
pip install httpx python-dotenv requests

# Respx for mocking HTTP responses (optional)
echo "📦 Installing respx for HTTP mocking (optional)..."
pip install respx starlette

# VCR.py for recording and replaying real Discord interactions
echo "📦 Installing VCR.py for recording real interactions..."
pip install vcrpy

# Install pytest-xdist for parallel test execution (optional)
echo "📦 Installing pytest-xdist for parallel testing (optional)..."
pip install pytest-xdist

echo "=============================================="
echo "✅ All dependencies installed successfully"
echo ""
echo "Run tests with:"
echo "python -m src.omega_bot_farm.qa.tests.run_discord_tests --install-deps --html"
echo ""
echo "Run live tests with:"
echo "python -m src.omega_bot_farm.qa.tests.run_discord_tests --live"
echo "==============================================" 