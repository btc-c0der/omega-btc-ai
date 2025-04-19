#!/usr/bin/env python3

"""
BitGet Position Analyzer Bot

This module implements the BitGet position analyzer bot that provides
position analysis, Fibonacci levels, and portfolio recommendations.

Copyright (c) 2024 OMEGA BTC AI
Licensed under the GBU2 License - see LICENSE file for details

This module provides position analysis and monitoring utilities for BitGet exchange.
It integrates with the trading analyzer architecture to provide a comprehensive
view of positions with Fibonacci-based analysis.
"""

import os
import json
import time
import logging
from typing import Dict, List, Tuple, Optional, Any, Union
from datetime import datetime
from decimal import Decimal

# Import quantum-secure logger
try:
    from src.omega_bot_farm.trading.b0ts.tests.quantum_secure_logger import get_quantum_logger
    logger = get_quantum_logger(app_name="bitget_position_analyzer_b0t")
    QUANTUM_LOGGING = True
except ImportError:
    logger = logging.getLogger("bitget_position_analyzer_b0t")
    QUANTUM_LOGGING = False
    logger.warning("Quantum-secure logger not available. Using standard logger.")

# Import the ExchangeService
try:
    from src.omega_bot_farm.trading.b0ts.exchanges.ccxt_b0t import ExchangeClientB0t
    EXCHANGE_SERVICE_AVAILABLE = True
except ImportError:
    logger.warning("Exchange service not available. Using mock data.")
    EXCHANGE_SERVICE_AVAILABLE = False
    ExchangeClientB0t = None  # Define as None to avoid unbound error

# Constants for Mathematical Harmony
PHI = 1.618034  # Golden Ratio - Divine Proportion
INV_PHI = 0.618034  # Inverse Golden Ratio
SCHUMANN_BASE = 7.83  # Earth's base frequency (Hz)

class Position:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return self.data

class PositionHistory:
    def __init__(self, timestamp: datetime, positions: List[Dict[str, Any]]):
        self.timestamp = timestamp
        self.positions = positions
        
    def __getitem__(self, key: str) -> Any:
        if key == 'timestamp':
            return self.timestamp
        elif key == 'positions':
            return self.positions
        raise KeyError(f"Key {key} not found in PositionHistory")

