#!/usr/bin/env python3

"""
Futures trading reporter for OmegaBTC AI.

This module connects the trader profiles with reporting systems to track
detailed performance metrics and prepare data for Grafana visualization.
"""

import datetime
import time
import json
import os
import uuid
from typing import Dict, List, Any, Optional, Tuple
import numpy as np

class TradeLogger:
    """
    Logger for trade entries, exits, and metrics.
    Stores data in JSON format for later analysis.
    """
    
    def __init__(self, log_dir: Optional[str] = None, debug_mode: bool = False):
        """
        Initialize trade logger.
        
        Args:
            log_dir: Directory for log files. If None, use current directory
            debug_mode: Whether to print debug information
        """
        self.log_dir = log_dir or os.path.join(os.getcwd(), "logs")
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.trades_file = os.path.join(self.log_dir, "trades.json")
        self.metrics_file = os.path.join(self.log_dir, "trader_metrics.json")
        
        self.debug_mode = debug_mode
        
        # Initialize trade log file if needed
        if not os.path.exists(self.trades_file):
            with open(self.trades_file, 'w') as f:
                json.dump([], f, cls=DateTimeEncoder, indent=2)
                
        # Initialize metrics log file if needed
        if not os.path.exists(self.metrics_file):
            with open(self.metrics_file, 'w') as f:
                json.dump([], f, cls=DateTimeEncoder, indent=2)
    
    def log_trade_entry(self, trader_name: str, trader_type: str, direction: str, 
                       entry_price: float, position_size: float, leverage: float, 
                       stop_loss: float, take_profits: List[Dict], emotional_state: str,
                       entry_reason: str, risk_percentage: float, market_context: Any,
                       session_id: str) -> str:
        """
        Log a new trade entry.
        
        Returns:
            trade_id: Unique identifier for the trade
        """
        # Generate trade ID
        trade_id = str(uuid.uuid4())
        
        # Create trade entry data
        trade_data = {
            "trade_id": trade_id,
            "trader_name": trader_name,
            "trader_type": trader_type,
            "direction": direction,
            "entry_price": float(entry_price),
            "position_size": float(position_size),
            "leverage": float(leverage),
            "stop_loss": float(stop_loss),
            "take_profits": take_profits,
            "emotional_state": emotional_state,
            "entry_reason": entry_reason,
            "risk_percentage": float(risk_percentage),
            "market_context": market_context,
            "entry_time": datetime.datetime.now().isoformat(),
            "session_id": session_id,
            "status": "OPEN"
        }
        
        # Load existing trades
        try:
            with open(self.trades_file, 'r') as f:
                trades = json.load(f)
        except:
            trades = []
        
        # Add new trade
        trades.append(trade_data)
        
        # Save updated trades
        try:
            with open(self.trades_file, 'w') as f:
                json.dump(trades, f, cls=DateTimeEncoder, indent=2)
        except Exception as e:
            if self.debug_mode:
                print(f"Error saving trade entry: {e}")
        
        return trade_id
    
    def log_trade_exit(self, trade_id: str, exit_price: float, exit_type: str,
                     pnl: float, exit_reason: str, emotional_state: str,
                     partial_percentage: float, exit_bar: int) -> bool:
        """
        Log a trade exit.
        
        Args:
            trade_id: Unique identifier for the trade
            exit_price: Exit price
            exit_type: Type of exit (stop_loss, take_profit, etc.)
            pnl: Profit/loss amount
            exit_reason: Reason for exiting
            emotional_state: Trader's emotional state at exit
            partial_percentage: Percentage of position closed (1.0 = full)
            exit_bar: Bar number when exit occurred (for simulation)
            
        Returns:
            bool: Success indicator
        """
        # Load existing trades
        try:
            with open(self.trades_file, 'r') as f:
                trades = json.load(f)
        except:
            if self.debug_mode:
                print(f"Error loading trades for exit: {trade_id}")
            return False
        
        # Find the trade
        found = False
        for trade in trades:
            if trade.get("trade_id") == trade_id:
                # Update with exit information
                trade["exit_price"] = float(exit_price)
                trade["exit_type"] = exit_type
                trade["pnl"] = float(pnl)
                trade["exit_reason"] = exit_reason
                trade["emotional_state_at_exit"] = emotional_state
                trade["exit_time"] = datetime.datetime.now().isoformat()
                trade["exit_bar"] = exit_bar
                
                # If full exit or almost full (≥99%)
                if partial_percentage >= 0.99:
                    trade["status"] = "CLOSED"
                else:
                    # For partial exits, indicate the percentage closed
                    trade["partial_exit"] = True
                    trade["partial_percentage"] = partial_percentage
                
                found = True
                break
        
        if not found:
            if self.debug_mode:
                print(f"Trade not found for exit: {trade_id}")
            return False
        
        # Save updated trades
        try:
            with open(self.trades_file, 'w') as f:
                json.dump(trades, f, cls=DateTimeEncoder, indent=2)
            return True
        except Exception as e:
            if self.debug_mode:
                print(f"Error saving trade exit: {e}")
            return False
    
    def log_trader_metrics(self, trader_name: str, trader_type: str, metrics: Dict) -> bool:
        """
        Log trader metrics.
        
        Args:
            trader_name: Name of the trader
            trader_type: Type of trader
            metrics: Metrics dictionary
            
        Returns:
            bool: Success indicator
        """
        # Add metadata
        metrics_data = {
            "trader_name": trader_name,
            "trader_type": trader_type,
            "timestamp": datetime.datetime.now().isoformat(),
            "metrics": metrics
        }
        
        # Load existing metrics
        try:
            with open(self.metrics_file, 'r') as f:
                all_metrics = json.load(f)
        except:
            all_metrics = []
        
        # Add new metrics
        all_metrics.append(metrics_data)
        
        # Save updated metrics
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(all_metrics, f, cls=DateTimeEncoder, indent=2)
            return True
        except Exception as e:
            if self.debug_mode:
                print(f"Error saving trader metrics: {e}")
            return False
    
    def get_trades_by_trader(self, trader_name: str) -> List[Dict]:
        """
        Get all trades for a specific trader.
        
        Args:
            trader_name: Name of the trader
            
        Returns:
            List of trade dictionaries
        """
        try:
            with open(self.trades_file, 'r') as f:
                trades = json.load(f)
                
            return [t for t in trades if t.get("trader_name") == trader_name]
        except Exception as e:
            if self.debug_mode:
                print(f"Error getting trades for {trader_name}: {e}")
            return []
    
    def get_metrics_by_trader(self, trader_name: str) -> List[Dict]:
        """
        Get all metrics for a specific trader.
        
        Args:
            trader_name: Name of the trader
            
        Returns:
            List of metrics dictionaries
        """
        try:
            with open(self.metrics_file, 'r') as f:
                metrics = json.load(f)
                
            return [m for m in metrics if m.get("trader_name") == trader_name]
        except Exception as e:
            if self.debug_mode:
                print(f"Error getting metrics for {trader_name}: {e}")
            return []


