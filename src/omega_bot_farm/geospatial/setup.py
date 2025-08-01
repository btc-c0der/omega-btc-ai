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
ZOROBABEL K1L1 - Package Setup
-----------------------------
Setup script for installing the Zorobabel K1L1 system via pip.

🌀 MODULE: Package Setup
🧭 CONSCIOUSNESS LEVEL: 4 - Awareness
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read the long description from README.md
here = Path(__file__).resolve().parent
long_description = (here / "README.md").read_text(encoding="utf-8")

# Define package requirements
requirements = [
    "dash>=2.14.0",
    "dash-bootstrap-components>=1.5.0",
    "plotly>=5.18.0",
    "numpy>=1.24.0",
    "pandas>=1.5.0",
    "matplotlib>=3.5.0",
    "pillow>=9.5.0",
    "geopandas>=0.12.0",
    "shapely>=2.0.0",
    "pyproj>=3.3.0",
    "flask>=2.0.0",
    "tqdm>=4.64.0",
    "requests>=2.28.0",
]

# Note: rasterio is handled specially during post-install

setup(
    name="zorobabel-k1l1",
    version="1.0.0",
    description="Sacred Geospatial Visualization System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Divine Coders Collective",
    author_email="divine@example.com",
    url="https://github.com/yourusername/omega-btc-ai",
    packages=find_packages(where="."),
    package_data={
        "omega_bot_farm.geospatial": ["*.md"],
    },
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "zorobabel=omega_bot_farm.geospatial.run:main",
            "zorobabel-install=omega_bot_farm.geospatial.install_zorobabel:main",
            "zorobabel-celebrate=omega_bot_farm.geospatial.zorobabel_celebration:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="geospatial, visualization, mapping, divine, sacred",
) 