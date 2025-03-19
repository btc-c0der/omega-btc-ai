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
import sys
import traceback

# Custom JSON encoder for datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for maximum logging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('bitget_live_trading.log')  # File output
    ]
)

# Set specific loggers to DEBUG level
logging.getLogger('omega_ai.trading.exchanges.bitget_trader').setLevel(logging.DEBUG)
logging.getLogger('omega_ai.trading.exchanges.bitget_live_traders').setLevel(logging.DEBUG)
logging.getLogger('omega_ai.trading.profiles').setLevel(logging.DEBUG)
logging.getLogger('omega_ai.alerts.telegram_market_report').setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

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
                 strategic_only: bool = False,
                 enable_pnl_alerts: bool = True,
                 pnl_alert_interval: int = 1):
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
            enable_pnl_alerts: Whether to enable PnL alerts (default: True)
            pnl_alert_interval: Minute interval for PnL alerts (default: 1, sends every minute)
        """
        self.use_testnet = use_testnet
        self.initial_capital = initial_capital
        self.symbol = symbol
        self.strategic_only = strategic_only
        self.enable_pnl_alerts = enable_pnl_alerts
        self.pnl_alert_interval = pnl_alert_interval
        self.last_pnl_alert_time = datetime.now(timezone.utc)
        
        # Log initialization parameters
        logger.debug(f"{CYAN}Initializing BitGetLiveTraders with parameters:{RESET}")
        logger.debug(f"  use_testnet: {use_testnet}")
        logger.debug(f"  initial_capital: {initial_capital}")
        logger.debug(f"  symbol: {symbol}")
        logger.debug(f"  strategic_only: {strategic_only}")
        logger.debug(f"  enable_pnl_alerts: {enable_pnl_alerts}")
        logger.debug(f"  pnl_alert_interval: {pnl_alert_interval}")
        
        # Look for API credentials in environment variables if not provided
        self.api_key = api_key or os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        self.secret_key = secret_key or os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        self.passphrase = passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        
        # Log API credentials status (safely)
        if not self.api_key or not self.secret_key or not self.passphrase:
            logger.warning(f"{YELLOW}One or more API credentials are missing. API authentication will fail.{RESET}")
        else:
            logger.info(f"{GREEN}API credentials loaded successfully.{RESET}")
            logger.debug(f"  API Key: {self.api_key[:5]}...{self.api_key[-3:] if len(self.api_key) > 5 else ''}")
            logger.debug(f"  Secret Key Length: {len(self.secret_key)} characters")
            logger.debug(f"  Passphrase Length: {len(self.passphrase)} characters")
            
        self.api_client = api_client
        self.use_coin_picker = use_coin_picker
        self.traders: Dict[str, BitGetTrader] = {}
        self.is_running = False
        self.coin_picker = CoinPicker(use_testnet=use_testnet) if use_coin_picker else None
        
        # Log environment information
        logger.debug(f"{CYAN}Environment Information:{RESET}")
        logger.debug(f"  Python Version: {sys.version}")
        logger.debug(f"  OS: {os.name}")
        logger.debug(f"  Working Directory: {os.getcwd()}")
        logger.debug(f"  Environment Variables:")
        for key in ["BITGET_TESTNET_API_KEY", "BITGET_API_KEY", "STRATEGIC_SUB_ACCOUNT_NAME"]:
            if key in os.environ:
                logger.debug(f"    {key}: {'*' * len(os.environ[key])}")
        
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
        profiles = {
            "strategic": StrategicTrader,
            "aggressive": AggressiveTrader,
            "scalping": ScalperTrader
        }
        
        # API version to use - v2 for better compatibility
        api_version = "v2"
        logger.info(f"{YELLOW}Initializing traders with API version {api_version}{RESET}")
        
        # For mainnet, only use the main account
        if not self.use_testnet:
            logger.info(f"{CYAN}Using main account only for mainnet trading{RESET}")
            trader = BitGetTrader(
                profile_type="strategic",
                api_key=self.api_key,
                secret_key=self.secret_key,
                passphrase=self.passphrase,
                use_testnet=self.use_testnet,
                initial_capital=self.initial_capital,
                api_client=self.api_client,
                api_version=api_version
            )
            trader.symbol = self.symbol
            self.traders["strategic"] = trader
            return
        
        # For testnet, initialize all profiles
        for profile_name, profile_class in profiles.items():
            try:
                # Get sub-account name from environment for strategic trader
                sub_account_name = None
                if profile_name == "strategic":
                    sub_account_name = os.environ.get("STRATEGIC_SUB_ACCOUNT_NAME")
                    if sub_account_name:
                        logger.info(f"{GREEN}Using sub-account: {sub_account_name}{RESET}")
                
                trader = BitGetTrader(
                    profile_type=profile_name,
                    api_key=self.api_key,
                    secret_key=self.secret_key,
                    passphrase=self.passphrase,
                    use_testnet=self.use_testnet,
                    initial_capital=self.initial_capital,
                    api_client=self.api_client,
                    api_version=api_version,
                    sub_account_name=sub_account_name
                )
                
                # Make sure trader is using the same symbol as us
                trader.symbol = self.symbol
                
                # Initialize the trader profile
                self.traders[profile_name] = trader
                logger.info(f"{GREEN}Initialized {profile_name} trader{RESET}")
                
            except Exception as e:
                logger.error(f"{RED}Failed to initialize {profile_name} trader: {str(e)}{RESET}")
                continue

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
            logger.debug(f"{CYAN}Getting market ticker for {trader.symbol} ({profile_name} trader){RESET}")
            ticker = trader.get_market_ticker(trader.symbol)
            
            if ticker and 'last' in ticker:
                current_price = float(ticker['last'])
                logger.debug(f"{GREEN}Current price for {trader.symbol}: {current_price}{RESET}")
                logger.debug(f"{CYAN}Full ticker data: {json.dumps(ticker, indent=2, cls=DateTimeEncoder)}{RESET}")
                
                # Update market context
                market_context = {
                    "price": current_price,
                    "symbol": trader.symbol,
                    "timestamp": datetime.now(timezone.utc).isoformat()  # Convert to ISO format string
                }
                logger.debug(f"{CYAN}Market context: {json.dumps(market_context, indent=2)}{RESET}")
                
                # Get current positions before executing trade
                logger.debug(f"{CYAN}Getting current positions for {profile_name} trader{RESET}")
                current_positions = trader.get_positions(trader.symbol)
                logger.debug(f"{CYAN}Current positions: {json.dumps(current_positions, indent=2, cls=DateTimeEncoder)}{RESET}")
                
                # Execute trading logic
                logger.debug(f"{CYAN}Executing trading logic for {profile_name} trader{RESET}")
                trade_result = trader.execute_trade(market_context)
                
                if trade_result:
                    logger.debug(f"{CYAN}Trade executed: {json.dumps(trade_result, indent=2, cls=DateTimeEncoder)}{RESET}")
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
                    logger.debug(f"{GREEN}Sent trade alert to Telegram{RESET}")
                else:
                    logger.debug(f"{YELLOW}No trade executed for {profile_name} trader{RESET}")
                
                # Update positions
                logger.debug(f"{CYAN}Updating positions for {profile_name} trader{RESET}")
                trader.update_positions(current_price)
                
                # Get updated positions
                updated_positions = trader.get_positions(trader.symbol)
                logger.debug(f"{CYAN}Updated positions: {json.dumps(updated_positions, indent=2, cls=DateTimeEncoder)}{RESET}")
                
                # Update performance metrics
                await self._update_performance_metrics(trader, profile_name)
            else:
                logger.error(f"{RED}Failed to get ticker data for {trader.symbol} ({profile_name} trader){RESET}")
                if ticker:
                    logger.error(f"{RED}Ticker response: {json.dumps(ticker, indent=2, cls=DateTimeEncoder)}{RESET}")
                else:
                    logger.error(f"{RED}No ticker data returned{RESET}")
                
        except Exception as e:
            logger.error(f"{RED}Error in trader update ({profile_name}): {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            logger.error(f"{RED}Exception traceback: {traceback.format_exc()}{RESET}")
            
            # Send error alert for critical failures
            try:
                error_msg = (
                    f"⚠️ ERROR IN {profile_name.upper()} TRADER\n"
                    f"Symbol: {trader.symbol}\n"
                    f"Error: {str(e)}\n"
                    f"Type: {type(e).__name__}"
                )
                await send_telegram_alert(error_msg)
                logger.debug(f"{GREEN}Sent error alert to Telegram{RESET}")
            except Exception as alert_error:
                logger.error(f"{RED}Failed to send error alert: {str(alert_error)}{RESET}")
            
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
            
            # Get current time
            current_time = datetime.now(timezone.utc)
            
            # Check if PnL alerts are enabled and if it's time to send an alert
            if self.enable_pnl_alerts:
                # Determine if we should send an alert based on the interval
                time_since_last_alert = (current_time - self.last_pnl_alert_time).total_seconds() / 60
                
                # Send alert if we've reached the specified interval and we're in the first 5 seconds of a minute
                if time_since_last_alert >= self.pnl_alert_interval and current_time.second < 5:
                    # Get detailed position information
                    positions_info = ""
                    unrealized_pnl = 0
                    realized_pnl = 0
                    
                    # Calculate PnL values with detailed breakdown
                    unrealized_pnl_by_symbol = {}
                    realized_pnl_by_symbol = {}
                    
                    if positions:
                        for pos in positions:
                            symbol = pos.get('symbol', 'UNKNOWN')
                            side = pos.get('holdSide', 'UNKNOWN').upper()
                            size = float(pos.get('total', 0))
                            price = float(pos.get('averageOpenPrice', 0))
                            unreal_pnl = float(pos.get('unrealizedPL', 0))
                            real_pnl = float(pos.get('achievedProfits', 0))
                            
                            # Track by symbol
                            if symbol not in unrealized_pnl_by_symbol:
                                unrealized_pnl_by_symbol[symbol] = 0
                                realized_pnl_by_symbol[symbol] = 0
                                
                            unrealized_pnl_by_symbol[symbol] += unreal_pnl
                            realized_pnl_by_symbol[symbol] += real_pnl
                            unrealized_pnl += unreal_pnl
                            realized_pnl += real_pnl
                            
                            positions_info += f"• {side}: {size:.4f} @ {price:.2f} USD | Unreal: {unreal_pnl:+.2f} | Real: {real_pnl:+.2f}\n"
                    
                    # Calculate total PnL
                    total_combined_pnl = unrealized_pnl + realized_pnl
                    
                    # Format the position status emoji based on PnL
                    status_emoji = "🟢" if total_combined_pnl >= 0 else "🔴"
                    
                    # Create alert message with a detailed breakdown table format
                    alert_msg = (
                        f"{status_emoji} {profile_name.upper()} TRADER PNL UPDATE\n\n"
                        f"📊 *SUMMARY*\n"
                        f"Symbol: {trader.symbol}\n"
                        f"Time: {current_time.strftime('%H:%M:%S UTC')}\n"
                        f"Active Positions: {len(positions) if positions else 0}\n\n"
                    )
                    
                    # Add PnL breakdown by symbol if available
                    if unrealized_pnl_by_symbol:
                        alert_msg += f"💰 *PNL BREAKDOWN*\n"
                        # Add header row
                        alert_msg += f"Symbol | Unrealized | Realized | Total\n"
                        alert_msg += f"-------|------------|----------|------\n"
                        
                        # Add data rows for each symbol
                        for symbol in sorted(unrealized_pnl_by_symbol.keys()):
                            unreal = unrealized_pnl_by_symbol[symbol]
                            real = realized_pnl_by_symbol[symbol]
                            total = unreal + real
                            alert_msg += f"{symbol} | {unreal:+.2f} | {real:+.2f} | {total:+.2f}\n"
                        
                        # Add totals row
                        alert_msg += f"-------|------------|----------|------\n"
                        alert_msg += f"TOTAL | {unrealized_pnl:+.2f} | {realized_pnl:+.2f} | {total_combined_pnl:+.2f}\n\n"
                    
                    # Add position details if available
                    if positions_info:
                        alert_msg += f"📈 *POSITION DETAILS*\n{positions_info}"
                        
                    # Send the alert
                    await send_telegram_alert(alert_msg)
                    logger.info(f"{GREEN}Sent PnL update to Telegram{RESET}")
                    
                    # Update the last alert time
                    self.last_pnl_alert_time = current_time
                
        except Exception as e:
            logger.error(f"{RED}Error updating performance metrics for {profile_name}: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            
    async def stop_trading(self) -> None:
        """Stop the live trading system and close all positions."""
        # First, get all positions that would be closed
        total_positions = 0
        positions_by_trader = {}
        
        for profile_name, trader in self.traders.items():
            try:
                positions = trader.get_positions(trader.symbol)
                if positions:
                    open_positions = [p for p in positions if p.get('status') == 'OPEN']
                    if open_positions:
                        total_positions += len(open_positions)
                        positions_by_trader[profile_name] = open_positions
            except Exception as e:
                logger.error(f"{RED}Error getting positions for {profile_name} trader: {str(e)}{RESET}")
        
        if total_positions > 0:
            # Send warning message with position details
            warning_msg = (
                f"⚠️ WARNING: {total_positions} OPEN POSITIONS FOUND\n\n"
                f"Traders with open positions:\n"
            )
            
            for profile_name, positions in positions_by_trader.items():
                warning_msg += f"\n{profile_name.upper()} ({len(positions)} positions):\n"
                for pos in positions:
                    warning_msg += f"- {pos.get('side', 'UNKNOWN')} {pos.get('size', 0)} BTC @ ${pos.get('entryPrice', 0)}\n"
            
            warning_msg += "\nDo you want to proceed with closing all positions? (yes/no)"
            
            # Send warning to Telegram
            await send_telegram_alert(warning_msg)
            
            # Wait for user confirmation
            confirmation = await self.wait_for_confirmation()
            if not confirmation:
                logger.info(f"{YELLOW}Position closure cancelled by user{RESET}")
                return
        
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

    async def wait_for_confirmation(self) -> bool:
        """Wait for user confirmation via Telegram."""
        # This is a placeholder - you'll need to implement the actual confirmation logic
        # based on your Telegram bot setup
        try:
            # For now, we'll just wait 30 seconds and assume confirmation
            await asyncio.sleep(30)
            return True
        except Exception as e:
            logger.error(f"{RED}Error waiting for confirmation: {str(e)}{RESET}")
            return False

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
    parser.add_argument('--no-pnl-alerts', action='store_true',
                      help='Disable PnL alerts (default: False)')
    parser.add_argument('--pnl-alert-interval', type=int, default=1,
                      help='Interval in minutes for PnL alerts (default: 1)')
    
    return parser.parse_args()

async def main():
    """Main entry point for the live traders system."""
    args = parse_args()
    
    # Determine if we should use testnet
    use_testnet = args.testnet or not args.mainnet
    
    # Allow debug option to be set from environment
    debug_mode = os.environ.get("BITGET_DEBUG", "").lower() in ("1", "true", "yes")
    if debug_mode:
        print(f"{YELLOW}Debug mode enabled - will show detailed API information{RESET}")
        # Set debug environment variable for BitGetTrader
        os.environ["BITGET_DEBUG"] = "true"
    
    # Initialize with command line arguments
    live_traders = BitGetLiveTraders(
        use_testnet=use_testnet,
        initial_capital=args.capital,
        symbol=args.symbol,
        api_key=args.api_key,
        secret_key=args.secret_key,
        passphrase=args.passphrase,
        use_coin_picker=args.use_coin_picker,
        strategic_only=args.strategic_only,
        enable_pnl_alerts=not args.no_pnl_alerts,
        pnl_alert_interval=args.pnl_alert_interval
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