class GrafanaMetricsFormatter:
    """
    Formats trading metrics data for Grafana dashboards and time series visualization.
    """
    
    @staticmethod
    def format_trade_time_series(trades: List[Dict]) -> Dict[str, List]:
        """
        Convert trade data to time series format for Grafana.
        
        Args:
            trades: List of trade dictionaries
            
        Returns:
            Dictionary with time series data for different metrics
        """
        # Initialize time series containers
        series = {
            'timestamps': [],
            'pnl': [],
            'cumulative_pnl': [],
            'position_sizes': [],
            'leverage': [],
            'win_loss': []  # 1 for win, 0 for loss
        }
        
        # Sort trades by entry time
        sorted_trades = sorted(trades, key=lambda t: t.get('entry_time', 0))
        
        # Process each trade
        cumulative_pnl = 0
        for trade in sorted_trades:
            # Skip open trades (no PnL data yet)
            if trade.get('status') != 'CLOSED':
                continue
                
            # Extract data
            exit_time = trade.get('exit_time')
            pnl = float(trade.get('pnl', 0))
            position_size = float(trade.get('position_size', 0))
            leverage = float(trade.get('leverage', 1))
            
            # Update cumulative PnL
            cumulative_pnl += pnl
            
            # Append to series
            series['timestamps'].append(exit_time)
            series['pnl'].append(pnl)
            series['cumulative_pnl'].append(cumulative_pnl)
            series['position_sizes'].append(position_size)
            series['leverage'].append(leverage)
            series['win_loss'].append(1 if pnl > 0 else 0)
            
        return series
    
    @staticmethod
    def format_exit_type_statistics(trades: List[Dict]) -> Dict[str, Any]:
        """
        Format exit type statistics for visualization.
        
        Args:
            trades: List of trade dictionaries
            
        Returns:
            Dictionary with exit type statistics
        """
        # Initialize counters
        exit_types = {
            'stop_loss': 0,
            'take_profit': 0,
            'trailing_stop': 0,
            'time_based': 0,
            'liquidation': 0,
            'market_condition': 0,
            'manual': 0,
            'other': 0
        }
        
        exit_pnl = {
            'stop_loss': 0,
            'take_profit': 0,
            'trailing_stop': 0,
            'time_based': 0,
            'liquidation': 0,
            'market_condition': 0,
            'manual': 0,
            'other': 0
        }
        
        # Count exit types
        for trade in trades:
            if trade.get('status') != 'CLOSED':
                continue
                
            exit_type = trade.get('exit_type', 'other')
            pnl = float(trade.get('pnl', 0))
            
            # Ensure exit type is in our categories
            if exit_type not in exit_types:
                exit_type = 'other'
                
            exit_types[exit_type] += 1
            exit_pnl[exit_type] += pnl
        
        # Calculate average PnL per exit type
        avg_pnl = {}
        for exit_type, count in exit_types.items():
            if count > 0:
                avg_pnl[exit_type] = exit_pnl[exit_type] / count
            else:
                avg_pnl[exit_type] = 0
                
        # Format for Grafana
        return {
            'counts': exit_types,
            'total_pnl': exit_pnl,
            'avg_pnl': avg_pnl
        }


