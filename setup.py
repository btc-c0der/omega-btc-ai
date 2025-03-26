from setuptools import setup, find_packages

setup(
    name="omega_ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "redis",
        "fastapi",
        "uvicorn",
        "websockets",
        "numpy",
        "pandas"
    ],
) 