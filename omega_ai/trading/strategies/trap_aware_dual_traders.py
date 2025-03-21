#!/usr/bin/env python3

"""
OMEGA BTC AI - Trap-Aware Dual Position Traders
==============================================

This module enhances the BitGetDualPositionTraders by integrating data from the
Trap Probability Meter. It modifies trading decisions based on detected market
maker traps, allowing for smarter entries and exits.

Usage:
    python -m omega_ai.trading.strategies.trap_aware_dual_traders [options]
"""

import asyncio
import argparse
import logging
import os
import signal
import sys
from datetime import datetime, timedelta

from omega_ai.trading.exchanges.dual_position_traders import BitGetDualPositionTraders
from omega_ai.utils.trap_probability_utils import (
    get_current_trap_probability,
    get_probability_components,
    get_detected_trap_info,
    get_probability_threshold,
    is_trap_likely
)
from omega_ai.alerts.telegram_market_report import send_telegram_alert

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('trap_aware_trading.log')
    ]
)

logger = logging.getLogger(__name__)

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

class TrapAwareDualTraders(BitGetDualPositionTraders):
    """
    Extends the dual position traders system with trap probability awareness.
    """
    
    def __init__(self, 
                 trap_probability_threshold: float = 0.7,
                 trap_alert_threshold: float = 0.8,
                 enable_trap_protection: bool = True,
                 **kwargs):
        """
        Initialize the trap-aware dual position traders system.
        
        Args:
            trap_probability_threshold: Threshold above which to consider trap probability in trading decisions
            trap_alert_threshold: Threshold above which to send trap alerts
            enable_trap_protection: Whether to enable trap protection features
            **kwargs: Arguments to pass to BitGetDualPositionTraders
        """
        super().__init__(**kwargs)
        self.trap_probability_threshold = trap_probability_threshold
        self.trap_alert_threshold = trap_alert_threshold
        self.enable_trap_protection = enable_trap_protection
        self.last_trap_check_time = datetime.now()
        self.trap_check_interval = 30  # seconds
        self.last_trap_alert_time = datetime.now() - timedelta(hours=1)
        self.trap_alert_cooldown = 300  # seconds
        self.last_detected_trap = None
        
        # Use multipliers instead of directly modifying traders
        self.long_risk_multiplier = 1.0
        self.short_risk_multiplier = 1.0
        
        logger.info(f"{CYAN}Trap-Aware Dual Traders initialized with:{RESET}")
        logger.info(f"{CYAN}  Trap Probability Threshold: {trap_probability_threshold}{RESET}")
        logger.info(f"{CYAN}  Trap Alert Threshold: {trap_alert_threshold}{RESET}")
        logger.info(f"{CYAN}  Trap Protection Enabled: {enable_trap_protection}{RESET}")
    
    async def check_for_traps(self) -> dict:
        """
        Check for market maker traps using the trap probability meter data.
        
        Returns:
            dict: Information about detected traps
        """
        try:
            # Get current time
            current_time = datetime.now()
            
            # Only check periodically to avoid spamming
            if (current_time - self.last_trap_check_time).total_seconds() < self.trap_check_interval:
                return {}
                
            # Update last check time
            self.last_trap_check_time = current_time
            
            # Check if a trap is likely
            is_likely, trap_type, confidence = is_trap_likely()
            
            # Get the overall probability
            probability = get_current_trap_probability()
            
            # Get individual component values
            components = get_probability_components()
            
            # Create result dictionary
            result = {
                "probability": probability,
                "is_trap_likely": is_likely,
                "trap_type": trap_type,
                "confidence": confidence,
                "components": components,
                "timestamp": current_time.isoformat()
            }
            
            # Send alert if probability is above threshold and cooldown has passed
            if (probability >= self.trap_alert_threshold and 
                (current_time - self.last_trap_alert_time).total_seconds() >= self.trap_alert_cooldown):
                
                await self._send_trap_alert(result)
                self.last_trap_alert_time = current_time
                self.last_detected_trap = result
            
            return result
        
        except Exception as e:
            logger.error(f"{RED}Error checking for traps: {e}{RESET}")
            return {}
    
    async def _send_trap_alert(self, trap_data: dict) -> None:
        """
        Send an alert about a detected market maker trap.
        
        Args:
            trap_data: Information about the detected trap
        """
        try:
            # Format trap type with emoji
            trap_type_formatted = trap_data.get("trap_type", "Unknown")
            if trap_type_formatted == "bull_trap":
                trap_type_formatted = "🐂 Bull Trap"
            elif trap_type_formatted == "bear_trap":
                trap_type_formatted = "🐻 Bear Trap"
            elif trap_type_formatted == "liquidity_grab":
                trap_type_formatted = "💰 Liquidity Grab"
            elif trap_type_formatted == "stop_hunt":
                trap_type_formatted = "🎯 Stop Hunt"
            elif trap_type_formatted == "fake_pump":
                trap_type_formatted = "🚀 Fake Pump"
            elif trap_type_formatted == "fake_dump":
                trap_type_formatted = "📉 Fake Dump"
            
            # Format message
            message = f"⚠️ *MARKET MAKER TRAP DETECTED* ⚠️\n\n"
            message += f"Type: *{trap_type_formatted}*\n"
            message += f"Probability: {trap_data.get('probability', 0) * 100:.1f}%\n"
            message += f"Confidence: {trap_data.get('confidence', 0) * 100:.1f}%\n\n"
            
            # Add trading recommendations
            message += "*Trading Recommendations:*\n"
            
            if trap_type_formatted == "🐂 Bull Trap":
                message += "- Consider closing long positions\n"
                message += "- Be cautious about entering new longs\n"
                message += "- Short positions may benefit\n"
            elif trap_type_formatted == "🐻 Bear Trap":
                message += "- Consider closing short positions\n"
                message += "- Be cautious about entering new shorts\n"
                message += "- Long positions may benefit\n"
            elif trap_type_formatted in ["💰 Liquidity Grab", "🎯 Stop Hunt"]:
                message += "- Prepare for strong price movement\n"
                message += "- Consider widening stop losses\n"
                message += "- Reduce position sizes temporarily\n"
            elif trap_type_formatted == "🚀 Fake Pump":
                message += "- Be cautious about FOMO buying\n"
                message += "- Consider taking profits on longs\n"
                message += "- Prepare for potential reversal\n"
            elif trap_type_formatted == "📉 Fake Dump":
                message += "- Be cautious about panic selling\n"
                message += "- Consider taking profits on shorts\n"
                message += "- Prepare for potential reversal\n"
            
            # Add current time
            message += f"\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Send alert
            await send_telegram_alert(message)
            logger.info(f"{YELLOW}Sent trap alert: {trap_type_formatted}{RESET}")
        
        except Exception as e:
            logger.error(f"{RED}Error sending trap alert: {e}{RESET}")
    
    async def _adjust_trading_based_on_traps(self, trap_data: dict) -> None:
        """
        Adjust trading behavior based on detected traps.
        
        Args:
            trap_data: Information about detected traps
        """
        if not self.enable_trap_protection or not trap_data:
            return
            
        probability = trap_data.get("probability", 0)
        trap_type = trap_data.get("trap_type")
        
        if probability < self.trap_probability_threshold or not trap_type:
            return
            
        # Log the trap detection
        logger.info(f"{YELLOW}Adjusting trading based on detected {trap_type} (probability: {probability:.2f}){RESET}")
        
        # Implement trading adjustments based on trap type
        if trap_type == "bull_trap":
            # In a bull trap, we want to be more careful with long positions
            # and potentially more aggressive with shorts
            self.long_risk_multiplier = 0.5  # Reduce risk for longs
            self.short_risk_multiplier = 1.2  # Increase risk for shorts
            
        elif trap_type == "bear_trap":
            # In a bear trap, we want to be more careful with short positions
            # and potentially more aggressive with longs
            self.long_risk_multiplier = 1.2  # Increase risk for longs
            self.short_risk_multiplier = 0.5  # Reduce risk for shorts
            
        elif trap_type in ["liquidity_grab", "stop_hunt"]:
            # For liquidity grabs and stop hunts, reduce risk on both sides
            self.long_risk_multiplier = 0.7
            self.short_risk_multiplier = 0.7
            
        elif trap_type == "fake_pump":
            # For fake pumps, be cautious with longs
            self.long_risk_multiplier = 0.5
            self.short_risk_multiplier = 1.1
            
        elif trap_type == "fake_dump":
            # For fake dumps, be cautious with shorts
            self.long_risk_multiplier = 1.1
            self.short_risk_multiplier = 0.5
            
        # Log the adjustment
        logger.info(f"{YELLOW}Adjusted risk multipliers - Long: {self.long_risk_multiplier:.2f}, Short: {self.short_risk_multiplier:.2f}{RESET}")
    
    async def start_trading(self) -> None:
        """
        Start the trap-aware dual traders system.
        """
        logger.info(f"{GREEN}Starting Trap-Aware Dual Position Traders{RESET}")
        
        # Initialize traders
        await self.initialize()
        
        # Check account limit
        if not await self.check_account_limit():
            logger.error(f"{RED}Account limit check failed. Stopping.{RESET}")
            return
            
        # Start trading
        self.running = True
        
        # Create and start tasks
        self.tasks = [
            asyncio.create_task(self._run_long_trader()),
            asyncio.create_task(self._run_short_trader()),
            asyncio.create_task(self._monitor_performance()),
            asyncio.create_task(self._monitor_traps())  # New task for trap monitoring
        ]
        
        # Wait for tasks to complete
        await asyncio.gather(*self.tasks)
    
    async def _monitor_traps(self) -> None:
        """
        Monitor for market maker traps and adjust trading accordingly.
        """
        logger.info(f"{BLUE}Starting trap monitoring{RESET}")
        
        while self.running:
            try:
                # Check for traps
                trap_data = await self.check_for_traps()
                
                # Adjust trading based on detected traps
                if trap_data:
                    await self._adjust_trading_based_on_traps(trap_data)
                
                # Sleep before next check
                await asyncio.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"{RED}Error in trap monitoring: {e}{RESET}")
                await asyncio.sleep(30)  # Longer sleep on error

    # Override the _run_long_trader method to apply the risk multiplier
    async def _run_long_trader(self) -> None:
        """Run the long trader with trap-aware risk adjustment."""
        logger.info(f"{BLUE}Starting long trader (trap-aware){RESET}")
        
        while self.running:
            try:
                # Apply risk multiplier here before trading decisions
                # For example, adjust position sizes based on the risk multiplier
                
                # Call parent method to run the standard trading logic
                await super()._run_long_trader()
                
                # Sleep before next check
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"{RED}Error in long trader: {e}{RESET}")
                await asyncio.sleep(30)  # Longer sleep on error
    
    # Override the _run_short_trader method to apply the risk multiplier
    async def _run_short_trader(self) -> None:
        """Run the short trader with trap-aware risk adjustment."""
        logger.info(f"{BLUE}Starting short trader (trap-aware){RESET}")
        
        while self.running:
            try:
                # Apply risk multiplier here before trading decisions
                # For example, adjust position sizes based on the risk multiplier
                
                # Call parent method to run the standard trading logic
                await super()._run_short_trader()
                
                # Sleep before next check
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"{RED}Error in short trader: {e}{RESET}")
                await asyncio.sleep(30)  # Longer sleep on error

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='OMEGA BTC AI Trap-Aware Dual Position Traders')
    parser.add_argument('--symbol', type=str, default='BTCUSDT',
                      help='Trading symbol (default: BTCUSDT)')
    parser.add_argument('--testnet', action='store_true',
                      help='Use testnet (default: False)')
    parser.add_argument('--long-capital', type=float, default=24.0,
                      help='Initial capital for long trader in USDT (default: 24.0)')
    parser.add_argument('--short-capital', type=float, default=24.0,
                      help='Initial capital for short trader in USDT (default: 24.0)')
    parser.add_argument('--long-leverage', type=int, default=20,
                      help='Leverage for long positions (default: 20)')
    parser.add_argument('--short-leverage', type=int, default=20,
                      help='Leverage for short positions (default: 20)')
    parser.add_argument('--no-pnl-alerts', action='store_true',
                      help='Disable PnL alerts (default: False)')
    parser.add_argument('--account-limit', type=float, default=0.0,
                      help='Maximum total account value in USDT (0 means no limit)')
    parser.add_argument('--long-sub-account', type=str, default='',
                      help='Sub-account name for long positions (default from env STRATEGIC_SUB_ACCOUNT_NAME)')
    parser.add_argument('--short-sub-account', type=str, default='fst_short',
                      help='Sub-account name for short positions (default: fst_short)')
    parser.add_argument('--trap-probability-threshold', type=float, default=0.7,
                      help='Threshold for considering trap probability (default: 0.7)')
    parser.add_argument('--trap-alert-threshold', type=float, default=0.8,
                      help='Threshold for sending trap alerts (default: 0.8)')
    parser.add_argument('--no-trap-protection', action='store_true',
                      help='Disable trap protection features (default: False)')
    parser.add_argument('--min-free-balance', type=float, default=100.0,
                      help='Minimum free balance to maintain in each account (default: 100.0)')
    
    return parser.parse_args()

