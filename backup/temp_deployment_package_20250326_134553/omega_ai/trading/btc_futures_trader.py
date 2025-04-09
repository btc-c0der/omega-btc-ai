#!/usr/bin/env python3

"""
BTC Futures Trading Simulator
============================

This module simulates a fully automated trading system for BTC futures contracts
based on signals from OmegaBTC's market analysis algorithms. It integrates with
existing Fibonacci pattern detection, MM trap identification, and multi-timeframe
trend analysis to make trading decisions.

Features
--------
1. Automated Strategy Execution:
   - Opens/closes long and short positions based on market signals
   - Integrates with Fibonacci levels for entry/exit targets
   - Uses MM trap detection to avoid manipulation events
   - Leverages multi-timeframe trend analysis for directional bias

2. Risk Management:
   - Dynamic position sizing based on volatility
   - Automatic stop-loss placement
   - Multiple take-profit targets with partial exits
   - Maximum drawdown protection

3. Performance Analytics:
   - Real-time profit/loss tracking (% and absolute)
   - Trade history with win/loss statistics
   - Drawdown analysis
   - Correlation with market regimes

4. Trade Visualization:
   - Entry/exit points with rationale
   - Take-profit and stop-loss levels
   - Real-time position status updates
   - Performance charts
"""

import datetime
import time
import json
import uuid
import numpy as np
import redis
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Union
from decimal import Decimal
import pandas as pd

from omega_ai.algos.omega_algorithms import OmegaAlgo
from omega_ai.db_manager.database import fetch_recent_movements
from omega_ai.trading.trading_analyzer import TradingAnalyzer
from omega_ai.trading.trade_simulation import simulate_trade_outcome, simulate_strategic_trade_outcome

