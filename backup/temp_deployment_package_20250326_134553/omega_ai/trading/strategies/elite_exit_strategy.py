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
OMEGA BTC AI - Elite Exit Strategy
================================

This module implements sophisticated exit strategies for trap-aware dual traders,
integrating multiple factors for optimal exit decisions.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from omega_ai.analysis.fibonacci_patterns import FibonacciPatternDetector
from omega_ai.monitor.monitor_market_trends import MarketTrendAnalyzer
from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT
from omega_ai.utils.trap_probability_utils import get_current_trap_probability

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

@dataclass
class ExitSignal:
    """Represents an exit signal with confidence and reasoning."""
    symbol: str
    side: str  # "long" or "short"
    exit_price: float
    stop_loss: float
    take_profit: float
    confidence: float
    reasons: List[str]
    pattern_type: Optional[str] = None
    market_regime: Optional[str] = None
    fibonacci_level: Optional[str] = None
    trap_probability: Optional[float] = None
    timestamp: datetime = datetime.now()

class EliteExitStrategy:
    """Implements sophisticated exit strategies for trap-aware dual traders."""
    
    def __init__(
        self,
        exchange: BitGetCCXT,
        symbol: str = "BTCUSDT",
        base_risk_percent: float = 1.0,
        min_confidence: float = 0.7,
        enable_trailing_stop: bool = True,
        trailing_stop_distance: float = 0.5,
        trailing_stop_step: float = 0.1,
        enable_fibonacci_exits: bool = True,
        enable_pattern_exits: bool = True,
        enable_trap_exits: bool = True
    ):
        """
        Initialize the elite exit strategy.
        
        Args:
            exchange: BitGetCCXT exchange instance
            symbol: Trading symbol
            base_risk_percent: Base risk percentage for position sizing
            min_confidence: Minimum confidence required for exit signals
            enable_trailing_stop: Whether to enable trailing stops
            trailing_stop_distance: Distance for trailing stop in percentage
            trailing_stop_step: Step size for trailing stop adjustments
            enable_fibonacci_exits: Whether to use Fibonacci-based exits
            enable_pattern_exits: Whether to use pattern-based exits
            enable_trap_exits: Whether to use trap-based exits
        """
        self.exchange = exchange
        self.symbol = symbol
        self.base_risk_percent = base_risk_percent
        self.min_confidence = min_confidence
        self.enable_trailing_stop = enable_trailing_stop
        self.trailing_stop_distance = trailing_stop_distance
        self.trailing_stop_step = trailing_stop_step
        self.enable_fibonacci_exits = enable_fibonacci_exits
        self.enable_pattern_exits = enable_pattern_exits
        self.enable_trap_exits = enable_trap_exits
        
        # Initialize components
        self.fibonacci_detector = FibonacciPatternDetector()
        self.market_analyzer = MarketTrendAnalyzer()
        
        # State tracking
        self.active_trailing_stops: Dict[str, float] = {}
        self.last_exit_time: Dict[str, datetime] = {}
        self.exit_cooldown = 300  # 5 minutes between exits
        
        logger.info(f"{CYAN}Initialized Elite Exit Strategy for {symbol}{RESET}")
        logger.info(f"{CYAN}Base Risk: {base_risk_percent}% | Min Confidence: {min_confidence}{RESET}")
    
    async def analyze_exit_opportunity(
        self,
        position: Dict,
        current_price: float
    ) -> Optional[ExitSignal]:
        """
        Analyze if an exit opportunity exists for the given position.
        
        Args:
            position: Current position information
            current_price: Current market price
            
        Returns:
            Optional[ExitSignal]: Exit signal if conditions are met
        """
        try:
            symbol = position.get('symbol', self.symbol)
            side = position.get('side', 'long')
            entry_price = float(position.get('entry_price', 0))
            
            if not entry_price:
                logger.warning(f"{YELLOW}No entry price found for position{RESET}")
                return None
            
            # Check cooldown period
            last_exit = self.last_exit_time.get(symbol)
            if last_exit and (datetime.now() - last_exit).total_seconds() < self.exit_cooldown:
                return None
            
            # Collect exit signals from different sources
            exit_signals = []
            
            # Check Fibonacci-based exits
            if self.enable_fibonacci_exits:
                fib_signal = await self._check_fibonacci_exit(side, current_price, entry_price)
                if fib_signal:
                    exit_signals.append(fib_signal)
            
            # Check pattern-based exits
            if self.enable_pattern_exits:
                pattern_signal = await self._check_pattern_exit(side, current_price, entry_price)
                if pattern_signal:
                    exit_signals.append(pattern_signal)
            
            # Check trap-based exits
            if self.enable_trap_exits:
                trap_signal = await self._check_trap_exit(side, current_price, entry_price)
                if trap_signal:
                    exit_signals.append(trap_signal)
            
            # Check market regime exits
            regime_signal = await self._check_market_regime_exit(side, current_price, entry_price)
            if regime_signal:
                exit_signals.append(regime_signal)
            
            if not exit_signals:
                return None
            
            # Calculate overall confidence and reasons
            total_confidence = sum(signal['confidence'] for signal in exit_signals) / len(exit_signals)
            reasons = [signal['reason'] for signal in exit_signals]
            
            if total_confidence < self.min_confidence:
                return None
            
            # Create exit signal
            signal = ExitSignal(
                symbol=symbol,
                side=side,
                exit_price=current_price,
                stop_loss=self._calculate_stop_loss(side, entry_price, current_price),
                take_profit=self._calculate_take_profit(side, entry_price, current_price),
                confidence=total_confidence,
                reasons=reasons,
                pattern_type=next((s.get('pattern_type') for s in exit_signals if 'pattern_type' in s), None),
                market_regime=next((s.get('market_regime') for s in exit_signals if 'market_regime' in s), None),
                fibonacci_level=next((s.get('fibonacci_level') for s in exit_signals if 'fibonacci_level' in s), None),
                trap_probability=get_current_trap_probability()
            )
            
            logger.info(f"{GREEN}Exit signal generated for {symbol} {side} position{RESET}")
            logger.info(f"{GREEN}Confidence: {total_confidence:.2f} | Reasons: {', '.join(reasons)}{RESET}")
            
            return signal
            
        except Exception as e:
            logger.error(f"{RED}Error analyzing exit opportunity: {e}{RESET}")
            return None
    
    async def _check_fibonacci_exit(
        self,
        side: str,
        current_price: float,
        entry_price: float
    ) -> Optional[Dict[str, Any]]:
        """Check for Fibonacci-based exit signals."""
        try:
            # Get Fibonacci levels
            fib_levels = await self.exchange.get_fibonacci_levels(self.symbol)
            if not fib_levels:
                return None
            
            # Calculate price movement from entry
            price_change = ((current_price - entry_price) / entry_price) * 100
            
            # Check for Fibonacci level alignment
            for level, price in fib_levels.items():
                distance = abs((current_price - price) / price * 100)
                if distance < 0.5:  # Within 0.5% of a Fibonacci level
                    # Determine if this is a good exit level
                    if side == 'long' and price < current_price:
                        return {
                            'confidence': 0.8,
                            'reason': f"Price near Fibonacci {level} level",
                            'fibonacci_level': level
                        }
                    elif side == 'short' and price > current_price:
                        return {
                            'confidence': 0.8,
                            'reason': f"Price near Fibonacci {level} level",
                            'fibonacci_level': level
                        }
            
            return None
            
        except Exception as e:
            logger.error(f"{RED}Error checking Fibonacci exit: {e}{RESET}")
            return None
    
    async def _check_pattern_exit(
        self,
        side: str,
        current_price: float,
        entry_price: float
    ) -> Optional[Dict[str, Any]]:
        """Check for pattern-based exit signals."""
        try:
            # Get recent price data
            ohlcv = await self.exchange.fetch_ohlcv(self.symbol, timeframe='1h', limit=100)
            if not ohlcv:
                return None
            
            # Convert to pattern points
            points = [
                {'price': candle[4], 'timestamp': datetime.fromtimestamp(candle[0] / 1000)}
                for candle in ohlcv
            ]
            
            # Detect patterns
            patterns = self.fibonacci_detector.detect_patterns(points)
            
            # Check for reversal patterns
            for pattern in patterns:
                pattern_type = pattern.get('type', '')
                if side == 'long' and 'Bearish' in pattern_type:
                    return {
                        'confidence': 0.75,
                        'reason': f"Detected {pattern_type} pattern",
                        'pattern_type': pattern_type
                    }
                elif side == 'short' and 'Bullish' in pattern_type:
                    return {
                        'confidence': 0.75,
                        'reason': f"Detected {pattern_type} pattern",
                        'pattern_type': pattern_type
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"{RED}Error checking pattern exit: {e}{RESET}")
            return None
    
    async def _check_trap_exit(
        self,
        side: str,
        current_price: float,
        entry_price: float
    ) -> Optional[Dict[str, Any]]:
        """Check for trap-based exit signals."""
        try:
            # Get current trap probability
            trap_probability = get_current_trap_probability()
            if trap_probability < 0.7:  # Only consider high probability traps
                return None
            
            # Check if we're in a trap that opposes our position
            if side == 'long' and trap_probability > 0.8:  # High probability bear trap
                return {
                    'confidence': trap_probability,
                    'reason': f"High probability bear trap detected ({trap_probability:.2f})"
                }
            elif side == 'short' and trap_probability > 0.8:  # High probability bull trap
                return {
                    'confidence': trap_probability,
                    'reason': f"High probability bull trap detected ({trap_probability:.2f})"
                }
            
            return None
            
        except Exception as e:
            logger.error(f"{RED}Error checking trap exit: {e}{RESET}")
            return None
    
    async def _check_market_regime_exit(
        self,
        side: str,
        current_price: float,
        entry_price: float
    ) -> Optional[Dict[str, Any]]:
        """Check for market regime-based exit signals."""
        try:
            # Get market trend analysis
            market_data = await self.market_analyzer.analyze_trends()
            if not market_data:
                return None
            
            # Check 15-minute trend
            trend_15m = market_data.get('15min', {}).get('trend', '')
            
            # Exit if trend opposes position
            if side == 'long' and 'Bearish' in trend_15m:
                return {
                    'confidence': 0.7,
                    'reason': "Market regime shifted to bearish",
                    'market_regime': trend_15m
                }
            elif side == 'short' and 'Bullish' in trend_15m:
                return {
                    'confidence': 0.7,
                    'reason': "Market regime shifted to bullish",
                    'market_regime': trend_15m
                }
            
            return None
            
        except Exception as e:
            logger.error(f"{RED}Error checking market regime exit: {e}{RESET}")
            return None
    
    def _calculate_stop_loss(
        self,
        side: str,
        entry_price: float,
        current_price: float
    ) -> float:
        """Calculate stop loss level based on current price and position."""
        if side == 'long':
            return current_price * (1 - self.base_risk_percent / 100)
        else:
            return current_price * (1 + self.base_risk_percent / 100)
    
    def _calculate_take_profit(
        self,
        side: str,
        entry_price: float,
        current_price: float
    ) -> float:
        """Calculate take profit level based on current price and position."""
        if side == 'long':
            return current_price * (1 + self.base_risk_percent * 2 / 100)  # 2:1 reward:risk
        else:
            return current_price * (1 - self.base_risk_percent * 2 / 100)  # 2:1 reward:risk
    
    async def update_trailing_stop(
        self,
        symbol: str,
        position: Dict,
        current_price: float
    ) -> Optional[float]:
        """Update trailing stop if conditions are met."""
        if not self.enable_trailing_stop:
            return None
            
        try:
            side = position.get('side', 'long')
            entry_price = float(position.get('entry_price', 0))
            
            if not entry_price:
                return None
            
            # Calculate current trailing stop
            current_stop = self.active_trailing_stops.get(symbol)
            if not current_stop:
                # Initialize trailing stop
                if side == 'long':
                    current_stop = entry_price * (1 - self.trailing_stop_distance / 100)
                else:
                    current_stop = entry_price * (1 + self.trailing_stop_distance / 100)
                self.active_trailing_stops[symbol] = current_stop
            
            # Update trailing stop if price moved favorably
            if side == 'long':
                new_stop = current_price * (1 - self.trailing_stop_distance / 100)
                if new_stop > current_stop:
                    current_stop = new_stop
            else:
                new_stop = current_price * (1 + self.trailing_stop_distance / 100)
                if new_stop < current_stop:
                    current_stop = new_stop
            
            self.active_trailing_stops[symbol] = current_stop
            return current_stop
            
        except Exception as e:
            logger.error(f"{RED}Error updating trailing stop: {e}{RESET}")
            return None
    
    async def execute_exit(
        self,
        signal: ExitSignal,
        position: Dict
    ) -> bool:
        """
        Execute the exit signal for the given position.
        
        Args:
            signal: Exit signal to execute
            position: Current position information
            
        Returns:
            bool: True if exit was successful
        """
        try:
            # Get current price
            ticker = await self.exchange.get_market_ticker(signal.symbol)
            current_price = float(ticker['last'])
            
            # Calculate position size
            position_size = float(position.get('size', 0))
            if not position_size:
                logger.warning(f"{YELLOW}No position size found{RESET}")
                return False
            
            # Place market order to close position
            order = await self.exchange.place_order(
                symbol=signal.symbol,
                side='sell' if signal.side == 'long' else 'buy',
                amount=position_size,
                order_type='market',
                reduce_only=True
            )
            
            if not order:
                logger.error(f"{RED}Failed to place exit order{RESET}")
                return False
            
            # Update last exit time
            self.last_exit_time[signal.symbol] = datetime.now()
            
            # Clear trailing stop
            if signal.symbol in self.active_trailing_stops:
                del self.active_trailing_stops[signal.symbol]
            
            # Log successful exit
            logger.info(f"{GREEN}Successfully exited {signal.symbol} {signal.side} position{RESET}")
            logger.info(f"{GREEN}Exit Price: {current_price} | PnL: {position.get('unrealized_pnl', 0)}{RESET}")
            
            return True
            
        except Exception as e:
            logger.error(f"{RED}Error executing exit: {e}{RESET}")
            return False
    
    async def monitor_positions(self) -> None:
        """Monitor positions and execute exits when conditions are met."""
        while True:
            try:
                # Get current positions
                positions = await self.exchange.get_positions(self.symbol)
                
                for position in positions:
                    # Skip if no position size
                    if float(position.get('size', 0)) == 0:
                        continue
                    
                    # Get current price
                    ticker = await self.exchange.get_market_ticker(self.symbol)
                    current_price = float(ticker['last'])
                    
                    # Update trailing stop if enabled
                    if self.enable_trailing_stop:
                        stop_price = await self.update_trailing_stop(
                            self.symbol,
                            position,
                            current_price
                        )
                        
                        # Check if trailing stop was hit
                        if stop_price:
                            if position['side'] == 'long' and current_price <= stop_price:
                                # Create exit signal for trailing stop
                                signal = ExitSignal(
                                    symbol=self.symbol,
                                    side=position['side'],
                                    exit_price=current_price,
                                    stop_loss=stop_price,
                                    take_profit=float(position.get('take_profit', 0)),
                                    confidence=0.9,
                                    reasons=["Trailing stop hit"]
                                )
                                await self.execute_exit(signal, position)
                            elif position['side'] == 'short' and current_price >= stop_price:
                                # Create exit signal for trailing stop
                                signal = ExitSignal(
                                    symbol=self.symbol,
                                    side=position['side'],
                                    exit_price=current_price,
                                    stop_loss=stop_price,
                                    take_profit=float(position.get('take_profit', 0)),
                                    confidence=0.9,
                                    reasons=["Trailing stop hit"]
                                )
                                await self.execute_exit(signal, position)
                    
                    # Check for other exit opportunities
                    exit_signal = await self.analyze_exit_opportunity(position, current_price)
                    if exit_signal:
                        await self.execute_exit(exit_signal, position)
                
                # Sleep before next check
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"{RED}Error monitoring positions: {e}{RESET}")
                await asyncio.sleep(30)  # Longer sleep on error 