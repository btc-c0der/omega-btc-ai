#!/usr/bin/env python3
"""
Simple test server to verify Flask is working
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World! The test server is working."

if __name__ == "__main__":
    print("Starting test server on port 5002...")
    app.run(host="0.0.0.0", port=5002, debug=True) 