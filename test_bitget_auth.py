#!/usr/bin/env python3

import hmac
import hashlib
import base64
import time
import requests

api_key = 'bg_c1b989edd804f4b3d06e3faca31be313'
secret_key = 'd6a94d146ae504f68b7d0f8f9acefb41cd991aeb110608ad16526d752fc0138a'
passphrase = 'aa03d3d008af2e989'

timestamp = str(int(time.time() * 1000))
method = 'GET'
request_path = '/api/mix/v1/position/allPosition'
query_string = '?marginCoin=USDT&productType=umcbl&symbol=BTCUSDT_UMCBL'

message = timestamp + method + request_path + query_string

signature = base64.b64encode(
    hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
).decode('utf-8')

print(f'Timestamp: {timestamp}')
print(f'Message: {message}')
print(f'Signature: {signature}')

headers = {
    'ACCESS-KEY': api_key,
    'ACCESS-SIGN': signature,
    'ACCESS-TIMESTAMP': timestamp,
    'ACCESS-PASSPHRASE': passphrase,
    'Content-Type': 'application/json',
}

url = 'https://api.bitget.com' + request_path + query_string
print(f'Making request to: {url}')
response = requests.get(url, headers=headers)

print(f'Status code: {response.status_code}')
print(f'Response: {response.text}') 