class BitgetPositionAnalyzerB0t:
    """
    BitGet Position Analyzer for Omega Bot Farm.
    
    This bot monitors and analyzes BitGet positions, providing insights based on
    Fibonacci ratios and position harmony. It integrates with the trading analyzer
    architecture to provide a comprehensive view of positions and trading opportunities.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_key = str(config.get('api_key', ''))
        self.api_secret = str(config.get('api_secret', ''))
        self.api_password = str(config.get('api_password', ''))
        self.use_testnet = bool(config.get('use_testnet', True))
        self.symbol = str(config.get('symbol', 'BTC/USDT'))
        self.positions: List[Position] = []
        self.position_history: List[PositionHistory] = []
        self.position_history_length = int(config.get('position_history_length', 10))
        
        # Exchange-related attributes
        self.exchange: Optional[Any] = None
        self.connection_method: Optional[str] = None
        self.exchange_service: Optional[Any] = None
        self.exchange_client_b0t: Optional[Any] = None
        
        # Account statistics
        self.account_balance: float = 0.0
        self.account_equity: float = 0.0
        self.total_position_value: float = 0.0
        self.total_pnl: float = 0.0
        self.long_exposure: float = 0.0
        self.short_exposure: float = 0.0
        
    async def analyze_positions(self) -> List[Dict[str, Any]]:
        try:
            if EXCHANGE_SERVICE_AVAILABLE and ExchangeClientB0t is not None:
                client = ExchangeClientB0t(
                    exchange_id='bitget',
                    api_key=self.api_key,
                    api_secret=self.api_secret,
                    api_password=self.api_password,
                    use_testnet=self.use_testnet,
                    symbol=self.symbol
                )
                await client.initialize()
                raw_positions = await client.fetch_positions()
                self.positions = [Position(pos) for pos in raw_positions]
                await client.close()
            else:
                # Mock data for testing
                self.positions = [
                    Position({"symbol": "BTC/USDT", "size": "0.1", "side": "long"}),
                    Position({"symbol": "ETH/USDT", "size": "1.0", "side": "short"})
                ]
            
            return [pos.to_dict() for pos in self.positions]
            
        except Exception as e:
            logger.error(f"Error analyzing positions: {str(e)}")
            return []
    
    async def get_positions(self) -> Dict[str, Any]:
        """
        Fetch current positions from BitGet exchange.
        
        Returns:
            Dict containing position data
        """
        if not self.exchange:
            return {
                "error": "Exchange client not initialized", 
                "positions": [],
                "connection": "NOT CONNECTED",
                "connection_attempts": getattr(self, 'connection_method', None)
            }
            
        try:
            # Handle positions fetch based on connection method
            positions = []
            
            # Fetch positions using the appropriate method
            if hasattr(self, 'connection_method') and self.connection_method:
                if self.connection_method == "ExchangeService" and self.exchange_service:
                    # Use exchange service async method
                    positions = await self.exchange_service.fetch_positions()
                    
                elif self.connection_method == "ExchangeClientB0t" and self.exchange_client_b0t:
                    # Use exchange client b0t async method if available
                    if hasattr(self.exchange_client_b0t, 'fetch_positions'):
                        positions = await self.exchange_client_b0t.fetch_positions()
                    else:
                        # Fall back to direct exchange call through the client
                        positions = self.exchange.fetch_positions()
                        
                elif self.connection_method == "CCXT direct":
                    # Direct exchange call
                    positions = self.exchange.fetch_positions()
            else:
                # No connection method was set, but we have an exchange object
                # Try direct call as last resort
                positions = self.exchange.fetch_positions()
            
            # Filter out positions with zero contracts and convert to appropriate type
            try:
                # Cast to List[Dict[str, Any]] to satisfy type checker
                active_positions: List[Dict[str, Any]] = [
                    {k: v for k, v in p.items()} if not isinstance(p, dict) else p 
                    for p in positions if float(p.get('contracts', 0)) > 0
                ]
            except Exception as e:
                logger.warning(f"Error processing positions data: {e}")
                # Fallback to safe conversion
                active_positions = []
                for p in positions:
                    try:
                        if float(p.get('contracts', 0)) > 0:
                            if isinstance(p, dict):
                                active_positions.append(p)
                            else:
                                active_positions.append({k: v for k, v in p.items()})
                    except Exception:
                        pass
            
            # Update position history
            self._update_position_history(active_positions)
            
            # Update account statistics
            await self._update_account_statistics(active_positions)
            
            # Detect changes from previous positions
            changes = self._detect_position_changes(active_positions)
            
            return {
                "success": True,
                "positions": active_positions,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "connection": f"CONNECTED TO BITGET{' TESTNET' if self.use_testnet else ' MAINNET'} via {self.connection_method or 'Unknown'}",
                "changes": changes,
                "account": {
                    "balance": self.account_balance,
                    "equity": self.account_equity,
                    "total_position_value": self.total_position_value,
                    "total_pnl": self.total_pnl,
                    "long_exposure": self.long_exposure,
                    "short_exposure": self.short_exposure,
                    "long_short_ratio": self._calculate_long_short_ratio(),
                    "exposure_to_equity_ratio": self._calculate_exposure_to_equity_ratio(),
                    "harmony_score": self._calculate_harmony_score()
                }
            }
            
        except Exception as e:
            logger.error(f"Error fetching positions: {e}")
            return {
                "error": str(e), 
                "positions": [],
                "connection": "ERROR FETCHING POSITIONS",
                "connection_method": getattr(self, 'connection_method', None)
            }
    
    def _update_position_history(self, positions: List[Dict[str, Any]]) -> None:
        """Update position history with new position data."""
        if positions:
            # Add current positions to history
            self.position_history.append(PositionHistory(
                timestamp=datetime.now(),
                positions=positions
            ))
            
            # Trim history if too long
            if len(self.position_history) > self.position_history_length:
                self.position_history = self.position_history[-self.position_history_length:]
    
    async def _update_account_statistics(self, positions: List[Dict[str, Any]]) -> None:
        """Update account statistics based on positions."""
        # Reset counters
        self.total_position_value = 0.0
        self.total_pnl = 0.0
        self.long_exposure = 0.0
        self.short_exposure = 0.0
        
        # Calculate totals
        for position in positions:
            notional_value = float(position.get('notional', 0.0))
            unrealized_pnl = float(position.get('unrealizedPnl', 0.0))
            side = str(position.get('side', '')).lower()
            
            self.total_position_value += notional_value
            self.total_pnl += unrealized_pnl
            
            if side == 'long':
                self.long_exposure += notional_value
            elif side == 'short':
                self.short_exposure += notional_value
        
        # Attempt to update account balance from exchange
        try:
            balance = None
            
            if EXCHANGE_SERVICE_AVAILABLE and ExchangeClientB0t is not None and self.exchange_client_b0t:
                balance = await self.exchange_client_b0t.fetch_balance()
            
            # Extract USDT balance if available
            if balance and isinstance(balance, dict):
                total = balance.get('total', {})
                if isinstance(total, dict) and 'USDT' in total:
                    self.account_balance = float(total['USDT'])
            
            # Calculate equity
            self.account_equity = self.account_balance + self.total_pnl
            
        except Exception as e:
            logger.warning(f"Could not fetch account balance: {e}")
            # Use last known balance plus PnL as a fallback
            self.account_equity = self.account_balance + self.total_pnl
    
    def _detect_position_changes(self, current_positions: List[Dict]) -> Dict[str, List]:
        """
        Detect changes between current and previous positions.
        
        Returns:
            Dict with new, closed, and changed positions
        """
        changes = {
            "new": [],
            "closed": [],
            "changed": []
        }
        
        # Can't detect changes if we don't have history
        if len(self.position_history) < 2:
            return changes
            
        # Get previous positions
        previous_positions = self.position_history[-2]["positions"]
        
        # Find position symbols
        current_symbols = {p.get('symbol'): p for p in current_positions}
        prev_symbols = {p.get('symbol'): p for p in previous_positions}
        
        # Detect new positions
        for symbol, position in current_symbols.items():
            if symbol not in prev_symbols:
                changes["new"].append(position)
            else:
                # Check if position size or PnL changed significantly
                prev_pos = prev_symbols[symbol]
                curr_contracts = float(position.get('contracts', 0))
                prev_contracts = float(prev_pos.get('contracts', 0))
                curr_pnl = float(position.get('unrealizedPnl', 0))
                prev_pnl = float(prev_pos.get('unrealizedPnl', 0))
                
                # Detect significant changes (>5% position size or >10% PnL)
                if abs(curr_contracts - prev_contracts) / max(prev_contracts, 1) > 0.05 or \
                   (prev_pnl != 0 and abs(curr_pnl - prev_pnl) / abs(prev_pnl) > 0.1):
                    changes["changed"].append({
                        "current": position,
                        "previous": prev_pos,
                        "contracts_change": curr_contracts - prev_contracts,
                        "pnl_change": curr_pnl - prev_pnl
                    })
        
        # Detect closed positions
        for symbol, position in prev_symbols.items():
            if symbol not in current_symbols:
                changes["closed"].append(position)
        
        return changes
    
    def _calculate_long_short_ratio(self) -> float:
        """Calculate long to short exposure ratio."""
        if self.short_exposure == 0:
            return float('inf') if self.long_exposure > 0 else 0
        return self.long_exposure / self.short_exposure
    
    def _calculate_exposure_to_equity_ratio(self) -> float:
        """Calculate total exposure to equity ratio."""
        if self.account_equity == 0:
            return 0
        return self.total_position_value / max(self.account_equity, 1.0)
    
    def _calculate_harmony_score(self) -> float:
        """
        Calculate position harmony score based on Fibonacci principles.
        
        Returns:
            Score between 0.0 (disharmonious) and 1.0 (perfect harmony)
        """
        # Base harmony score
        harmony = 0.5
        
        # Factors that contribute to harmony
        
        # 1. Long-short balance (ideally near PHI ratio)
        long_short_ratio = self._calculate_long_short_ratio()
        if 0 < long_short_ratio < float('inf'):
            # How close is the ratio to PHI or its inverse?
            ls_harmony = min(
                abs(long_short_ratio - PHI),
                abs(long_short_ratio - INV_PHI)
            ) / PHI
            harmony += (0.2 - ls_harmony) if ls_harmony < 0.2 else 0
        
        # 2. Exposure level (ideally near INV_PHI of equity)
        exp_ratio = self._calculate_exposure_to_equity_ratio()
        exp_harmony = abs(exp_ratio - INV_PHI) / INV_PHI
        harmony += (0.2 - exp_harmony) if exp_harmony < 0.2 else 0
        
        # 3. PnL contribution (positive PnL contributes to harmony)
        if self.total_position_value > 0:
            pnl_ratio = self.total_pnl / self.total_position_value
            harmony += 0.2 if pnl_ratio > 0 else -0.2
        
        # Constrain to valid range
        return max(0.0, min(1.0, harmony))
    
    def generate_fibonacci_levels(self, base_price: float, side: str) -> Dict[str, float]:
        """
        Generate Fibonacci retracement and extension levels from a base price.
        
        Args:
            base_price: Base price to calculate levels from
            side: Position side ('long' or 'short')
            
        Returns:
            Dict of Fibonacci levels
        """
        if side.lower() == 'long':
            # Long position - levels above base price
            levels = {
                "0.0%": base_price,
                "23.6%": base_price * (1 + 0.236),
                "38.2%": base_price * (1 + 0.382),
                "50.0%": base_price * (1 + 0.5),
                "61.8%": base_price * (1 + 0.618),  # Golden Ratio
                "78.6%": base_price * (1 + 0.786),
                "100.0%": base_price * 2,
                "161.8%": base_price * (1 + 1.618),  # Golden Ratio
                "261.8%": base_price * (1 + 2.618)   # PHI^3
            }
        else:
            # Short position - levels below base price
            levels = {
                "0.0%": base_price,
                "23.6%": base_price * (1 - 0.236),
                "38.2%": base_price * (1 - 0.382),
                "50.0%": base_price * (1 - 0.5),
                "61.8%": base_price * (1 - 0.618),  # Golden Ratio
                "78.6%": base_price * (1 - 0.786),
                "100.0%": base_price * 0,  # Zero
                "161.8%": None,  # Not applicable for shorts
                "261.8%": None   # Not applicable for shorts
            }
        
        return levels
    
    def analyze_position(self, position: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single position with Fibonacci levels and harmony metrics.
        
        Args:
            position: Position data from exchange
            
        Returns:
            Dict containing position analysis
        """
        try:
            # Extract position details
            symbol = position.get('symbol', '')
            side = position.get('side', '').lower()
            contracts = float(position.get('contracts', 0))
            notional = float(position.get('notional', 0))
            entry_price = float(position.get('entryPrice', 0))
            mark_price = float(position.get('markPrice', 0))
            unrealized_pnl = float(position.get('unrealizedPnl', 0))
            
            # Calculate PnL percentage
            pnl_percentage = (unrealized_pnl / notional) * 100 if notional > 0 else 0
            
            # Generate Fibonacci levels for take profit and stop loss
            fib_levels = self.generate_fibonacci_levels(entry_price, side)
            
            # Calculate distance to each level as percentage
            level_distances = {}
            for level_name, level_price in fib_levels.items():
                if level_price is not None:
                    if side == 'long':
                        distance_pct = ((level_price - mark_price) / mark_price) * 100
                    else:
                        distance_pct = ((mark_price - level_price) / mark_price) * 100
                    level_distances[level_name] = distance_pct
            
            # Determine if position is in harmony with Fibonacci principles
            # (e.g., position size follows Fibonacci ratio of account)
            position_ratio = notional / max(self.account_equity, 1.0)
            is_fib_size = 0.5 < position_ratio < 0.7  # Close to 0.618 (golden ratio)
            
            # Determine best Fibonacci-based take profit and stop loss levels
            take_profit_levels = []
            stop_loss_levels = []
            
            if side == 'long':
                # For longs, take profit above, stop loss below
                for level, price in fib_levels.items():
                    if price is not None and price > mark_price:
                        take_profit_levels.append((level, price))
                    elif price is not None and price < mark_price:
                        stop_loss_levels.append((level, price))
            else:
                # For shorts, take profit below, stop loss above
                for level, price in fib_levels.items():
                    if price is not None and price < mark_price:
                        take_profit_levels.append((level, price))
                    elif price is not None and price > mark_price:
                        stop_loss_levels.append((level, price))
            
            # Sort levels by proximity to current price
            take_profit_levels.sort(key=lambda x: abs(x[1] - mark_price))
            stop_loss_levels.sort(key=lambda x: abs(x[1] - mark_price))
            
            # Recommended take profit and stop loss based on golden ratio
            recommended_tp = None
            recommended_sl = None
            
            if take_profit_levels:
                # Prefer the 61.8% level for take profit if available
                for level, price in take_profit_levels:
                    if "61.8%" in level:
                        recommended_tp = (level, price)
                        break
                if recommended_tp is None:
                    recommended_tp = take_profit_levels[0]
            
            if stop_loss_levels:
                # Prefer the 38.2% level for stop loss if available
                for level, price in stop_loss_levels:
                    if "38.2%" in level:
                        recommended_sl = (level, price)
                        break
                if recommended_sl is None and stop_loss_levels:
                    recommended_sl = stop_loss_levels[0]
            
            return {
                "position": position,
                "analysis": {
                    "fibonacci_levels": fib_levels,
                    "level_distances": level_distances,
                    "is_fibonacci_sized": is_fib_size,
                    "pnl_percentage": pnl_percentage,
                    "recommended_take_profit": recommended_tp,
                    "recommended_stop_loss": recommended_sl,
                    "current_harmony": self._calculate_position_harmony(position)
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing position: {e}")
            return {"position": position, "analysis": {"error": str(e)}}
    
    def _calculate_position_harmony(self, position: Dict[str, Any]) -> float:
        """
        Calculate harmony score for an individual position.
        
        Args:
            position: Position data from exchange
            
        Returns:
            Harmony score between 0.0 and 1.0
        """
        try:
            # Extract position details
            contracts = float(position.get('contracts', 0))
            notional = float(position.get('notional', 0))
            leverage = float(position.get('leverage', 1))
            unrealized_pnl = float(position.get('unrealizedPnl', 0))
            
            # Base harmony score
            harmony = 0.5
            
            # 1. Position size relative to account (ideally INV_PHI)
            position_size_ratio = notional / max(self.account_equity, 1.0)
            size_harmony = abs(position_size_ratio - INV_PHI) / INV_PHI
            harmony += (0.2 - size_harmony) if size_harmony < 0.2 else 0
            
            # 2. Leverage harmony (ideally near Fibonacci numbers: 1, 2, 3, 5, 8, 13, 21)
            fib_numbers = [1, 2, 3, 5, 8, 13, 21]
            leverage_harmony = min([abs(leverage - fib) for fib in fib_numbers]) / 5
            harmony += (0.15 - leverage_harmony) if leverage_harmony < 0.15 else 0
            
            # 3. PnL contribution
            if notional > 0:
                pnl_ratio = unrealized_pnl / notional
                harmony += 0.15 if pnl_ratio > 0 else -0.15
            
            # Constrain to valid range
            return max(0.0, min(1.0, harmony))
            
        except Exception as e:
            logger.error(f"Error calculating position harmony: {e}")
            return 0.5  # Default to neutral harmony on error
    
    def analyze_all_positions(self) -> Dict[str, Any]:
        """
        Analyze all current positions.
        
        Returns:
            Dict containing analysis of all positions
        """
        try:
            # Get current positions (handle as a sync operation for simplicity)
            positions_data = self.get_positions()
            
            # Since get_positions is now async, we need to handle it synchronously here
            # This is a simplified approach - in production, use asyncio.run or similar
            
            # If it's a coroutine (when using exchange_service), run it manually
            import asyncio
            if asyncio.iscoroutine(positions_data):
                loop = asyncio.get_event_loop()
                positions_data = loop.run_until_complete(positions_data)
            
            if "error" in positions_data:
                return positions_data
                
            positions = positions_data.get("positions", [])
            
            # Analyze each position
            analyses = []
            for position in positions:
                analyses.append(self.analyze_position(position))
            
            # Calculate overall portfolio harmony
            harmony_score = self._calculate_harmony_score()
            
            # Generate portfolio recommendations
            recommendations = self._generate_portfolio_recommendations(positions, harmony_score)
            
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_positions": len(positions),
                "account_stats": positions_data.get("account", {}),
                "position_analyses": analyses,
                "harmony_score": harmony_score,
                "recommendations": recommendations,
                "changes": positions_data.get("changes", {})
            }
            
        except Exception as e:
            logger.error(f"Error analyzing positions: {e}")
            return {"error": str(e)}
    
    def _generate_portfolio_recommendations(self, positions: List[Dict], harmony_score: float) -> List[str]:
        """
        Generate portfolio recommendations based on position analysis.
        
        Args:
            positions: List of positions
            harmony_score: Overall harmony score
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Check if we have positions
        if not positions:
            recommendations.append("No open positions. Consider opening positions at Fibonacci retracement levels of major market movements.")
            return recommendations
        
        # Check overall harmony
        if harmony_score < 0.4:
            recommendations.append("Portfolio harmony is low. Consider rebalancing positions to improve Fibonacci alignment.")
        elif harmony_score > 0.7:
            recommendations.append("Portfolio has good Fibonacci harmony. Maintain current balance.")
        
        # Check long-short ratio
        long_short_ratio = self._calculate_long_short_ratio()
        if 0 < long_short_ratio < float('inf'):
            if abs(long_short_ratio - PHI) > 0.5 and abs(long_short_ratio - INV_PHI) > 0.5:
                if long_short_ratio > PHI:
                    recommendations.append(f"Long exposure ({long_short_ratio:.2f}x short) exceeds golden ratio. Consider reducing long positions.")
                elif long_short_ratio < INV_PHI:
                    recommendations.append(f"Short exposure ({1/long_short_ratio:.2f}x long) exceeds golden ratio. Consider reducing short positions.")
        elif long_short_ratio == float('inf'):
            recommendations.append("Portfolio is 100% long. Consider adding short positions for balance.")
        elif long_short_ratio == 0:
            recommendations.append("Portfolio is 100% short. Consider adding long positions for balance.")
        
        # Check exposure level
        exposure_ratio = self._calculate_exposure_to_equity_ratio()
        if exposure_ratio > 2.0:
            recommendations.append(f"Total exposure ({exposure_ratio:.2f}x equity) is high. Consider reducing position sizes.")
        elif exposure_ratio < 0.3:
            recommendations.append(f"Total exposure ({exposure_ratio:.2f}x equity) is low. Consider increasing position sizes.")
        
        # Individual position recommendations
        for position in positions:
            symbol = position.get('symbol', '')
            side = position.get('side', '').lower()
            unrealized_pnl = float(position.get('unrealizedPnl', 0))
            notional = float(position.get('notional', 0))
            
            # Check for positions with significant losses
            if notional > 0 and unrealized_pnl < 0 and abs(unrealized_pnl) / notional > 0.1:
                recommendations.append(f"Consider closing or reducing {symbol} {side} position with {abs(unrealized_pnl/notional)*100:.1f}% loss.")
            
            # Check for positions with significant gains
            if notional > 0 and unrealized_pnl > 0 and unrealized_pnl / notional > 0.2:
                recommendations.append(f"Consider taking profit on {symbol} {side} position with {unrealized_pnl/notional*100:.1f}% gain.")
        
        return recommendations

def main(config: Dict[str, Any]) -> None:
    """
    Initialize and run the BitGet position analyzer bot.
    
    Args:
        config: Configuration dictionary with API credentials and settings
    """
    try:
        bot = BitgetPositionAnalyzerB0t(config=config)
        logger.info("BitGet position analyzer bot initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize BitGet position analyzer bot: {e}")

if __name__ == "__main__":
    # Example configuration
    example_config = {
        "api_key": "",  # Will use environment variable if not provided
        "api_secret": "",  # Will use environment variable if not provided
        "api_password": "",  # Will use environment variable if not provided
        "use_testnet": True,
        "symbol": "BTC/USDT",
        "position_history_length": 10
    }
    main(config=example_config) 