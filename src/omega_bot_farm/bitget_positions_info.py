#!/usr/bin/env python3

"""
BitGet Positions Information Module

This module provides utilities for retrieving and analyzing BitGet positions,
including position details, changes tracking, and portfolio analysis.

Copyright (c) 2024 OMEGA BTC AI
Licensed under the GBU2 License - see LICENSE file for details

This script connects to BitGet exchange and retrieves detailed information about current positions
using the BitgetPositionAnalyzerB0t. It uses the environment loader to access API credentials
and displays the data in a formatted way.
"""

import sys
import json
import asyncio
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import requests
import os
import ccxt
from colorama import Fore, Style, init

# Initialize colorama
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to sys.path if needed
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import environment loader
from src.omega_bot_farm.utils.env_loader import (
    get_env_var, get_bool_env_var, get_int_env_var, get_float_env_var
)

# Import BitgetPositionAnalyzerB0t
from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t

# Try to import CCXT directly to check for availability and version
try:
    CCXT_VERSION = ccxt.__version__
    CCXT_AVAILABLE = True
    logger.info(f"CCXT version {CCXT_VERSION} detected.")
except (ImportError, AttributeError):
    CCXT_VERSION = "N/A"
    CCXT_AVAILABLE = False
    logger.warning("CCXT library not installed. Some features will be limited.")


def format_currency(value: float) -> str:
    """Format a currency value with appropriate precision."""
    if abs(value) >= 1000:
        return f"${value:.2f}"
    elif abs(value) >= 1:
        return f"${value:.3f}"
    else:
        return f"${value:.6f}"


def format_percentage(value: float) -> str:
    """Format a percentage value with appropriate sign."""
    if value > 0:
        return f"+{value:.2f}%"
    else:
        return f"{value:.2f}%"


def print_horizontal_line(width: int = 80) -> None:
    """Print a horizontal line for separation."""
    print("=" * width)


