from setuptools import setup, find_packages

setup(
    name="omega-btc-ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-cors",
        "flask-socketio",
        "gevent-websocket",
        "redis",
        "ccxt",
    ],
) 