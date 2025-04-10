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
import time
import hmac
import hashlib
import base64

# API credentials
api_key = 'bg_c1b989edd804f4b3d06e3faca31be313'
secret_key = 'd6a94d146ae504f68b7d0f8f9acefb41cd991aeb110608ad16526d752fc0138a'
passphrase = 'aa03d3d008af2e989'

# Generate timestamp
timestamp = str(int(time.time() * 1000))

# Endpoint details
method = 'GET'
request_path = '/api/mix/v1/account/accounts'
query_string = '?productType=umcbl'
url = 'https://api.bitget.com' + request_path + query_string

# Create message to sign
message = timestamp + method + request_path + query_string

# Generate signature (base64-encoded)
signature = base64.b64encode(
    hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
).decode('utf-8')

# Headers with complete authentication
headers = {
    'ACCESS-KEY': api_key,
    'ACCESS-SIGN': signature,
    'ACCESS-TIMESTAMP': timestamp,
    'ACCESS-PASSPHRASE': passphrase,
    'Content-Type': 'application/json'
}

print(f'Testing API Key: {api_key}')
print(f'Secret Key: {secret_key[:5]}...{secret_key[-5:]}')  # Show first and last 5 chars
print(f'Passphrase: {passphrase}')
print(f'Timestamp: {timestamp}')
print(f'Message to sign: {message}')
print(f'Generated signature: {signature}')
print(f'Making request to: {url}')
response = requests.get(url, headers=headers)

print(f'Status code: {response.status_code}')
print(f'Response: {json.dumps(response.json(), indent=2) if response.content else "No content"}') 