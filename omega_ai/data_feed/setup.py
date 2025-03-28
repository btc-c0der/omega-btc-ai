from setuptools import setup, find_packages

setup(
    name="omega_ai",
    version="0.420",
    packages=find_packages(),
    install_requires=[
        "websockets>=11.0.3",
        "redis>=5.0.1",
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "cryptography>=42.0.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0"
    ],
    python_requires=">=3.11.8",
) 