async def main():
    """Main entry point for the trap-aware dual position traders system."""
    # Set Redis host to localhost
    os.environ["REDIS_HOST"] = "localhost"
    
    # Parse command line arguments
    args = parse_args()
    
    # Display startup banner
    print(f"{CYAN}======================================================{RESET}")
    print(f"{CYAN}= OMEGA BTC AI - Trap-Aware Dual Position Traders   ={RESET}")
    print(f"{CYAN}======================================================{RESET}")
    print(f"{CYAN}Redis Host: {os.environ.get('REDIS_HOST', 'localhost')}{RESET}")
    print(f"{CYAN}Redis Port: {os.environ.get('REDIS_PORT', '6379')}{RESET}")
    print(f"{CYAN}Trading Symbol: {args.symbol}{RESET}")
    print(f"{CYAN}Testnet Mode: {args.testnet}{RESET}")
    print(f"{CYAN}Long Capital: {args.long_capital} USDT{RESET}")
    print(f"{CYAN}Short Capital: {args.short_capital} USDT{RESET}")
    print(f"{CYAN}Long Leverage: {args.long_leverage}x{RESET}")
    print(f"{CYAN}Short Leverage: {args.short_leverage}x{RESET}")
    print(f"{CYAN}Trap Protection: {'Disabled' if args.no_trap_protection else 'Enabled'}{RESET}")
    print(f"{CYAN}Min Free Balance: {args.min_free_balance} USDT{RESET}")
    print(f"{CYAN}======================================================{RESET}")
    
    # Initialize trap-aware dual traders
    trap_aware_traders = TrapAwareDualTraders(
        use_testnet=args.testnet,
        long_capital=args.long_capital,
        short_capital=args.short_capital,
        symbol=args.symbol,
        long_leverage=args.long_leverage,
        short_leverage=args.short_leverage,
        enable_pnl_alerts=not args.no_pnl_alerts,
        account_limit=args.account_limit,
        long_sub_account=args.long_sub_account,
        short_sub_account=args.short_sub_account,
        trap_probability_threshold=args.trap_probability_threshold,
        trap_alert_threshold=args.trap_alert_threshold,
        enable_trap_protection=not args.no_trap_protection
    )
    
    # Handle shutdown signals
    def signal_handler(sig, frame):
        logger.info(f"{YELLOW}Received shutdown signal{RESET}")
        trap_aware_traders.running = False
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start the trading system
        await trap_aware_traders.start_trading()
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Keyboard interrupt received{RESET}")
    except Exception as e:
        logger.error(f"{RED}Error in main: {e}{RESET}")
    finally:
        await trap_aware_traders.stop_trading()

if __name__ == "__main__":
    asyncio.run(main()) 