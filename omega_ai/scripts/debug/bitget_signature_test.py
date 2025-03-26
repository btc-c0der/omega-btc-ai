#!/usr/bin/env python3
"""
OMEGA BTC AI - BitGet API Signature Test Tool
=============================================

This utility script helps debug BitGet API authentication issues by:
1. Generating and displaying signatures with the same parameters using different methods
2. Testing basic API calls to validate authentication
3. Providing detailed request/response information

Author: OMEGA BTC AI Team
"""

import os
import sys
import hmac
import base64
import hashlib
import json
import time
import requests
import argparse
from urllib.parse import urlencode
from colorama import Fore, Style, init
from typing import Dict, Any, Optional
from dotenv import load_dotenv  # Add dotenv import

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Initialize colorama
init(autoreset=True)

class BitGetSignatureTest:
    """Test BitGet API signature generation and authentication."""
    
    def __init__(self,
                 api_key: str = "",
                 secret_key: str = "",
                 passphrase: str = "",
                 use_testnet: bool = True,
                 debug: bool = True,
                 sub_account_name: Optional[str] = None):
        """
        Initialize the signature test.
        
        Args:
            api_key: BitGet API key
            secret_key: BitGet secret key
            passphrase: BitGet API passphrase
            use_testnet: Whether to use testnet (default: True)
            debug: Enable debug mode (default: True)
            sub_account_name: Sub-account name for API requests (optional)
        """
        self.use_testnet = use_testnet
        self.debug = debug
        self.sub_account_name = sub_account_name
        
        # Set API URLs based on testnet or mainnet
        if use_testnet:
            self.api_url = "https://api-testnet.bitget.com"
        else:
            self.api_url = "https://api.bitget.com"
            
        # Get API credentials from parameters or environment variables
        self.api_key = api_key or os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        self.secret_key = secret_key or os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        self.passphrase = passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        
        # Get sub-account name from environment variable if not provided
        if not self.sub_account_name:
            # Try both strategic and general sub account env vars
            self.sub_account_name = os.environ.get("STRATEGIC_SUB_ACCOUNT_NAME") or os.environ.get("SUB_ACCOUNT_NAME")
        
        # Verify API credentials
        if not self.api_key or not self.secret_key or not self.passphrase:
            # Check both testnet and mainnet credentials
            if not use_testnet:
                # If we're in mainnet mode, try testnet credentials as fallback
                self.api_key = self.api_key or os.environ.get("BITGET_TESTNET_API_KEY", "")
                self.secret_key = self.secret_key or os.environ.get("BITGET_TESTNET_SECRET_KEY", "")
                self.passphrase = self.passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE", "")
                
                if self.api_key and self.secret_key and self.passphrase:
                    print(f"{Fore.YELLOW}No mainnet credentials found, using testnet credentials instead.{Style.RESET_ALL}")
                    self.use_testnet = True
                    self.api_url = "https://api-testnet.bitget.com"
            else:
                # If we're in testnet mode, try mainnet credentials as fallback
                self.api_key = self.api_key or os.environ.get("BITGET_API_KEY", "")
                self.secret_key = self.secret_key or os.environ.get("BITGET_SECRET_KEY", "")
                self.passphrase = self.passphrase or os.environ.get("BITGET_PASSPHRASE", "")
                
                if self.api_key and self.secret_key and self.passphrase:
                    print(f"{Fore.YELLOW}No testnet credentials found, using mainnet credentials instead.{Style.RESET_ALL}")
                    self.use_testnet = False
                    self.api_url = "https://api.bitget.com"
                    
        # Final check for credentials
        if not self.api_key or not self.secret_key or not self.passphrase:
            print(f"{Fore.RED}Error: API credentials missing. Please provide API key, secret key, and passphrase.{Style.RESET_ALL}")
            sys.exit(1)
        
        print(f"{Fore.GREEN}API credentials loaded. API Key: {self.api_key[:5]}...{self.api_key[-3:] if len(self.api_key) > 5 else ''}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Secret Key Length: {len(self.secret_key)} characters{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Passphrase Length: {len(self.passphrase)} characters{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Using: {'TESTNET' if self.use_testnet else 'MAINNET'}{Style.RESET_ALL}")
        
        if self.sub_account_name:
            print(f"{Fore.GREEN}Using sub-account: {self.sub_account_name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No sub-account specified{Style.RESET_ALL}")
    
    def generate_signature_v1(self, timestamp, method, request_path, body=None, params=None):
        """
        Generate signature using implementation version 1.
        
        This matches the implementation from the BitGetWalletQuery class.
        """
        # Ensure method is uppercase
        method = method.upper()
        
        # Start with timestamp + method + requestPath
        message = str(timestamp) + method + request_path
        
        # Add query string if present (for GET requests)
        if params and method == "GET":
            # Sort parameters by key
            sorted_params = sorted(params.items())
            # Create query string
            query_string = "&".join([f"{key}={value}" for key, value in sorted_params])
            # Add to message with question mark
            message += "?" + query_string
        
        # Add request body if present (for POST requests)
        if body and method == "POST":
            if isinstance(body, dict):
                message += json.dumps(body)
            else:
                message += body
        
        # Create signature using HMAC-SHA256
        signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode("utf-8"),
                message.encode("utf-8"),
                hashlib.sha256
            ).digest()
        ).decode("utf-8")
        
        return signature, message
    
    def generate_signature_v2(self, timestamp, method, request_path, body=None, params=None):
        """
        Generate signature using implementation version 2.
        
        This matches the implementation from your example code.
        """
        # Ensure method is uppercase
        method = method.upper()
        
        # Combine timestamp and request parameters
        request_params = request_path
        
        # Add query parameters for GET requests
        if params and method == "GET":
            query_string = urlencode(sorted(params.items()))
            request_params += "?" + query_string
        
        # Add body for POST requests (not in your original example but necessary)
        if body and method == "POST":
            if isinstance(body, dict):
                request_params += json.dumps(body)
            else:
                request_params += body
        
        # Create the message
        message = str(timestamp) + method + request_params
        
        # Create signature using HMAC-SHA256
        signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode("utf-8"),
                message.encode("utf-8"),
                hashlib.sha256
            ).digest()
        ).decode("utf-8")
        
        return signature, message
    
    def make_request(self, method, endpoint, params=None, body=None, version=1):
        """
        Make an authenticated request to the BitGet API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint to access
            params: Query parameters for GET requests
            body: Request body for POST requests
            version: Signature generation version to use (1 or 2)
            
        Returns:
            Response data from the API
        """
        # Initialize params if None
        if params is None:
            params = {}
            
        # Add sub-account parameter for appropriate endpoints
        # Skip adding it to market data endpoints which don't support subAccountName
        if self.sub_account_name and not any(x in endpoint for x in ["/market/", "/public/"]):
            params["subAccountName"] = self.sub_account_name
            
        # Prepare the request
        url = self.api_url + endpoint
        timestamp = str(int(time.time() * 1000))
        
        # Generate signature based on selected version
        if version == 1:
            signature, pre_sign_message = self.generate_signature_v1(timestamp, method, endpoint, body, params)
        else:
            signature, pre_sign_message = self.generate_signature_v2(timestamp, method, endpoint, body, params)
        
        # Prepare headers with authentication
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }
        
        if self.debug:
            print(f"\n{Fore.YELLOW}=== API Request Details ==={Style.RESET_ALL}")
            print(f"URL: {url}")
            print(f"Method: {method}")
            print(f"Timestamp: {timestamp}")
            print(f"Params: {params}")
            print(f"Body: {body}")
            print(f"Pre-sign message: {pre_sign_message}")
            print(f"Signature: {signature}")
            print(f"Headers: {json.dumps({k: v for k, v in headers.items() if k != 'ACCESS-SIGN'}, indent=2)}")
            if self.sub_account_name:
                print(f"Using sub-account: {self.sub_account_name}")
        
        # Build URL with query parameters for GET requests
        if method.upper() == "GET" and params:
            query_string = urlencode(params)
            url += "?" + query_string
        
        # Make the request
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=body, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            # Check if response is valid JSON
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {"error": "Invalid JSON response", "text": response.text}
                
            if self.debug:
                print(f"\n{Fore.YELLOW}=== API Response Details ==={Style.RESET_ALL}")
                print(f"Status Code: {response.status_code}")
                print(f"Response: {json.dumps(response_data, indent=2)}")
                
            # Check for successful response
            if response.status_code == 200 and response_data.get("code") == "00000":
                print(f"{Fore.GREEN}✓ Request successful!{Style.RESET_ALL}")
                return response_data.get("data", {})
            else:
                print(f"{Fore.RED}✗ Request failed: {response_data.get('msg', 'Unknown error')}{Style.RESET_ALL}")
                return {"error": response_data.get("msg", "Unknown error")}
                
        except Exception as e:
            error_message = f"Request error: {str(e)}"
            print(f"{Fore.RED}✗ {error_message}{Style.RESET_ALL}")
            return {"error": error_message}
    
    def compare_signatures(self, method, endpoint, params=None, body=None):
        """Compare signature generation between different implementations."""
        timestamp = str(int(time.time() * 1000))
        
        # Generate signatures using both versions
        sig1, msg1 = self.generate_signature_v1(timestamp, method, endpoint, body, params)
        sig2, msg2 = self.generate_signature_v2(timestamp, method, endpoint, body, params)
        
        # Print comparison
        print(f"\n{Fore.CYAN}=== Signature Comparison ==={Style.RESET_ALL}")
        print(f"Timestamp: {timestamp}")
        print(f"Method: {method}")
        print(f"Endpoint: {endpoint}")
        print(f"Params: {params}")
        print(f"Body: {body}")
        print(f"\n{Fore.YELLOW}Version 1:{Style.RESET_ALL}")
        print(f"Pre-sign message: {msg1}")
        print(f"Signature: {sig1}")
        print(f"\n{Fore.YELLOW}Version 2:{Style.RESET_ALL}")
        print(f"Pre-sign message: {msg2}")
        print(f"Signature: {sig2}")
        
        # Check if signatures match
        if sig1 == sig2:
            print(f"\n{Fore.GREEN}Both signature implementations match!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}Signatures do not match!{Style.RESET_ALL}")
        
        return {
            "timestamp": timestamp,
            "version1": {"message": msg1, "signature": sig1},
            "version2": {"message": msg2, "signature": sig2},
            "match": sig1 == sig2
        }
    
    def test_api_endpoints(self):
        """Test basic API endpoints to verify authentication."""
        # Test 1: Get ticker - simple GET request without parameters
        print(f"\n{Fore.CYAN}=== Test 1: Get Ticker (GET) ==={Style.RESET_ALL}")
        params = {"symbol": "BTCUSDT_UMCBL"}
        self.make_request("GET", "/api/mix/v1/market/ticker", params=params, version=1)
        
        # Test 2: Get account balance - GET request with authentication
        print(f"\n{Fore.CYAN}=== Test 2: Get Account Balance (GET) ==={Style.RESET_ALL}")
        params = {"productType": "umcbl", "marginCoin": "USDT"}
        self.make_request("GET", "/api/mix/v1/account/account", params=params, version=1)
        
        # Test 3: Compare with Version 2 signature
        print(f"\n{Fore.CYAN}=== Test 3: Get Account Balance with Version 2 Signature (GET) ==={Style.RESET_ALL}")
        self.make_request("GET", "/api/mix/v1/account/account", params=params, version=2)
        
        # Test 4: Place a mock order - POST request (will not execute on testnet)
        print(f"\n{Fore.CYAN}=== Test 4: Mock Order Placement (POST) ==={Style.RESET_ALL}")
        order_body = {
            "symbol": "BTCUSDT_UMCBL",
            "marginCoin": "USDT",
            "size": "0.001",
            "side": "open_long",
            "orderType": "market",
            "timeInForceValue": "normal"
        }
        self.make_request("POST", "/api/mix/v1/order/placeOrder", body=order_body, version=1)
        
        # Test 5: Get sub-account assets (if sub-account is specified)
        if self.sub_account_name:
            print(f"\n{Fore.CYAN}=== Test 5: Get Sub-Account Assets (GET) ==={Style.RESET_ALL}")
            params = {"productType": "umcbl"}
            # Note: We're not adding subAccountName here because it's handled in make_request
            self.make_request("GET", "/api/mix/v1/account/account", params=params, version=1)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='BitGet API Signature Test Tool')
    parser.add_argument('--testnet', action='store_true', 
                      help='Use testnet (default)')
    parser.add_argument('--mainnet', action='store_true', 
                      help='Use mainnet')
    parser.add_argument('--api-key', type=str, default='',
                      help='BitGet API key')
    parser.add_argument('--secret-key', type=str, default='',
                      help='BitGet secret key')
    parser.add_argument('--passphrase', type=str, default='',
                      help='BitGet API passphrase')
    parser.add_argument('--compare-only', action='store_true',
                      help='Only compare signature generation, do not make API calls')
    parser.add_argument('--debug', action='store_true',
                      help='Enable detailed debug output')
    parser.add_argument('--sub-account', type=str, default='',
                      help='Sub-account name to use for API requests')
    
    return parser.parse_args()

