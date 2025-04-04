#!/usr/bin/env python3

"""
BitGet Position Analyzer for Omega Bot Farm

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

# Import quantum-secure logger
try:
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.tests.quantum_secure_logger import get_quantum_logger
    logger = get_quantum_logger(app_name="bitget_position_analyzer_b0t")
    QUANTUM_LOGGING = True
except ImportError:
    logger = logging.getLogger("bitget_position_analyzer_b0t")
    QUANTUM_LOGGING = False

# Import the ExchangeService
try:
    from src.omega_bot_farm.services.exchange_service import ExchangeService, create_exchange_service
    EXCHANGE_SERVICE_AVAILABLE = True
except ImportError:
    EXCHANGE_SERVICE_AVAILABLE = False
    create_exchange_service = None  # Define as None to avoid unbound error
    logging.warning("ExchangeService not available. Using direct CCXT if available.")
    # Try to import ccxt for exchange API access as fallback
    try:
        import ccxt
        CCXT_AVAILABLE = True
    except ImportError:
        CCXT_AVAILABLE = False
        logging.warning("ccxt module not installed. BitGet position analysis will be limited.")

# Import ExchangeClientB0t as additional option
try:
    from src.omega_bot_farm.trading.exchanges.ccxt_b0t import ExchangeClientB0t
    EXCHANGE_CLIENT_B0T_AVAILABLE = True
except ImportError:
    EXCHANGE_CLIENT_B0T_AVAILABLE = False
    ExchangeClientB0t = None  # Define as None to avoid unbound error
    logging.warning("ExchangeClientB0t not available. Will try other connection methods.")

# Constants for Mathematical Harmony
PHI = 1.618034  # Golden Ratio - Divine Proportion
INV_PHI = 0.618034  # Inverse Golden Ratio
SCHUMANN_BASE = 7.83  # Earth's base frequency (Hz)

class BitgetPositionAnalyzerB0t:
    """
    BitGet Position Analyzer for Omega Bot Farm.
    
    This bot monitors and analyzes BitGet positions, providing insights based on
    Fibonacci ratios and position harmony. It integrates with the trading analyzer
    architecture to provide a comprehensive view of positions and trading opportunities.
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 api_secret: Optional[str] = None,
                 api_passphrase: Optional[str] = None,
                 use_testnet: bool = False,
                 position_history_length: int = 10):
        """
        Initialize the BitGet Position Analyzer bot.
        
        Args:
            api_key: BitGet API key (will use env var BITGET_API_KEY if None)
            api_secret: BitGet API secret (will use env var BITGET_SECRET_KEY if None)
            api_passphrase: BitGet API passphrase (will use env var BITGET_PASSPHRASE if None)
            use_testnet: Whether to use BitGet testnet
            position_history_length: Number of position snapshots to keep in history
        """
        # Check if our environment loader is available
        try:
            # Import with absolute path to avoid relative import issues
            from src.omega_bot_farm.utils.env_loader import get_env_var, get_bool_env_var, get_int_env_var
            # Load API credentials from environment with loader
            self.api_key = api_key or get_env_var("BITGET_API_KEY", "")
            self.api_secret = api_secret or get_env_var("BITGET_SECRET_KEY", "")
            self.api_passphrase = api_passphrase or get_env_var("BITGET_PASSPHRASE", "")
            self.use_testnet = use_testnet if use_testnet is not None else get_bool_env_var("USE_TESTNET", False)
            history_length = position_history_length or get_int_env_var("POSITION_HISTORY_LENGTH", 10)
        except ImportError:
            # Fall back to standard os.environ if loader not available
            self.api_key = api_key or os.environ.get("BITGET_API_KEY", "")
            self.api_secret = api_secret or os.environ.get("BITGET_SECRET_KEY", "")
            self.api_passphrase = api_passphrase or os.environ.get("BITGET_PASSPHRASE", "")
            self.use_testnet = use_testnet
            history_length = position_history_length
        
        # Position tracking
        self.position_history = []
        self.position_history_length = history_length
        
        # Exchange service or client
        self.exchange_service = None
        self.exchange = None
        
        # Initialize exchange service or direct ccxt client
        self._initialize_exchange()
        
        # Account statistics
        self.account_balance = 0.0
        self.account_equity = 0.0
        self.total_position_value = 0.0
        self.total_pnl = 0.0
        self.long_exposure = 0.0
        self.short_exposure = 0.0
        
        logger.info(f"BitgetPositionAnalyzerB0t initialized. Exchange service available: {EXCHANGE_SERVICE_AVAILABLE}")
    
    def _initialize_exchange(self) -> None:
        """Initialize the exchange service, CCXT client, or ExchangeClientB0t."""
        # Keep track of connection attempts
        connection_methods_tried = []
        
        # Initialize attributes to avoid unbound errors
        self.connection_method = None
        self.exchange_client_b0t = None
        
        # 1. Try using direct CCXT as the primary option
        if CCXT_AVAILABLE:
            try:
                connection_methods_tried.append("CCXT direct")
                logger.info("Attempting to connect via direct CCXT (primary method)...")
                
                if not self.api_key or not self.api_secret or not self.api_passphrase:
                    logger.error("Cannot initialize exchange: Missing API credentials")
                    # Continue to other methods rather than returning
                else:
                    # Import ccxt here to avoid unbound error
                    import ccxt
                    
                    # Use regular dict instead of typed Dict to avoid type mismatch
                    exchange_config = {
                        'apiKey': self.api_key,
                        'secret': self.api_secret,
                        'password': self.api_passphrase,
                        'options': {
                            'defaultType': 'swap',
                            'adjustForTimeDifference': True,
                            'testnet': self.use_testnet,
                        }
                    }
                    
                    self.exchange = ccxt.bitget(exchange_config)
                    
                    if self.use_testnet:
                        self.exchange.set_sandbox_mode(True)
                        logger.info("Connected to BitGet TESTNET via direct CCXT")
                    else:
                        logger.info("Connected to BitGet MAINNET via direct CCXT")
                    
                    self.connection_method = "CCXT direct"
                    return
            except Exception as e:
                logger.error(f"Failed to initialize BitGet exchange via CCXT direct: {e}")
                self.exchange = None
        
        # 2. Try using ExchangeClientB0t if available
        if EXCHANGE_CLIENT_B0T_AVAILABLE and ExchangeClientB0t is not None:
            try:
                connection_methods_tried.append("ExchangeClientB0t")
                logger.info("Attempting to connect via ExchangeClientB0t (fallback 1)...")
                
                exchange_client = ExchangeClientB0t(
                    exchange_id="bitget",
                    api_key=self.api_key,
                    api_secret=self.api_secret,
                    api_password=self.api_passphrase,
                    use_testnet=self.use_testnet
                )
                
                # Check if initialization was successful
                if hasattr(exchange_client, 'exchange') and exchange_client.exchange:
                    logger.info(f"Connected to BitGet {'TESTNET' if self.use_testnet else 'MAINNET'} via ExchangeClientB0t")
                    self.exchange = exchange_client.exchange
                    self.exchange_client_b0t = exchange_client
                    self.connection_method = "ExchangeClientB0t"
                    return
                else:
                    logger.warning("Failed to initialize exchange via ExchangeClientB0t")
            except Exception as e:
                logger.error(f"Error initializing ExchangeClientB0t: {e}")
                self.exchange_client_b0t = None
                self.exchange = None

        # 3. Try using the ExchangeService if available as last resort
        if EXCHANGE_SERVICE_AVAILABLE and create_exchange_service is not None:
            try:
                connection_methods_tried.append("ExchangeService")
                logger.info("Attempting to connect via ExchangeService (fallback 2)...")
                
                self.exchange_service = create_exchange_service(
                    exchange_id="bitget",
                    api_key=self.api_key,
                    api_secret=self.api_secret,
                    api_passphrase=self.api_passphrase,
                    use_testnet=self.use_testnet
                )
                
                # Get the underlying exchange client
                self.exchange = self.exchange_service.get_exchange_client()
                
                if self.exchange:
                    logger.info(f"Connected to BitGet {'TESTNET' if self.use_testnet else 'MAINNET'} via ExchangeService")
                    self.connection_method = "ExchangeService"
                    return
                else:
                    logger.warning("Failed to initialize exchange via ExchangeService")
            except Exception as e:
                logger.error(f"Error initializing ExchangeService: {e}")
                self.exchange_service = None
                self.exchange = None
        
        # Add back the error message for when all connection methods fail
        # This should be at the end of the _initialize_exchange method
        # If we get here, all connection methods failed
        logger.error(f"All connection methods failed: {', '.join(connection_methods_tried)}")
        logger.error("Cannot initialize exchange: Neither CCXT direct, ExchangeClientB0t, nor ExchangeService worked")
    
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
    
    def _update_position_history(self, positions: List[Dict]) -> None:
        """Update position history with new position data."""
        if len(positions) > 0:
            # Add current positions to history
            self.position_history.append({
                "timestamp": datetime.now(),
                "positions": positions
            })
            
            # Trim history if too long
            if len(self.position_history) > self.position_history_length:
                self.position_history = self.position_history[-self.position_history_length:]
    
    async def _update_account_statistics(self, positions: List[Dict]) -> None:
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
            side = position.get('side', '').lower()
            
            self.total_position_value += notional_value
            self.total_pnl += unrealized_pnl
            
            if side == 'long':
                self.long_exposure += notional_value
            elif side == 'short':
                self.short_exposure += notional_value
        
        # Attempt to update account balance from exchange
        try:
            balance = None
            
            # Use the appropriate method based on connection type
            if hasattr(self, 'connection_method') and self.connection_method:
                if self.connection_method == "ExchangeService" and self.exchange_service:
                    # Use exchange service async method
                    balance = await self.exchange_service.fetch_balance()
                    
                elif self.connection_method == "ExchangeClientB0t" and self.exchange_client_b0t:
                    # Use exchange client b0t async method if available
                    if hasattr(self.exchange_client_b0t, 'fetch_balance'):
                        balance = await self.exchange_client_b0t.fetch_balance()
                    else:
                        # Fall back to direct exchange call
                        balance = self.exchange.fetch_positions() if self.exchange else None
                        
                elif self.connection_method == "CCXT direct" and self.exchange:
                    # Direct exchange call
                    balance = self.exchange.fetch_balance()
            elif self.exchange:
                # No connection method was set, try direct call
                balance = self.exchange.fetch_balance()
            
            # Extract USDT balance if available
            if balance and isinstance(balance, dict):
                # Safely access balance properties
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

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Create analyzer
        analyzer = BitgetPositionAnalyzerB0t()
        
        # Get and analyze positions
        analysis = analyzer.analyze_all_positions()
        
        # Print analysis results
        print(json.dumps(analysis, indent=2))
    
    # Run the main function
    asyncio.run(main()) 