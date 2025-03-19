"""
OMEGA BTC AI - BitGet Live Traders Module
=======================================

This module implements a live trading system with multiple trader profiles on BitGet,
each starting with 24 USDT and trading BTC. The system includes real-time monitoring,
risk management, and performance tracking.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import asyncio
import logging
import argparse
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader
from omega_ai.trading.exchanges.coin_picker import CoinPicker, CoinType, CoinInfo
from omega_ai.trading.profiles import (
    StrategicTrader,
    AggressiveTrader,
    NewbieTrader,
    ScalperTrader
)
from omega_ai.alerts.telegram_market_report import send_telegram_alert
import json
import os

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BitGetLiveTraders:
    """Manages multiple live traders on BitGet with different profiles."""
    
    def __init__(self, 
                 use_testnet: bool = True,
                 initial_capital: float = 24.0,
                 symbol: str = "BTCUSDT",
                 api_key: str = "",
                 secret_key: str = "",
                 passphrase: str = "",
                 api_client: Optional[Any] = None,
                 use_coin_picker: bool = False,
                 strategic_only: bool = False):
        """
        Initialize the live traders system.
        
        Args:
            use_testnet: Whether to use testnet (default: True)
            initial_capital: Initial capital per trader in USDT (default: 24.0)
            symbol: Trading symbol (default: BTCUSDT)
            api_key: BitGet API key
            secret_key: BitGet secret key
            passphrase: BitGet API passphrase
            api_client: Optional external API client for testing (default: None)
            use_coin_picker: Whether to use CoinPicker for symbol verification (default: False)
            strategic_only: Whether to only use the strategic trader profile (default: False)
        """
        self.use_testnet = use_testnet
        self.initial_capital = initial_capital
        self.symbol = symbol
        self.strategic_only = strategic_only
        
        # Look for API credentials in environment variables if not provided
        self.api_key = api_key or os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        self.secret_key = secret_key or os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        self.passphrase = passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        
        # Log API credentials status
        if not self.api_key or not self.secret_key or not self.passphrase:
            logger.warning(f"{YELLOW}One or more API credentials are missing. API authentication will fail.{RESET}")
        else:
            logger.info(f"{GREEN}API credentials loaded successfully.{RESET}")
            
        self.api_client = api_client
        self.use_coin_picker = use_coin_picker
        self.traders: Dict[str, BitGetTrader] = {}
        self.is_running = False
        self.coin_picker = CoinPicker(use_testnet=use_testnet) if use_coin_picker else None
        
    async def initialize(self) -> None:
        """Initialize the trading system."""
        # Verify symbol exists and is valid
        if not await self._verify_symbol():
            logger.error(f"{RED}Invalid symbol {self.symbol}. Using default BTCUSDT{RESET}")
            self.symbol = "BTCUSDT"
            
        await self._initialize_traders()
        
    async def _verify_symbol(self) -> bool:
        """Verify if the symbol is valid and available for futures trading."""
        try:
            # Skip verification if CoinPicker is disabled
            if not self.use_coin_picker or not self.coin_picker:
                logger.info(f"{YELLOW}CoinPicker disabled, skipping symbol verification{RESET}")
                # Instead, use BitGetTrader to verify the symbol
                test_trader = BitGetTrader(
                    profile_type="strategic",
                    api_key=self.api_key,
                    secret_key=self.secret_key,
                    passphrase=self.passphrase,
                    use_testnet=self.use_testnet,
                    api_version="v1"  # Use v1 API for now since we're experiencing issues with v2
                )
                return test_trader.verify_symbol(self.symbol)
                
            # Update coin picker cache
            if not self.coin_picker.update_coins_cache():
                logger.warning(f"{YELLOW}Failed to update coins cache, skipping verification{RESET}")
                return True
                
            # Get symbol info
            symbol_info = self.coin_picker.get_symbol_info(self.symbol)
            if not symbol_info:
                return False
                
            # Verify it's a futures symbol
            if symbol_info.type != CoinType.FUTURES:
                logger.error(f"{RED}Symbol {self.symbol} is not a futures contract{RESET}")
                return False
                
            # Verify it's a USDT contract
            if symbol_info.quote_currency != "USDT":
                logger.error(f"{RED}Symbol {self.symbol} is not a USDT contract{RESET}")
                return False
                
            # Get market analysis
            analysis = self.coin_picker.analyze_symbol(self.symbol)
            if not analysis:
                return False
                
            logger.info(f"{GREEN}Symbol {self.symbol} verified successfully{RESET}")
            logger.info(f"{BLUE}Symbol details:{RESET}")
            logger.info(f"Base currency: {analysis['base_currency']}")
            logger.info(f"Quote currency: {analysis['quote_currency']}")
            logger.info(f"Last price: {analysis['last_price']}")
            logger.info(f"24h volume: {analysis['volume_24h']}")
            logger.info(f"24h price change: {analysis['price_change_24h']}%")
            logger.info(f"Maker fee rate: {analysis['maker_fee_rate']}")
            logger.info(f"Taker fee rate: {analysis['taker_fee_rate']}")
            
            return True
            
        except Exception as e:
            logger.error(f"{RED}Error verifying symbol: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            return False
        
    async def _initialize_traders(self) -> None:
        """Initialize traders with different profiles."""
        # Define available profiles
        if self.strategic_only:
            profiles = {
                "strategic": StrategicTrader
            }
            logger.info(f"{GREEN}Strategic-only mode enabled. Only initializing Strategic trader.{RESET}")
        else:
            profiles = {
                "strategic": StrategicTrader,
                "aggressive": AggressiveTrader,
                "newbie": NewbieTrader,
                "scalper": ScalperTrader
            }
        
        # API version to use - v1 is more stable and has different endpoints
        api_version = "v1"
        logger.info(f"{YELLOW}Initializing traders with API version {api_version}{RESET}")
        
        for profile_name, profile_class in profiles.items():
            try:
                trader = BitGetTrader(
                    profile_type=profile_name,
                    api_key=self.api_key,
                    secret_key=self.secret_key,
                    passphrase=self.passphrase,
                    use_testnet=self.use_testnet,
                    initial_capital=self.initial_capital,
                    api_client=self.api_client,  # Pass the external API client if provided
                    api_version=api_version  # Use v1 API for stability
                )
                
                # Make sure trader is using the same symbol as us
                trader.symbol = self.symbol
                
                self.traders[profile_name] = trader
                logger.info(f"{GREEN}Initialized {profile_name} trader with {self.initial_capital} USDT{RESET}")
                logger.info(f"{CYAN}Trader API URL: {trader.api_url}{RESET}")
                logger.info(f"{CYAN}Trader API Base: {trader.api_base}{RESET}")
                logger.info(f"{CYAN}Trader Symbol: {trader.symbol} (will be formatted as {trader.format_symbol(trader.symbol, api_version)} for API calls){RESET}")
                
                # Send initialization alert
                alert_msg = (
                    f"🚀 {profile_name.upper()} TRADER INITIALIZED\n"
                    f"Symbol: {self.symbol}\n"
                    f"Capital: {self.initial_capital} USDT\n"
                    f"Mode: {'TESTNET' if self.use_testnet else 'MAINNET'}\n"
                    f"API Version: {api_version}"
                )
                await send_telegram_alert(alert_msg)
                
            except Exception as e:
                logger.error(f"{RED}Failed to initialize {profile_name} trader: {str(e)}{RESET}")
                logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
                logger.error(f"{RED}Exception args: {e.args}{RESET}")
                
    async def start_trading(self) -> None:
        """Start the live trading system."""
        # Initialize traders if not already done
        if not self.traders:
            await self.initialize()
            
        self.is_running = True
        logger.info(f"{CYAN}Starting OMEGA BTC AI Live Traders System{RESET}")
        
        try:
            while self.is_running:
                # Update each trader
                for profile_name, trader in self.traders.items():
                    try:
                        await self._update_trader(trader, profile_name)
                    except Exception as e:
                        logger.error(f"{RED}Error updating {profile_name} trader: {str(e)}{RESET}")
                
                # Wait before next update
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info(f"{YELLOW}Shutting down live traders system...{RESET}")
            await self.stop_trading()
            
    async def _update_trader(self, trader: BitGetTrader, profile_name: str) -> None:
        """Update a single trader's state and execute trading logic."""
        try:
            # Get current market data
            logger.info(f"{CYAN}Getting market ticker for {trader.symbol} ({profile_name} trader){RESET}")
            ticker = trader.get_market_ticker(trader.symbol)
            
            if ticker and 'last' in ticker:
                current_price = float(ticker['last'])
                logger.info(f"{GREEN}Current price for {trader.symbol}: {current_price}{RESET}")
                
                # Update market context
                market_context = {
                    "price": current_price,
                    "symbol": trader.symbol,
                    "timestamp": datetime.now(timezone.utc)
                }
                
                # Execute trading logic
                trade_result = trader.execute_trade(market_context)
                
                if trade_result:
                    # Send trade alert
                    alert_msg = (
                        f"🎯 {profile_name.upper()} TRADER EXECUTED TRADE\n"
                        f"Symbol: {trader.symbol}\n"
                        f"Direction: {trade_result.get('direction', 'UNKNOWN')}\n"
                        f"Size: {trade_result.get('size', 0):.4f}\n"
                        f"Entry Price: {trade_result.get('entry_price', 0):.2f}\n"
                        f"Stop Loss: {trade_result.get('stop_loss', 0):.2f}"
                    )
                    await send_telegram_alert(alert_msg)
                
                # Update positions
                trader.update_positions(current_price)
                
                # Update performance metrics
                await self._update_performance_metrics(trader, profile_name)
            else:
                logger.error(f"{RED}Failed to get ticker data for {trader.symbol} ({profile_name} trader){RESET}")
                if ticker:
                    logger.error(f"{RED}Ticker response: {json.dumps(ticker, indent=2)}{RESET}")
                else:
                    logger.error(f"{RED}No ticker data returned{RESET}")
                
        except Exception as e:
            logger.error(f"{RED}Error in trader update ({profile_name}): {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            
            # Send error alert for critical failures
            try:
                error_msg = (
                    f"⚠️ ERROR IN {profile_name.upper()} TRADER\n"
                    f"Symbol: {trader.symbol}\n"
                    f"Error: {str(e)}\n"
                    f"Type: {type(e).__name__}"
                )
                await send_telegram_alert(error_msg)
            except:
                logger.error(f"{RED}Failed to send error alert{RESET}")
            
    async def _update_performance_metrics(self, trader: BitGetTrader, profile_name: str) -> None:
        """Update and log trader performance metrics."""
        try:
            # Calculate metrics
            total_pnl = trader.get_total_pnl()
            logger.info(f"{CYAN}Getting positions for {trader.symbol} ({profile_name} trader){RESET}")
            positions = trader.get_positions(trader.symbol)
            
            # Log performance
            logger.info(
                f"{BLUE}{profile_name.upper()} Performance:\n"
                f"Symbol: {trader.symbol}\n"
                f"Total PnL: {total_pnl:.2f} USDT\n"
                f"Active Positions: {len(positions) if positions else 0}{RESET}"
            )
            
            # Send performance update every hour
            if datetime.now(timezone.utc).minute == 0:
                alert_msg = (
                    f"📊 {profile_name.upper()} HOURLY PERFORMANCE\n"
                    f"Symbol: {trader.symbol}\n"
                    f"PnL: {total_pnl:.2f} USDT\n"
                    f"Active Positions: {len(positions) if positions else 0}"
                )
                await send_telegram_alert(alert_msg)
                
        except Exception as e:
            logger.error(f"{RED}Error updating performance metrics for {profile_name}: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            
    async def stop_trading(self) -> None:
        """Stop the live trading system and close all positions."""
        self.is_running = False
        
        for profile_name, trader in self.traders.items():
            try:
                logger.info(f"{YELLOW}Shutting down {profile_name} trader...{RESET}")
                
                # Close all open positions
                logger.info(f"{CYAN}Getting positions for {trader.symbol} ({profile_name} trader) before shutdown{RESET}")
                positions = trader.get_positions(trader.symbol)
                
                if positions:
                    logger.info(f"{CYAN}Found {len(positions)} positions to close for {profile_name} trader{RESET}")
                    for position in positions:
                        if position.get('status') == 'OPEN':
                            logger.info(f"{YELLOW}Closing position for {trader.symbol} ({profile_name} trader){RESET}")
                            trader.close_position(
                                symbol=trader.symbol,
                                side=position.get('side', 'LONG')
                            )
                else:
                    logger.info(f"{GREEN}No open positions to close for {profile_name} trader{RESET}")
                            
                # Send shutdown alert
                alert_msg = (
                    f"🛑 {profile_name.upper()} TRADER SHUTDOWN\n"
                    f"Symbol: {trader.symbol}\n"
                    f"Final PnL: {trader.get_total_pnl():.2f} USDT"
                )
                await send_telegram_alert(alert_msg)
                
            except Exception as e:
                logger.error(f"{RED}Error during {profile_name} trader shutdown: {str(e)}{RESET}")
                logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
                logger.error(f"{RED}Exception args: {e.args}{RESET}")
                
        logger.info(f"{GREEN}Live traders system stopped successfully{RESET}")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='OMEGA BTC AI Live Traders')
    parser.add_argument('--symbol', type=str, default='BTCUSDT',
                      help='Trading symbol (default: BTCUSDT)')
    parser.add_argument('--testnet', action='store_true',
                      help='Use testnet (default: True)')
    parser.add_argument('--mainnet', action='store_true',
                      help='Use mainnet (default: False)')
    parser.add_argument('--capital', type=float, default=24.0,
                      help='Initial capital per trader in USDT (default: 24.0)')
    parser.add_argument('--api-key', type=str, default='',
                      help='BitGet API key')
    parser.add_argument('--secret-key', type=str, default='',
                      help='BitGet secret key')
    parser.add_argument('--passphrase', type=str, default='',
                      help='BitGet API passphrase')
    parser.add_argument('--use-coin-picker', action='store_true',
                      help='Use CoinPicker for symbol verification (default: False)')
    parser.add_argument('--strategic-only', action='store_true',
                      help='Only use the strategic fibonacci trader (default: False)')
    
    return parser.parse_args()

async def main():
    """Main entry point for the live traders system."""
    args = parse_args()
    
    # Determine if we should use testnet
    use_testnet = args.testnet or not args.mainnet
    
    # Initialize with command line arguments
    live_traders = BitGetLiveTraders(
        use_testnet=use_testnet,
        initial_capital=args.capital,
        symbol=args.symbol,
        api_key=args.api_key,
        secret_key=args.secret_key,
        passphrase=args.passphrase,
        use_coin_picker=args.use_coin_picker,
        strategic_only=args.strategic_only
    )
    
    try:
        # Start the trading system
        await live_traders.start_trading()
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Received shutdown signal{RESET}")
    finally:
        await live_traders.stop_trading()

if __name__ == "__main__":
    asyncio.run(main()) 