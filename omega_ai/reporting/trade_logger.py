#!/usr/bin/env python3

"""
Trade logger for OmegaBTC AI trading simulations.
Records detailed information about trades and trader state.
"""

import datetime
import json
import os
import time
from typing import Dict, List, Any, Optional
import uuid

class TradeLogger:
    """
    Records trade entries, exits, and performance metrics for analysis and visualization.
    """
    
    def __init__(self, log_dir: str = None, write_to_file: bool = True, debug_mode: bool = False):
        """
        Initialize the trade logger.
        
        Args:
            log_dir: Directory to store log files
            write_to_file: Whether to write logs to files
            debug_mode: Whether to print debug information
        """
        self.write_to_file = write_to_file
        self.debug_mode = debug_mode
        
        # Set up log directory
        if log_dir:
            self.log_dir = log_dir
        else:
            self.log_dir = os.path.join(os.getcwd(), 'logs')
            
        if write_to_file and not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        # Initialize storage for in-memory logs
        self.trades = []
        self.metrics = []
        self.market_data = []
        
    def log_trade_entry(self, trader_name: str, trader_type: str, 
                       direction: str, entry_price: float, position_size: float,
                       leverage: float, stop_loss: float, take_profits: List[Dict],
                       emotional_state: str, entry_reason: str) -> str:
        """
        Log a new trade entry.
        
        Args:
            trader_name: Name of the trader
            trader_type: Type of trader (aggressive, strategic, newbie)
            direction: Trade direction (LONG/SHORT)
            entry_price: Entry price
            position_size: Position size
            leverage: Leverage used
            stop_loss: Stop loss price
            take_profits: List of take profit levels
            emotional_state: Trader's emotional state at entry
            entry_reason: Reason for entering the trade
            
        Returns:
            trade_id: Unique identifier for the trade
        """
        # Generate unique trade ID
        trade_id = str(uuid.uuid4())
        
        # Create trade entry record
        entry_time = datetime.datetime.now().isoformat()
        trade = {
            'trade_id': trade_id,
            'trader_name': trader_name,
            'trader_type': trader_type,
            'direction': direction,
            'entry_price': entry_price,
            'position_size': position_size,
            'leverage': leverage,
            'stop_loss': stop_loss,
            'take_profits': take_profits,
            'emotional_state': emotional_state,
            'entry_reason': entry_reason,
            'entry_time': entry_time,
            'status': 'OPEN'
        }
        
        # Add to in-memory storage
        self.trades.append(trade)
        
        # Write to file if enabled
        if self.write_to_file:
            self._write_trade_to_file(trade)
            
        # Print debug info if enabled
        if self.debug_mode:
            print(f"[ENTRY] {trader_name} entered {direction} at {entry_price} ({leverage}x) - {entry_reason}")
            
        return trade_id
    
    def log_trade_exit(self, trade_id: str, exit_price: float, exit_type: str,
                     pnl: float, exit_reason: str) -> bool:
        """
        Log a trade exit.
        
        Args:
            trade_id: Trade identifier
            exit_price: Exit price
            exit_type: Type of exit (stop_loss, take_profit, etc.)
            pnl: Profit and loss amount
            exit_reason: Reason for exiting
            
        Returns:
            bool: Success indicator
        """
        # Find trade in memory
        trade = None
        for t in self.trades:
            if t.get('trade_id') == trade_id:
                trade = t
                break
                
        if not trade:
            if self.debug_mode:
                print(f"[ERROR] Trade {trade_id} not found")
            return False
            
        # Update trade with exit information
        exit_time = datetime.datetime.now().isoformat()
        trade.update({
            'exit_price': exit_price,
            'exit_type': exit_type,
            'pnl': pnl,
            'exit_reason': exit_reason,
            'exit_time': exit_time,
            'status': 'CLOSED'
        })
        
        # Calculate trade duration
        try:
            entry_time = datetime.datetime.fromisoformat(trade['entry_time'])
            exit_time_dt = datetime.datetime.fromisoformat(exit_time)
            duration_seconds = (exit_time_dt - entry_time).total_seconds()
            trade['duration_minutes'] = duration_seconds / 60
        except (ValueError, TypeError):
            trade['duration_minutes'] = 0
        
        # Write updated trade to file if enabled
        if self.write_to_file:
            self._write_trade_to_file(trade)
            
        # Print debug info if enabled
        if self.debug_mode:
            pnl_str = f"+${pnl:.2f}" if pnl >= 0 else f"-${abs(pnl):.2f}"
            print(f"[EXIT] {trade['trader_name']} exited at {exit_price} - {exit_type} - {pnl_str}")
            
        return True
    
    def log_trader_metrics(self, trader_name: str, trader_type: str, metrics: Dict[str, Any]) -> None:
        """
        Log trader performance metrics.
        
        Args:
            trader_name: Name of the trader
            trader_type: Type of trader
            metrics: Dictionary of metrics
        """
        # Add timestamp and trader info
        metrics_record = {
            'timestamp': datetime.datetime.now().isoformat(),
            'trader_name': trader_name,
            'trader_type': trader_type,
            **metrics
        }
        
        # Add to in-memory storage
        self.metrics.append(metrics_record)
        
        # Write to file if enabled
        if self.write_to_file:
            self._write_metrics_to_file(metrics_record)
    
    def log_market_data(self, data: Dict[str, Any]) -> None:
        """
        Log market data for context.
        
        Args:
            data: Dictionary of market data
        """
        # Add timestamp
        data_record = {
            'timestamp': datetime.datetime.now().isoformat(),
            **data
        }
        
        # Add to in-memory storage
        self.market_data.append(data_record)
        
        # Write to file if enabled
        if self.write_to_file:
            self._write_market_data_to_file(data_record)
    
    def get_trades_by_trader(self, trader_name: str) -> List[Dict[str, Any]]:
        """
        Get all trades for a specific trader.
        
        Args:
            trader_name: Name of the trader
            
        Returns:
            List of trade dictionaries
        """
        return [trade for trade in self.trades if trade.get('trader_name') == trader_name]
    
    def get_metrics_by_trader(self, trader_name: str) -> List[Dict[str, Any]]:
        """
        Get all metrics for a specific trader.
        
        Args:
            trader_name: Name of the trader
            
        Returns:
            List of metric dictionaries
        """
        return [metric for metric in self.metrics if metric.get('trader_name') == trader_name]
    
    def _write_trade_to_file(self, trade: Dict[str, Any]) -> None:
        """Write trade data to log file."""
        filename = os.path.join(self.log_dir, f"trades_{trade['trader_type']}.jsonl")
        with open(filename, 'a') as f:
            f.write(json.dumps(trade) + '\n')
    
    def _write_metrics_to_file(self, metrics: Dict[str, Any]) -> None:
        """Write metrics data to log file."""
        filename = os.path.join(self.log_dir, f"metrics_{metrics['trader_type']}.jsonl")
        with open(filename, 'a') as f:
            f.write(json.dumps(metrics) + '\n')
    
    def _write_market_data_to_file(self, data: Dict[str, Any]) -> None:
        """Write market data to log file."""
        filename = os.path.join(self.log_dir, "market_data.jsonl")
        with open(filename, 'a') as f:
            f.write(json.dumps(data) + '\n')