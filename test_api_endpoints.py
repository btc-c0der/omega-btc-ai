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

"""
Test script for OMEGA BTC AI Dashboard API endpoints
JAH BLESS! 🙏
"""

import requests
import json
from datetime import datetime
import sys
from typing import Dict, Any
import time

# API Configuration
BASE_URL = "http://localhost:5000"
ENDPOINTS = {
    "health": "/api/health",
    "trap_probability": "/api/trap-probability",
    "position": "/api/position",
    "btc_price": "/api/btc-price",
    "data": "/api/data"
}

def print_header(text: str) -> None:
    """Print a formatted header"""
    print("\n" + "="*50)
    print(f"🔍 {text}")
    print("="*50)

def print_success(text: str) -> None:
    """Print success message"""
    print(f"✅ {text}")

def print_error(text: str) -> None:
    """Print error message"""
    print(f"❌ {text}")

def print_info(text: str) -> None:
    """Print info message"""
    print(f"ℹ️  {text}")

def format_response(data: Dict[str, Any]) -> str:
    """Format response data for pretty printing"""
    return json.dumps(data, indent=2)

def check_endpoint(endpoint_path: str, name: str) -> bool:
    """Test a single endpoint and return success status"""
    url = f"{BASE_URL}{endpoint_path}"
    print_header(f"Testing {name} endpoint")
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        print_info(f"URL: {url}")
        print_info(f"Response Time: {response_time:.2f}ms")
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Response received successfully!")
            print_info("Response Data:")
            print(format_response(data))
            return True
        else:
            print_error(f"Failed with status code: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Connection Error: Could not connect to the server")
        print_error("Make sure the API server is running on localhost:5000")
        return False
    except requests.exceptions.Timeout:
        print_error("Timeout Error: Request took too long")
        return False
    except Exception as e:
        print_error(f"Unexpected Error: {str(e)}")
        return False

def main() -> None:
    """Main test function"""
    print_header("Starting OMEGA BTC AI API Tests")
    print_info(f"Testing against base URL: {BASE_URL}")
    
    results = {}
    for name, endpoint in ENDPOINTS.items():
        print("\n" + "-"*50)
        success = check_endpoint(endpoint, name)
        results[name] = success
    
    # Print summary
    print_header("Test Summary")
    total_tests = len(results)
    passed_tests = sum(1 for success in results.values() if success)
    failed_tests = total_tests - passed_tests
    
    print_info(f"Total Tests: {total_tests}")
    print_info(f"Passed: {passed_tests}")
    print_info(f"Failed: {failed_tests}")
    
    if failed_tests > 0:
        print_error("\nFailed Endpoints:")
        for name, success in results.items():
            if not success:
                print_error(f"- {name}")
        sys.exit(1)
    else:
        print_success("\nAll endpoints tested successfully! JAH BLESS! 🙏")
        sys.exit(0)

if __name__ == "__main__":
    main() 