#!/usr/bin/env python3
"""
OMEGA BTC AI - BitGet API Environment Test
==========================================

A simple script to test the BitGet API signature using credentials from the .env file.
This verifies that the dotenv integration with the BitGet signature test is working.

Author: OMEGA BTC AI Team
"""

import os
import sys
from dotenv import load_dotenv
from colorama import Fore, Style, init
from omega_ai.scripts.debug.bitget_signature_test import BitGetSignatureTest

# Initialize colorama
init(autoreset=True)

def main():
    """Main entry point."""
    print(f"{Fore.CYAN}=============================={Style.RESET_ALL}")
    print(f"{Fore.CYAN}BitGet API Env Test{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=============================={Style.RESET_ALL}")
    
    # Load environment variables from .env file in the project root
    try:
        # Get the absolute path to the project root
        project_root = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(project_root, '.env')
        
        if os.path.exists(env_path):
            load_dotenv(env_path)
            print(f"{Fore.GREEN}Loaded environment from {env_path}{Style.RESET_ALL}")
            
            # Print available environment variables related to BitGet
            if 'BITGET_API_KEY' in os.environ:
                api_key = os.environ['BITGET_API_KEY']
                print(f"{Fore.CYAN}Found BITGET_API_KEY: {api_key[:5]}...{api_key[-3:] if len(api_key) > 5 else ''}{Style.RESET_ALL}")
            if 'BITGET_SECRET_KEY' in os.environ:
                print(f"{Fore.CYAN}Found BITGET_SECRET_KEY with length: {len(os.environ['BITGET_SECRET_KEY'])}{Style.RESET_ALL}")
            if 'BITGET_PASSPHRASE' in os.environ:
                print(f"{Fore.CYAN}Found BITGET_PASSPHRASE with length: {len(os.environ['BITGET_PASSPHRASE'])}{Style.RESET_ALL}")
            
            # Check for testnet credentials too
            if 'BITGET_TESTNET_API_KEY' in os.environ:
                testnet_api_key = os.environ['BITGET_TESTNET_API_KEY']
                print(f"{Fore.CYAN}Found BITGET_TESTNET_API_KEY: {testnet_api_key[:5]}...{testnet_api_key[-3:] if len(testnet_api_key) > 5 else ''}{Style.RESET_ALL}")
            if 'BITGET_TESTNET_SECRET_KEY' in os.environ:
                print(f"{Fore.CYAN}Found BITGET_TESTNET_SECRET_KEY with length: {len(os.environ['BITGET_TESTNET_SECRET_KEY'])}{Style.RESET_ALL}")
            if 'BITGET_TESTNET_PASSPHRASE' in os.environ:
                print(f"{Fore.CYAN}Found BITGET_TESTNET_PASSPHRASE with length: {len(os.environ['BITGET_TESTNET_PASSPHRASE'])}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No .env file found at {env_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error loading .env file: {str(e)}{Style.RESET_ALL}")
        
    # Default to testnet
    use_testnet = True
    
    # Determine if we have mainnet or testnet credentials
    if 'BITGET_API_KEY' in os.environ and 'BITGET_SECRET_KEY' in os.environ and 'BITGET_PASSPHRASE' in os.environ:
        print(f"{Fore.GREEN}Found mainnet credentials, using those for test.{Style.RESET_ALL}")
        use_testnet = False
    elif 'BITGET_TESTNET_API_KEY' in os.environ and 'BITGET_TESTNET_SECRET_KEY' in os.environ and 'BITGET_TESTNET_PASSPHRASE' in os.environ:
        print(f"{Fore.YELLOW}Found testnet credentials, using those for test.{Style.RESET_ALL}")
        use_testnet = True
    else:
        print(f"{Fore.RED}No complete set of credentials found. Please check your .env file.{Style.RESET_ALL}")
        sys.exit(1)
        
    # Create the signature test instance
    tester = BitGetSignatureTest(
        use_testnet=use_testnet,
        debug=True,
        # No need to pass API credentials as they'll be loaded from environment
    )
    
    # Run a simple test of signature comparison
    print(f"\n{Fore.CYAN}Testing signature generation...{Style.RESET_ALL}")
    params = {"symbol": "BTCUSDT_UMCBL"}
    tester.compare_signatures("GET", "/api/mix/v1/market/ticker", params=params)
    
    # Test a simple API call
    print(f"\n{Fore.CYAN}Testing API authentication (ticker endpoint)...{Style.RESET_ALL}")
    result = tester.make_request("GET", "/api/mix/v1/market/ticker", params=params, version=1)
    
    if "error" not in result:
        print(f"{Fore.GREEN}Success! API authentication is working properly.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Failed! API authentication is not working. Check your credentials.{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}Test completed.{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 