def main():
    """Main entry point."""
    # Load environment variables from .env file
    try:
        # Try to load from specified file paths in order of preference
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
        env_paths = [
            os.path.join(root_dir, '.env'),  # Project root .env
            '.env',                           # Current directory .env
            os.path.join(os.path.dirname(__file__), '.env'),  # Script directory .env
        ]
        env_loaded = False
        
        for env_path in env_paths:
            if os.path.exists(env_path):
                load_dotenv(env_path)
                print(f"{Fore.GREEN}Loaded environment from {env_path}{Style.RESET_ALL}")
                env_loaded = True
                
                # Print available environment variables related to BitGet
                if 'BITGET_API_KEY' in os.environ:
                    print(f"{Fore.CYAN}Found BITGET_API_KEY in environment with length: {len(os.environ['BITGET_API_KEY'])}{Style.RESET_ALL}")
                if 'BITGET_SECRET_KEY' in os.environ:
                    print(f"{Fore.CYAN}Found BITGET_SECRET_KEY in environment with length: {len(os.environ['BITGET_SECRET_KEY'])}{Style.RESET_ALL}")
                if 'BITGET_PASSPHRASE' in os.environ:
                    print(f"{Fore.CYAN}Found BITGET_PASSPHRASE in environment with length: {len(os.environ['BITGET_PASSPHRASE'])}{Style.RESET_ALL}")
                
                # Check for testnet credentials too
                if 'BITGET_TESTNET_API_KEY' in os.environ:
                    print(f"{Fore.CYAN}Found BITGET_TESTNET_API_KEY in environment with length: {len(os.environ['BITGET_TESTNET_API_KEY'])}{Style.RESET_ALL}")
                if 'BITGET_TESTNET_SECRET_KEY' in os.environ:
                    print(f"{Fore.CYAN}Found BITGET_TESTNET_SECRET_KEY in environment with length: {len(os.environ['BITGET_TESTNET_SECRET_KEY'])}{Style.RESET_ALL}")
                if 'BITGET_TESTNET_PASSPHRASE' in os.environ:
                    print(f"{Fore.CYAN}Found BITGET_TESTNET_PASSPHRASE in environment with length: {len(os.environ['BITGET_TESTNET_PASSPHRASE'])}{Style.RESET_ALL}")
                
                break
                
        if not env_loaded:
            print(f"{Fore.YELLOW}No .env file found, using system environment variables{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error loading .env file: {str(e)}{Style.RESET_ALL}")
    
    args = parse_args()
    
    # Use testnet by default, unless mainnet is specified
    use_testnet = not args.mainnet
    
    # Create test instance
    tester = BitGetSignatureTest(
        api_key=args.api_key,
        secret_key=args.secret_key,
        passphrase=args.passphrase,
        use_testnet=use_testnet,
        debug=args.debug,
        sub_account_name=args.sub_account
    )
    
    # Print header
    print(f"\n{Fore.CYAN}=============================={Style.RESET_ALL}")
    print(f"{Fore.CYAN}BitGet API Signature Test Tool{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=============================={Style.RESET_ALL}")
    
    # Compare signatures for a few common scenarios
    print(f"\n{Fore.CYAN}Testing signature generation...{Style.RESET_ALL}")
    
    # Test with typical parameters
    params = {"symbol": "BTCUSDT_UMCBL"}
    
    # Add sub-account to test params if provided
    if tester.sub_account_name:
        params_with_sub = params.copy()
        params_with_sub["subAccountName"] = tester.sub_account_name
        
        print(f"\n{Fore.CYAN}Comparing signatures WITH sub-account parameter:{Style.RESET_ALL}")
        tester.compare_signatures("GET", "/api/mix/v1/market/ticker", params=params_with_sub)
    
    # Test 1: Simple GET with params (without sub-account)
    print(f"\n{Fore.CYAN}Comparing signatures WITHOUT sub-account parameter:{Style.RESET_ALL}")
    tester.compare_signatures("GET", "/api/mix/v1/market/ticker", params=params)
    
    # Test 2: GET with multiple params
    params_multi = {"productType": "umcbl", "marginCoin": "USDT"}
    if tester.sub_account_name:
        params_multi["subAccountName"] = tester.sub_account_name
    tester.compare_signatures("GET", "/api/mix/v1/account/account", params=params_multi)
    
    # Test 3: POST with body
    order_body = {
        "symbol": "BTCUSDT_UMCBL",
        "marginCoin": "USDT",
        "size": "0.001",
        "side": "open_long",
        "orderType": "market",
        "timeInForceValue": "normal"
    }
    tester.compare_signatures("POST", "/api/mix/v1/order/placeOrder", body=order_body)
    
    # Only make API calls if not in compare-only mode
    if not args.compare_only:
        print(f"\n{Fore.CYAN}Testing API authentication...{Style.RESET_ALL}")
        tester.test_api_endpoints()
    
    print(f"\n{Fore.GREEN}Test completed.{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 