#!/usr/bin/env python3
"""
OMEGA BTC AI - Open Positions Summary
=====================================

A script that generates a summary of all current open positions across all traders.
Uses the same authentication approach as the BitGet live traders.

Author: OMEGA BTC AI Team
"""

import os
import sys
import json
import asyncio
import argparse
from datetime import datetime, timezone, timedelta
from tabulate import tabulate
from colorama import Fore, Style, init

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader
from omega_ai.trading.profiles import (
    StrategicTrader,
    AggressiveTrader,
    NewbieTrader,
    ScalperTrader
)

# Initialize colorama
init(autoreset=True)

class PositionsSummary:
    """Summarizes current open positions from BitGet."""
    
    def __init__(self, 
                 use_testnet: bool = False,
                 symbol: str = "",
                 target_profit_pct: float = 2.0):
        """
        Initialize the positions summary.
        
        Args:
            use_testnet: Whether to use testnet (default: False)
            symbol: Trading symbol (default: empty string, which means all symbols)
            target_profit_pct: Target profit percentage for positions (default: 2.0%)
        """
        self.use_testnet = use_testnet
        self.symbol = symbol
        self.target_profit_pct = target_profit_pct
        self.wallet_target = 1000.0  # Default target of 1000 USDT
        
        # Get API credentials from environment variables
        self.api_key = os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        self.secret_key = os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        self.passphrase = os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        
        # Verify API credentials are available
        if not self.api_key or not self.secret_key or not self.passphrase:
            print(f"{Fore.RED}Error: API credentials are missing. Please set environment variables.{Style.RESET_ALL}")
            print(f"Required variables: {'BITGET_TESTNET_API_KEY' if use_testnet else 'BITGET_API_KEY'}, " + 
                  f"{'BITGET_TESTNET_SECRET_KEY' if use_testnet else 'BITGET_SECRET_KEY'}, " +
                  f"{'BITGET_TESTNET_PASSPHRASE' if use_testnet else 'BITGET_PASSPHRASE'}")
            print(f"{Fore.YELLOW}API Key Preview: {self.api_key[:5]}...{self.api_key[-3:] if len(self.api_key) > 5 else ''}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Secret Key Length: {len(self.secret_key)} characters{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Passphrase Length: {len(self.passphrase)} characters{Style.RESET_ALL}")
            sys.exit(1)
        else:
            print(f"{Fore.GREEN}API credentials loaded. API Key: {self.api_key[:5]}...{self.api_key[-3:] if len(self.api_key) > 5 else ''}{Style.RESET_ALL}")
        
        # Create BitGet trader instances for each profile
        self.traders = {
            "strategic": BitGetTrader(
                profile_type="strategic",
                api_key=self.api_key,
                secret_key=self.secret_key,
                passphrase=self.passphrase,
                use_testnet=self.use_testnet,
                api_version="v1"
            ),
            "aggressive": BitGetTrader(
                profile_type="aggressive",
                api_key=self.api_key,
                secret_key=self.secret_key,
                passphrase=self.passphrase,
                use_testnet=self.use_testnet,
                api_version="v1"
            ),
            "newbie": BitGetTrader(
                profile_type="newbie",
                api_key=self.api_key,
                secret_key=self.secret_key,
                passphrase=self.passphrase,
                use_testnet=self.use_testnet,
                api_version="v1"
            ),
            "scalper": BitGetTrader(
                profile_type="scalper",
                api_key=self.api_key,
                secret_key=self.secret_key,
                passphrase=self.passphrase,
                use_testnet=self.use_testnet,
                api_version="v1"
            )
        }
    
    def _create_progress_bar(self, current, target, width=40):
        """Create a colorful progress bar showing progress towards target."""
        percent = min(current / target, 1.0) if target > 0 else 0
        filled_width = int(width * percent)
        empty_width = width - filled_width
        
        # Choose color based on progress
        if percent < 0.3:
            color = Fore.RED
        elif percent < 0.7:
            color = Fore.YELLOW
        else:
            color = Fore.GREEN
            
        # Create the progress bar
        bar = f"{color}{'█' * filled_width}{Fore.WHITE}{'░' * empty_width}{Style.RESET_ALL}"
        percent_str = f"{percent * 100:.1f}%"
        
        return f"{bar} {percent_str} ({current:.2f}/{target:.2f} USDT)"
    
    async def get_wallet_info(self):
        """Get wallet information from BitGet."""
        wallet_info = {
            'total_balance': 0.0,
            'available_balance': 0.0,
            'wallet_address': 'Not available',
            'asset_details': {}
        }
        
        # Use the first trader to get account info
        if self.traders:
            try:
                trader = next(iter(self.traders.values()))
                account_info = trader.get_account_balance()
                
                if account_info and isinstance(account_info, dict):
                    wallet_info['total_balance'] = float(account_info.get('equity', 0))
                    wallet_info['available_balance'] = float(account_info.get('available', 0))
                    wallet_info['asset_details']['USDT'] = {
                        'total': float(account_info.get('equity', 0)),
                        'available': float(account_info.get('available', 0)),
                        'frozen': float(account_info.get('equity', 0)) - float(account_info.get('available', 0))
                    }
                    
                # Use API key as identifier
                if self.api_key:
                    wallet_info['wallet_address'] = f"BitGet:{self.api_key[:8]}..."
            except Exception as e:
                print(f"{Fore.RED}Error getting wallet information: {str(e)}{Style.RESET_ALL}")
                # Check if it's a signature error
                if "sign signature error" in str(e).lower():
                    print(f"{Fore.YELLOW}Authentication error detected. Please check your API credentials.{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Tip: API keys must have read permissions for account data.{Style.RESET_ALL}")
        
        return wallet_info
        
    async def get_all_positions(self):
        """Get all open positions for all traders."""
        all_positions = []
        current_prices = {}
        market_data = {}
        
        print(f"{Fore.CYAN}Fetching open positions...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}API authentication using key: {self.api_key[:5]}...{Style.RESET_ALL}")
        
        # Track if we've seen authentication errors
        auth_error_seen = False
        
        # Test authentication first to verify API credentials
        try:
            # Use the first trader to test authentication
            trader = next(iter(self.traders.values()))
            test_result = trader.get_market_ticker("BTCUSDT_UMCBL")
            if test_result:
                print(f"{Fore.GREEN}Authentication test successful!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Authentication test failed - API returned empty response{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Authentication test error: {str(e)}{Style.RESET_ALL}")
            if "sign signature error" in str(e).lower():
                auth_error_seen = True
                print(f"{Fore.YELLOW}API signature verification failed. Check your API key, secret and passphrase.{Style.RESET_ALL}")
            # Continue anyway to show details of the error
        
        for profile_name, trader in self.traders.items():
            # Skip this trader if we've already seen auth errors
            if auth_error_seen:
                print(f"{Fore.YELLOW}Skipping {profile_name} trader due to previous authentication errors{Style.RESET_ALL}")
                continue
                
            try:
                positions = []
                # Get positions
                if self.symbol:
                    positions = trader.get_positions(self.symbol) or []
                    
                    # Get current price and market data if we don't have it yet
                    if self.symbol not in current_prices:
                        ticker = trader.get_market_ticker(self.symbol)
                        if ticker and 'last' in ticker:
                            current_prices[self.symbol] = float(ticker['last'])
                            # Store market data for this symbol
                            market_data[self.symbol] = {
                                'price': float(ticker['last']),
                                'high_24h': float(ticker.get('high24h', 0)),
                                'low_24h': float(ticker.get('low24h', 0)),
                                'price_change_24h': float(ticker.get('priceChangePercent', 0)) * 100,
                                'volume_24h': float(ticker.get('baseVolume', 0)),
                                'funding_rate': float(ticker.get('fundingRate', 0)) * 100,
                                'timestamp': datetime.now(timezone.utc)
                            }
                else:
                    # The get_all_positions method might not be implemented in BitGetTrader
                    # So we'll create a simple implementation here
                    try:
                        print(f"{Fore.YELLOW}Attempting to get all positions for {profile_name}...{Style.RESET_ALL}")
                        # Try to call the method if it exists
                        if hasattr(trader, 'get_all_positions'):
                            positions = trader.get_all_positions() or []
                        else:
                            # Fallback to checking common symbols
                            print(f"{Fore.YELLOW}get_all_positions not available, checking common symbols...{Style.RESET_ALL}")
                            common_symbols = ["BTCUSDT_UMCBL", "ETHUSDT_UMCBL", "SOLUSDT_UMCBL", "XRPUSDT_UMCBL"]
                            positions = []
                            
                            for symbol in common_symbols:
                                try:
                                    symbol_positions = trader.get_positions(symbol) or []
                                    positions.extend(symbol_positions)
                                except Exception as sym_err:
                                    # Skip symbols that fail
                                    continue
                    except Exception as general_err:
                        error_msg = str(general_err)
                        print(f"{Fore.RED}Error getting all positions: {error_msg}{Style.RESET_ALL}")
                        if "sign signature error" in error_msg.lower():
                            auth_error_seen = True
                            print(f"{Fore.YELLOW}API signature verification failed. Check your API key, secret and passphrase.{Style.RESET_ALL}")
                            print(f"{Fore.YELLOW}Will continue with partial data...{Style.RESET_ALL}")
                        continue
                    
                    # Get current prices and market data for all symbols with positions
                    for pos in positions:
                        symbol = pos.get('symbol')
                        if symbol and symbol not in current_prices:
                            try:
                                ticker = trader.get_market_ticker(symbol)
                                if ticker and 'last' in ticker:
                                    current_prices[symbol] = float(ticker['last'])
                                    # Store market data for this symbol
                                    market_data[symbol] = {
                                        'price': float(ticker['last']),
                                        'high_24h': float(ticker.get('high24h', 0)),
                                        'low_24h': float(ticker.get('low24h', 0)),
                                        'price_change_24h': float(ticker.get('priceChangePercent', 0)) * 100,
                                        'volume_24h': float(ticker.get('baseVolume', 0)),
                                        'funding_rate': float(ticker.get('fundingRate', 0)) * 100,
                                        'timestamp': datetime.now(timezone.utc)
                                    }
                            except Exception as ticker_err:
                                # Continue with partial data if ticker fetch fails
                                print(f"{Fore.YELLOW}Error getting ticker for {symbol}: {str(ticker_err)}{Style.RESET_ALL}")
                                continue
                
                # Add profile name to each position
                for position in positions:
                    position['profile'] = profile_name
                    all_positions.append(position)
                    
            except Exception as e:
                error_msg = str(e)
                print(f"{Fore.RED}Error getting positions for {profile_name}: {error_msg}{Style.RESET_ALL}")
                if "sign signature error" in error_msg.lower():
                    auth_error_seen = True
                    print(f"{Fore.YELLOW}API signature verification failed. Skipping remaining traders.{Style.RESET_ALL}")
                    break
        
        if auth_error_seen:
            print(f"\n{Fore.YELLOW}=== AUTHENTICATION TROUBLESHOOTING TIPS ==={Style.RESET_ALL}")
            print(f"{Fore.YELLOW}1. Check that your API key, secret key, and passphrase are correct{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}2. Ensure your API key has read permissions for account and positions{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}3. Check if you're using testnet flag correctly (--testnet for testnet, --mainnet for mainnet){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}4. Verify that your API key is not expired or restricted by IP{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}5. Time synchronization issues can sometimes cause signature errors{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Running with limited functionality...\n{Style.RESET_ALL}")
            
        return all_positions, current_prices, market_data
    
    def _determine_market_trend(self, market_data, symbol):
        """Determine the market trend for the given symbol."""
        data = market_data.get(symbol, {})
        if not data:
            return f"{Fore.YELLOW}UNKNOWN{Style.RESET_ALL}"
        
        # Get price change percentage for 24h
        price_change = data.get('price_change_24h', 0)
        
        # Determine trend based on price change
        if price_change > 3:
            return f"{Fore.GREEN}STRONG BULLISH ({price_change:.2f}%){Style.RESET_ALL}"
        elif price_change > 1:
            return f"{Fore.GREEN}BULLISH ({price_change:.2f}%){Style.RESET_ALL}"
        elif price_change > -1:
            return f"{Fore.YELLOW}NEUTRAL ({price_change:.2f}%){Style.RESET_ALL}"
        elif price_change > -3:
            return f"{Fore.RED}BEARISH ({price_change:.2f}%){Style.RESET_ALL}"
        else:
            return f"{Fore.RED}STRONG BEARISH ({price_change:.2f}%){Style.RESET_ALL}"
    
    def generate_summary(self, positions, current_prices, market_data, wallet_info):
        """Generate a summary of open positions."""
        if not positions:
            print(f"{Fore.YELLOW}No open positions found.{Style.RESET_ALL}")
            return
        
        # Map BitGet position fields to our expected format and filter open positions
        # BitGet uses 'holdSide' for position side (long/short) and doesn't have explicit 'status' field
        processed_positions = []
        for pos in positions:
            if 'holdSide' in pos and pos.get('total', 0) and float(pos.get('total', 0)) > 0:
                # Map to our expected format
                processed_pos = {
                    'symbol': pos.get('symbol', 'UNKNOWN'),
                    'profile': pos.get('profile', 'UNKNOWN'),
                    'side': pos.get('holdSide', 'UNKNOWN').upper(),
                    'size': float(pos.get('total', 0)),
                    'entry_price': float(pos.get('averageOpenPrice', 0)),
                    'unrealized_pnl': float(pos.get('unrealizedPL', 0)),
                    'realized_pnl': float(pos.get('achievedProfits', 0)),
                    'leverage': int(pos.get('leverage', 1)),
                    'status': 'OPEN'  # BitGet positions with size > 0 are considered open
                }
                processed_positions.append(processed_pos)
        
        open_positions = processed_positions
        
        if not open_positions:
            print(f"{Fore.YELLOW}No open positions found.{Style.RESET_ALL}")
            return
        
        # Print wallet information first
        print(f"\n{Fore.MAGENTA}===== WALLET INFORMATION ====={Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Wallet Address: {Fore.CYAN}{wallet_info.get('wallet_address', 'Not available')}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Total Balance: {Fore.CYAN}{wallet_info.get('total_balance', 0):.2f} USDT{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Available Balance: {Fore.CYAN}{wallet_info.get('available_balance', 0):.2f} USDT{Style.RESET_ALL}")
        
        # Display progress bar if wallet information is available
        if wallet_info.get('total_balance', 0) > 0:
            print(f"{Fore.MAGENTA}Progress to Target ({self.wallet_target:.0f} USDT):{Style.RESET_ALL}")
            print(self._create_progress_bar(wallet_info.get('total_balance', 0), self.wallet_target))
        else:
            print(f"{Fore.YELLOW}Wallet information unavailable - authentication error or insufficient permissions{Style.RESET_ALL}")
            
        # Check if we have market data before showing the market summary
        if market_data:
            # Print market summary
            print(f"\n{Fore.CYAN}===== MARKET SUMMARY ====={Style.RESET_ALL}")
            for symbol, data in market_data.items():
                trend = self._determine_market_trend(market_data, symbol)
                print(f"{Fore.CYAN}{symbol}{Style.RESET_ALL}: {data.get('price', 0):.2f} | 24h: {data.get('low_24h', 0):.2f}-{data.get('high_24h', 0):.2f} | Trend: {trend} | Funding: {data.get('funding_rate', 0):.4f}%")
        
        # Prepare data for tabulation
        table_data = []
        total_unrealized_pnl = 0
        total_realized_pnl = 0
        
        for pos in open_positions:
            symbol = pos.get('symbol', 'UNKNOWN')
            profile = pos.get('profile', 'UNKNOWN').upper()
            side = pos.get('side', 'UNKNOWN')
            size = pos.get('size', 0)
            entry_price = pos.get('entry_price', 0)
            unrealized_pnl = pos.get('unrealized_pnl', 0)
            realized_pnl = pos.get('realized_pnl', 0)
            leverage = pos.get('leverage', 1)
            
            # Calculate current PnL based on latest price
            current_price = current_prices.get(symbol)
            
            if current_price and entry_price:
                if side == 'LONG':
                    price_pnl = (current_price - entry_price) / entry_price * 100
                    # Calculate distance to take profit based on target percentage
                    target_price = entry_price * (1 + self.target_profit_pct/100)
                    distance_to_target = ((target_price) - current_price) / entry_price * 100
                else:  # SHORT
                    price_pnl = (entry_price - current_price) / entry_price * 100
                    # Calculate distance to take profit based on target percentage
                    target_price = entry_price * (1 - self.target_profit_pct/100)
                    distance_to_target = (current_price - target_price) / entry_price * 100
            else:
                price_pnl = 0
                distance_to_target = 0
            
            total_unrealized_pnl += unrealized_pnl
            total_realized_pnl += realized_pnl
            
            # Format data with colors
            side_colored = f"{Fore.GREEN}{side}{Style.RESET_ALL}" if side == 'LONG' else f"{Fore.RED}{side}{Style.RESET_ALL}"
            pnl_colored = f"{Fore.GREEN}{unrealized_pnl:.2f}{Style.RESET_ALL}" if unrealized_pnl >= 0 else f"{Fore.RED}{unrealized_pnl:.2f}{Style.RESET_ALL}"
            realized_pnl_colored = f"{Fore.GREEN}{realized_pnl:.2f}{Style.RESET_ALL}" if realized_pnl >= 0 else f"{Fore.RED}{realized_pnl:.2f}{Style.RESET_ALL}"
            price_pnl_colored = f"{Fore.GREEN}{price_pnl:.2f}%{Style.RESET_ALL}" if price_pnl >= 0 else f"{Fore.RED}{price_pnl:.2f}%{Style.RESET_ALL}"
            
            # Determine if we're close to target
            target_status = ""
            if distance_to_target <= 0:
                target_status = f"{Fore.GREEN}TARGET MET{Style.RESET_ALL}"
            elif distance_to_target < 0.25:
                target_status = f"{Fore.YELLOW}VERY CLOSE{Style.RESET_ALL}"
            elif distance_to_target < 0.5:
                target_status = f"{Fore.YELLOW}CLOSE{Style.RESET_ALL}"
            else:
                target_status = f"{Fore.CYAN}{distance_to_target:.2f}% away{Style.RESET_ALL}"
            
            table_data.append([
                profile,
                symbol,
                side_colored,
                f"{size:.4f}",
                f"{entry_price:.2f}",
                f"{current_price:.2f}" if current_price else "N/A",
                price_pnl_colored,
                pnl_colored,
                realized_pnl_colored,
                target_status,
                f"{leverage}x"
            ])
        
        # Print summary header
        print(f"\n{Fore.CYAN}===== OPEN POSITIONS SUMMARY ====={Style.RESET_ALL}")
        print(f"{Fore.CYAN}Mode: {'TESTNET' if self.use_testnet else 'MAINNET'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Target Profit: {self.target_profit_pct:.2f}%{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total Positions: {len(open_positions)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total Unrealized PnL: {Fore.GREEN if total_unrealized_pnl >= 0 else Fore.RED}{total_unrealized_pnl:.2f} USDT{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total Realized PnL: {Fore.GREEN if total_realized_pnl >= 0 else Fore.RED}{total_realized_pnl:.2f} USDT{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total PnL: {Fore.GREEN if total_unrealized_pnl + total_realized_pnl >= 0 else Fore.RED}{(total_unrealized_pnl + total_realized_pnl):.2f} USDT{Style.RESET_ALL}")
        
        # Print positions table
        print("\n" + tabulate(
            table_data,
            headers=["PROFILE", "SYMBOL", "SIDE", "SIZE", "ENTRY", "CURRENT", "% CHANGE", "UNREAL PNL", "REAL PNL", "TARGET STATUS", "LEVERAGE"],
            tablefmt="grid"
        ))
        
        # Print summary footer
        print(f"\n{Fore.CYAN}================================={Style.RESET_ALL}")
    
    async def run(self):
        """Run the positions summary."""
        positions, current_prices, market_data = await self.get_all_positions()
        wallet_info = await self.get_wallet_info()
        self.generate_summary(positions, current_prices, market_data, wallet_info)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='OMEGA BTC AI - Open Positions Summary')
    parser.add_argument('--symbol', type=str, default="",
                      help='Trading symbol (default: all symbols)')
    parser.add_argument('--testnet', action='store_true',
                      help='Use testnet (default: False)')
    parser.add_argument('--mainnet', action='store_true',
                      help='Use mainnet (default: True)')
    parser.add_argument('--target', type=float, default=2.0,
                      help='Target profit percentage (default: 2.0)')
    parser.add_argument('--debug', action='store_true', 
                      help='Enable detailed API debugging (default: False)')
    
    args = parser.parse_args()
    
    # Set symbol to empty string if "all" is specified
    if args.symbol.lower() in ("all", "none"):
        args.symbol = ""
    
    return args

async def main():
    """Main entry point for the positions summary."""
    args = parse_args()
    
    # Determine if we should use testnet
    use_testnet = args.testnet or not args.mainnet
    
    # Allow debug option to be set from environment
    debug_mode = args.debug or os.environ.get("BITGET_DEBUG", "").lower() in ("1", "true", "yes")
    if debug_mode:
        print(f"{Fore.YELLOW}Debug mode enabled - will show detailed API information{Style.RESET_ALL}")
        # Set debug environment variable for BitGetTrader
        os.environ["BITGET_DEBUG"] = "true"
    
    # Initialize and run the positions summary
    summary = PositionsSummary(
        use_testnet=use_testnet,
        symbol=args.symbol,
        target_profit_pct=args.target
    )
    
    await summary.run()

if __name__ == "__main__":
    print(f"{Fore.GREEN}OMEGA BTC AI - Open Positions Summary Tool{Style.RESET_ALL}")
    print(f"{Fore.GREEN}========================================{Style.RESET_ALL}")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}") 