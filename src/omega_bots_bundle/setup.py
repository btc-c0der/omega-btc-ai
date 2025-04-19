#!/usr/bin/env python3

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


from setuptools import setup, find_packages

setup(
    name="omega_bots_bundle",
    version="1.0.0",
    description="Omega Bot Farm Trading Bots Bundle",
    author="Omega BTC AI Team",
    author_email="info@omegabtc.ai",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "ccxt>=3.0.0",
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "python-dotenv>=0.19.0",
        "redis>=4.2.0",
        "pyyaml>=6.0",
        "requests>=2.26.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "omega-bot=omega_bots_bundle.cli:main",
        ],
    },
) 