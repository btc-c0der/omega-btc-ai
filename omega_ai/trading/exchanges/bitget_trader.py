#!/usr/bin/env python3

"""
BitGet Trader Integration for OmegaBTC AI

This module provides the BitGet exchange integration for our trader profiles.
It handles all direct communication with the BitGet API while maintaining
our trader profile system's behavior and risk management.
"""

import logging
import time
import hmac
import hashlib
import json
import requests
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from requests.exceptions import RequestException
import random
from threading import Lock
import base64
import os

from ..profiles.trader_base import TraderProfile, RiskParameters
from ..profiles.aggressive_trader import AggressiveTrader
from ..profiles.strategic_trader import StrategicTrader
from ..profiles.newbie_trader import NewbieTrader
from ..profiles.scalper_trader import ScalperTrader

logger = logging.getLogger(__name__)

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Add rate limit constants
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1  # seconds
MAX_RETRY_DELAY = 10  # seconds
REQUEST_RATE_LIMIT = 0.5  # seconds between requests
SHUTDOWN_TIMEOUT = 5  # seconds to wait for shutdown

class RateLimiter:
    """Rate limiter for API requests."""
    def __init__(self, min_interval: float):
        self.min_interval = min_interval
        self.last_request_time = 0
        self.lock = Lock()
    
    def wait(self):
        """Wait if necessary to respect rate limits."""
        with self.lock:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.min_interval:
                time.sleep(self.min_interval - time_since_last)
            self.last_request_time = time.time()

# Global rate limiter
rate_limiter = RateLimiter(REQUEST_RATE_LIMIT)

def _handle_rate_limit(response: requests.Response, retry_count: int) -> bool:
    """Handle rate limit responses and determine if we should retry."""
    if response.status_code == 429:  # Rate limit hit
        return True
    if response.status_code == 404 and retry_count > 0:  # Potential fake 404
        try:
            error_data = response.json()
            if error_data.get("code") == "40404":  # BitGet's "Request URL NOT FOUND"
                return True
        except:
            pass
    return False

def _get_retry_delay(retry_count: int) -> float:
    """Calculate exponential backoff delay with jitter."""
    delay = min(INITIAL_RETRY_DELAY * (2 ** retry_count), MAX_RETRY_DELAY)
    jitter = random.uniform(0, 0.1 * delay)
    return delay + jitter

