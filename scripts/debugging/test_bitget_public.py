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

# Test a public endpoint that doesn't require authentication
url = 'https://api.bitget.com/api/mix/v1/market/ticker?symbol=BTCUSDT_UMCBL&productType=umcbl'

print(f'Making request to: {url}')
response = requests.get(url)

print(f'Status code: {response.status_code}')
print(f'Response: {json.dumps(response.json(), indent=2)}') 