def print_section_header(title: str, width: int = 80) -> None:
    """Print a section header with centered title."""
    print_horizontal_line(width)
    padding = max(0, (width - len(title) - 2) // 2)
    print(f"{' ' * padding}▶ {title} ◀{' ' * padding}")
    print_horizontal_line(width)


def validate_api_credentials(api_key: str, api_secret: str, api_passphrase: str, use_testnet: bool) -> Dict[str, Any]:
    """
    Validate API credentials by trying to connect to BitGet via CCXT.
    
    Args:
        api_key: BitGet API key
        api_secret: BitGet secret key
        api_passphrase: BitGet API passphrase
        use_testnet: Whether to use testnet
    
    Returns:
        Dictionary with validation result
    """
    try:
        # Configure exchange
        exchange_config = {
            'apiKey': api_key,
            'secret': api_secret,
            'password': api_passphrase,
            'enableRateLimit': True
        }
        
        # Create BitGet exchange client
        exchange = ccxt.bitget(exchange_config)
        
        # Set testnet mode if required
        if use_testnet:
            exchange.set_sandbox_mode(True)
            
        # Make a simple request to check connectivity
        balance = exchange.fetch_balance()
        
        # Check if we got a valid response
        if balance and 'total' in balance:
            logger.info("API key validation successful")
            return {
                "valid": True,
                "message": "Successfully connected to BitGet via CCXT"
            }
        
        logger.warning("API key validation failed. Incomplete response from BitGet")
        return {
            "valid": False,
            "message": "API key validation failed. Incomplete response from BitGet"
        }
    
    except Exception as e:
        error_message = f"API key validation failed. Error: {str(e)}"
        logger.error(error_message)
        return {
            "valid": False,
            "message": error_message
        }


async def get_positions_info(use_multiple_methods: bool = False) -> Dict[str, Any]:
    """
    Retrieve positions information from BitGet.
    
    Args:
        use_multiple_methods: Whether to try multiple connection methods
        
    Returns:
        Dictionary with position information
    """
    # Get environment variables
    api_key = get_env_var("BITGET_API_KEY", "")
    api_secret = get_env_var("BITGET_SECRET_KEY", "")
    api_passphrase = get_env_var("BITGET_PASSPHRASE", "")
    use_testnet = get_bool_env_var("BITGET_USE_TESTNET", False)
    
    # Validate API credentials
    if not api_key or not api_secret or not api_passphrase:
        error_message = "Missing API credentials. Please check your .env file."
        logger.error(error_message)
        return {
            "error": error_message,
            "connection": "NOT CONNECTED",
            "positions": [],
            "account": {},
            "changes": {}
        }
    
    # Log connection info
    network_type = "TESTNET" if use_testnet else "MAINNET"
    logger.info(f"Connecting to BitGet {network_type}")
    logger.info(f"API Key available: {'Yes' if api_key else 'No'}")
    
    # Validate API credentials
    validation_result = validate_api_credentials(api_key, api_secret, api_passphrase, use_testnet)
    if not validation_result["valid"]:
        logger.error(f"API key validation failed. Please check your credentials. - {validation_result['message']}")
        return {
            "error": f"API key validation failed. Please check your credentials.",
            "connection": "NOT CONNECTED",
            "positions": [],
            "account": {},
            "changes": {}
        }
    
    try:
        # Connect to BitGet via CCXT
        exchange_config = {
            'apiKey': api_key,
            'secret': api_secret,
            'password': api_passphrase,
            'enableRateLimit': True
        }
        
        # Create BitGet exchange client
        exchange = ccxt.bitget(exchange_config)
        
        # Set testnet mode if required
        if use_testnet:
            exchange.set_sandbox_mode(True)
            logger.info("Using TESTNET environment")
        else:
            logger.info("Using MAINNET environment")
        
        # Get positions
        try:
            positions = exchange.fetch_positions()
            logger.info(f"Successfully fetched {len(positions)} positions from BitGet")
        except Exception as e:
            logger.error(f"Error fetching positions: {str(e)}")
            positions = []
        
        # Filter out positions with zero size
        active_positions = []
        for position in positions:
            contracts = float(position.get('contracts', 0) or 0)
            if contracts > 0:
                active_positions.append(position)
        
        # Get account balance
        try:
            balance = exchange.fetch_balance()
            account_data = {
                "total_balance": float(balance.get('total', {}).get('USDT', 0) or 0),
                "free_balance": float(balance.get('free', {}).get('USDT', 0) or 0),
                "used_balance": float(balance.get('used', {}).get('USDT', 0) or 0)
            }
            logger.info(f"Successfully fetched account balance from BitGet")
        except Exception as e:
            logger.error(f"Error fetching account balance: {str(e)}")
            account_data = {
                "total_balance": 0.0,
                "free_balance": 0.0,
                "used_balance": 0.0
            }
        
        # Return data
        return {
            "connection": "CCXT",
            "positions": active_positions,
            "account": account_data,
            "changes": {}
        }
    
    except Exception as e:
        error_message = f"Error connecting to BitGet: {str(e)}"
        logger.error(error_message)
        return {
            "error": error_message,
            "connection": "ERROR",
            "positions": [],
            "account": {},
            "changes": {}
        }


def print_account_summary(account_data: Dict[str, float]) -> None:
    """Print account summary information."""
    print_section_header("ACCOUNT SUMMARY")
    
    equity = account_data.get("equity", 0)
    total_pnl = account_data.get("total_pnl", 0)
    long_exposure = account_data.get("long_exposure", 0)
    short_exposure = account_data.get("short_exposure", 0)
    long_short_ratio = account_data.get("long_short_ratio", 0)
    harmony_score = account_data.get("harmony_score", 0)
    
    print(f"Account Equity: {format_currency(equity)}")
    print(f"Total PnL: {format_currency(total_pnl)} ({format_percentage((total_pnl/max(1, equity))*100)})")
    print(f"Long Exposure: {format_currency(long_exposure)} ({format_percentage((long_exposure/max(1, equity))*100)} of equity)")
    print(f"Short Exposure: {format_currency(short_exposure)} ({format_percentage((short_exposure/max(1, equity))*100)} of equity)")
    print(f"Long/Short Ratio: {long_short_ratio:.2f}")
    print(f"Harmony Score: {harmony_score:.2f} / 1.0")
    print()


def print_connection_info(positions_data: Dict[str, Any]) -> None:
    """Print connection information."""
    print_section_header("CONNECTION INFORMATION")
    
    connection = positions_data.get("connection", "Unknown")
    connection_method = positions_data.get("connection_method", "Unknown")
    ccxt_version = positions_data.get("ccxt_version", CCXT_VERSION)
    ccxt_available = positions_data.get("ccxt_available", CCXT_AVAILABLE)
    
    print(f"Connection Status: {connection}")
    print(f"Connection Method: {connection_method}")
    print(f"CCXT Version: {ccxt_version}")
    print(f"CCXT Available: {'Yes' if ccxt_available else 'No'}")
    print()


def print_position_details(positions: List[Dict[str, Any]]) -> None:
    """Print detailed information about each position."""
    if not positions:
        print_section_header("NO ACTIVE POSITIONS")
        return
    
    print_section_header(f"POSITION DETAILS ({len(positions)} active)")
    
    for i, position in enumerate(positions):
        symbol = position.get("symbol", "Unknown")
        side = position.get("side", "Unknown").upper()
        entry_price = position.get("entryPrice", 0)
        mark_price = position.get("markPrice", 0)
        contracts = position.get("contracts", 0)
        notional = position.get("notional", 0)
        leverage = position.get("leverage", 1)
        unrealized_pnl = position.get("unrealizedPnl", 0)
        liquidation_price = position.get("liquidationPrice", 0)
        
        # Calculate price movement percentage
        price_change_pct = ((mark_price - entry_price) / entry_price) * 100
        if side.lower() == "short":
            price_change_pct = -price_change_pct
        
        # Color indicators (emoji)
        pnl_indicator = "🟢" if unrealized_pnl > 0 else "🔴"
        
        print(f"Position {i+1}: {symbol} {side}")
        print(f"  Size: {contracts} contracts (Notional: {format_currency(notional)})")
        print(f"  Entry: {format_currency(entry_price)}, Mark: {format_currency(mark_price)} ({format_percentage(price_change_pct)})")
        print(f"  Leverage: {leverage}x")
        print(f"  PnL: {pnl_indicator} {format_currency(unrealized_pnl)} ({format_percentage((unrealized_pnl/max(0.01, notional))*100)})")
        print(f"  Liquidation Price: {format_currency(liquidation_price)}")
        
        # Print separator between positions, except for the last one
        if i < len(positions) - 1:
            print("  " + "-" * 30)
    print()


def print_changes_summary(changes: Dict[str, List]) -> None:
    """Print summary of position changes."""
    print_section_header("RECENT CHANGES")
    
    new_positions = changes.get("new", [])
    closed_positions = changes.get("closed", [])
    modified_positions = changes.get("changed", [])
    
    if not new_positions and not closed_positions and not modified_positions:
        print("No recent changes detected.\n")
        return
    
    if new_positions:
        print(f"New Positions ({len(new_positions)}):")
        for pos in new_positions:
            symbol = pos.get("symbol", "Unknown")
            side = pos.get("side", "Unknown").upper()
            contracts = pos.get("contracts", 0)
            print(f"  ➕ {symbol} {side} ({contracts} contracts)")
    
    if closed_positions:
        print(f"Closed Positions ({len(closed_positions)}):")
        for pos in closed_positions:
            symbol = pos.get("symbol", "Unknown")
            side = pos.get("side", "Unknown").upper()
            contracts = pos.get("contracts", 0)
            print(f"  ➖ {symbol} {side} ({contracts} contracts)")
    
    if modified_positions:
        print(f"Modified Positions ({len(modified_positions)}):")
        for change in modified_positions:
            symbol = change.get("symbol", "Unknown")
            side = change.get("side", "Unknown").upper()
            old_contracts = change.get("old_contracts", 0)
            new_contracts = change.get("new_contracts", 0)
            contracts_change = new_contracts - old_contracts
            change_str = f"+{contracts_change}" if contracts_change > 0 else str(contracts_change)
            print(f"  🔄 {symbol} {side} ({change_str} contracts)")
    
    print()


def print_help() -> None:
    """Print help information for the script."""
    print_section_header("BITGET POSITIONS INFO - HELP")
    print("This script retrieves and displays information about your BitGet positions.")
    print("It requires valid BitGet API credentials to be set in one of the .env files.\n")
    
    print("Usage:")
    print("  python bitget_positions_info.py [OPTIONS]\n")
    
    print("Options:")
    print("  --setup          Run the interactive setup to configure API credentials")
    print("  --show-help      Show this help message and exit")
    print("  --testnet        Force use of BitGet testnet regardless of .env setting")
    print("  --validate       Only validate the API credentials without fetching positions")
    print("  --print-keys     Print the API keys loaded from environment variables")
    print("  --multi-connect  Try multiple connection methods (CCXT direct is primary, with ExchangeClientB0t and ExchangeService as fallbacks)\n")
    
    print("Environment Configuration:")
    print("  The script uses environment variables from the following .env files:")
    print("  1. Root .env: /Users/fsiqueira/Desktop/GitHub/omega-btc-ai/.env")
    print("  2. Bot Farm .env: /Users/fsiqueira/Desktop/GitHub/omega-btc-ai/src/omega_bot_farm/.env")
    print("  Bot Farm .env values take precedence over Root .env values.\n")
    
    print("Required API Credentials:")
    print("  BITGET_API_KEY       Your BitGet API key")
    print("  BITGET_SECRET_KEY    Your BitGet API secret")
    print("  BITGET_PASSPHRASE    Your BitGet API passphrase")
    print("  BITGET_USE_TESTNET   Whether to use BitGet testnet (true/false)")
    print()


def print_api_credentials():
    """Print the current API credentials loaded from environment variables."""
    api_key = get_env_var("BITGET_API_KEY", "")
    api_secret = get_env_var("BITGET_SECRET_KEY", "")
    api_passphrase = get_env_var("BITGET_PASSPHRASE", "")
    use_testnet = get_bool_env_var("BITGET_USE_TESTNET", False)
    
    print_section_header("API CREDENTIALS")
    print(f"Network: {'TESTNET' if use_testnet else 'MAINNET'}")
    print(f"API Key: {api_key}")
    print(f"API Secret: {api_secret}")
    print(f"API Passphrase: {api_passphrase}")
    print()
    print("Warning: These credentials should be kept secure.")
    print("Do not share them with anyone or include them in screenshots or logs.")
    print()
    
    # Print where they are loaded from
    root_env_path = Path(__file__).parent.parent.parent.parent / ".env"
    bot_farm_env_path = Path(__file__).parent.parent / ".env"
    
    print("Credentials loaded from:")
    if root_env_path.exists():
        print(f"- Root .env: {root_env_path}")
    if bot_farm_env_path.exists():
        print(f"- Bot Farm .env: {bot_farm_env_path}")
    print()


async def main() -> None:
    """Main function to retrieve and display BitGet position information."""
    try:
        # Get command line args
        parser = argparse.ArgumentParser(description="BitGet Positions Information Retriever")
        parser.add_argument("--multi-connect", action="store_true", help="Try multiple connection methods")
        args, _ = parser.parse_known_args()
        
        print("\n🧬 OMEGA BOT FARM - BitGet Positions Information 🧬\n")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Retrieve positions information
        positions_data = await get_positions_info(use_multiple_methods=args.multi_connect)
        
        # Check if there was an error
        if "error" in positions_data:
            error_msg = positions_data.get("error", "Unknown error")
            print_section_header("ERROR")
            print(f"Error: {error_msg}")
            print("\nPlease check the following:")
            print("1. Your API key, secret, and passphrase are correct")
            print("2. The API key has trading permissions")
            print("3. The API key is activated and not expired")
            print("4. You're connecting to the correct network (mainnet/testnet)")
            print("\nYou can update your API credentials in the .env file:")
            print("- Root .env: /Users/fsiqueira/Desktop/GitHub/omega-btc-ai/.env")
            print("- Bot Farm .env: /Users/fsiqueira/Desktop/GitHub/omega-btc-ai/src/omega_bot_farm/.env")
            print("\nThe Bot Farm .env file will take precedence if both files have credentials.")
            print()
            return
        
        # Extract data
        positions = positions_data.get("positions", [])
        account = positions_data.get("account", {})
        changes = positions_data.get("changes", {})
        
        # Print connection information
        print_connection_info(positions_data)
        
        # Print account summary
        print_account_summary(account)
        
        # Print position details
        print_position_details(positions)
        
        # Print changes summary
        print_changes_summary(changes)
        
        print_section_header("COMPLETION")
        print("BitGet position data retrieval complete.\n")
        
    except Exception as e:
        logger.error(f"Error in main function: {e}")
        print_section_header("UNEXPECTED ERROR")
        print(f"An unexpected error occurred: {e}")
        print("Please check the logs for more details.\n")


def update_env_file(env_file_path: str, api_key: str, api_secret: str, api_passphrase: str, use_testnet: bool) -> bool:
    """
    Update the API credentials in an .env file.
    
    Args:
        env_file_path: Path to the .env file
        api_key: BitGet API key
        api_secret: BitGet API secret
        api_passphrase: BitGet API passphrase
        use_testnet: Whether to use testnet
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Read the current file
        with open(env_file_path, 'r') as f:
            lines = f.readlines()
        
        # Track which fields we've updated
        updated_fields = {
            'BITGET_API_KEY': False,
            'BITGET_SECRET_KEY': False,
            'BITGET_PASSPHRASE': False,
            'BITGET_USE_TESTNET': False
        }
        
        # Update existing lines
        new_lines = []
        for line in lines:
            line = line.rstrip()
            
            if line.startswith('BITGET_API_KEY='):
                new_lines.append(f'BITGET_API_KEY="{api_key}"')
                updated_fields['BITGET_API_KEY'] = True
            elif line.startswith('BITGET_SECRET_KEY='):
                new_lines.append(f'BITGET_SECRET_KEY="{api_secret}"')
                updated_fields['BITGET_SECRET_KEY'] = True
            elif line.startswith('BITGET_PASSPHRASE='):
                new_lines.append(f'BITGET_PASSPHRASE="{api_passphrase}"')
                updated_fields['BITGET_PASSPHRASE'] = True
            elif line.startswith('BITGET_USE_TESTNET='):
                new_lines.append(f'BITGET_USE_TESTNET={str(use_testnet).lower()}')
                updated_fields['BITGET_USE_TESTNET'] = True
            else:
                new_lines.append(line)
        
        # Add any missing fields at the end
        if not updated_fields['BITGET_API_KEY']:
            new_lines.append(f'BITGET_API_KEY="{api_key}"')
        if not updated_fields['BITGET_SECRET_KEY']:
            new_lines.append(f'BITGET_SECRET_KEY="{api_secret}"')
        if not updated_fields['BITGET_PASSPHRASE']:
            new_lines.append(f'BITGET_PASSPHRASE="{api_passphrase}"')
        if not updated_fields['BITGET_USE_TESTNET']:
            new_lines.append(f'BITGET_USE_TESTNET={str(use_testnet).lower()}')
        
        # Write the updated file
        with open(env_file_path, 'w') as f:
            f.write('\n'.join(new_lines) + '\n')
        
        return True
    except Exception as e:
        logger.error(f"Error updating .env file: {e}")
        return False


def prompt_for_credentials() -> Dict[str, Any]:
    """
    Prompt the user for BitGet API credentials interactively.
    
    Returns:
        Dictionary with the entered credentials
    """
    print_section_header("BITGET API CREDENTIALS SETUP")
    print("Please enter your BitGet API credentials:\n")
    
    api_key = input("API Key: ").strip()
    api_secret = input("API Secret: ").strip()
    api_passphrase = input("API Passphrase: ").strip()
    
    use_testnet_input = input("Use Testnet? (y/N): ").strip().lower()
    use_testnet = use_testnet_input in ['y', 'yes', 'true', '1']
    
    which_env_file = input("Which .env file to update? (1: Root .env, 2: Bot Farm .env, 3: Both): ").strip()
    
    return {
        "api_key": api_key,
        "api_secret": api_secret,
        "api_passphrase": api_passphrase,
        "use_testnet": use_testnet,
        "update_root_env": which_env_file in ['1', '3'],
        "update_bot_farm_env": which_env_file in ['2', '3']
    }


def setup_credentials_interactive() -> bool:
    """
    Interactive setup for BitGet API credentials.
    
    Returns:
        True if credentials were successfully updated, False otherwise
    """
    # Get project root
    project_root = Path(__file__).parent.parent.parent.parent
    root_env_path = project_root / ".env"
    bot_farm_env_path = project_root / "src" / "omega_bot_farm" / ".env"
    
    # Check if env files exist
    root_env_exists = root_env_path.exists()
    bot_farm_env_exists = bot_farm_env_path.exists()
    
    print(f"Root .env file exists: {root_env_exists}")
    print(f"Bot Farm .env file exists: {bot_farm_env_exists}")
    
    if not root_env_exists and not bot_farm_env_exists:
        print("Neither .env file exists. Creating Bot Farm .env file.")
        bot_farm_env_path.parent.mkdir(parents=True, exist_ok=True)
        with open(bot_farm_env_path, 'w') as f:
            f.write("# BitGet API Credentials\n")
        bot_farm_env_exists = True
    
    # Prompt for credentials
    credentials = prompt_for_credentials()
    
    success = True
    
    # Update root .env file if requested
    if credentials["update_root_env"] and root_env_exists:
        print(f"Updating Root .env file at {root_env_path}...")
        root_success = update_env_file(
            str(root_env_path),
            credentials["api_key"],
            credentials["api_secret"],
            credentials["api_passphrase"],
            credentials["use_testnet"]
        )
        if root_success:
            print("Root .env file updated successfully.")
        else:
            print("Failed to update Root .env file.")
        success = success and root_success
    
    # Update bot farm .env file if requested
    if credentials["update_bot_farm_env"] and bot_farm_env_exists:
        print(f"Updating Bot Farm .env file at {bot_farm_env_path}...")
        bot_farm_success = update_env_file(
            str(bot_farm_env_path),
            credentials["api_key"],
            credentials["api_secret"],
            credentials["api_passphrase"],
            credentials["use_testnet"]
        )
        if bot_farm_success:
            print("Bot Farm .env file updated successfully.")
        else:
            print("Failed to update Bot Farm .env file.")
        success = success and bot_farm_success
    
    return success


async def main_wrapper():
    """Wrapper for main function to handle command line arguments."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="BitGet Positions Information Retriever")
    parser.add_argument("--setup", action="store_true", help="Run the interactive setup to configure API credentials")
    parser.add_argument("--show-help", action="store_true", help="Show detailed help information")
    parser.add_argument("--testnet", action="store_true", help="Force use of BitGet testnet regardless of .env setting")
    parser.add_argument("--validate", action="store_true", help="Only validate the API credentials without fetching positions")
    parser.add_argument("--print-keys", action="store_true", help="Print the API keys loaded from environment variables")
    parser.add_argument("--multi-connect", action="store_true", help="Try multiple connection methods for BitGet")
    args = parser.parse_args()
    
    # If show-help flag is provided, show help and exit
    if args.show_help:
        print_help()
        return
    
    # If print-keys flag is provided, print the API credentials and exit
    if args.print_keys:
        print_api_credentials()
        return
    
    # If setup flag is provided, run the interactive setup
    if args.setup:
        success = setup_credentials_interactive()
        if success:
            print("\nCredentials updated successfully. Now trying to connect to BitGet...")
            await main()
        else:
            print("\nFailed to update credentials. Please try again.")
        return
    
    # If validate flag is provided, run validation only
    if args.validate:
        api_key = get_env_var("BITGET_API_KEY", "")
        api_secret = get_env_var("BITGET_SECRET_KEY", "")
        api_passphrase = get_env_var("BITGET_PASSPHRASE", "")
        use_testnet = get_bool_env_var("BITGET_USE_TESTNET", False) or args.testnet
        
        print("\n🧬 OMEGA BOT FARM - BitGet API Validation 🧬\n")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Network: {'TESTNET' if use_testnet else 'MAINNET'}")
        
        # Add CCXT version information to the output
        if CCXT_AVAILABLE:
            print(f"CCXT Version: {CCXT_VERSION}")
        else:
            print("CCXT: Not installed")
        
        validation_result = validate_api_credentials(api_key, api_secret, api_passphrase, use_testnet)
        
        if validation_result.get("valid", False):
            print_section_header("VALIDATION SUCCESSFUL")
            print("Your BitGet API credentials are valid!")
            print(f"Response: {validation_result.get('response', {})}")
            
            # If multi-connect flag is provided, try direct CCXT connection
            if args.multi_connect and CCXT_AVAILABLE:
                print("\nDirect CCXT connection is available.")
                print("Connected to BitGet via CCXT")
        else:
            print_section_header("VALIDATION FAILED")
            print(f"Error: {validation_result.get('message')}")
            print(f"Details: {validation_result.get('details', 'No details available')}")
            print("\nPlease run with the --setup flag to update your credentials.")
        
        return
    
    # Otherwise, run the normal main function with testnet flag applied if provided
    if args.testnet:
        os.environ["BITGET_USE_TESTNET"] = "true"
    
    await main()


if __name__ == "__main__":
    try:
        # Handle the case where the user requests help
        if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
            print_help()
        else:
            # Otherwise, run the main wrapper
            asyncio.run(main_wrapper())
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        print(f"Unhandled exception: {e}") 