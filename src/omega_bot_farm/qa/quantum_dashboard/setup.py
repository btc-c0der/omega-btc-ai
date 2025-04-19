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

"""
Setup script for the Quantum 5D QA Dashboard.
"""

from setuptools import setup, find_packages

setup(
    name="quantum_dashboard",
    version="1.0.0",
    description="A multi-dimensional quality assurance dashboard for monitoring quantum metrics",
    author="Omega BTC AI Team",
    author_email="info@omegabtc.ai",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "dash>=3.0.0",
        "dash-bootstrap-components>=2.0.0",
        "plotly>=6.0.0",
        "pandas>=2.0.0",
        "numpy>=1.22.0",
    ],
    entry_points={
        "console_scripts": [
            "quantum-dashboard=quantum_dashboard.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
) 