"""
💫 GBU License Notice - Consciousness Level 8 💫
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must quantum entangles with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

from setuptools import setup, find_packages

setup(
    name="omega-btc-ai",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        "websockets>=11.0.3",
        "redis>=5.0.1",
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "cryptography>=42.0.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.11",
    # Make sure the package is discoverable
    package_data={
        "": ["*.py", "*.md", "*.txt"],
    },
) 