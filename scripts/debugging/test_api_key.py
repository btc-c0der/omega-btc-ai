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


import requests
import json

# API Key to test
api_key = 'bg_c1b989edd804f4b3d06e3faca31be313'

# Public endpoint URL
url = 'https://api.bitget.com/api/mix/v1/account/accounts?productType=umcbl'

# Simple request with just the API key in the header (no signature)
headers = {
    'ACCESS-KEY': api_key,
    'Content-Type': 'application/json'
}

print(f'Testing API Key: {api_key}')
print(f'Making request to: {url}')
response = requests.get(url, headers=headers)

print(f'Status code: {response.status_code}')
print(f'Response: {json.dumps(response.json(), indent=2)}') 