def _make_request(method: str, url: str, **kwargs) -> requests.Response:
    """Make an HTTP request with rate limit handling and retries."""
    retry_count = 0
    last_error = None
    response = None
    
    while retry_count < MAX_RETRIES:
        try:
            # Apply rate limiting
            rate_limiter.wait()
            
            # Log request details
            logger.info(f"{CYAN}=== Request Details ==={RESET}")
            logger.info(f"Method: {method}")
            logger.info(f"URL: {url}")
            logger.info(f"Headers: {json.dumps(kwargs.get('headers', {}), indent=2)}")
            logger.info(f"Body: {json.dumps(kwargs.get('json', {}), indent=2)}")
            
            response = requests.request(method, url, **kwargs)
            
            # Log response details
            logger.info(f"{CYAN}=== Response Details ==={RESET}")
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            try:
                logger.info(f"Response Body: {json.dumps(response.json(), indent=2)}")
            except:
                logger.info(f"Response Body: {response.text}")
            
            if _handle_rate_limit(response, retry_count):
                delay = _get_retry_delay(retry_count)
                logger.warning(f"{YELLOW}Rate limit hit or potential fake 404. Retrying in {delay:.2f} seconds... (Attempt {retry_count + 1}/{MAX_RETRIES}){RESET}")
                time.sleep(delay)
                retry_count += 1
                continue
                
            response.raise_for_status()
            return response
            
        except RequestException as e:
            last_error = e
            delay = _get_retry_delay(retry_count)
            logger.warning(f"{YELLOW}Request failed. Retrying in {delay:.2f} seconds... (Attempt {retry_count + 1}/{MAX_RETRIES}){RESET}")
            logger.error(f"{RED}Error details: {str(e)}{RESET}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"{RED}Response status: {e.response.status_code}{RESET}")
                logger.error(f"{RED}Response headers: {dict(e.response.headers)}{RESET}")
                try:
                    logger.error(f"{RED}Response body: {json.dumps(e.response.json(), indent=2)}{RESET}")
                except:
                    logger.error(f"{RED}Response body: {e.response.text}{RESET}")
            time.sleep(delay)
            retry_count += 1
    
    if last_error:
        raise last_error
    if response is None:
        raise RequestException("Failed to make request after all retries")
    return response

class BitGetTrader:
    """BitGet exchange integration for our trader profiles."""
    
    # Class constants
    PRODUCT_TYPE = "USDT-FUTURES"  # Product type for USDT-margined perpetual contracts
    PRODUCT_TYPE_PARAM = "USDT-FUTURES"  # Product type parameter for API v2 endpoints
    
    # Cache for sub-account names
    _sub_account_cache = {}
    _sub_account_cache_time = 0
    _sub_account_cache_ttl = 300  # Cache TTL in seconds (5 minutes)
    
    @classmethod
    def format_symbol(cls, symbol: str, api_version: str = "v2") -> str:
        """Format symbol according to BitGet's API requirements.
        
        Args:
            symbol: Symbol to format, e.g. "BTCUSDT"
            api_version: API version to format for (v1 or v2)
            
        Returns:
            Formatted symbol, e.g. "BTCUSDT_UMCBL" for v1 or "BTCUSDT" for v2
        """
        # For API v1, append _UMCBL suffix if not already present
        if api_version == "v1":
            if symbol.endswith("_UMCBL"):
                return symbol
            return f"{symbol}_UMCBL"
        # For API v2, use symbol as is
        else:
            # Remove _UMCBL suffix if present (in case we're upgrading from v1)
            if symbol.endswith("_UMCBL"):
                return symbol[:-7]
            return symbol
    
    def __init__(self, 
                 profile_type: str = "strategic",
                 api_key: str = "",
                 secret_key: str = "",
                 passphrase: str = "",
                 use_testnet: bool = True,
                 initial_capital: float = 10000.0,
                 margin_mode: str = "fixed",  # "fixed" or "crossed"
                 api_client: Optional[Any] = None,
                 api_version: str = "v1",
                 sub_account_name: Optional[str] = None,  # Name of the sub-account to use
                 sub_account_id: Optional[str] = None,    # ID of the sub-account to use
                ):
        """
        Initialize the BitGet trader with the specified settings.
        
        Args:
            profile_type: Type of trader profile (strategic, aggressive, newbie, scalper)
            api_key: BitGet API key
            secret_key: BitGet secret key
            passphrase: BitGet API passphrase
            use_testnet: Whether to use testnet (default: True)
            initial_capital: Initial capital in USDT (default: 10000.0)
            margin_mode: Margin mode (fixed or crossed) (default: fixed)
            api_client: Optional external API client for testing
            api_version: API version to use (v1 or v2) (default: v1)
            sub_account_name: Name of the sub-account to use (optional)
            sub_account_id: ID of the sub-account to use (optional)
        """
        # API configuration
        self.use_testnet = use_testnet
        self.is_shutting_down = False
        self.symbol = "BTCUSDT"  # Default to BTCUSDT
        self.api_version = api_version
        
        # Sub-account configuration
        if not use_testnet and (sub_account_name or sub_account_id):
            logger.warning(f"{YELLOW}Sub-accounts are not allowed in mainnet. Using main account only.{RESET}")
            self.sub_account_name = None
            self.sub_account_id = None
        else:
            if not sub_account_name and profile_type:
                # Try to get sub-account name from environment variables based on profile type
                env_prefix = profile_type.upper()
                self.sub_account_name = os.environ.get(f"{env_prefix}_SUB_ACCOUNT_NAME")
                if self.sub_account_name:
                    logger.info(f"{CYAN}Using sub-account from environment: {self.sub_account_name}{RESET}")
            else:
                self.sub_account_name = sub_account_name
                
            self.sub_account_id = sub_account_id
        
        # Look for API credentials in environment variables if not provided
        self.api_key = api_key or os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        self.secret_key = secret_key or os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        self.passphrase = passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        
        # Log API credentials status
        if not self.api_key or not self.secret_key or not self.passphrase:
            logger.warning(f"{YELLOW}One or more API credentials are missing. API authentication will fail.{RESET}")
        
        # External API client for testing
        self.api_client = api_client
        
        # Set API base path based on version
        if api_version == "v1":
            self.api_base = "/api/mix/v1"
            self.PRODUCT_TYPE_PARAM = "umcbl"
        else:  # v2
            self.api_base = "/api/v2/mix"
            self.PRODUCT_TYPE_PARAM = "USDT-FUTURES"
        
        # Set different API URLs based on testnet/mainnet
        if self.use_testnet:
            self.api_url = "https://api-testnet.bitget.com"
        else:
            self.api_url = "https://api.bitget.com"
            
        logger.info(f"{CYAN}Initialized BitGetTrader with API {api_version}{RESET}")
        logger.info(f"{CYAN}API Base: {self.api_base}{RESET}")
        logger.info(f"{CYAN}Product Type Param: {self.PRODUCT_TYPE_PARAM}{RESET}")
        
        # Validate sub-account parameters only for testnet
        if use_testnet:
            is_valid, error_msg = self._validate_sub_account(self.sub_account_name, self.sub_account_id)
            if not is_valid:
                logger.error(f"{RED}Invalid sub-account configuration: {error_msg}{RESET}")
                raise ValueError(f"Invalid sub-account configuration: {error_msg}")
            elif self.sub_account_name:
                logger.info(f"{CYAN}Using sub-account: {self.sub_account_name}{RESET}")
            elif self.sub_account_id:
                logger.info(f"{CYAN}Using sub-account with ID: {self.sub_account_id}{RESET}")
        
        # Initialize the appropriate trader profile
        self.profile = self._initialize_profile(profile_type, initial_capital)
        
        # Trading state
        self.positions: List[Dict[str, Any]] = []
        self.trade_history: List[Dict[str, Any]] = []
        self.current_price: float = 0.0
        
        # Risk management
        self.risk_params = self.profile._get_risk_parameters()
        
        # Verify symbol
        if not self.verify_symbol():
            raise ValueError(f"Invalid trading symbol for {'testnet' if use_testnet else 'live'} trading")
        
    def _validate_sub_account(self, sub_account_name: Optional[str], sub_account_id: Optional[str]) -> Tuple[bool, Optional[str]]:
        """
        Validate if a sub-account exists and is accessible.
        
        Args:
            sub_account_name: Name of the sub-account (optional)
            sub_account_id: ID of the sub-account (optional)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Use v2 API endpoint for sub-account assets
            endpoint = "/api/v2/mix/account/sub-account-assets"
            
            # Required parameters for v2 API
            params = {
                "productType": "USDT-FUTURES"  # Use USDT-FUTURES for USDT margined contracts
            }
            
            # Add sub-account parameters if available
            if sub_account_name:
                params["subAccountName"] = sub_account_name
            elif sub_account_id:
                params["subAccountId"] = sub_account_id
            
            # Get current timestamp
            timestamp = str(int(time.time() * 1000))
            
            # Get headers with authentication
            headers = self._get_auth_headers(timestamp, "GET", endpoint, params)
            
            # Make the request
            response = _make_request("GET", f"{self.api_url}{endpoint}", 
                                  headers=headers, params=params)
            result = response.json()
            
            if result.get("code") == "00000" and result.get("data"):
                # If we're checking a specific sub-account and got a non-empty response,
                # the API confirms the account exists
                if sub_account_name or sub_account_id:
                    # Check if we got any accounts in the response
                    if len(result.get("data", [])) > 0:
                        # For backwards compatibility, also check the specific format pattern
                        if sub_account_name:
                            for account in result.get("data", []):
                                user_id = str(account.get("userId"))
                                # Support both formats: exact custom name and sub_[userId] format
                                if sub_account_name == f"sub_{user_id}" or sub_account_name:
                                    # Cache the result
                                    self._sub_account_cache[user_id] = sub_account_name
                                    return True, None
                        # If we're checking by ID, any response with data is valid
                        elif sub_account_id:
                            return True, None
                    
                    # If we get here, the sub-account wasn't found in the response
                    if sub_account_name:
                        return False, f"Sub-account '{sub_account_name}' not found"
                    else:
                        return False, f"Sub-account ID {sub_account_id} not found"
                else:
                    # No specific sub-account to validate, just check if we can access the endpoint
                    return True, None
            else:
                error_msg = result.get("msg", "Unknown error")
                return False, f"Failed to validate sub-account: {error_msg}"
            
        except Exception as e:
            logger.error(f"{RED}Error validating sub-account: {str(e)}{RESET}")
            return False, f"Error validating sub-account: {str(e)}"
    
    def _initialize_profile(self, profile_type: str, initial_capital: float) -> TraderProfile:
        """Initialize the appropriate trader profile based on type."""
        profile_map = {
            "aggressive": AggressiveTrader,
            "strategic": StrategicTrader,
            "newbie": NewbieTrader,
            "scalper": ScalperTrader
        }
        
        profile_class = profile_map.get(profile_type.lower(), StrategicTrader)
        return profile_class(initial_capital=initial_capital)
    
    def generate_signature(self, timestamp: str, method: str, request_path: str, body: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> str:
        """Generate the signature required for BitGet API authentication.
        
        Args:
            timestamp: Current timestamp in milliseconds
            method: HTTP method (GET, POST, etc.)
            request_path: API endpoint path
            body: Request body for POST requests
            params: Query parameters for GET requests
            
        Returns:
            Base64-encoded signature
        """
        # Ensure method is uppercase as required by BitGet
        method = method.upper()
        
        # Start with timestamp + method + requestPath
        # Add a space between method and request_path as per BitGet requirements
        message = str(timestamp) + method + " " + request_path
        
        # Add query string if present (for GET requests)
        if params and method == "GET":
            # Sort parameters by key as required by BitGet
            sorted_params = sorted(params.items())
            # Create query string
            query_string = "&".join([f"{key}={value}" for key, value in sorted_params])
            # Add to message with question mark only if not already in request_path
            if query_string and "?" not in request_path:
                message += "?" + query_string
        
        # Add body for POST requests
        if body and method == "POST":
            if isinstance(body, dict):
                message += json.dumps(body)
            else:
                message += body
        
        # For debugging
        logger.debug(f"Pre-signed message: {message}")
        
        # Create signature using HMAC-SHA256
        hmac_obj = hmac.new(
            self.secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        )
        # Use base64 encoding as required by BitGet
        return base64.b64encode(hmac_obj.digest()).decode('utf-8')
    
    def _get_auth_headers(self, timestamp: str, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, body: Optional[str] = None) -> Dict[str, str]:
        """Generate authentication headers for API requests.
        
        Args:
            timestamp: Current timestamp in milliseconds
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Optional query parameters
            body: Request body for POST requests
            
        Returns:
            Dictionary of authentication headers
        """
        # Create a copy of params to avoid modifying the original
        if params is None:
            params = {}
        else:
            params = params.copy()
            
        # Only add sub-account parameters for endpoints that support them
        # Position endpoints don't support subAccountName as a parameter
        if self.sub_account_name and not any(x in endpoint for x in ["/position/", "/market/"]):
            params["subAccountName"] = self.sub_account_name
        elif self.sub_account_id and not any(x in endpoint for x in ["/position/", "/market/"]):
            params["subAccountId"] = self.sub_account_id
        
        # For v2 API, we need to handle parameters differently
        if self.api_version == "v2":
            # Sort parameters by key as required by BitGet
            sorted_params = sorted(params.items())
            # Create query string
            query_string = "&".join([f"{key}={value}" for key, value in sorted_params])
            # Add to endpoint with question mark if there are parameters
            if query_string:
                # Only add query string if it's not already in the endpoint
                if "?" not in endpoint:
                    endpoint = f"{endpoint}?{query_string}"
        
        # Generate signature with params and body
        signature = self.generate_signature(timestamp, method, endpoint, body, params)
        
        # Log signature details for debugging
        logger.debug(f"Generating signature for: {method} {endpoint}")
        if params:
            logger.debug(f"With params: {params}")
        if body:
            logger.debug(f"With body: {body}")
        
        # Build headers
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }
        
        return headers
    
    def get_account_balance(self, symbol: str = "BTCUSDT") -> Optional[float]:
        """Get current account balance for the specified symbol."""
        # Use external API client if provided
        if self.api_client:
            try:
                response = self.api_client.get_account_balance(symbol)
                if response and response.get("code") == "00000" and response.get("data"):
                    return float(response["data"]["equity"])
                else:
                    logger.error(f"Error fetching account balance: {response.get('msg')}")
                    return None
            except Exception as e:
                logger.error(f"Error getting account balance: {e}")
                return None
        
        # Use internal implementation if no external client
        endpoint = f"{self.api_base}/account/account"
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Set parameters as query params
        params = {
            "productType": self.PRODUCT_TYPE_PARAM,
            "marginCoin": "USDT"  # Required parameter
        }
        
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== Account Balance Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Query Params: {json.dumps(params, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            account_data = response.json()
            
            if account_data.get("code") == "00000" and account_data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved account balance{RESET}")
                return float(account_data["data"]["equity"])
            else:
                error_msg = account_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error fetching account balance: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(account_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error getting account balance: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
    
    def place_order(self, 
                   symbol: str,
                   side: str,
                   order_type: str,
                   price: Optional[float] = None,
                   quantity: Optional[float] = None,
                   margin_mode: str = "crossed",
                   leverage: str = "20",
                   time_in_force: str = "normal",
                   reduce_only: bool = False,
                   post_only: bool = False) -> Optional[Dict[str, Any]]:
        """Place a futures order on BitGet."""
        # Use external API client if provided
        if self.api_client:
            try:
                # Format symbol for external client
                formatted_symbol = self.format_symbol(symbol, self.api_version)
                params: Dict[str, Any] = {
                    "symbol": formatted_symbol,
                    "marginCoin": "USDT",  # Required for v1 API
                    "side": side,  # Already mapped to open_long/open_short by caller
                    "orderType": order_type.upper(),
                    "marginMode": margin_mode.upper(),
                    "leverage": leverage,
                    "timeInForceValue": time_in_force,  # Changed from timeInForce to timeInForceValue
                    "reduceOnly": str(reduce_only).lower(),
                    "postOnly": str(post_only).lower(),
                    "productType": self.PRODUCT_TYPE_PARAM,
                    "clientOid": f"omega_{int(time.time() * 1000)}"  # Required unique client order ID
                }
                
                if order_type.lower() == "limit":
                    if price is None or quantity is None:
                        logger.error("Price and quantity required for limit orders")
                        return None
                    params["price"] = str(price)
                    params["size"] = str(quantity)
                elif order_type.lower() == "market":
                    if quantity is None:
                        logger.error("Quantity required for market orders")
                        return None
                    params["size"] = str(quantity)
                
                return self.api_client.place_order(**params)
            except Exception as e:
                logger.error(f"Error placing order: {e}")
                return None
        
        # Use internal implementation if no external client
        endpoint = f"{self.api_base}/order/placeOrder"
        method = "POST"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        params: Dict[str, Any] = {
            "symbol": formatted_symbol,
            "marginCoin": "USDT",  # Required for v1 API
            "side": side,  # Already mapped to open_long/open_short by caller
            "orderType": order_type.upper(),
            "marginMode": margin_mode.upper(),
            "leverage": leverage,
            "timeInForceValue": time_in_force,  # Changed from timeInForce to timeInForceValue
            "reduceOnly": str(reduce_only).lower(),
            "postOnly": str(post_only).lower(),
            "productType": self.PRODUCT_TYPE_PARAM,
            "clientOid": f"omega_{int(time.time() * 1000)}"  # Required unique client order ID
        }
        
        if order_type.lower() == "limit":
            if price is None or quantity is None:
                logger.error("Price and quantity required for limit orders")
                return None
            params["price"] = str(price)
            params["size"] = str(quantity)
        elif order_type.lower() == "market":
            if quantity is None:
                logger.error("Quantity required for market orders")
                return None
            params["size"] = str(quantity)
        
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== Order Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"Body: {json.dumps(params, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, json=params)
            order_data = response.json()
            
            if order_data.get("code") == "00000" and order_data.get("data"):
                logger.info(f"{GREEN}Successfully placed order{RESET}")
                return order_data
            else:
                error_msg = order_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error placing order: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(order_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return None
    
    def close_position(self, symbol: str, side: str, margin_mode: str = "crossed") -> Optional[Dict[str, Any]]:
        """Close an existing position."""
        # Use external API client if provided
        if self.api_client:
            try:
                # Format symbol for external client
                formatted_symbol = self.format_symbol(symbol, self.api_version)
                params: Dict[str, Any] = {
                    "symbol": formatted_symbol,
                    "side": "SELL" if side.lower() == "long" else "BUY",
                    "orderType": "MARKET",
                    "marginMode": margin_mode.upper(),
                    "size": "position_amount",
                    "productType": self.PRODUCT_TYPE_PARAM
                }
                return self.api_client.close_position(**params)
            except Exception as e:
                logger.error(f"Error closing position: {e}")
                return None
        
        # Use internal implementation if no external client
        # Different endpoint for different API versions
        if self.api_version == "v1":
            endpoint = f"{self.api_base}/order/close-positions"  # v1 endpoint
        else:
            endpoint = f"{self.api_base}/order/close-positions"  # v2 endpoint
            
        method = "POST"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        # Build parameters based on API version
        if self.api_version == "v1":
            params: Dict[str, Any] = {
                "symbol": formatted_symbol,
                "marginMode": margin_mode.upper(),
                "productType": self.PRODUCT_TYPE_PARAM
            }
            # v1 requires holdSide parameter
            if side.lower() == "long":
                params["holdSide"] = "long"
            else:
                params["holdSide"] = "short"
        else:
            params: Dict[str, Any] = {
                "symbol": formatted_symbol,
                "marginMode": margin_mode.upper(),
                "productType": self.PRODUCT_TYPE_PARAM
            }
        
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== Close Position Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"Side: {side}")
        logger.info(f"API Version: {self.api_version}")
        logger.info(f"Body: {json.dumps(params, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, json=params)
            close_data = response.json()
            
            if close_data.get("code") == "00000" and close_data.get("data"):
                logger.info(f"{GREEN}Successfully closed position{RESET}")
                return close_data
            else:
                error_msg = close_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error closing position: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(close_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return None
    
    def execute_trade(self, market_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute a trade based on the profile's decision."""
        # Get trading decision from profile
        should_trade, reason, direction, leverage = self.profile.should_enter_trade(market_context)
        
        if not should_trade:
            logger.info(f"Profile decided not to trade: {reason}")
            return None
        
        # Calculate position size
        entry_price = market_context.get("price", 0)
        position_size = self.profile.determine_position_size(direction, entry_price)
        
        if position_size <= 0:
            logger.error("Invalid position size calculated")
            return None
        
        # Map direction to BitGet's expected format
        side_mapping = {
            "LONG": "open_long",
            "SHORT": "open_short"
        }
        mapped_side = side_mapping.get(direction, "open_long")
        
        # Place the order with correct side mapping
        order_response = self.place_order(
            symbol=self.symbol,
            side=mapped_side,  # Use mapped side instead of BUY/SELL
            order_type="MARKET",
            quantity=position_size,
            time_in_force="normal",
            leverage=str(leverage)
        )
        
        if not order_response or order_response.get("code") != "00000":
            logger.error(f"Failed to place order: {order_response}")
            return None
        
        # Calculate stop loss and take profit levels
        stop_loss = self.profile.set_stop_loss(direction, entry_price)
        take_profits = self.profile.set_take_profit(direction, entry_price, stop_loss)
        
        # Record the position
        position: Dict[str, Any] = {
            "direction": direction,
            "entry_price": entry_price,
            "size": position_size,
            "leverage": leverage,
            "stop_loss": stop_loss,
            "take_profits": take_profits,
            "entry_time": datetime.now(),
            "order_id": order_response.get("data", {}).get("orderId")
        }
        
        self.positions.append(position)
        return position
    
    def update_positions(self, current_price: float) -> None:
        """Update all positions with current price and check for exits."""
        self.current_price = current_price
        
        for position in self.positions[:]:  # Copy list to allow removal during iteration
            # Check stop loss
            if position["direction"] == "LONG" and current_price <= position["stop_loss"]:
                self._close_position(position, "Stop loss hit")
                continue
            elif position["direction"] == "SHORT" and current_price >= position["stop_loss"]:
                self._close_position(position, "Stop loss hit")
                continue
            
            # Check take profits
            for tp in position["take_profits"]:
                if position["direction"] == "LONG" and current_price >= tp["price"]:
                    self._close_position(position, f"Take profit hit at {tp['price']}")
                    break
                elif position["direction"] == "SHORT" and current_price <= tp["price"]:
                    self._close_position(position, f"Take profit hit at {tp['price']}")
                    break
    
    def _close_position(self, position: Dict[str, Any], reason: str) -> None:
        """Close a position and record the trade result."""
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol("BTCUSDT", self.api_version)
        
        close_response = self.close_position(
            symbol=formatted_symbol,
            side=position["direction"]
        )
        
        if not close_response or close_response.get("code") != "00000":
            logger.error(f"Failed to close position: {close_response}")
            return
        
        # Calculate PnL
        exit_price = float(close_response.get("data", {}).get("price", self.current_price))
        price_diff = exit_price - position["entry_price"]
        if position["direction"] == "SHORT":
            price_diff = -price_diff
        
        pnl = (price_diff / position["entry_price"]) * position["size"] * position["leverage"]
        
        # Record trade history
        trade: Dict[str, Any] = {
            "entry_time": position["entry_time"],
            "exit_time": datetime.now(),
            "direction": position["direction"],
            "entry_price": position["entry_price"],
            "exit_price": exit_price,
            "size": position["size"],
            "leverage": position["leverage"],
            "pnl": pnl,
            "reason": reason
        }
        
        self.trade_history.append(trade)
        
        # Update profile with trade result
        self.profile.process_trade_result(
            pnl,
            (trade["exit_time"] - trade["entry_time"]).total_seconds() / 60  # Duration in minutes
        )
        
        # Remove position from active positions
        self.positions.remove(position)
    
    def get_trade_history(self) -> List[Dict[str, Any]]:
        """Get the complete trade history."""
        return self.trade_history
    
    def get_positions(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get current positions.
        
        Args:
            symbol: Trading symbol (optional)
            
        Returns:
            List of position objects
        """
        try:
            # Validate symbol
            if symbol:
                symbol = self.format_symbol(symbol, self.api_version)
            
            # If a specific symbol is requested, try singlePosition first
            if symbol:
                try:
                    endpoint = "/api/v2/mix/position/single-position"
                    params = {
                        "symbol": symbol,
                        "marginCoin": "USDT",
                        "productType": "USDT-FUTURES"
                    }
                    
                    # Get fresh timestamp
                    timestamp = str(int(time.time() * 1000))
                    
                    # Get request headers with authentication - passing params directly
                    headers = self._get_auth_headers(timestamp, "GET", endpoint, params)
                    
                    # Build URL with query parameters manually to ensure consistency
                    url = f"{self.api_url}{endpoint}"
                    
                    # Make request with params passed separately to ensure they're properly encoded in URL
                    response = _make_request("GET", url, headers=headers, params=params)
                    
                    # Parse response
                    result = response.json()
                    
                    if result.get("code") == "00000" and result.get("data"):
                        positions = result.get("data", [])
                        # If we're in a single-hold position mode, there will be only one position per symbol
                        if not isinstance(positions, list):
                            positions = [positions]
                        return positions
                except Exception as e:
                    logger.warning(f"{YELLOW}Error with singlePosition endpoint, falling back to allPosition: {str(e)}{RESET}")
                    # Fall through to try the allPosition endpoint
            
            # Define endpoint for all positions or fallback from single position error
            endpoint = "/api/v2/mix/position/all-position"
            params = {
                "marginCoin": "USDT",
                "productType": "USDT-FUTURES"
            }
            
            # Loop for retries, generating new timestamp each time
            for retry in range(MAX_RETRIES):
                try:
                    # Get fresh timestamp for each request attempt
                    timestamp = str(int(time.time() * 1000))
                    
                    # Get request headers with authentication
                    headers = self._get_auth_headers(timestamp, "GET", endpoint, params)
                    
                    # Build URL with query parameters manually to ensure consistency
                    url = f"{self.api_url}{endpoint}"
                    
                    # Make request
                    response = _make_request("GET", url, headers=headers, params=params)
                    
                    # Parse response
                    result = response.json()
                    
                    if result.get("code") == "00000" and result.get("data"):
                        positions = result.get("data", [])
                        
                        # If we're looking for a specific symbol, filter the results
                        if symbol:
                            positions = [p for p in positions if p.get("symbol") == symbol]
                            
                        return positions
                    else:
                        logger.error(f"{RED}Failed to get positions: {result.get('msg', 'Unknown error')}{RESET}")
                        if retry < MAX_RETRIES - 1:
                            # Only log if we're going to retry
                            logger.warning(f"{YELLOW}Retrying ({retry + 1}/{MAX_RETRIES})...{RESET}")
                            time.sleep(_get_retry_delay(retry))
                            continue
                        return []
                except Exception as inner_e:
                    if retry < MAX_RETRIES - 1:
                        # Only log if we're going to retry
                        logger.error(f"{RED}Error in get_positions attempt {retry + 1}: {str(inner_e)}{RESET}")
                        time.sleep(_get_retry_delay(retry))
                        continue
                    raise  # Re-raise on final attempt
            
            # If we get here, all retries failed
            return []
            
        except Exception as e:
            logger.error(f"{RED}Error getting positions: {str(e)}{RESET}")
            return []
    
    def get_position_risk(self, symbol: str = "BTCUSDT") -> Optional[Dict[str, Any]]:
        """Get position risk information."""
        # Different endpoint based on API version
        if self.api_version == "v1":
            endpoint = f"{self.api_base}/position/allPosition"  # Correct endpoint for v1
        else:
            endpoint = f"{self.api_base}/position/single-position"  # Endpoint for v2
            
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        # Set parameters as query params
        params = {
            "marginCoin": "USDT"  # Required parameter
        }
        
        # Only add symbol for v2 or if explicitly required for v1
        if self.api_version != "v1" or True:  # Always add for now
            params["symbol"] = formatted_symbol
        
        # Add product type for v1
        if self.api_version == "v1":
            params["productType"] = self.PRODUCT_TYPE_PARAM
        
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== Position Risk Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"API Version: {self.api_version}")
        logger.info(f"Query Params: {json.dumps(params, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            data = response.json()
            
            if data.get("code") == "00000" and data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved position risk{RESET}")
                return data["data"]
            else:
                error_msg = data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error fetching position risk: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error getting position risk: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
            
    def set_leverage(self, symbol: str, leverage: str, margin_mode: str = "crossed") -> Optional[Dict[str, Any]]:
        """Set leverage for a symbol."""
        endpoint = f"{self.api_base}/account/set-leverage"
        method = "POST"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        body = {
            "symbol": formatted_symbol,
            "leverage": leverage,
            "marginMode": margin_mode.upper(),
            "productType": self.PRODUCT_TYPE_PARAM
        }
        
        headers = self._get_auth_headers(timestamp, method, endpoint, body)
        
        logger.info(f"{CYAN}=== Set Leverage Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"Body: {json.dumps(body, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, json=body)
            leverage_data = response.json()
            
            if leverage_data.get("code") == "00000" and leverage_data.get("data"):
                logger.info(f"{GREEN}Successfully set leverage{RESET}")
                return leverage_data
            else:
                error_msg = leverage_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error setting leverage: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(leverage_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error setting leverage: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
            
    def set_margin_mode(self, symbol: str, margin_mode: str) -> Optional[Dict[str, Any]]:
        """Set margin mode for a symbol."""
        endpoint = f"{self.api_base}/account/set-margin-mode"
        method = "POST"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        body = {
            "symbol": formatted_symbol,
            "marginMode": margin_mode.upper(),
            "productType": self.PRODUCT_TYPE_PARAM
        }
        
        headers = self._get_auth_headers(timestamp, method, endpoint, body)
        
        logger.info(f"{CYAN}=== Set Margin Mode Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"Body: {json.dumps(body, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, json=body)
            margin_data = response.json()
            
            if margin_data.get("code") == "00000" and margin_data.get("data"):
                logger.info(f"{GREEN}Successfully set margin mode{RESET}")
                return margin_data
            else:
                error_msg = margin_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error setting margin mode: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(margin_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error setting margin mode: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
    
    def get_total_pnl(self) -> float:
        """Calculate total profit/loss from all trades and open positions."""
        # Get realized PnL from trade history
        realized_pnl = sum(trade["pnl"] for trade in self.trade_history if "pnl" in trade)
        
        # Get unrealized PnL from open positions
        unrealized_pnl = 0.0
        
        try:
            if self.symbol:
                positions = self.get_positions(self.symbol)
                if positions:
                    for position in positions:
                        if position and "unrealizedPL" in position:
                            unrealized_pnl += float(position.get("unrealizedPL", 0))
                        # Also include achievedProfits (realized PnL for open positions)
                        if position and "achievedProfits" in position:
                            realized_pnl += float(position.get("achievedProfits", 0))
        except Exception as e:
            logger.error(f"Error calculating unrealized PnL: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
        
        # Return total PnL (realized + unrealized)
        total_pnl = realized_pnl + unrealized_pnl
        
        # Log PnL breakdown for debugging
        logger.debug(f"PnL Breakdown - Realized: {realized_pnl:.2f}, Unrealized: {unrealized_pnl:.2f}, Total: {total_pnl:.2f}")
        
        return total_pnl
    
    def get_market_ticker(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get current market ticker data."""
        # Different endpoint based on API version
        if self.api_version == "v1":
            endpoint = f"{self.api_base}/market/ticker"  # Endpoint for v1
        else:
            endpoint = "/api/v2/mix/market/ticker"  # Endpoint for v2
            
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        # Set parameters as query params - different for each API version
        params = {}
        
        if self.api_version == "v1":
            # For v1, we need symbol and productType
            params = {
                "symbol": formatted_symbol,
                "productType": self.PRODUCT_TYPE_PARAM
            }
        else:
            # For v2, we need symbol and productType
            params = {
                "symbol": formatted_symbol,
                "productType": "USDT-FUTURES"
            }
        
        try:
            # Get headers with authentication
            headers = self._get_auth_headers(timestamp, method, endpoint, params)
            
            # Make the request
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            data = response.json()
            
            if data.get("code") == "00000" and data.get("data"):
                # Handle different response formats based on API version
                if self.api_version == "v1":
                    ticker_data = data.get("data", {})
                else:
                    # For v2, data is a list of tickers
                    tickers = data.get("data", [])
                    # Find the ticker for our symbol
                    ticker_data = next((t for t in tickers if t.get("symbol") == formatted_symbol), {})
                
                # Map the response fields to a consistent format
                mapped_ticker = {
                    "last": float(ticker_data.get("lastPr", 0)),
                    "ask": float(ticker_data.get("askPr", 0)),
                    "bid": float(ticker_data.get("bidPr", 0)),
                    "high": float(ticker_data.get("high24h", 0)),
                    "low": float(ticker_data.get("low24h", 0)),
                    "volume": float(ticker_data.get("baseVolume", 0)),
                    "quoteVolume": float(ticker_data.get("quoteVolume", 0)),
                    "change": float(ticker_data.get("change24h", 0)),
                    "markPrice": float(ticker_data.get("markPrice", 0)),
                    "indexPrice": float(ticker_data.get("indexPrice", 0)),
                    "fundingRate": float(ticker_data.get("fundingRate", 0)),
                    "timestamp": int(ticker_data.get("ts", 0))
                }
                
                logger.info("Successfully retrieved ticker")
                return mapped_ticker
            else:
                error_msg = data.get("msg", "Unknown error")
                logger.error(f"Failed to get ticker data: {error_msg}")
                logger.error(f"Response: {json.dumps(data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting ticker data: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
    
    def get_orderbook(self, symbol: str, limit: int = 100) -> Optional[Dict[str, Any]]:
        """Get order book data."""
        endpoint = f"{self.api_base}/market/orderbook"
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        # Set parameters as query params
        params = {
            "symbol": formatted_symbol,
            "limit": str(limit)
        }
        
        # Add product type parameter for v1 API
        if self.api_version == "v1":
            params["productType"] = self.PRODUCT_TYPE_PARAM
            
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== Orderbook Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"Query Params: {params}")
        logger.info(f"Headers: {headers}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            data = response.json()
            
            if data.get("code") == "00000" and data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved orderbook{RESET}")
                return data["data"]
            else:
                error_msg = data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error fetching orderbook: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error getting orderbook: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
            
    def get_recent_trades(self, symbol: str, limit: int = 100) -> Optional[List[Dict[str, Any]]]:
        """Get recent trades."""
        endpoint = f"{self.api_base}/market/trades"
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Format symbol properly for the API version
        formatted_symbol = self.format_symbol(symbol, self.api_version)
        
        # Set parameters as query params
        params = {
            "symbol": formatted_symbol,
            "limit": str(limit)
        }
        
        # Add product type parameter for v1 API
        if self.api_version == "v1":
            params["productType"] = self.PRODUCT_TYPE_PARAM
            
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== Trades Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Symbol: Original={symbol}, Formatted={formatted_symbol}")
        logger.info(f"Query Params: {params}")
        logger.info(f"Headers: {headers}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            data = response.json()
            
            if data.get("code") == "00000" and data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved trades{RESET}")
                return data["data"]
            else:
                error_msg = data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error fetching trades: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error getting trades: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None
    
    def verify_symbol(self, symbol: str = "BTCUSDT") -> bool:
        """Verify if the symbol is valid and available for futures trading."""
        logger.info(f"{CYAN}=== Symbol Verification ==={RESET}")
        logger.info(f"Symbol: {symbol}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"API Base: {self.api_base}")
        logger.info(f"API Version: {self.api_version}")
        
        # Use external API client if provided
        if self.api_client:
            try:
                logger.info("Using external API client for verification")
                response = self.api_client.get_symbols()
                if response and response.get("code") == "00000" and response.get("data"):
                    symbols = response["data"]
                    
                    # For API v1, symbols are in format BTCUSDT_UMCBL
                    if self.api_version == "v1":
                        symbol_to_check = f"{symbol}_UMCBL"
                    else:
                        symbol_to_check = symbol
                        
                    logger.info(f"Checking for symbol: {symbol_to_check}")
                    symbol_exists = any(s["symbol"] == symbol_to_check for s in symbols)
                    logger.info(f"Symbol verification result: {symbol_exists}")
                    return symbol_exists
                else:
                    logger.error(f"Error fetching symbols: {response.get('msg')}")
                    return False
            except Exception as e:
                logger.error(f"Error verifying symbol: {e}")
                return False
        
        # Use internal implementation if no external client
        # Different endpoint based on API version
        if self.api_version == "v1":
            endpoint = f"{self.api_base}/market/contracts"  # Endpoint for v1: /api/mix/v1/market/contracts
        else:
            endpoint = f"{self.api_base}/market/contracts"  # Endpoint for v2
        
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Parameters as query params
        params = {
            "productType": self.PRODUCT_TYPE_PARAM
        }
        
        # For proper debugging, log exactly what we're using
        logger.info(f"{CYAN}=== Symbol Verification Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"Timestamp: {timestamp}")
        logger.info(f"API Version: {self.api_version}")
        logger.info(f"Query Params: {params}")
        
        # Generate signed headers
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        logger.info(f"Headers: {headers}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            symbols_data = response.json()
            
            if symbols_data.get("code") == "00000" and symbols_data.get("data"):
                symbols = symbols_data["data"]
                logger.info(f"Retrieved {len(symbols)} symbols")
                
                # For API v1, symbols are in format BTCUSDT_UMCBL
                if self.api_version == "v1":
                    symbol_to_check = f"{symbol}_UMCBL"
                else:
                    symbol_to_check = symbol
                    
                logger.info(f"Checking for symbol: {symbol_to_check}")
                
                # Check if our symbol exists in the returned symbols
                # For v1, we check the 'symbol' field
                if self.api_version == "v1":
                    symbol_exists = any(s.get("symbol") == symbol_to_check for s in symbols)
                else:
                    # For v2, format may differ
                    symbol_exists = any(s.get("symbol") == symbol_to_check for s in symbols)
                
                logger.info(f"{GREEN}Symbol verification result: {symbol_exists}{RESET}")
                
                if symbol_exists:
                    # Log a few symbols for reference
                    logger.info(f"{GREEN}Available symbols sample:{RESET}")
                    for s in symbols[:5]:  # Log first 5 symbols as example
                        logger.info(f"  - {s.get('symbol', 'Unknown')}")
                else:
                    # Log the first 10 symbols to help debugging
                    logger.warning(f"{YELLOW}Symbol {symbol_to_check} not found in available symbols.{RESET}")
                    logger.warning(f"{YELLOW}First 10 available symbols:{RESET}")
                    for s in symbols[:10]:
                        logger.warning(f"  - {s.get('symbol', 'Unknown')}")
                    
                    # Check if symbol without suffix exists in a different form
                    for s in symbols[:20]:
                        if symbol in str(s.get("symbol", "")):
                            logger.warning(f"{YELLOW}Found potential match: {s.get('symbol', 'Unknown')}{RESET}")
                
                return symbol_exists
            else:
                error_msg = symbols_data.get("msg", "Unknown error")
                logger.error(f"{RED}Error fetching symbols: {error_msg}{RESET}")
                logger.error(f"Full response: {json.dumps(symbols_data, indent=2)}")
                return False
                
        except Exception as e:
            logger.error(f"{RED}Error verifying symbol: {str(e)}{RESET}")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return False

    async def shutdown(self) -> None:
        """Gracefully shutdown the trader."""
        self.is_shutting_down = True
        logger.info(f"{YELLOW}Shutting down trader...{RESET}")
        
        try:
            # Close all open positions
            positions = self.get_positions()
            if positions:
                for position in positions:
                    if position.get('status') == 'OPEN':
                        self.close_position(
                            symbol=self.symbol,
                            side=position.get('side', 'LONG')
                        )
            
            logger.info(f"{GREEN}Trader shutdown complete{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}Error during trader shutdown: {str(e)}{RESET}")
        finally:
            self.is_shutting_down = False

    def get_all_positions(self, product_type: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get all positions for the account.
        
        Args:
            product_type: Product type (default: None, will use class constant)
            
        Returns:
            List of position information or None if request fails
        """
        # Use external API client if provided
        if self.api_client:
            try:
                response = self.api_client.get_all_positions(product_type or self.PRODUCT_TYPE_PARAM)
                if response and response.get("code") == "00000" and response.get("data"):
                    return response["data"]
                else:
                    logger.error(f"Error fetching all positions: {response.get('msg')}")
                    return None
            except Exception as e:
                logger.error(f"Error getting all positions: {e}")
                return None
        
        # Use internal implementation if no external client
        # Different endpoint based on API version
        if self.api_version == "v1":
            endpoint = f"{self.api_base}/position/allPosition"  # Correct endpoint for v1
        else:
            endpoint = f"{self.api_base}/position/all-position"  # Endpoint for v2
            
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        
        # Set parameters as query params
        params = {
            "productType": product_type or self.PRODUCT_TYPE_PARAM,
            "marginCoin": "USDT"  # Required parameter
        }
        
        headers = self._get_auth_headers(timestamp, method, endpoint, params)
        
        logger.info(f"{CYAN}=== All Positions Request Debug ==={RESET}")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Method: {method}")
        logger.info(f"API Version: {self.api_version}")
        logger.info(f"Query Params: {json.dumps(params, indent=2)}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Timestamp: {timestamp}")
        
        try:
            response = _make_request(method, self.api_url + endpoint, headers=headers, params=params)
            positions_data = response.json()
            
            if positions_data.get("code") == "00000" and positions_data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved all positions{RESET}")
                return positions_data["data"]
            else:
                error_msg = positions_data.get("msg", "Unknown error")
                logger.error(f"\033[91mERROR: Error fetching all positions: {error_msg}\033[0m")
                logger.error(f"Full response: {json.dumps(positions_data, indent=2)}")
                return None
                
        except Exception as e:
            logger.error(f"\033[91mERROR: Error getting all positions: {str(e)}\033[0m")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception args: {e.args}")
            return None

    def get_historical_positions(self, 
                               symbol: str = "BTCUSDT",
                               start_time: Optional[int] = None,
                               end_time: Optional[int] = None,
                               limit: int = 100,
                               product_type: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """Get historical positions for a symbol.
        
        Args:
            symbol: Trading symbol (default: BTCUSDT)
            start_time: Start time in milliseconds (optional)
            end_time: End time in milliseconds (optional)
            limit: Number of records to return (default: 100)
            product_type: Product type (optional)
            
        Returns:
            List of historical positions or None if request fails
        """
        try:
            # Format symbol according to API version
            formatted_symbol = self.format_symbol(symbol, self.api_version)
            
            # Build query parameters
            params = {
                "symbol": formatted_symbol,
                "productType": product_type or self.PRODUCT_TYPE_PARAM,
                "pageSize": str(limit)
            }
            
            # Add time range if provided
            if start_time:
                params["startTime"] = str(start_time)
            if end_time:
                params["endTime"] = str(end_time)
                
            # Generate timestamp and signature
            timestamp = str(int(time.time() * 1000))
            endpoint = f"{self.api_base}/position/history-position"
            
            # Sort parameters alphabetically and create query string
            sorted_params = sorted(params.items())
            query_string = "&".join([f"{key}={value}" for key, value in sorted_params])
            
            # Get auth headers with sorted parameters
            headers = self._get_auth_headers(timestamp, "GET", endpoint, dict(sorted_params))
            
            # Make request with sorted parameters
            url = f"{self.api_url}{endpoint}?{query_string}"
            response = _make_request(
                "GET",
                url,
                headers=headers
            )
            
            # Parse response
            data = response.json()
            
            if data.get("code") == "00000":  # Success code
                return data.get("data", [])
            else:
                logger.error(f"{RED}Error getting historical positions: {data.get('msg')}{RESET}")
                return None
                
        except Exception as e:
            logger.error(f"{RED}ERROR: Error getting historical positions: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            return None

    def create_sub_account(self, sub_account_name: str, password: str) -> Optional[Dict[str, Any]]:
        """Create a new sub-account.
        
        Args:
            sub_account_name: Name for the new sub-account
            password: Password for the sub-account
            
        Returns:
            Dictionary containing sub-account details if successful, None otherwise
        """
        endpoint = "/api/v2/account/sub-account"
        timestamp = str(int(time.time() * 1000))
        
        # Set parameters
        data = {
            "subAccountName": sub_account_name,
            "password": password,
            "productType": self.PRODUCT_TYPE_PARAM
        }
        
        # Get headers with authentication
        headers = self._get_auth_headers(timestamp, "POST", endpoint)
        
        try:
            response = _make_request("POST", f"{self.api_url}{endpoint}", 
                                  headers=headers, json=data)
            result = response.json()
            
            if result.get("code") == "00000" and result.get("data"):
                logger.info(f"{GREEN}Successfully created sub-account: {sub_account_name}{RESET}")
                return result["data"]
            else:
                error_msg = result.get("msg", "Unknown error")
                logger.error(f"{RED}Failed to create sub-account: {error_msg}{RESET}")
                return None
                
        except Exception as e:
            logger.error(f"{RED}Failed to create sub-account: {str(e)}{RESET}")
            return None

    def get_sub_account_name(self, sub_account_id: str) -> Optional[str]:
        """
        Get the sub-account name from its ID.
        
        Args:
            sub_account_id: The ID of the sub-account
            
        Returns:
            The sub-account name if found, None otherwise
        """
        # Check cache first
        if sub_account_id in self._sub_account_cache:
            return self._sub_account_cache[sub_account_id]
            
        try:
            # Use v2 API endpoint for sub-account assets
            endpoint = "/api/v2/mix/account/sub-account-assets"
            
            # Required parameters for v2 API
            params = {
                "productType": "USDT-FUTURES"  # Use USDT-FUTURES for USDT margined contracts
            }
            
            # Get current timestamp
            timestamp = str(int(time.time() * 1000))
            
            # Get headers with authentication
            headers = self._get_auth_headers(timestamp, "GET", endpoint, params)
            
            # Make the request
            response = _make_request("GET", f"{self.api_url}{endpoint}", 
                                  headers=headers, params=params)
            result = response.json()
            
            if result.get("code") == "00000" and result.get("data"):
                # Look for the sub-account in the response
                for account in result.get("data", []):
                    if str(account.get("userId")) == str(sub_account_id):
                        # Generate a name based on the user ID since API doesn't provide it
                        sub_account_name = f"sub_{sub_account_id}"
                        # Cache the result
                        self._sub_account_cache[sub_account_id] = sub_account_name
                        return sub_account_name
                
                logger.error(f"{RED}Sub-account ID {sub_account_id} not found in response{RESET}")
                return None
            else:
                error_msg = result.get("msg", "Unknown error")
                logger.error(f"{RED}Failed to get sub-account name: {error_msg}{RESET}")
                return None
                
        except Exception as e:
            logger.error(f"{RED}Error getting sub-account name: {str(e)}{RESET}")
            return None

    def get_sub_accounts(self) -> List[Dict[str, Any]]:
        """Get all sub-accounts and their assets."""
        try:
            # Check if cache is still valid
            current_time = time.time()
            if current_time - self._sub_account_cache_time < self._sub_account_cache_ttl:
                # Return cached data if available
                if self._sub_account_cache:
                    return [{"subAccountName": name, "subUserId": uid} 
                            for uid, name in self._sub_account_cache.items()]
            
            # Use v2 API endpoint for sub-account assets
            endpoint = "/api/v2/mix/account/sub-account-assets"
            
            # Required parameters for v2 API
            params = {
                "productType": "USDT-FUTURES"  # Use USDT-FUTURES for USDT margined contracts
            }
            
            # Get current timestamp
            timestamp = str(int(time.time() * 1000))
            
            # Get headers with authentication
            headers = self._get_auth_headers(timestamp, "GET", endpoint, params)
            
            # Make the request
            response = _make_request("GET", f"{self.api_url}{endpoint}", 
                                  headers=headers, params=params)
            result = response.json()
            
            if result.get("code") == "00000" and result.get("data"):
                # Clear old cache
                self._sub_account_cache.clear()
                
                # Process and cache the results
                accounts = []
                for account_data in result["data"]:
                    user_id = account_data.get("userId")
                    if user_id:
                        # Generate a name based on the user ID
                        sub_account_name = f"sub_{user_id}"
                        # Cache the result
                        self._sub_account_cache[user_id] = sub_account_name
                        # Add to accounts list
                        accounts.append({
                            "subAccountName": sub_account_name,
                            "subUserId": user_id,
                            "assets": account_data.get("assetList", [])
                        })
                
                # Update cache timestamp
                self._sub_account_cache_time = current_time
                
                logger.info(f"{GREEN}Successfully retrieved {len(accounts)} sub-accounts{RESET}")
                return accounts
            else:
                error_msg = result.get("msg", "Unknown error")
                logger.error(f"{RED}Failed to get sub-accounts: {error_msg}{RESET}")
                return []
                
        except Exception as e:
            logger.error(f"{RED}Failed to get sub-accounts: {str(e)}{RESET}")
            return []

    def get_sub_account_balance(self, sub_account_name: str) -> Optional[Dict[str, Any]]:
        """Get balance for a specific sub-account.
        
        Args:
            sub_account_name: Name of the sub-account
            
        Returns:
            Dictionary containing sub-account balance if successful, None otherwise
        """
        endpoint = "/api/v2/account/sub-account-balance"
        timestamp = str(int(time.time() * 1000))
        
        # Set parameters
        params = {
            "subAccountName": sub_account_name,
            "productType": self.PRODUCT_TYPE_PARAM
        }
        
        # Get headers with authentication
        headers = self._get_auth_headers(timestamp, "GET", endpoint, params)
        
        try:
            response = _make_request("GET", f"{self.api_url}{endpoint}", 
                                  headers=headers, params=params)
            data = response.json()
            
            if data.get("code") == "00000" and data.get("data"):
                logger.info(f"{GREEN}Successfully retrieved sub-account balance{RESET}")
                return data["data"]
            else:
                error_msg = data.get("msg", "Unknown error")
                logger.error(f"{RED}Failed to get sub-account balance: {error_msg}{RESET}")
                return None
                
        except Exception as e:
            logger.error(f"{RED}Failed to get sub-account balance: {str(e)}{RESET}")
            return None

    def transfer_to_sub_account(self, sub_account_name: str, amount: float, coin: str = "USDT") -> Optional[Dict[str, Any]]:
        """Transfer funds to a sub-account.
        
        Args:
            sub_account_name: Name of the sub-account
            amount: Amount to transfer
            coin: Coin to transfer (default: USDT)
            
        Returns:
            Dictionary containing transfer details if successful, None otherwise
        """
        endpoint = "/api/v2/account/sub-account-transfer"
        timestamp = str(int(time.time() * 1000))
        
        # Set parameters
        data = {
            "subAccountName": sub_account_name,
            "amount": str(amount),
            "coin": coin,
            "productType": self.PRODUCT_TYPE_PARAM
        }
        
        # Get headers with authentication
        headers = self._get_auth_headers(timestamp, "POST", endpoint)
        
        try:
            response = _make_request("POST", f"{self.api_url}{endpoint}", 
                                  headers=headers, json=data)
            result = response.json()
            
            if result.get("code") == "00000" and result.get("data"):
                logger.info(f"{GREEN}Successfully transferred {amount} {coin} to {sub_account_name}{RESET}")
                return result["data"]
            else:
                error_msg = result.get("msg", "Unknown error")
                logger.error(f"{RED}Failed to transfer to sub-account: {error_msg}{RESET}")
                return None
                
        except Exception as e:
            logger.error(f"{RED}Failed to transfer to sub-account: {str(e)}{RESET}")
            return None

    @classmethod
    def setup_sub_accounts(cls, use_testnet: bool = True) -> Dict[str, 'BitGetTrader']:
        """Set up sub-accounts using environment variables.
        
        Args:
            use_testnet: Whether to use testnet (default: True)
            
        Returns:
            Dictionary of trader instances keyed by profile type
        """
        traders = {}
        profile_types = ["strategic", "aggressive", "scalping"]
        
        # Initialize main account trader
        main_trader = cls(
            profile_type="strategic",
            use_testnet=use_testnet,
            api_version="v2"
        )
        
        # For mainnet, only use the main account
        if not use_testnet:
            logger.info(f"{CYAN}Using main account only for mainnet trading{RESET}")
            traders["strategic"] = main_trader
            return traders
        
        # For testnet, set up sub-accounts
        for profile_type in profile_types:
            env_prefix = profile_type.upper()
            sub_account_name = os.environ.get(f"{env_prefix}_SUB_ACCOUNT_NAME")
            sub_account_password = os.environ.get(f"{env_prefix}_SUB_ACCOUNT_PASSWORD")
            initial_balance = float(os.environ.get(f"{env_prefix}_SUB_ACCOUNT_INITIAL_BALANCE", "0.0"))
            
            if sub_account_name and sub_account_password:
                # Create sub-account if it doesn't exist
                sub_accounts = main_trader.get_sub_accounts()
                if not sub_accounts or not any(acc["subAccountName"] == sub_account_name for acc in sub_accounts):
                    logger.info(f"{CYAN}Creating sub-account: {sub_account_name}{RESET}")
                    result = main_trader.create_sub_account(sub_account_name, sub_account_password)
                    if result and result.get("code") == "00000":
                        logger.info(f"{GREEN}Successfully created sub-account: {sub_account_name}{RESET}")
                    else:
                        logger.error(f"{RED}Failed to create sub-account: {sub_account_name}{RESET}")
                        continue
                
                # Transfer initial balance if specified
                if initial_balance > 0:
                    logger.info(f"{CYAN}Transferring initial balance to {sub_account_name}{RESET}")
                    result = main_trader.transfer_to_sub_account(sub_account_name, initial_balance)
                    if result and result.get("code") == "00000":
                        logger.info(f"{GREEN}Successfully transferred initial balance{RESET}")
                    else:
                        logger.error(f"{RED}Failed to transfer initial balance{RESET}")
                
                # Create trader instance for this sub-account
                traders[profile_type] = cls(
                    profile_type=profile_type,
                    use_testnet=use_testnet,
                    api_version="v2",
                    sub_account_name=sub_account_name
                )
                logger.info(f"{GREEN}Created trader instance for {sub_account_name}{RESET}")
            else:
                logger.warning(f"{YELLOW}Missing environment variables for {profile_type} sub-account{RESET}")
        
        return traders 