# Terminal colors for visual output
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
BRIGHT_GREEN = "\033[96m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
GOLD = "\033[93m"
YELLOW = "\033[93m"
LIGHT_ORANGE = "\033[38;5;214m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BLACK_BG = "\033[40m"
BLUE_BG = "\033[44m"
GREEN_BG = "\033[42m"
RED_BG = "\033[41m"
YELLOW_BG = "\033[43m"
BOLD = "\033[1m"

# Redis connection
redis_conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# ======= Data Models =======

@dataclass
class Position:
    """Trading position data model."""
    id: str
    direction: str  # "LONG" or "SHORT"
    entry_price: float
    size: float  # In BTC
    leverage: int
    entry_time: datetime.datetime
    entry_reason: str
    exit_price: Optional[float] = None
    exit_time: Optional[datetime.datetime] = None
    exit_reason: Optional[str] = None
    take_profits: List[Dict[str, float]] = field(default_factory=list)
    stop_loss: Optional[float] = None
    realized_pnl: float = 0.0
    status: str = "OPEN"  # OPEN, CLOSED, LIQUIDATED
    
    def calculate_unrealized_pnl(self, current_price: float) -> Tuple[float, float]:
        """Calculate unrealized profit/loss in USD and percentage."""
        if self.direction == "LONG":
            pnl_pct = (current_price - self.entry_price) / self.entry_price * 100 * self.leverage
            pnl_usd = (current_price - self.entry_price) * self.size * self.leverage
        else:  # SHORT
            pnl_pct = (self.entry_price - current_price) / self.entry_price * 100 * self.leverage
            pnl_usd = (self.entry_price - current_price) * self.size * self.leverage
        
        return pnl_usd, pnl_pct
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        result = asdict(self)
        # Convert datetime objects to ISO format
        result['entry_time'] = self.entry_time.isoformat()
        if self.exit_time:
            result['exit_time'] = self.exit_time.isoformat()
        return result

@dataclass
class TradeHistory:
    """Trade history containing all closed positions."""
    trades: List[Position] = field(default_factory=list)
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    total_pnl: float = 0.0
    win_rate: float = 0.0
    average_win: float = 0.0
    average_loss: float = 0.0
    largest_win: float = 0.0
    largest_loss: float = 0.0
    
    def add_trade(self, position: Position) -> None:
        """Add a closed trade to history and update statistics."""
        self.trades.append(position)
        self.total_trades += 1
        
        if position.realized_pnl > 0:
            self.winning_trades += 1
            self.largest_win = max(self.largest_win, position.realized_pnl)
        else:
            self.losing_trades += 1
            self.largest_loss = min(self.largest_loss, position.realized_pnl)
        
        self.total_pnl += position.realized_pnl
        self.win_rate = (self.winning_trades / self.total_trades) if self.total_trades > 0 else 0
        
        # Calculate average win/loss
        wins = [t.realized_pnl for t in self.trades if t.realized_pnl > 0]
        losses = [t.realized_pnl for t in self.trades if t.realized_pnl <= 0]
        
        self.average_win = sum(wins) / len(wins) if wins else 0
        self.average_loss = sum(losses) / len(losses) if losses else 0

# ======= Trading Strategy Logic =======

class BtcFuturesTrader:
    """BTC Futures Trading Simulator."""
    
    def __init__(self, 
                 initial_capital: float = 10000.0,
                 max_leverage: int = 5,
                 risk_per_trade: float = 0.02,  # % of capital to risk per trade
                 max_positions: int = 3,
                 api_key: str = None,
                 api_secret: str = None,
                 **kwargs):
        """Initialize the trader with config parameters."""
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.max_leverage = max_leverage
        self.risk_per_trade = risk_per_trade
        self.max_positions = max_positions
        
        self.open_positions: List[Position] = []
        self.trade_history = TradeHistory()
        self.current_price = kwargs.get('btc_last_price', 1.0) if kwargs.get('btc_last_price', 1.0) > 0 else 1.0
        
        # Internal state tracking
        self.last_analysis_time = datetime.datetime.min
        self.analysis_cooldown = 60  # seconds between full analyses
        self.last_market_bias = None
        
        # Initialize trading analyzer
        self.analyzer = TradingAnalyzer(debug_mode=True)
        
        # Initialize Binance client
        from binance.client import Client
        self.client = Client(api_key, api_secret)
        
        # Initialize logger
        import logging
        self.logger = logging.getLogger(__name__)
    
    def get_historical_data(self,
                          symbol: str,
                          interval: str,
                          start_time: datetime.datetime,
                          end_time: datetime.datetime) -> pd.DataFrame:
        """
        Fetch historical klines data from Binance Futures.
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            interval (str): Kline interval (e.g., '1h', '4h', '1d')
            start_time (datetime): Start time for historical data
            end_time (datetime): End time for historical data
            
        Returns:
            pd.DataFrame: DataFrame with historical data
        """
        try:
            # Convert datetime to milliseconds timestamp
            start_ms = int(start_time.timestamp() * 1000)
            end_ms = int(end_time.timestamp() * 1000)
            
            # Fetch klines data
            klines = self.client.futures_klines(
                symbol=symbol,
                interval=interval,
                startTime=start_ms,
                endTime=end_ms
            )
            
            # Return empty DataFrame if no data
            if not klines:
                return pd.DataFrame(columns=[
                    'timestamp', 'open', 'high', 'low', 'close', 'volume',
                    'close_time', 'quote_volume', 'trades', 'taker_buy_volume',
                    'taker_buy_quote_volume', 'ignore'
                ])
            
            # Convert to DataFrame
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'trades', 'taker_buy_volume',
                'taker_buy_quote_volume', 'ignore'
            ])
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Convert string values to float
            float_columns = ['open', 'high', 'low', 'close', 'volume', 'quote_volume',
                           'taker_buy_volume', 'taker_buy_quote_volume']
            for col in float_columns:
                df[col] = df[col].astype(float)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching historical data: {e}")
            # Return empty DataFrame on error
            return pd.DataFrame(columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'trades', 'taker_buy_volume',
                'taker_buy_quote_volume', 'ignore'
            ])
    
    def load_state(self, filename: str = "trader_state.json") -> bool:
        """Load trader state from file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            self.capital = data.get('capital', self.initial_capital)
            
            # Load open positions
            for pos_data in data.get('open_positions', []):
                pos = Position(
                    id=pos_data['id'],
                    direction=pos_data['direction'],
                    entry_price=pos_data['entry_price'],
                    size=pos_data['size'],
                    leverage=pos_data['leverage'],
                    entry_time=datetime.datetime.fromisoformat(pos_data['entry_time']),
                    entry_reason=pos_data['entry_reason'],
                    take_profits=pos_data.get('take_profits', []),
                    stop_loss=pos_data.get('stop_loss')
                )
                self.open_positions.append(pos)
            
            # Load trade history
            history_data = data.get('trade_history', {})
            self.trade_history.total_trades = history_data.get('total_trades', 0)
            self.trade_history.winning_trades = history_data.get('winning_trades', 0)
            self.trade_history.losing_trades = history_data.get('losing_trades', 0)
            self.trade_history.total_pnl = history_data.get('total_pnl', 0.0)
            self.trade_history.win_rate = history_data.get('win_rate', 0.0)
            self.trade_history.average_win = history_data.get('average_win', 0.0)
            self.trade_history.average_loss = history_data.get('average_loss', 0.0)
            self.trade_history.largest_win = history_data.get('largest_win', 0.0)
            self.trade_history.largest_loss = history_data.get('largest_loss', 0.0)
            
            for trade_data in history_data.get('trades', []):
                trade = Position(
                    id=trade_data['id'],
                    direction=trade_data['direction'],
                    entry_price=trade_data['entry_price'],
                    size=trade_data['size'],
                    leverage=trade_data['leverage'],
                    entry_time=datetime.datetime.fromisoformat(trade_data['entry_time']),
                    entry_reason=trade_data['entry_reason'],
                    exit_price=trade_data.get('exit_price'),
                    exit_time=datetime.datetime.fromisoformat(trade_data['exit_time']) if trade_data.get('exit_time') else None,
                    exit_reason=trade_data.get('exit_reason'),
                    realized_pnl=trade_data.get('realized_pnl', 0.0),
                    status=trade_data.get('status', 'CLOSED')
                )
                self.trade_history.trades.append(trade)
            
            print(f"{GREEN}✅ Trader state loaded from {filename}{RESET}")
            return True
            
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"{YELLOW}⚠️ No saved state found or invalid format. Starting fresh.{RESET}")
            return False
    
    def save_state(self, filename: str = "trader_state.json") -> None:
        """Save trader state to file."""
        data = {
            'capital': self.capital,
            'open_positions': [pos.to_dict() for pos in self.open_positions],
            'trade_history': {
                'trades': [trade.to_dict() for trade in self.trade_history.trades],
                'total_trades': self.trade_history.total_trades,
                'winning_trades': self.trade_history.winning_trades,
                'losing_trades': self.trade_history.losing_trades,
                'total_pnl': self.trade_history.total_pnl,
                'win_rate': self.trade_history.win_rate,
                'average_win': self.trade_history.average_win,
                'average_loss': self.trade_history.average_loss,
                'largest_win': self.trade_history.largest_win,
                'largest_loss': self.trade_history.largest_loss
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"{GREEN}✅ Trader state saved to {filename}{RESET}")
    
    def update_current_price(self) -> float:
        """Get latest BTC price from Redis."""
        try:
            price_str = redis_conn.get("last_btc_price")
            if price_str:
                self.current_price = float(price_str)
                return self.current_price
            return 0.0
        except Exception as e:
            print(f"{RED}❌ Error getting current price: {e}{RESET}")
            return 0.0
    
    def calculate_position_size(self, entry_price: float, stop_loss: float, leverage: int) -> float:
        """Calculate position size based on risk parameters."""
        if entry_price <= 0 or stop_loss <= 0 or entry_price == stop_loss:
            return 0.0
            
        risk_amount = self.capital * self.risk_per_trade
        price_distance = abs(entry_price - stop_loss)
        
        # Calculate size in BTC
        size = risk_amount / (price_distance * leverage)
        
        # Ensure size is reasonable
        max_size = (self.capital * 0.5) / (entry_price / leverage)  # Max 50% of capital
        size = min(size, max_size)
        
        return round(size, 8)  # BTC position size with 8 decimal places
    
    def calculate_take_profits(self, 
                              entry_price: float, 
                              stop_loss: float, 
                              direction: str,
                              levels: int = 3) -> List[Dict[str, float]]:
        """Calculate multiple take profit levels with assigned percentages."""
        take_profits = []
        risk = abs(entry_price - stop_loss)
        
        # Risk-reward ratios for each TP level
        reward_ratios = [1.5, 2.5, 3.5]
        # Percentage of position to close at each TP
        close_percentages = [0.4, 0.3, 0.3]  
        
        for i in range(levels):
            if direction == "LONG":
                tp_price = entry_price + (risk * reward_ratios[i])
            else:
                tp_price = entry_price - (risk * reward_ratios[i])
                
            take_profits.append({
                "price": tp_price,
                "percentage": close_percentages[i],
                "hit": False
            })
            
        return take_profits
    
    def get_fibonacci_entry_zones(self) -> Dict[str, float]:
        """Get potential entry zones based on Fibonacci levels."""
        try:
            # Get realtime Fibonacci levels from Redis
            fib_levels = {}
            levels = redis_conn.hgetall("realtime_fibonacci_levels")
            
            for level_name, price_str in levels.items():
                if level_name != "timestamp":
                    try:
                        fib_levels[level_name] = float(price_str)
                    except ValueError:
                        continue
            
            return fib_levels
            
        except Exception as e:
            print(f"{RED}❌ Error getting Fibonacci entry zones: {e}{RESET}")
            return {}
    
    def check_market_bias(self) -> str:
        """Get current market bias (bullish/bearish) from Redis."""
        try:
            bias_data = redis_conn.hgetall("market_bias")
            if bias_data:
                bias = bias_data.get("bias", "Neutral/Sideways")
                self.last_market_bias = bias
                return bias
            
            if self.last_market_bias:  # Use cached result if available
                return self.last_market_bias
                
            return "Neutral/Sideways"
        except Exception as e:
            print(f"{RED}❌ Error checking market bias: {e}{RESET}")
            return "Neutral/Sideways"  # Default to neutral
    
    def check_mm_traps(self) -> Dict:
        """Check for recent MM traps to avoid entering manipulated markets."""
        try:
            trap_data = redis_conn.get("latest_mm_trap")
            if trap_data:
                return json.loads(trap_data)
            return {}
        except Exception as e:
            print(f"{RED}❌ Error checking MM traps: {e}{RESET}")
            return {}
    
    def should_open_position(self) -> Tuple[bool, str, float]:
        """Determine if we should open a new position based on market signals."""
        if len(self.open_positions) >= self.max_positions:
            return False, "Maximum positions already open", 0
            
        # Use the dedicated analyzer for decision making
        should_trade, reason, leverage = self.analyzer.analyze_trading_opportunity()
        return should_trade, reason, leverage
        
    def open_position(self, direction: str, reason: str, leverage: int = 1) -> Optional[Position]:
        """Open a new trading position."""
        if not self.current_price or self.current_price <= 0:
            print(f"{RED}❌ Invalid current price {self.current_price}{RESET}")
            return None
            
        # Determine stop loss based on direction and nearest support/resistance
        stop_distance = self.current_price * 0.01  # Default 1% stop
        
        if direction == "LONG":
            # For longs, set stop below nearest support
            stop_loss = self.current_price - stop_distance
        else:
            # For shorts, set stop above nearest resistance
            stop_loss = self.current_price + stop_distance
        
        # Calculate position size based on risk
        size = self.calculate_position_size(self.current_price, stop_loss, leverage)
        
        if size <= 0:
            print(f"{RED}❌ Invalid position size calculated{RESET}")
            return None
        
        # Calculate take profit levels
        take_profits = self.calculate_take_profits(
            self.current_price, stop_loss, direction, levels=3
        )
        
        position = Position(
            id=str(uuid.uuid4()),
            direction=direction,
            entry_price=self.current_price,
            size=size,
            leverage=leverage,
            entry_time=datetime.datetime.now(datetime.UTC),
            entry_reason=reason,
            stop_loss=stop_loss,
            take_profits=take_profits,
            status="OPEN"
        )
        
        # Add to open positions
        self.open_positions.append(position)
        
        # Format take profit output
        tp_texts = []
        for i, tp in enumerate(take_profits, 1):
            tp_texts.append(f"TP{i}: ${tp['price']:.2f} ({tp['percentage']*100:.0f}%)")
        
        # Print position details
        print(f"\n{GREEN_BG}{WHITE}{BOLD} NEW {direction} POSITION OPENED {RESET}")
        print(f"{YELLOW}Entry Price: ${position.entry_price:.2f}{RESET}")
        print(f"{RED}Stop Loss: ${position.stop_loss:.2f} ({abs(position.stop_loss - position.entry_price) / position.entry_price * 100:.2f}%){RESET}")
        print(f"{GREEN}Take Profits: {' | '.join(tp_texts)}{RESET}")
        print(f"{BLUE}Size: {position.size:.8f} BTC | Leverage: {position.leverage}x{RESET}")
        print(f"{CYAN}Reason: {position.entry_reason}{RESET}")
        
        return position
    
    def check_stop_loss_hit(self, position: Position) -> bool:
        """Check if stop loss has been hit for a position."""
        if not position.stop_loss:
            return False
            
        if position.direction == "LONG" and self.current_price <= position.stop_loss:
            return True
        elif position.direction == "SHORT" and self.current_price >= position.stop_loss:
            return True
            
        return False
    
    def check_take_profit_hits(self, position: Position) -> Tuple[bool, float]:
        """
        Check if any take profit levels have been hit.
        Returns (is_fully_closed, size_to_close)
        """
        if not position.take_profits:
            return False, 0.0
        
        size_to_close = 0.0
        remaining_size = position.size
        active_tps = [tp for tp in position.take_profits if not tp.get("hit", False)]
        
        for tp in active_tps:
            tp_hit = False
            
            if position.direction == "LONG" and self.current_price >= tp["price"]:
                tp_hit = True
            elif position.direction == "SHORT" and self.current_price <= tp["price"]:
                tp_hit = True
                
            if tp_hit:
                # Mark this TP as hit
                tp["hit"] = True
                close_size = position.size * tp["percentage"]
                size_to_close += close_size
                remaining_size -= close_size
                
                print(f"{GREEN}✅ Take profit hit at ${tp['price']:.2f} - closing {tp['percentage']*100:.0f}% of position{RESET}")
        
        return remaining_size <= 0.0001, size_to_close  # Fully closed if < 0.0001 BTC left
    
    def close_position(self, position: Position, reason: str, percentage: float = 1.0) -> None:
        """Close a position (fully or partially)."""
        if percentage <= 0 or percentage > 1:
            print(f"{RED}❌ Invalid close percentage: {percentage}{RESET}")
            return
            
        # Calculate realized PnL
        if position.direction == "LONG":
            pnl_per_btc = self.current_price - position.entry_price
        else:  # SHORT
            pnl_per_btc = position.entry_price - self.current_price
            
        size_to_close = position.size * percentage
        realized_pnl = pnl_per_btc * size_to_close * position.leverage
        
        # Update position
        if percentage >= 0.999:  # Full close
            position.exit_price = self.current_price
            position.exit_time = datetime.datetime.now(datetime.UTC)
            position.exit_reason = reason
            position.realized_pnl = realized_pnl
            position.status = "CLOSED"
            
            # Move to history
            self.trade_history.add_trade(position)
            self.open_positions.remove(position)
            
            # Update capital
            self.capital += realized_pnl
            
            pnl_percentage = (realized_pnl / (position.entry_price * position.size)) * 100
            pnl_color = GREEN if realized_pnl > 0 else RED
            
            print(f"\n{BLUE_BG}{WHITE}{BOLD} POSITION CLOSED {RESET}")
            print(f"{YELLOW}Entry: ${position.entry_price:.2f} | Exit: ${position.exit_price:.2f}{RESET}")
            print(f"{pnl_color}PnL: ${realized_pnl:.2f} ({pnl_percentage:.2f}%){RESET}")
            print(f"{CYAN}Reason: {reason}{RESET}")
            print(f"{BLUE}New Capital: ${self.capital:.2f}{RESET}")
        else:  # Partial close
            position.size -= size_to_close
            position.realized_pnl += realized_pnl
            
            # Update capital
            self.capital += realized_pnl
            
            print(f"\n{YELLOW_BG}{BLACK_BG}{BOLD} PARTIAL CLOSE ({percentage*100:.0f}%) {RESET}")
            print(f"{YELLOW}Price: ${self.current_price:.2f} | Remaining Size: {position.size:.8f} BTC{RESET}")
            print(f"{GREEN if realized_pnl > 0 else RED}Realized PnL: ${realized_pnl:.2f}{RESET}")
            print(f"{BLUE}New Capital: ${self.capital:.2f}{RESET}")
    
    def manage_open_positions(self) -> None:
        """Check and manage all open positions for SL/TP."""
        if not self.open_positions:
            return
            
        # Make a copy to avoid modifying during iteration
        positions = self.open_positions.copy()
        
        for position in positions:
            if position not in self.open_positions:
                continue  # Position was already removed
                
            # Check stop loss
            if self.check_stop_loss_hit(position):
                self.close_position(position, "Stop Loss Hit")
                continue
                
            # Check take profits
            fully_closed, size_to_close = self.check_take_profit_hits(position)
            if fully_closed:
                self.close_position(position, "All Take Profits Hit")
            elif size_to_close > 0:
                close_percentage = size_to_close / position.size
                self.close_position(position, "Partial Take Profit", percentage=close_percentage)
    
    def print_position_status(self) -> None:
        """Print current status of all open positions."""
        if not self.open_positions:
            print(f"\n{CYAN}No open positions{RESET}")
            return
            
        print(f"\n{BLUE_BG}{WHITE}{BOLD} OPEN POSITIONS ({len(self.open_positions)}) {RESET}")
        
        for pos in self.open_positions:
            # Calculate unrealized PnL
            pnl_usd, pnl_pct = pos.calculate_unrealized_pnl(self.current_price)
            
            # Determine color based on PnL
            pnl_color = GREEN if pnl_usd > 0 else RED
            
            # Calculate distance to SL and nearest TP
            sl_distance = abs(self.current_price - pos.stop_loss) / self.current_price * 100
            
            nearest_tp = None
            nearest_tp_distance = float('inf')
            
            for tp in pos.take_profits:
                distance = abs(self.current_price - tp["price"])
                if distance < nearest_tp_distance:
                    nearest_tp_distance = distance
                    nearest_tp = tp
            
            # Format TP and SL distances
            tp_distance_pct = nearest_tp_distance / self.current_price * 100 if nearest_tp else 0
            tp_direction = "↑" if (pos.direction == "LONG" and nearest_tp) else "↓" if nearest_tp else "-"
            sl_direction = "↓" if pos.direction == "LONG" else "↑"
            
            # Count active TPs
            active_tps = sum(1 for tp in pos.take_profits if not tp.get("hit", False))
            hit_tps = sum(1 for tp in pos.take_profits if tp.get("hit", False))
            
            # Entry time formatting
            entry_ago = (datetime.datetime.now(datetime.UTC) - pos.entry_time).total_seconds() / 60  # minutes
            time_str = f"{entry_ago:.0f}m" if entry_ago < 60 else f"{entry_ago/60:.1f}h"
            
            # Print position details
            direction_color = GREEN if pos.direction == "LONG" else RED
            print(f"{direction_color}{pos.direction} {pos.size:.4f} BTC {pos.leverage}x @ ${pos.entry_price:.2f} {RESET}({time_str} ago)")
            print(f"  {pnl_color}PnL: ${pnl_usd:.2f} ({pnl_pct:+.2f}%){RESET}")
            print(f"  SL: ${pos.stop_loss:.2f} ({sl_direction}{sl_distance:.1f}%) | TP: {hit_tps}/{len(pos.take_profits)} hit")
            
            if nearest_tp:
                nearest_pct = nearest_tp["percentage"] * 100
                print(f"  Next TP: ${nearest_tp['price']:.2f} ({tp_direction}{tp_distance_pct:.1f}%, {nearest_pct:.0f}% size)")

    def print_performance_summary(self) -> None:
        """Print trading performance summary."""
        pnl = self.capital - self.initial_capital
        pnl_pct = (pnl / self.initial_capital) * 100
        pnl_color = GREEN if pnl >= 0 else RED
        
        print(f"\n{MAGENTA}══════════════════════════════════════{RESET}")
        print(f"{WHITE}{BOLD} BTC FUTURES TRADING PERFORMANCE {RESET}")
        print(f"{MAGENTA}══════════════════════════════════════{RESET}")
        
        print(f"Initial Capital: ${self.initial_capital:.2f}")
        print(f"Current Capital: ${self.capital:.2f}")
        print(f"Overall P&L: {pnl_color}${pnl:.2f} ({pnl_pct:+.2f}%){RESET}")
        
        # Trading statistics
        if self.trade_history.total_trades > 0:
            print(f"\n{LIGHT_ORANGE}Trading Statistics:{RESET}")
            print(f"  Total Trades: {self.trade_history.total_trades}")
            print(f"  Win Rate: {self.trade_history.win_rate*100:.1f}% ({self.trade_history.winning_trades}/{self.trade_history.total_trades})")
            print(f"  Avg Win: ${self.trade_history.average_win:.2f}")
            print(f"  Avg Loss: ${self.trade_history.average_loss:.2f}")
            print(f"  Best Trade: ${self.trade_history.largest_win:.2f}")
            print(f"  Worst Trade: ${self.trade_history.largest_loss:.2f}")
            
            # Calculate profit factor
            if self.trade_history.average_loss != 0:
                profit_factor = abs(self.trade_history.average_win / self.trade_history.average_loss)
                print(f"  Profit Factor: {profit_factor:.2f}")
        
        # Current exposure
        if self.open_positions:
            total_exposure = sum(pos.size * self.current_price * pos.leverage for pos in self.open_positions)
            exposure_pct = (total_exposure / self.capital) * 100
            print(f"\n{YELLOW}Current Exposure: ${total_exposure:.2f} ({exposure_pct:.1f}% of capital){RESET}")
    
    def run_backtest(self, price_data: List[float], timestamps: List[datetime.datetime], volumes: List[float]) -> None:
        """Run trading strategy against historical price data."""
        print(f"{BLUE}Starting backtest with {len(price_data)} price points...{RESET}")
        
        for i, (price, timestamp, volume) in enumerate(zip(price_data, timestamps, volumes)):
            self.current_price = price
            
            # Manage existing positions
            self.manage_open_positions()
            
            # Every 5 candles, check for new entry signals
            if i % 5 == 0:
                should_open, reason, leverage = self.should_open_position()
                if should_open and "LONG" in reason:
                    self.open_position("LONG", reason, leverage)
                elif should_open and "SHORT" in reason:
                    self.open_position("SHORT", reason, leverage)
            
            # Print progress every 100 candles
            if i % 100 == 0 and i > 0:
                print(f"Processed {i}/{len(price_data)} price points...")
        
        # Close any remaining positions at the end
        for pos in self.open_positions.copy():
            self.close_position(pos, "End of Backtest")
            
        # Print final performance
        self.print_performance_summary()

    def run_live_trading_simulation(self, update_interval: float = 5.0) -> None:
        """Run live trading simulation with real-time market data."""
        print(f"{MAGENTA}{BOLD}Starting BTC Futures Trading Simulation{RESET}")
        print(f"{YELLOW}Initial Capital: ${self.initial_capital:.2f} | Max Leverage: {self.max_leverage}x{RESET}")
        print(f"{BLUE}Press Ctrl+C to stop the simulation{RESET}")
        
        try:
            while True:
                # Update current price
                previous_price = self.current_price
                self.update_current_price()
                
                if self.current_price <= 0:
                    print(f"{YELLOW}Waiting for valid price data...{RESET}")
                    time.sleep(update_interval)
                    continue
                
                # Display current price and brief market info
                price_change = ((self.current_price / previous_price) - 1) * 100 if previous_price > 0 else 0
                price_color = GREEN if price_change >= 0 else RED
                price_arrow = "▲" if price_change > 0 else "▼" if price_change < 0 else "•"
                
                print(f"\n{WHITE}{BOLD}[{datetime.datetime.now().strftime('%H:%M:%S')}] {RESET}" + 
                      f"BTC: {price_color}${self.current_price:.2f} {price_arrow} ({price_change:+.2f}%){RESET}")
                
                # Manage existing positions (check SL/TP)
                self.manage_open_positions()
                
                # Display current positions
                self.print_position_status()
                
                # Check for new position entries (not too frequently)
                now = datetime.datetime.now()
                if (now - self.last_analysis_time).total_seconds() >= self.analysis_cooldown:
                    should_open, reason, leverage = self.should_open_position()
                    if should_open and "LONG" in reason:
                        self.open_position("LONG", reason, leverage)
                    elif should_open and "SHORT" in reason:
                        self.open_position("SHORT", reason, leverage)
                    self.last_analysis_time = now
                
                # Periodically show performance summary
                if now.minute % 15 == 0 and now.second < 10:  # Every 15 minutes
                    self.print_performance_summary()
                
                # Save state periodically
                if now.minute % 30 == 0 and now.second < 10:  # Every 30 minutes
                    self.save_state()
                
                time.sleep(update_interval)
                
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Trading simulation stopped by user{RESET}")
            self.print_performance_summary()
            self.save_state()  # Save final state

def main():
    """Main entry point for the trading simulator."""
    print(f"{MAGENTA}{BOLD}╔════════════════════════════════════════════╗{RESET}")
    print(f"{MAGENTA}{BOLD}║             BTC FUTURES TRADER             ║{RESET}")
    print(f"{MAGENTA}{BOLD}║          OMEGA BTC AI SIMULATION           ║{RESET}")
    print(f"{MAGENTA}{BOLD}╚════════════════════════════════════════════╝{RESET}")
    
    # Initialize trader
    trader = BtcFuturesTrader(
        initial_capital=10000.0,
        max_leverage=5,
        risk_per_trade=0.02,
        max_positions=3
    )
    
    # Try to load previous state
    trader.load_state()
    
    # Start live trading simulation
    trader.run_live_trading_simulation(update_interval=5.0)

if __name__ == "__main__":
    main()
