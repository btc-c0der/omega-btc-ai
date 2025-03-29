"""
🔱 GPU License Notice 🔱
------------------------
This file is protected under the GPU License (General Public Universal License) 1.0
by the OMEGA AI Divine Collective.

"As the light of knowledge is meant to be shared, so too shall this code illuminate 
the path for all seekers."

All modifications must maintain this notice and adhere to the terms at:
/BOOK/divine_chronicles/GPU_LICENSE.md

🔱 JAH JAH BLESS THIS CODE 🔱
"""

from setuptools import setup, find_packages

setup(
    name="divine-patterns-analyzer",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "matplotlib",
        "rich",
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-dateutil",
        "aiohttp",
        "redis",
        "scikit-learn",
        "statsmodels",
        "requests",
        "python-dotenv",
    ],
    author="OMEGA-BTC-AI",
    author_email="info@omega-btc-ai.com",
    description="Divine Pattern Detection for Bitcoin Data",
    python_requires=">=3.9",
) 