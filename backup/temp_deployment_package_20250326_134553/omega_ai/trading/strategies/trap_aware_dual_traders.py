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
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional
import traceback
import redis

from omega_ai.trading.exchanges.dual_position_traders import BitGetDualPositionTraders
from omega_ai.utils.trap_probability_utils import (
    get_current_trap_probability,
    get_probability_components,
    get_detected_trap_info,
    get_probability_threshold,
    is_trap_likely
)
from omega_ai.alerts.telegram_market_report import send_telegram_alert
from omega_ai.trading.strategies.elite_exit_strategy import EliteExitStrategy
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader
from omega_ai.trading.strategies.enhanced_exit_strategy import EnhancedExitStrategy
from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT

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
                 enable_elite_exits: bool = True,
                 elite_exit_confidence: float = 0.7,
                 **kwargs):
        """
        Initialize the trap-aware dual position traders system.
        
        Args:
            trap_probability_threshold: Threshold above which to consider trap probability in trading decisions
            trap_alert_threshold: Threshold above which to send trap alerts
            enable_trap_protection: Whether to enable trap protection features
            enable_elite_exits: Whether to enable elite exit strategy
            elite_exit_confidence: Minimum confidence required for elite exit signals
            **kwargs: Arguments to pass to BitGetDualPositionTraders
        """
        super().__init__(**kwargs)
        self.trap_probability_threshold = trap_probability_threshold
        self.trap_alert_threshold = trap_alert_threshold
        self.enable_trap_protection = enable_trap_protection
        self.enable_elite_exits = enable_elite_exits
        self.elite_exit_confidence = elite_exit_confidence
        self.last_trap_check_time = datetime.now()
        self.trap_check_interval = 30  # seconds
        self.last_trap_alert_time = datetime.now() - timedelta(hours=1)
        self.trap_alert_cooldown = 300  # seconds
        self.last_detected_trap = None
        
        # Initialize enhanced exit strategy
        self.exit_strategy = EnhancedExitStrategy(
            config={
                'base_risk_percent': 1.0,
                'enable_scalping': True,
                'scalping_coefficient': 0.3,
                'strategic_coefficient': 0.6,
                'aggressive_coefficient': 0.1,
                'enable_trailing_stop': True,
                'trailing_activation_threshold': 1.0,
                'trailing_distance_factor': 0.3,
                'min_tp_distance': 0.5,
                'max_tp_levels': 4
            }
        )
        
        # Use multipliers instead of directly modifying traders
        self.long_risk_multiplier = 1.0
        self.short_risk_multiplier = 1.0
        
        logger.info(f"{CYAN}Trap-Aware Dual Traders initialized with:{RESET}")
        logger.info(f"{CYAN}  Trap Probability Threshold: {trap_probability_threshold}{RESET}")
        logger.info(f"{CYAN}  Trap Alert Threshold: {trap_alert_threshold}{RESET}")
        logger.info(f"{CYAN}  Trap Protection Enabled: {enable_trap_protection}{RESET}")
        logger.info(f"{CYAN}  Elite Exit Strategy Enabled: {enable_elite_exits}{RESET}")
        logger.info(f"{CYAN}  Elite Exit Confidence: {elite_exit_confidence}{RESET}")
    
    async def initialize(self) -> None:
        """Initialize the trap-aware dual position traders system."""
        # First initialize the parent class
        await super().initialize()
        
        # Now initialize the elite exit strategy if enabled
        if self.enable_elite_exits and self.long_trader and self.long_trader.traders and "strategic" in self.long_trader.traders:
            # Get the exchange from the long trader (both traders use the same exchange)
            try:
                # First try to access exchange directly
                strategic_trader = self.long_trader.traders["strategic"]
                
                # Different ways the exchange might be accessible
                if hasattr(strategic_trader, 'exchange') and isinstance(strategic_trader.exchange, BitGetCCXT):
                    exchange = strategic_trader.exchange
                elif isinstance(strategic_trader, BitGetCCXT):
                    # If it's already a BitGetCCXT instance, use it directly
                    exchange = strategic_trader
                else:
                    # As a fallback, create a new BitGetCCXT instance
                    logger.warning(f"{YELLOW}Creating new BitGetCCXT instance for elite exit strategy{RESET}")
                    exchange = BitGetCCXT(
                        config={
                            'api_key': self.api_key,
                            'api_secret': self.secret_key,
                            'api_password': self.passphrase,
                            'use_testnet': self.use_testnet,
                            'sub_account': self.long_sub_account
                        }
                    )
                    await exchange.initialize()
                
                # Make sure exchange is a BitGetCCXT instance
                if not isinstance(exchange, BitGetCCXT):
                    raise TypeError("Exchange must be a BitGetCCXT instance")
                
                self.elite_exit_strategy = EliteExitStrategy(
                    exchange=exchange,
                    symbol=self.symbol,
                    min_confidence=self.elite_exit_confidence
                )
                logger.info(f"{GREEN}Elite exit strategy initialized with confidence threshold: {self.elite_exit_confidence}{RESET}")
            except Exception as e:
                logger.error(f"{RED}Error initializing elite exit strategy: {e}{RESET}")
        elif self.enable_elite_exits:
            logger.error(f"{RED}Could not initialize elite exit strategy: long trader not properly initialized{RESET}")
    
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
            if (isinstance(probability, (int, float)) and 
                probability >= self.trap_alert_threshold and 
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
        
        if not isinstance(probability, (int, float)) or probability < self.trap_probability_threshold or not trap_type:
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

    async def _run_long_trader(self) -> None:
        """Run the long position trader with trap awareness."""
        if not self.long_trader:
            logger.error(f"{RED}Long trader not initialized{RESET}")
            return
            
        # Ensure the trader is initialized
        await self.long_trader.initialize()
        
        while self.running:
            try:
                # Check for traps
                trap_info = await self.check_for_traps()
                
                # Adjust trading based on trap detection
                if trap_info.get('trap_detected'):
                    await self._adjust_trading_based_on_traps(trap_info)
                
                # Get current positions
                positions = await self.long_trader.traders["strategic"].get_positions()
                
                if positions:
                    # Get current price
                    try:
                        current_price = await self.long_trader.get_current_price(self.symbol)
                    except Exception as e:
                        logger.error(f"{RED}Error getting current price: {str(e)}{RESET}")
                        current_price = None
                    
                    if current_price:
                        # Check each position for exit conditions
                        for position in positions:
                            position_id = position.get('id', '')
                            
                            # Update trailing stops
                            new_stop = await self.exit_strategy.update_trailing_stop(
                                position_id,
                                current_price
                            )
                            
                            if new_stop and new_stop != position.get('stopLossPrice'):
                                await self._update_stop_loss(position, new_stop)
                            
                            # Check exit conditions
                            should_exit, exit_info = await self.exit_strategy.check_exit_conditions(
                                position_id,
                                current_price,
                                trap_info
                            )
                            
                            if should_exit and exit_info:
                                # Execute the exit
                                await self._execute_exit(position, exit_info)
                
                # Run the trader
                await self.long_trader.start_trading()
                
                # Sleep briefly
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"{RED}Error in long trader: {str(e)}{RESET}")
                await asyncio.sleep(5)

    async def _run_short_trader(self) -> None:
        """Run the short position trader with trap awareness."""
        if not self.short_trader:
            logger.error(f"{RED}Short trader not initialized{RESET}")
            return
            
        # Ensure the trader is initialized
        await self.short_trader.initialize()
        
        while self.running:
            try:
                # Check for traps
                trap_info = await self.check_for_traps()
                
                # Adjust trading based on trap detection
                if trap_info.get('trap_detected'):
                    await self._adjust_trading_based_on_traps(trap_info)
                
                # Get current positions
                positions = await self.short_trader.traders["strategic"].get_positions()
                
                if positions:
                    # Get current price
                    try:
                        current_price = await self.short_trader.get_current_price(self.symbol)
                    except Exception as e:
                        logger.error(f"{RED}Error getting current price: {str(e)}{RESET}")
                        current_price = None
                    
                    if current_price:
                        # Check each position for exit conditions
                        for position in positions:
                            position_id = position.get('id', '')
                            
                            # Update trailing stops
                            new_stop = await self.exit_strategy.update_trailing_stop(
                                position_id,
                                current_price
                            )
                            
                            if new_stop and new_stop != position.get('stopLossPrice'):
                                await self._update_stop_loss(position, new_stop)
                            
                            # Check exit conditions
                            should_exit, exit_info = await self.exit_strategy.check_exit_conditions(
                                position_id,
                                current_price,
                                trap_info
                            )
                            
                            if should_exit and exit_info:
                                # Execute the exit
                                await self._execute_exit(position, exit_info)
                
                # Run the trader
                await self.short_trader.start_trading()
                
                # Sleep briefly
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"{RED}Error in short trader: {str(e)}{RESET}")
                await asyncio.sleep(5)

    async def _update_stop_loss(self, position: Dict, new_stop: float) -> None:
        """Update stop loss order for a position."""
        try:
            symbol = position.get('symbol', '')
            stop_order_id = position.get('stopLossId')
            
            if stop_order_id:
                # Modify existing stop order
                await self.long_trader.traders["strategic"].edit_order(
                    symbol=symbol,
                    order_id=stop_order_id,
                    price=new_stop
                )
            else:
                # Create new stop loss order
                direction = position.get('side', '').lower()
                contracts = float(position.get('contracts', 0))
                
                opposite_side = 'sell' if direction == 'buy' else 'buy'
                await self.long_trader.traders["strategic"].create_order(
                    symbol=symbol,
                    type='stop',
                    side=opposite_side,
                    amount=contracts,
                    price=new_stop,
                    params={
                        'stopPrice': new_stop,
                        'reduceOnly': True
                    }
                )
            
            logger.info(f"{GREEN}Updated stop loss to {new_stop} for {symbol} position{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}Error updating stop loss: {str(e)}{RESET}")

    async def _execute_exit(self, position: Dict, exit_info: Dict) -> None:
        """Execute a full or partial position exit."""
        try:
            symbol = position.get('symbol', '')
            direction = position.get('side', '').lower()
            contracts = float(position.get('contracts', 0))
            
            # Calculate size to close
            exit_percentage = exit_info.get('percentage', 100)
            size_to_close = contracts * (exit_percentage / 100)
            
            # Create market order to close
            opposite_side = 'sell' if direction == 'buy' else 'buy'
            await self.long_trader.traders["strategic"].create_market_order(
                symbol=symbol,
                side=opposite_side,
                amount=size_to_close,
                reduce_only=True
            )
            
            # Log the exit
            reason = exit_info.get('reason', 'unknown')
            price = exit_info.get('price', 0)
            logger.info(f"{GREEN}Executed {exit_percentage}% {reason} exit at {price} for {symbol} position{RESET}")
            
            # Process the exit in our tracking
            await self.exit_strategy.process_partial_exit(position.get('id', ''), exit_info)
            
        except Exception as e:
            logger.error(f"{RED}Error executing exit: {str(e)}{RESET}")

