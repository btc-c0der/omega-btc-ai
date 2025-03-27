#!/usr/bin/env python3
"""
🔮 GPU (General Public Universal) License 1.0
--------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GPU (General Public Universal) License v1.0
Date: 2025-03-28
Location: The Cosmic Void
"""

from setuptools import setup, find_packages

setup(
    name="omega-btc-ai",
    version="0.5.1",
    description="OMEGA BTC AI - BTC Live Feed v3",
    author="OMEGA BTC AI DIVINE COLLECTIVE",
    author_email="divine@omega-btc-ai.com",
    url="https://github.com/btc-c0der/omega-btc-ai",
    packages=find_packages(),
    scripts=[
        "scripts/monitor_btc_feed_v3.py",
    ],
    install_requires=[
        "websocket-client>=1.3.1",
        "redis>=4.3.4",
        "requests>=2.27.1",
        "fastapi>=0.95.0",
        "uvicorn>=0.21.1",
        "pydantic>=1.9.0",
        "python-dotenv>=0.19.2",
        "colorama>=0.4.4",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: GPU License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.9",
    license="GPU License",
) 