#!/usr/bin/env python3

import requests
import json

# Test a public endpoint that doesn't require authentication
url = 'https://api.bitget.com/api/mix/v1/market/ticker?symbol=BTCUSDT_UMCBL&productType=umcbl'

print(f'Making request to: {url}')
response = requests.get(url)

print(f'Status code: {response.status_code}')
print(f'Response: {json.dumps(response.json(), indent=2)}') 