class TrapAwareDualTradersPositionsTracker:
    """Trap-Aware Dual Traders positions tracker."""
    
    def __init__(
        self,
        trap_probability_threshold: float = 0.7,
        trap_alert_threshold: float = 0.8,
        enable_trap_protection: bool = True,
        enable_elite_exits: bool = True,
        elite_exit_confidence: float = 0.7
    ):
        """Initialize the TADT positions tracker.
        
        Args:
            trap_probability_threshold: Threshold for trap probability detection
            trap_alert_threshold: Threshold for trap alert generation
            enable_trap_protection: Whether to enable trap protection
            enable_elite_exits: Whether to enable elite exit strategies
            elite_exit_confidence: Confidence threshold for elite exits
        """
        self.trap_probability_threshold = trap_probability_threshold
        self.trap_alert_threshold = trap_alert_threshold
        self.enable_trap_protection = enable_trap_protection
        self.enable_elite_exits = enable_elite_exits
        self.elite_exit_confidence = elite_exit_confidence
        
        self.long_trader: Optional[BitGetTrader] = None
        self.short_trader: Optional[BitGetTrader] = None
        self.live_traders: Optional[BitGetLiveTraders] = None
        self._monitoring_task: Optional[asyncio.Task] = None
        self._stop_monitoring = False

    async def initialize(self) -> None:
        """Initialize the TADT positions tracker."""
        try:
            self.live_traders = BitGetLiveTraders()
            await self.live_traders.initialize()
            self.long_trader = self.live_traders.long_trader
            self.short_trader = self.live_traders.short_trader
            logger.info("TADT positions tracker initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TADT positions tracker: {e}")
            raise

    async def get_positions_summary(self) -> Dict[str, Any]:
        """Get a summary of current positions for both sub-accounts.
        
        Returns:
            Dict containing positions summary and total PnL
        """
        if not self.long_trader or not self.short_trader:
            raise RuntimeError("TADT positions tracker not initialized")
            
        long_positions = await self.long_trader.get_positions()
        short_positions = await self.short_trader.get_positions()
        
        total_pnl = sum(
            float(pos.get("unrealizedPnl", 0)) + float(pos.get("realizedPnl", 0))
            for pos in long_positions + short_positions
        )
        
        return {
            "long_positions": long_positions,
            "short_positions": short_positions,
            "total_pnl": total_pnl,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    async def get_position_history(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get position history for both sub-accounts.
        
        Returns:
            Dict containing position history for both long and short traders
        """
        if not self.long_trader or not self.short_trader:
            raise RuntimeError("TADT positions tracker not initialized")
            
        long_history = await self.long_trader.get_trade_history()
        short_history = await self.short_trader.get_trade_history()
        
        return {
            "long_history": long_history,
            "short_history": short_history,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    async def analyze_trader_performance(self, trader_type: str) -> Dict[str, Any]:
        """Analyze performance metrics for a specific trader.
        
        Args:
            trader_type: Either "long" or "short"
            
        Returns:
            Dict containing performance metrics
        """
        if not self.long_trader or not self.short_trader:
            raise RuntimeError("TADT positions tracker not initialized")
            
        trader = self.long_trader if trader_type == "long" else self.short_trader
        history = await trader.get_trade_history()
        
        if not history:
            return {
                "total_trades": 0,
                "win_rate": 0.0,
                "average_pnl": 0.0,
                "profit_factor": 0.0
            }
            
        total_trades = len(history)
        winning_trades = sum(1 for trade in history if float(trade["pnl"]) > 0)
        total_pnl = sum(float(trade["pnl"]) for trade in history)
        gross_profit = sum(float(trade["pnl"]) for trade in history if float(trade["pnl"]) > 0)
        gross_loss = abs(sum(float(trade["pnl"]) for trade in history if float(trade["pnl"]) < 0))
        
        return {
            "total_trades": total_trades,
            "win_rate": winning_trades / total_trades if total_trades > 0 else 0.0,
            "average_pnl": total_pnl / total_trades if total_trades > 0 else 0.0,
            "profit_factor": gross_profit / gross_loss if gross_loss > 0 else float('inf')
        }

    async def detect_trap_patterns(self, trader_type: str) -> List[Dict[str, Any]]:
        """Detect trap patterns in position history.
        
        Args:
            trader_type: Either "long" or "short"
            
        Returns:
            List of detected trap patterns
        """
        if not self.long_trader or not self.short_trader:
            raise RuntimeError("TADT positions tracker not initialized")
            
        trader = self.long_trader if trader_type == "long" else self.short_trader
        history = await trader.get_trade_history()
        
        traps = []
        for trade in history:
            # Simple trap pattern detection based on price movement
            entry_price = float(trade["entryPrice"])
            exit_price = float(trade["exitPrice"])
            pnl = float(trade["pnl"])
            
            if trader_type == "long":
                is_trap = pnl < 0 and (exit_price - entry_price) / entry_price < -0.01
            else:
                is_trap = pnl < 0 and (entry_price - exit_price) / entry_price < -0.01
                
            if is_trap:
                traps.append({
                    "pattern_type": "price_trap",
                    "confidence": self.trap_probability_threshold,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "pnl": pnl,
                    "timestamp": trade["exitTime"]
                })
                
        return traps

    async def get_risk_metrics(self) -> Dict[str, Any]:
        """Calculate risk metrics for current positions.
        
        Returns:
            Dict containing risk metrics
        """
        if not self.long_trader or not self.short_trader:
            raise RuntimeError("TADT positions tracker not initialized")
            
        long_positions = await self.long_trader.get_positions()
        short_positions = await self.short_trader.get_positions()
        
        total_exposure = sum(
            float(pos.get("contracts", 0)) * float(pos.get("entryPrice", 0))
            for pos in long_positions + short_positions
        )
        
        total_margin = sum(
            float(pos.get("marginBalance", 0))
            for pos in long_positions + short_positions
        )
        
        total_leverage = sum(
            float(pos.get("leverage", 0))
            for pos in long_positions + short_positions
        )
        
        return {
            "total_exposure": total_exposure,
            "margin_ratio": total_margin / total_exposure if total_exposure > 0 else 0.0,
            "leverage_ratio": total_leverage / len(long_positions + short_positions) if long_positions or short_positions else 0.0,
            "position_concentration": len(long_positions + short_positions),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    async def generate_performance_report(self) -> Dict[str, Any]:
        """Generate a comprehensive performance report.
        
        Returns:
            Dict containing performance report
        """
        positions_summary = await self.get_positions_summary()
        position_history = await self.get_position_history()
        long_performance = await self.analyze_trader_performance("long")
        short_performance = await self.analyze_trader_performance("short")
        risk_metrics = await self.get_risk_metrics()
        
        long_traps = await self.detect_trap_patterns("long")
        short_traps = await self.detect_trap_patterns("short")
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "positions_summary": positions_summary,
            "performance_metrics": {
                "long_trader": long_performance,
                "short_trader": short_performance
            },
            "risk_metrics": risk_metrics,
            "trap_patterns": {
                "long_trader": long_traps,
                "short_trader": short_traps
            }
        }

    async def monitor_positions_continuously(self) -> None:
        """Monitor positions continuously and generate alerts."""
        self._stop_monitoring = False
        
        while not self._stop_monitoring:
            try:
                # Get current positions and analyze
                positions_summary = await self.get_positions_summary()
                risk_metrics = await self.get_risk_metrics()
                
                # Check for high risk conditions
                if risk_metrics["margin_ratio"] < 0.1:
                    logger.warning("Low margin ratio detected!")
                    
                # Check for trap patterns
                long_traps = await self.detect_trap_patterns("long")
                short_traps = await self.detect_trap_patterns("short")
                
                if long_traps or short_traps:
                    logger.warning(f"Trap patterns detected! Long: {len(long_traps)}, Short: {len(short_traps)}")
                    
                # Generate performance report
                report = await self.generate_performance_report()
                logger.info(f"Performance report generated: {report}")
                
                # Wait before next check
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in position monitoring: {e}")
                await asyncio.sleep(5)  # Wait before retrying

    def stop_monitoring(self) -> None:
        """Stop the continuous position monitoring."""
        self._stop_monitoring = True

async def check_redis_connectivity():
    """Check if Redis is available and responsive"""
    try:
        redis_host = os.environ.get("REDIS_HOST", "localhost")
        redis_port = int(os.environ.get("REDIS_PORT", 6379))
        print(f"{YELLOW}DEBUG: Checking Redis connectivity at {redis_host}:{redis_port}{RESET}")
        
        # Create Redis client
        r = redis.Redis(host=redis_host, port=redis_port, socket_connect_timeout=5.0)
        
        # Try to ping Redis
        response = r.ping()
        if response:
            print(f"{GREEN}Redis connectivity test: SUCCESS{RESET}")
            return True
        else:
            print(f"{RED}Redis connectivity test: FAILED (no ping response){RESET}")
            return False
    except Exception as e:
        print(f"{RED}Redis connectivity test: FAILED with error: {str(e)}{RESET}")
        return False

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='OMEGA BTC AI Trap-Aware Dual Position Traders')
    parser.add_argument('--symbol', type=str, default='BTCUSDT',
                      help='Trading symbol (default: BTCUSDT)')
    parser.add_argument('--testnet', action='store_true',
                      help='Use testnet (default: False)')
    parser.add_argument('--mainnet', action='store_true', default=True,
                      help='Use mainnet (default: True)')
    parser.add_argument('--long-capital', type=float, default=150.0,
                      help='Initial capital for long trader in USDT (default: 150.0)')
    parser.add_argument('--short-capital', type=float, default=200.0,
                      help='Initial capital for short trader in USDT (default: 200.0)')
    parser.add_argument('--long-leverage', type=int, default=11,
                      help='Leverage for long positions (default: 11)')
    parser.add_argument('--short-leverage', type=int, default=11,
                      help='Leverage for short positions (default: 11)')
    parser.add_argument('--no-pnl-alerts', action='store_true',
                      help='Disable PnL alerts (default: False)')
    parser.add_argument('--account-limit', type=float, default=1500.0,
                      help='Maximum total account value in USDT (default: 1500.0)')
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
    parser.add_argument('--min-free-balance', type=float, default=0.0,
                      help='Minimum free balance to maintain in each account (default: 0.0)')
    parser.add_argument('--enable-elite-exits', action='store_true',
                      help='Enable elite exit strategy (default: False)')
    parser.add_argument('--elite-exit-confidence', type=float, default=0.7,
                      help='Minimum confidence required for elite exit signals (default: 0.7)')
    
    return parser.parse_args()

async def main():
    """Main entry point for the trap-aware dual position traders system."""
    # Set Redis host to localhost
    os.environ["REDIS_HOST"] = "localhost"
    
    # Parse command line arguments
    args = parse_args()
    
    # Display startup banner with detailed debug info
    print(f"{CYAN}======================================================{RESET}")
    print(f"{CYAN}= OMEGA BTC AI - Trap-Aware Dual Position Traders   ={RESET}")
    print(f"{CYAN}======================================================{RESET}")
    print(f"{CYAN}Redis Host: {os.environ.get('REDIS_HOST', 'localhost')}{RESET}")
    print(f"{CYAN}Redis Port: {os.environ.get('REDIS_PORT', '6379')}{RESET}")
    print(f"{CYAN}Trading Symbol: {args.symbol}{RESET}")
    print(f"{CYAN}Testnet Mode: {args.testnet}{RESET}")
    print(f"{CYAN}Mainnet Mode: {args.mainnet}{RESET}")
    print(f"{CYAN}Long Capital: {args.long_capital} USDT{RESET}")
    print(f"{CYAN}Short Capital: {args.short_capital} USDT{RESET}")
    print(f"{CYAN}Long Leverage: {args.long_leverage}x{RESET}")
    print(f"{CYAN}Short Leverage: {args.short_leverage}x{RESET}")
    print(f"{CYAN}Trap Protection: {'Disabled' if args.no_trap_protection else 'Enabled'}{RESET}")
    print(f"{CYAN}Min Free Balance: {args.min_free_balance} USDT{RESET}")
    print(f"{CYAN}Elite Exit Strategy: {'Disabled' if not args.enable_elite_exits else 'Enabled'}{RESET}")
    print(f"{CYAN}Elite Exit Confidence: {args.elite_exit_confidence}{RESET}")
    print(f"{CYAN}Account Limit: {args.account_limit} USDT{RESET}")
    print(f"{CYAN}Long Sub-account: {args.long_sub_account or 'Default (from env)'}{RESET}")
    print(f"{CYAN}Short Sub-account: {args.short_sub_account}{RESET}")
    print(f"{CYAN}======================================================{RESET}")
    print(f"{YELLOW}DEBUG: Starting initialization...{RESET}")
    
    # Check Redis connectivity first
    redis_ok = await check_redis_connectivity()
    if not redis_ok:
        print(f"{RED}ERROR: Redis connection failed. Cannot continue.{RESET}")
        print(f"{MAGENTA}STATUS:ERROR:Redis connection failed{RESET}")
        return
    
    try:
        # Initialize trap-aware dual traders
        trap_aware_traders = TrapAwareDualTraders(
            use_testnet=args.testnet,
            long_capital=args.long_capital,
            short_capital=args.short_capital,
            symbol=args.symbol,
            long_leverage=args.long_leverage,
            short_leverage=args.short_leverage,
            enable_pnl_alerts=not args.no_pnl_alerts,
            account_limit=0.0 if args.min_free_balance == 0.0 else args.account_limit,
            long_sub_account=args.long_sub_account,
            short_sub_account=args.short_sub_account,
            trap_probability_threshold=args.trap_probability_threshold,
            trap_alert_threshold=args.trap_alert_threshold,
            enable_trap_protection=not args.no_trap_protection,
            enable_elite_exits=args.enable_elite_exits,
            elite_exit_confidence=args.elite_exit_confidence
        )
        
        print(f"{YELLOW}DEBUG: TrapAwareDualTraders instance created{RESET}")
        
        # Check current trap probability
        try:
            probability = get_current_trap_probability()
            is_likely, trap_type, confidence = is_trap_likely()
            
            print(f"\n{YELLOW}==== CURRENT MARKET CONDITIONS ===={RESET}")
            print(f"{YELLOW}Trap Probability: {probability * 100:.1f}%{RESET}")
            
            if is_likely and trap_type:
                print(f"{RED}WARNING: Likely {trap_type.upper()} detected (Confidence: {confidence * 100:.1f}%){RESET}")
            else:
                print(f"{GREEN}No traps currently detected{RESET}")
            
            components = get_probability_components()
            if components and isinstance(components, dict):
                print(f"\n{CYAN}Component Analysis:{RESET}")
                for name, value in components.items():
                    if isinstance(value, (int, float)):
                        if value > 0.7:
                            color = RED
                        elif value > 0.5:
                            color = YELLOW
                        else:
                            color = GREEN
                        print(f"{CYAN}- {name.replace('_', ' ').title()}: {color}{value * 100:.1f}%{RESET}")
            
            print(f"\n{CYAN}==== STARTING TRADING SYSTEM ===={RESET}")
        except Exception as e:
            print(f"{RED}Error getting trap probability: {e}{RESET}")
            print(f"{YELLOW}DEBUG: Continuing despite trap probability error{RESET}")
        
        # Handle shutdown signals
        def signal_handler(sig, frame):
            logger.info(f"{YELLOW}Received shutdown signal{RESET}")
            trap_aware_traders.running = False
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            # Print status marker for the shell script to pick up
            print(f"{MAGENTA}STATUS:STARTING{RESET}")
            print(f"{YELLOW}DEBUG: About to call check_account_limit{RESET}")
            
            # Check account limit early
            has_limit = await trap_aware_traders.check_account_limit()
            print(f"{YELLOW}DEBUG: check_account_limit result: {has_limit}{RESET}")
            if not has_limit:
                print(f"{RED}Account limit check failed. Stopping.{RESET}")
                print(f"{MAGENTA}STATUS:ERROR:Account limit exceeded{RESET}")
                return
                
            print(f"{YELLOW}DEBUG: About to call trap_aware_traders.start_trading(){RESET}")
            
            # Start the trading system
            await trap_aware_traders.start_trading()
        except KeyboardInterrupt:
            logger.info(f"{YELLOW}Keyboard interrupt received{RESET}")
            print(f"{MAGENTA}STATUS:STOPPING{RESET}")
        except Exception as e:
            logger.error(f"{RED}Error in main: {e}{RESET}")
            print(f"{RED}ERROR: {str(e)}{RESET}")
            print(f"{RED}Traceback: {traceback.format_exc()}{RESET}")
            print(f"{MAGENTA}STATUS:ERROR:{str(e)}{RESET}")
        finally:
            print(f"{MAGENTA}STATUS:STOPPING{RESET}")
            await trap_aware_traders.stop_trading()
            print(f"{MAGENTA}STATUS:STOPPED{RESET}")
    except Exception as e:
        print(f"{RED}CRITICAL ERROR during initialization: {str(e)}{RESET}")
        print(f"{RED}Traceback: {traceback.format_exc()}{RESET}")
        print(f"{MAGENTA}STATUS:ERROR:Initialization failed: {str(e)}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 