class GrafanaDashboardGenerator:
    """Generate Grafana dashboards with proper layout and panel positioning."""
    
    def __init__(self):
        self.panel_id = 0
        self.current_y = 0
        
    def create_dashboard_base(self, title: str, description: str = "") -> Dict[str, Any]:
        """Create the base dashboard structure."""
        return {
            "annotations": {
                "list": [
                    {
                        "builtIn": 1,
                        "datasource": "-- Grafana --",
                        "enable": True,
                        "hide": True,
                        "iconColor": "rgba(0, 211, 255, 1)",
                        "name": "Annotations & Alerts",
                        "type": "dashboard"
                    }
                ]
            },
            "editable": True,
            "gnetId": None,
            "graphTooltip": 0,
            "id": None,
            "links": [],
            "panels": [],
            "refresh": "5s",
            "schemaVersion": 27,
            "style": "dark",
            "tags": ["trading", "bitcoin", "simulation"],
            "templating": {
                "list": [
                    {
                        "current": {
                            "selected": False,
                            "text": "All",
                            "value": "$__all"
                        },
                        "description": None,
                        "error": None,
                        "hide": 0,
                        "includeAll": True,
                        "label": "Trader",
                        "multi": False,
                        "name": "trader",
                        "options": [],
                        "query": "SHOW TAG VALUES FROM \"trader_metrics\" WITH KEY = \"trader\"",
                        "refresh": 1,
                        "regex": "",
                        "skipUrlSync": False,
                        "sort": 0,
                        "tagValuesQuery": "",
                        "tags": [],
                        "tagsQuery": "",
                        "type": "query",
                        "useTags": False
                    }
                ]
            },
            "time": {
                "from": "now-6h",
                "to": "now"
            },
            "timepicker": {},
            "timezone": "",
            "title": title,
            "description": description,
            "version": 0
        }
    
    def create_win_rate_panel(self, dashboard: Dict, width: int = 8, height: int = 8) -> Dict:
        """Create a win rate gauge panel with proper positioning."""
        panel = {
            "id": self.panel_id,
            "title": "Win Rate by Trader Type",
            "type": "gauge",
            "datasource": "InfluxDB",
            "gridPos": {
                "h": height,
                "w": width,
                "x": 0,
                "y": self.current_y
            },
            "targets": [
                {
                    "query": "SELECT mean(\"win_rate\") FROM \"trader_metrics\" WHERE $timeFilter AND \"trader\" =~ /$trader/ GROUP BY \"trader_type\"",
                    "refId": "A"
                }
            ],
            "fieldConfig": {
                "defaults": {
                    "color": {"mode": "thresholds"},
                    "mappings": [],
                    "max": 100,
                    "min": 0,
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {"color": "red", "value": None},
                            {"color": "yellow", "value": 40},
                            {"color": "green", "value": 60}
                        ]
                    },
                    "unit": "percent"
                }
            }
        }
        
        dashboard["panels"].append(panel)
        self.panel_id += 1
        return dashboard
    
    def create_pnl_panel(self, dashboard: Dict, width: int = 16, height: int = 8, x_pos: int = 8) -> Dict:
        """Create a P&L timeseries panel with proper positioning."""
        panel = {
            "id": self.panel_id,
            "title": "Trade P&L by Trader",
            "type": "timeseries",
            "datasource": "InfluxDB",
            "gridPos": {
                "h": height,
                "w": width,
                "x": x_pos,
                "y": self.current_y
            },
            "targets": [
                {
                    "query": "SELECT \"pnl\" FROM \"trade_exits\" WHERE $timeFilter AND \"trader\" =~ /$trader/ GROUP BY \"trader\"",
                    "refId": "A"
                }
            ],
            "fieldConfig": {
                "defaults": {
                    "color": {"mode": "palette-classic"},
                    "custom": {
                        "axisLabel": "P&L",
                        "axisPlacement": "auto",
                        "barAlignment": 0,
                        "drawStyle": "bars",
                        "fillOpacity": 100,
                        "gradientMode": "none",
                        "hideFrom": {"legend": False, "tooltip": False, "viz": False},
                        "lineInterpolation": "linear",
                        "lineWidth": 1,
                        "pointSize": 5,
                        "scaleDistribution": {"type": "linear"},
                        "showPoints": "auto",
                        "spanNulls": False,
                        "stacking": {"group": "A", "mode": "none"},
                        "thresholdsStyle": {"mode": "off"}
                    },
                    "mappings": [],
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [{"color": "green", "value": None}]
                    },
                    "unit": "currencyUSD"
                }
            }
        }
        
        dashboard["panels"].append(panel)
        self.panel_id += 1
        return dashboard
    
    def create_trader_capital_panel(self, dashboard: Dict, width: int = 24, height: int = 8) -> Dict:
        """Create a trader capital comparison panel."""
        panel = {
            "id": self.panel_id,
            "title": "Trader Capital Comparison",
            "type": "timeseries",
            "datasource": "InfluxDB",
            "gridPos": {
                "h": height,
                "w": width,
                "x": 0,
                "y": self.current_y
            },
            "targets": [
                {
                    "query": "SELECT \"capital\" FROM \"trader_metrics\" WHERE $timeFilter AND \"trader\" =~ /$trader/ GROUP BY \"trader\"",
                    "refId": "A"
                }
            ],
            "fieldConfig": {
                "defaults": {
                    "color": {"mode": "palette-classic"},
                    "custom": {
                        "axisLabel": "Capital",
                        "axisPlacement": "auto",
                        "drawStyle": "line",
                        "fillOpacity": 10,
                        "gradientMode": "none",
                        "lineInterpolation": "smooth",
                        "lineWidth": 2,
                        "pointSize": 5,
                        "scaleDistribution": {"type": "linear"},
                        "showPoints": "never",
                        "spanNulls": True,
                    },
                    "mappings": [],
                    "unit": "currencyUSD"
                }
            }
        }
        
        dashboard["panels"].append(panel)
        self.panel_id += 1
        return dashboard
    
    def create_emotional_state_panel(self, dashboard: Dict, trader_type: str, 
                                   width: int = 12, height: int = 8, x_pos: int = 0) -> Dict:
        """Create an emotional state panel for a specific trader type."""
        panel = {
            "id": self.panel_id,
            "title": f"{trader_type} Trader Emotional States",
            "type": "piechart",
            "datasource": "InfluxDB",
            "gridPos": {
                "h": height,
                "w": width,
                "x": x_pos,
                "y": self.current_y
            },
            "options": {
                "legend": {
                    "displayMode": "list",
                    "placement": "right",
                    "values": ["percent"]
                },
                "pieType": "pie",
                "reduceOptions": {
                    "calcs": ["sum"],
                    "fields": "value",
                    "values": False
                },
                "tooltip": {
                    "mode": "single"
                }
            },
            "targets": [
                {
                    "query": f"SELECT count(\"pnl\") FROM \"trade_exits\" WHERE $timeFilter AND \"trader_type\" = '{trader_type}' AND \"trader\" =~ /$trader/ GROUP BY \"emotional_state\"",
                    "refId": "A"
                }
            ]
        }
        
        dashboard["panels"].append(panel)
        self.panel_id += 1
        return dashboard
    
    def create_exit_type_panel(self, dashboard: Dict, trader_type: str, 
                             width: int = 12, height: int = 8, x_pos: int = 12) -> Dict:
        """Create an exit type distribution panel for a specific trader type."""
        panel = {
            "id": self.panel_id,
            "title": f"{trader_type} Trader Exit Types",
            "type": "piechart",
            "datasource": "InfluxDB",
            "gridPos": {
                "h": height,
                "w": width,
                "x": x_pos,
                "y": self.current_y
            },
            "options": {
                "legend": {
                    "displayMode": "list",
                    "placement": "right",
                    "values": ["percent"]
                },
                "pieType": "pie",
                "reduceOptions": {
                    "calcs": ["sum"],
                    "fields": "value",
                    "values": False
                },
                "tooltip": {
                    "mode": "single"
                }
            },
            "targets": [
                {
                    "query": f"SELECT count(\"pnl\") FROM \"trade_exits\" WHERE $timeFilter AND \"trader_type\" = '{trader_type}' AND \"trader\" =~ /$trader/ GROUP BY \"exit_type\"",
                    "refId": "A"
                }
            ]
        }
        
        dashboard["panels"].append(panel)
        self.panel_id += 1
        return dashboard
    
    def add_row(self, dashboard: Dict, title: str) -> Dict:
        """Add a collapsible row to organize panels."""
        panel = {
            "id": self.panel_id,
            "title": title,
            "type": "row",
            "collapsed": False,
            "gridPos": {
                "h": 1,
                "w": 24,
                "x": 0,
                "y": self.current_y
            }
        }
        
        dashboard["panels"].append(panel)
        self.panel_id += 1
        self.current_y += 1
        return dashboard
    
    def create_trader_dashboard(self, title: str) -> Dict:
        """Create a complete trader dashboard with proper panel organization."""
        dashboard = self.create_dashboard_base(title)
        
        # Overview row
        self.add_row(dashboard, "Performance Overview")
        self.create_trader_capital_panel(dashboard)
        self.current_y += 8
        
        # Win/Loss metrics row
        self.add_row(dashboard, "Win/Loss Metrics")
        self.create_win_rate_panel(dashboard)
        self.create_pnl_panel(dashboard)
        self.current_y += 8
        
        # Individual trader rows
        trader_types = ["Aggressive", "Strategic", "Newbie"]
        for trader in trader_types:
            self.add_row(dashboard, f"{trader} Trader Metrics")
            self.create_emotional_state_panel(dashboard, trader)
            self.create_exit_type_panel(dashboard, trader)
            self.current_y += 8
        
        return dashboard

    def export_dashboard(self, dashboard: Dict, output_file: str) -> bool:
        """Export dashboard to a JSON file."""
        try:
            with open(output_file, 'w') as f:
                json.dump(dashboard, f, cls=DateTimeEncoder, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting dashboard: {e}")
            return False


class FuturesReporter:
    """
    Comprehensive futures trading reporter that tracks performance across
    different trader profiles and prepares data for visualization.
    """
    
    def __init__(self, 
               influxdb_url: Optional[str] = None,
               influxdb_token: Optional[str] = None,
               influxdb_org: Optional[str] = "omegabtc",
               influxdb_bucket: Optional[str] = "trading_metrics",
               log_dir: Optional[str] = None,
               reporting_interval: int = 60,  # seconds
               debug_mode: bool = False):
        """
        Initialize the futures reporter.
        
        Args:
            influxdb_url: URL of InfluxDB server (if None, skip direct ingestion)
            influxdb_token: InfluxDB authentication token
            influxdb_org: InfluxDB organization
            influxdb_bucket: InfluxDB bucket for metrics
            log_dir: Directory for log files
            reporting_interval: How often to send metrics to InfluxDB (seconds)
            debug_mode: Whether to print debug information
        """
        self.influxdb_url = influxdb_url
        self.influxdb_token = influxdb_token
        self.influxdb_org = influxdb_org
        self.influxdb_bucket = influxdb_bucket
        self.reporting_interval = reporting_interval
        self.debug_mode = debug_mode
        
        # Initialize logger
        self.logger = TradeLogger(log_dir=log_dir, debug_mode=debug_mode)
        
        # Initialize trader mapping
        self.traders = {}
        self.active_trades = {}  # Maps trade_id to trader_name
        
        # Session stats
        self.session_start_time = datetime.datetime.now()
        self.session_id = str(uuid.uuid4())
        
        if self.debug_mode:
            print(f"Initialized FuturesReporter with session ID: {self.session_id}")
    
    def register_trader(self, trader_name: str, trader_type: str, trader_instance: Any) -> None:
        """
        Register a trader with the reporting system.
        
        Args:
            trader_name: Name identifier
            trader_type: Type of trader (aggressive, strategic, newbie)
            trader_instance: Trader object instance
        """
        self.traders[trader_name] = {
            'type': trader_type,
            'instance': trader_instance,
            'trade_count': 0,
            'win_count': 0,
            'loss_count': 0,
            'pnl_history': [],
            'last_reported': datetime.datetime.now(),
            'initial_capital': getattr(trader_instance, 'initial_capital', 10000.0),
            'current_capital': getattr(trader_instance, 'capital', 10000.0),
            'liquidation_events': 0
        }
        
        if self.debug_mode:
            print(f"Registered trader: {trader_name} ({trader_type})")
    
    def record_trade_entry(self, trader_name: str, direction: str, entry_price: float, 
                         position_size: float, leverage: float, stop_loss: float, 
                         take_profits: List[Dict], entry_reason: str) -> Optional[str]:
        """
        Record a new trade entry.
        
        Args:
            trader_name: Name of the trader
            direction: Trade direction (LONG/SHORT)
            entry_price: Entry price
            position_size: Position size
            leverage: Leverage used
            stop_loss: Stop loss price
            take_profits: List of take profit levels
            entry_reason: Reason for entering the trade
            
        Returns:
            trade_id: Unique trade identifier or None if failed
        """
        if trader_name not in self.traders:
            if self.debug_mode:
                print(f"Unknown trader: {trader_name}")
            return None
        
        trader_info = self.traders[trader_name]
        trader_instance = trader_info['instance']
        
        # Get emotional state from trader instance if available
        emotional_state = "neutral"
        if hasattr(trader_instance, 'state') and hasattr(trader_instance.state, 'emotional_state'):
            emotional_state = trader_instance.state.emotional_state
        
        # Get market context if available
        market_context = None
        if hasattr(trader_instance, 'analyzer') and hasattr(trader_instance.analyzer, 'get_market_context'):
            try:
                market_context = trader_instance.analyzer.get_market_context()
            except:
                market_context = None
        
        # Calculate risk percentage
        risk_percentage = 0
        if hasattr(trader_instance, 'capital') and trader_instance.capital > 0:
            notional_value = position_size * entry_price * leverage
            risk_percentage = notional_value / trader_instance.capital
        
        # Log the trade entry
        trade_id = self.logger.log_trade_entry(
            trader_name=trader_name,
            trader_type=trader_info['type'],
            direction=direction,
            entry_price=entry_price,
            position_size=position_size,
            leverage=leverage,
            stop_loss=stop_loss,
            take_profits=take_profits,
            emotional_state=emotional_state,
            entry_reason=entry_reason,
            risk_percentage=risk_percentage,
            market_context=market_context,
            session_id=self.session_id
        )
        
        # Track the active trade
        self.active_trades[trade_id] = trader_name
        trader_info['trade_count'] += 1
        
        return trade_id
    
    def record_trade_exit(self, trade_id: str, exit_price: float, exit_type: str,
                        pnl: float, exit_reason: str, partial_percentage: float = 1.0,
                        exit_bar: int = 0) -> bool:
        """
        Record a trade exit.
        
        Args:
            trade_id: Trade identifier
            exit_price: Exit price
            exit_type: Type of exit (stop_loss, take_profit, etc.)
            pnl: Profit and loss amount
            exit_reason: Reason for exiting
            partial_percentage: Percentage of position closed (1.0 = full)
            exit_bar: Bar number when exit occurred (for simulation)
            
        Returns:
            bool: Success indicator
        """
        if trade_id not in self.active_trades:
            if self.debug_mode:
                print(f"Unknown trade ID: {trade_id}")
            return False
        
        trader_name = self.active_trades[trade_id]
        trader_info = self.traders[trader_name]
        trader_instance = trader_info['instance']
        
        # Get emotional state at exit if available
        emotional_state = "neutral"
        if hasattr(trader_instance, 'state') and hasattr(trader_instance.state, 'emotional_state'):
            emotional_state = trader_instance.state.emotional_state
        
        # Check if this was a liquidation
        is_liquidation = exit_type.lower() == 'liquidation'
        if is_liquidation:
            trader_info['liquidation_events'] += 1
        
        # Log the trade exit
        success = self.logger.log_trade_exit(
            trade_id=trade_id,
            exit_price=exit_price,
            exit_type=exit_type,
            pnl=pnl,
            exit_reason=exit_reason,
            emotional_state=emotional_state,
            partial_percentage=partial_percentage,
            exit_bar=exit_bar
        )
        
        if not success:
            return False
        
        # Update trader statistics
        trader_info['pnl_history'].append(pnl)
        if pnl > 0:
            trader_info['win_count'] += 1
        else:
            trader_info['loss_count'] += 1
        
        # Update current capital if available
        if hasattr(trader_instance, 'capital'):
            trader_info['current_capital'] = trader_instance.capital
        
        # Remove from active trades if fully closed
        if partial_percentage >= 0.99:  # Consider it fully closed if ≥99% is closed
            del self.active_trades[trade_id]
        
        return True
    
    def record_trader_metrics(self, trader_name: str) -> bool:
        """
        Record current metrics for a trader.
        
        Args:
            trader_name: Name of the trader
            
        Returns:
            bool: Success indicator
        """
        if trader_name not in self.traders:
            if self.debug_mode:
                print(f"Unknown trader: {trader_name}")
            return False
        
        trader_info = self.traders[trader_name]
        trader_instance = trader_info['instance']
        
        # Calculate metrics from trader instance
        metrics = self._extract_trader_metrics(trader_instance, trader_info)
        
        # Log the metrics
        self.logger.log_trader_metrics(
            trader_name=trader_name,
            trader_type=trader_info['type'],
            metrics=metrics
        )
        
        trader_info['last_reported'] = datetime.datetime.now()
        
        return True
    
    def _extract_trader_metrics(self, trader_instance: Any, trader_info: Dict) -> Dict[str, Any]:
        """Extract performance metrics from a trader instance."""
        metrics = {
            'total_trades': trader_info['trade_count'],
            'winning_trades': trader_info['win_count'],
            'losing_trades': trader_info['loss_count'],
            'liquidation_events': trader_info['liquidation_events'],
            'initial_capital': trader_info['initial_capital'],
            'current_capital': trader_info['current_capital'],
        }
        
        # Calculate profit/loss percentage
        if trader_info['initial_capital'] > 0:
            pnl_pct = (trader_info['current_capital'] - trader_info['initial_capital']) / trader_info['initial_capital'] * 100
            metrics['pnl_percentage'] = pnl_pct
        
        # Calculate win rate
        if trader_info['trade_count'] > 0:
            win_rate = trader_info['win_count'] / trader_info['trade_count'] * 100
            metrics['win_rate'] = win_rate
        
        # Extract additional metrics from trader instance
        if hasattr(trader_instance, 'state'):
            state = trader_instance.state
            metrics['emotional_state'] = getattr(state, 'emotional_state', 'neutral')
            metrics['confidence'] = getattr(state, 'confidence', 0.5)
            metrics['risk_appetite'] = getattr(state, 'risk_appetite', 0.5)
            metrics['consecutive_wins'] = getattr(state, 'consecutive_wins', 0)
            metrics['consecutive_losses'] = getattr(state, 'consecutive_losses', 0)
            metrics['drawdown'] = getattr(state, 'drawdown', 0)
        
        # Extract trader-specific metrics
        if trader_info['type'] == 'aggressive':
            if hasattr(trader_instance, 'impulsiveness'):
                metrics['impulsiveness'] = trader_instance.impulsiveness
            if hasattr(trader_instance, 'fomo_susceptibility'):
                metrics['fomo_susceptibility'] = trader_instance.fomo_susceptibility
            if hasattr(trader_instance, 'trade_durations') and trader_instance.trade_durations:
                metrics['avg_trade_duration'] = sum(trader_instance.trade_durations) / len(trader_instance.trade_durations)
        
        # Newbie-specific metrics
        elif trader_info['type'] == 'newbie':
            if hasattr(trader_instance, 'fomo_trades'):
                metrics['fomo_trades'] = trader_instance.fomo_trades
            if hasattr(trader_instance, 'panic_sells'):
                metrics['panic_sells'] = trader_instance.panic_sells
            if hasattr(trader_instance, 'max_consecutive_losses'):
                metrics['max_consecutive_losses'] = trader_instance.max_consecutive_losses
        
        # Strategic-specific metrics
        elif trader_info['type'] == 'strategic':
            if hasattr(trader_instance, 'patience_score'):
                metrics['patience_score'] = trader_instance.patience_score
            if hasattr(trader_instance, 'analysis_depth'):
                metrics['analysis_depth'] = trader_instance.analysis_depth
            if hasattr(trader_instance, 'market_regime_accuracy'):
                metrics['market_regime_accuracy'] = trader_instance.market_regime_accuracy
        
        return metrics
    
    def _generate_trader_report(self, trader_name: str) -> Dict[str, Any]:
        """Generate a detailed report for a specific trader."""
        trader_info = self.traders.get(trader_name)
        if not trader_info:
            return {}
        
        # Get trades and metrics from logger
        trades = self.logger.get_trades_by_trader(trader_name)
        metrics_history = self.logger.get_metrics_by_trader(trader_name)
        
        # Current metrics
        current_metrics = self._extract_trader_metrics(trader_info['instance'], trader_info)
        
        # Calculate additional statistics
        avg_pnl = 0
        if trader_info['pnl_history']:
            avg_pnl = sum(trader_info['pnl_history']) / len(trader_info['pnl_history'])
        
        profit_factor = 0
        if trades:
            winning_trades = [t for t in trades if float(t.get('pnl', 0)) > 0]
            losing_trades = [t for t in trades if float(t.get('pnl', 0)) <= 0]
            
            total_profit = sum([float(t.get('pnl', 0)) for t in winning_trades])
            total_loss = abs(sum([float(t.get('pnl', 0)) for t in losing_trades]))
            
            if total_loss > 0:
                profit_factor = total_profit / total_loss
        
        # Calculate trade durations
        trade_durations = []
        for trade in trades:
            entry_time = trade.get('entry_time')
            exit_time = trade.get('exit_time')
            if entry_time and exit_time:
                try:
                    entry_dt = datetime.datetime.fromisoformat(entry_time)
                    exit_dt = datetime.datetime.fromisoformat(exit_time)
                    duration = (exit_dt - entry_dt).total_seconds() / 60  # minutes
                    trade_durations.append(duration)
                except:
                    pass
        
        avg_duration = 0
        if trade_durations:
            avg_duration = sum(trade_durations) / len(trade_durations)
        
        # Exit type breakdown
        exit_types = {}
        for trade in trades:
            exit_type = trade.get('exit_type', 'unknown')
            if exit_type not in exit_types:
                exit_types[exit_type] = 0
            exit_types[exit_type] += 1
        
        # Compile the report
        report = {
            'trader_name': trader_name,
            'trader_type': trader_info['type'],
            'total_trades': trader_info['trade_count'],
            'winning_trades': trader_info['win_count'],
            'losing_trades': trader_info['loss_count'],
            'win_rate': 0 if trader_info['trade_count'] == 0 else (trader_info['win_count'] / trader_info['trade_count'] * 100),
            'liquidation_events': trader_info['liquidation_events'],
            'profit_factor': profit_factor,
            'avg_pnl': avg_pnl,
            'avg_duration_minutes': avg_duration,
            'exit_types': exit_types,
            'current_metrics': current_metrics,
            'pnl_history': trader_info['pnl_history'],
            'current_capital': trader_info['current_capital'],
            'initial_capital': trader_info['initial_capital'],
            'return_percentage': (trader_info['current_capital'] - trader_info['initial_capital']) / trader_info['initial_capital'] * 100
        }
        
        return report
    
    def generate_performance_report(self, trader_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive performance report.
        
        Args:
            trader_name: Optional trader name (if None, report on all traders)
            
        Returns:
            Dictionary with performance report data
        """
        if trader_name and trader_name in self.traders:
            # Report for single trader
            return self._generate_trader_report(trader_name)
        else:
            # Report for all traders
            report = {
                'timestamp': datetime.datetime.now().isoformat(),
                'session_id': self.session_id,
                'session_duration_hours': (datetime.datetime.now() - self.session_start_time).total_seconds() / 3600,
                'traders': {}
            }
            
            for name in self.traders:
                report['traders'][name] = self._generate_trader_report(name)
                
            return report
    
    def export_grafana_time_series(self, trader_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Export data formatted for Grafana time series visualization.
        
        Args:
            trader_name: Optional trader name (if None, export all traders)
            
        Returns:
            Dictionary with Grafana-formatted time series data
        """
        result = {}
        
        if trader_name and trader_name in self.traders:
            # Export for single trader
            trades = self.logger.get_trades_by_trader(trader_name)
            metrics = self.logger.get_metrics_by_trader(trader_name)
            
            result[trader_name] = {
                'trades': GrafanaMetricsFormatter.format_trade_time_series(trades),
                'metrics': self._format_metrics_for_grafana(metrics),
                'exit_types': GrafanaMetricsFormatter.format_exit_type_statistics(trades)
            }
        else:
            # Export for all traders
            for name in self.traders:
                trades = self.logger.get_trades_by_trader(name)
                metrics = self.logger.get_metrics_by_trader(name)
                
                result[name] = {
                    'trades': GrafanaMetricsFormatter.format_trade_time_series(trades),
                    'metrics': self._format_metrics_for_grafana(metrics),
                    'exit_types': GrafanaMetricsFormatter.format_exit_type_statistics(trades)
                }
                
        return result
    
    def _format_metrics_for_grafana(self, metrics_list: List[Dict]) -> Dict[str, List]:
        """Format metrics for Grafana time series visualization."""
        # Extract timestamps and metric values
        series = {
            'timestamps': [],
            'capital': [],
            'win_rate': [],
            'drawdown': [],
            'risk_appetite': [],
            'confidence': []
        }
        
        for metrics_data in metrics_list:
            timestamp = metrics_data.get('timestamp')
            metrics = metrics_data.get('metrics', {})
            
            series['timestamps'].append(timestamp)
            series['capital'].append(metrics.get('current_capital', 0))
            series['win_rate'].append(metrics.get('win_rate', 0))
            series['drawdown'].append(metrics.get('drawdown', 0))
            series['risk_appetite'].append(metrics.get('risk_appetite', 0.5))
            series['confidence'].append(metrics.get('confidence', 0.5))
            
        return series
    
    def export_grafana_dashboard(self, output_file: str) -> bool:
        """
        Generate and export a Grafana dashboard JSON file.
        
        Args:
            output_file: Path to save the dashboard JSON file
            
        Returns:
            bool: Success indicator
        """
        try:
            generator = GrafanaDashboardGenerator()
            dashboard = generator.create_trader_dashboard("OmegaBTC Trading Simulation")
            return generator.export_dashboard(dashboard, output_file)
        except Exception as e:
            if self.debug_mode:
                print(f"Error generating dashboard: {e}")
            return False

    def schedule_metrics_reporting(self, interval_seconds: int = 300):
        """
        Schedule regular metrics reporting for all traders.
        
        Args:
            interval_seconds: Interval between reports in seconds
        """
        import threading
        
        def report_metrics():
            while True:
                for trader_name in self.traders:
                    self.record_trader_metrics(trader_name)
                time.sleep(interval_seconds)
        
        thread = threading.Thread(target=report_metrics, daemon=True)
        thread.start()

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return super().default(obj)