from setuptools import setup, find_packages

setup(
    name="omega-btc-ai",
    version="0.3.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
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
) 