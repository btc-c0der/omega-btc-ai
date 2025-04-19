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
Grafana metrics formatter for OmegaBTC AI trading simulations.
Prepares metrics in formats suitable for Grafana dashboards.
"""

import datetime
import time
import json
from typing import Dict, List, Any, Optional, Tuple
import numpy as np

class GrafanaMetricsFormatter:
    """
    Formats trading metrics data for Grafana dashboards and time series visualization.
    """
    
    @staticmethod
    def format_trade_time_series(trades: List[Dict[str, Any]]) -> Dict[str, List]:
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
            'entry_prices': [],
            'exit_prices': [],
            'win_loss': [],  # 1 for win, 0 for loss
            'duration': [],  # Trade duration in minutes
            'direction': [],  # 1 for long, -1 for short
            'emotional_states': []
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
            entry_time = trade.get('entry_time')
            exit_time = trade.get('exit_time')
            pnl = float(trade.get('pnl', 0))
            position_size = float(trade.get('position_size', 0))
            leverage = float(trade.get('leverage', 1))
            entry_price = float(trade.get('entry_price', 0))
            exit_price = float(trade.get('exit_price', 0))
            direction = 1 if trade.get('direction') == 'LONG' else -1
            emotional_state = trade.get('emotional_state', 'neutral')
            
            # Calculate trade duration in minutes
            duration = 0
            if entry_time and exit_time:
                entry_dt = datetime.datetime.fromisoformat(entry_time.replace('Z', '+00:00'))
                exit_dt = datetime.datetime.fromisoformat(exit_time.replace('Z', '+00:00'))
                duration = (exit_dt - entry_dt).total_seconds() / 60
            
            # Update cumulative PnL
            cumulative_pnl += pnl
            
            # Append to series
            series['timestamps'].append(exit_time)
            series['pnl'].append(pnl)
            series['cumulative_pnl'].append(cumulative_pnl)
            series['position_sizes'].append(position_size)
            series['leverage'].append(leverage)
            series['entry_prices'].append(entry_price)
            series['exit_prices'].append(exit_price)
            series['win_loss'].append(1 if pnl > 0 else 0)
            series['duration'].append(duration)
            series['direction'].append(direction)
            series['emotional_states'].append(emotional_state)
            
        return series
    
    @staticmethod
    def format_trader_performance_metrics(metrics: List[Dict[str, Any]]) -> Dict[str, List]:
        """
        Format trader performance metrics for time series visualization.
        
        Args:
            metrics: List of metrics dictionaries
            
        Returns:
            Dictionary with time series data for different metrics
        """
        # Initialize time series containers
        series = {
            'timestamps': [],
            'capital': [],
            'win_rate': [],
            'drawdown': [],
            'profit_factor': [],
            'sharpe_ratio': [],
            'risk_appetite': [],
            'confidence': [],
            'emotional_state': [],
            'leverage_used': []
        }
        
        # Sort metrics by timestamp
        sorted_metrics = sorted(metrics, key=lambda m: m.get('timestamp', ''))
        
        # Process each metrics entry
        for metric in sorted_metrics:
            timestamp = metric.get('timestamp')
            if not timestamp:
                continue
                
            # Append to series
            series['timestamps'].append(timestamp)
            series['capital'].append(float(metric.get('capital', 0)))
            series['win_rate'].append(float(metric.get('win_rate', 0)))
            series['drawdown'].append(float(metric.get('max_drawdown', 0)))
            series['profit_factor'].append(float(metric.get('profit_factor', 0)))
            series['sharpe_ratio'].append(float(metric.get('sharpe_ratio', 0)))
            series['risk_appetite'].append(float(metric.get('risk_appetite', 0.5)))
            series['confidence'].append(float(metric.get('confidence', 0.5)))
            series['emotional_state'].append(metric.get('emotional_state', 'neutral'))
            series['leverage_used'].append(float(metric.get('avg_leverage', 1)))
            
        return series
    
    @staticmethod
    def format_exit_type_statistics(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
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
    
    @staticmethod
    def create_influxdb_points(trader_name: str, trader_type: str, trades: List[Dict], metrics: Dict[str, Any]) -> List[Dict]:
        """
        Create InfluxDB data points from trader metrics.
        
        Args:
            trader_name: Name of the trader
            trader_type: Type of trader (aggressive, strategic, newbie)
            trades: List of trade dictionaries
            metrics: Dictionary of metrics
            
        Returns:
            List of InfluxDB data points
        """
        points = []
        
        # Add trade points
        for trade in trades:
            if trade.get('status') != 'CLOSED':
                continue
                
            exit_time = trade.get('exit_time')
            if not exit_time:
                continue
                
            # Create trade point
            points.append({
                'measurement': 'trades',
                'tags': {
                    'trader': trader_name,
                    'trader_type': trader_type,
                    'direction': trade.get('direction', ''),
                    'exit_type': trade.get('exit_type', ''),
                    'emotional_state': trade.get('emotional_state', 'neutral')
                },
                'time': exit_time,
                'fields': {
                    'entry_price': float(trade.get('entry_price', 0)),
                    'exit_price': float(trade.get('exit_price', 0)),
                    'position_size': float(trade.get('position_size', 0)),
                    'leverage': float(trade.get('leverage', 1)),
                    'pnl': float(trade.get('pnl', 0)),
                    'duration_minutes': float(trade.get('duration_minutes', 0)),
                    'win': 1 if float(trade.get('pnl', 0)) > 0 else 0
                }
            })
        
        # Add metrics points
        for timestamp, values in zip(metrics.get('timestamps', []), zip(
            metrics.get('capital', []),
            metrics.get('win_rate', []),
            metrics.get('drawdown', []),
            metrics.get('profit_factor', []),
            metrics.get('sharpe_ratio', []),
            metrics.get('risk_appetite', []),
            metrics.get('confidence', [])
        )):
            capital, win_rate, drawdown, profit_factor, sharpe, risk_appetite, confidence = values
            
            points.append({
                'measurement': 'trader_metrics',
                'tags': {
                    'trader': trader_name,
                    'trader_type': trader_type
                },
                'time': timestamp,
                'fields': {
                    'capital': float(capital),
                    'win_rate': float(win_rate),
                    'drawdown': float(drawdown),
                    'profit_factor': float(profit_factor),
                    'sharpe_ratio': float(sharpe),
                    'risk_appetite': float(risk_appetite),
                    'confidence': float(confidence)
                }
            })
            
        return points
    
    @staticmethod
    def generate_grafana_dashboard_json(traders: List[str]) -> Dict[str, Any]:
        """
        Generate Grafana dashboard JSON configuration.
        
        Args:
            traders: List of trader names
            
        Returns:
            Grafana dashboard JSON configuration
        """
        # Base dashboard template
        dashboard = {
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
            "tags": ["OmegaBTC", "trading"],
            "templating": {
                "list": [
                    {
                        "allValue": None,
                        "current": {
                            "selected": False,
                            "text": "All",
                            "value": "$__all"
                        },
                        "datasource": "InfluxDB",
                        "definition": "SHOW TAG VALUES WITH KEY = \"trader\"",
                        "description": None,
                        "error": None,
                        "hide": 0,
                        "includeAll": True,
                        "label": "Trader",
                        "multi": False,
                        "name": "trader",
                        "options": [],
                        "query": "SHOW TAG VALUES WITH KEY = \"trader\"",
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
            "timepicker": {
                "refresh_intervals": [
                    "5s",
                    "10s",
                    "30s",
                    "1m",
                    "5m",
                    "15m",
                    "30m",
                    "1h",
                    "2h",
                    "1d"
                ]
            },
            "timezone": "",
            "title": "OmegaBTC Trader Profiles Comparison",
            "uid": "omegabtc-traders",
            "version": 1
        }
        
        # Add panels for each trader
        y_pos = 0
        
        # Add PnL panel
        dashboard["panels"].append({
            "aliasColors": {},
            "bars": False,
            "dashLength": 10,
            "dashes": False,
            "datasource": "InfluxDB",
            "fieldConfig": {
                "defaults": {
                    "custom": {}
                },
                "overrides": []
            },
            "fill": 1,
            "fillGradient": 0,
            "gridPos": {
                "h": 8,
                "w": 24,
                "x": 0,
                "y": y_pos
            },
            "hiddenSeries": False,
            "id": 1,
            "legend": {
                "avg": False,
                "current": False,
                "max": False,
                "min": False,
                "show": True,
                "total": False,
                "values": False
            },
            "lines": True,
            "linewidth": 1,
            "nullPointMode": "null",
            "options": {
                "alertThreshold": True
            },
            "percentage": False,
            "pluginVersion": "7.4.0",
            "pointradius": 2,
            "points": False,
            "renderer": "flot",
            "seriesOverrides": [],
            "spaceLength": 10,
            "stack": False,
            "steppedLine": False,
            "targets": [
                {
                    "groupBy": [
                        {
                            "params": [
                                "$__interval"
                            ],
                            "type": "time"
                        },
                        {
                            "params": [
                                "trader"
                            ],
                            "type": "tag"
                        },
                        {
                            "params": [
                                "none"
                            ],
                            "type": "fill"
                        }
                    ],
                    "measurement": "trader_metrics",
                    "orderByTime": "ASC",
                    "policy": "default",
                    "refId": "A",
                    "resultFormat": "time_series",
                    "select": [
                        [
                            {
                                "params": [
                                    "capital"
                                ],
                                "type": "field"
                            },
                            {
                                "params": [],
                                "type": "mean"
                            }
                        ]
                    ],
                    "tags": [
                        {
                            "key": "trader",
                            "operator": "=~",
                            "value": "/^$trader$/"
                        }
                    ]
                }
            ],
            "thresholds": [],
            "timeFrom": None,
            "timeRegions": [],
            "timeShift": None,
            "title": "Trader Capital Over Time",
            "tooltip": {
                "shared": True,
                "sort": 0,
                "value_type": "individual"
            },
            "type": "graph",
            "xaxis": {
                "buckets": None,
                "mode": "time",
                "name": None,
                "show": True,
                "values": []
            },
            "yaxes": [
                {
                    "format": "currencyUSD",
                    "label": None,
                    "logBase": 1,
                    "max": None,
                    "min": None,
                    "show": True
                },
                {
                    "format": "short",
                    "label": None,
                    "logBase": 1,
                    "max": None,
                    "min": None,
                    "show": True
                }
            ],
            "yaxis": {
                "align": False,
                "alignLevel": None
            }
        })
        
        y_pos += 8
        
        # Add Win Rate panel
        dashboard["panels"].append({
            "aliasColors": {},
            "bars": False,
            "dashLength": 10,
            "dashes": False,
            "datasource": "InfluxDB",
            "fieldConfig": {
                "defaults": {
                    "custom": {}
                },
                "overrides": []
            },
            "fill": 1,
            "fillGradient": 0,
            "gridPos": {
                "h": 8,
                "w": 12,
                "x": 0,
                "y": y_pos
            },
            "hiddenSeries": False,
            "id": 2,
            "legend": {
                "avg": False,
                "current": False,
                "max": False,
                "min": False,
                "show": True,
                "total": False,
                "values": False
            },
            "lines": True,
            "linewidth": 1,
            "nullPointMode": "null",
            "options": {
                "alertThreshold": True
            },
            "percentage": False,
            "pluginVersion": "7.4.0",
            "pointradius": 2,
            "points": False,
            "renderer": "flot",
            "seriesOverrides": [],
            "spaceLength": 10,
            "stack": False,
            "steppedLine": False,
            "targets": [
                {
                    "groupBy": [
                        {
                            "params": [
                                "$__interval"
                            ],
                            "type": "time"
                        },
                        {
                            "params": [
                                "trader"
                            ],
                            "type": "tag"
                        },
                        {
                            "params": [
                                "none"
                            ],
                            "type": "fill"
                        }
                    ],
                    "measurement": "trader_metrics",
                    "orderByTime": "ASC",
                    "policy": "default",
                    "refId": "A",
                    "resultFormat": "time_series",
                    "select": [
                        [
                            {
                                "params": [
                                    "win_rate"
                                ],
                                "type": "field"
                            },
                            {
                                "params": [],
                                "type": "mean"
                            }
                        ]
                    ],
                    "tags": [
                        {
                            "key": "trader",
                            "operator": "=~",
                            "value": "/^$trader$/"
                        }
                    ]
                }
            ],
            "thresholds": [],
            "timeFrom": None,
            "timeRegions": [],
            "timeShift": None,
            "title": "Win Rate",
            "tooltip": {
                "shared": True,
                "sort": 0,
                "value_type": "individual"
            },
            "type": "graph",
            "xaxis": {
                "buckets": None,
                "mode": "time",
                "name": None,
                "show": True,
                "values": []
            },
            "yaxes": [
                {
                    "format": "percentunit",
                    "label": None,
                    "logBase": 1,
                    "max": "1",
                    "min": "0",
                    "show": True
                },
                {
                    "format": "short",
                    "label": None,
                    "logBase": 1,
                    "max": None,
                    "min": None,
                    "show": True
                }
            ],
            "yaxis": {
                "align": False,
                "alignLevel": None
            }
        })
        
        # Add Drawdown panel
        dashboard["panels"].append({
            "aliasColors": {},
            "bars": False,
            "dashLength": 10,
            "dashes": False,
            "datasource": "InfluxDB",
            "fieldConfig": {
                "defaults": {
                    "custom": {}
                },
                "overrides": []
            },
            "fill": 1,
            "fillGradient": 0,
            "gridPos": {
                "h": 8,
                "w": 12,
                "x": 12,
                "y": y_pos
            },
            "hiddenSeries": False,
            "id": 3,
            "legend": {
                "avg": False,
                "current": False,
                "max": False,
                "min": False,
                "show": True,
                "total": False,
                "values": False
            },
            "lines": True,
            "linewidth": 1,
            "nullPointMode": "null",
            "options": {
                "alertThreshold": True
            },
            "percentage": False,
            "pluginVersion": "7.4.0",
            "pointradius": 2,
            "points": False,
            "renderer": "flot",
            "seriesOverrides": [],
            "spaceLength": 10,
            "stack": False,
            "steppedLine": False,
            "targets": [
                {
                    "groupBy": [
                        {
                            "params": [
                                "$__interval"
                            ],
                            "type": "time"
                        },
                        {
                            "params": [
                                "trader"
                            ],
                            "type": "tag"
                        },
                        {
                            "params": [
                                "none"
                            ],
                            "type": "fill"
                        }
                    ],
                    "measurement": "trader_metrics",
                    "orderByTime": "ASC",
                    "policy": "default",
                    "refId": "A",
                    "resultFormat": "time_series",
                    "select": [
                        [
                            {
                                "params": [
                                    "drawdown"
                                ],
                                "type": "field"
                            },
                            {
                                "params": [],
                                "type": "mean"
                            }
                        ]
                    ],
                    "tags": [
                        {
                            "key": "trader",
                            "operator": "=~",
                            "value": "/^$trader$/"
                        }
                    ]
                }
            ],
            "thresholds": [],
            "timeFrom": None,
            "timeRegions": [],
            "timeShift": None,
            "title": "Drawdown",
            "tooltip": {
                "shared": True,
                "sort": 0,
                "value_type": "individual"
            },
            "type": "graph",
            "xaxis": {
                "buckets": None,
                "mode": "time",
                "name": None,
                "show": True,
                "values": []
            },
            "yaxes": [
                {
                    "format": "percentunit",
                    "label": None,
                    "logBase": 1,
                    "max": "1",
                    "min": "0",
                    "show": True
                },
                {
                    "format": "short",
                    "label": None,
                    "logBase": 1,
                    "max": None,
                    "min": None,
                    "show": True
                }
            ],
            "yaxis": {
                "align": False,
                "alignLevel": None
            }
        })
        
        y_pos += 8
        
        # Add exit type statistics panel
        dashboard["panels"].append({
            "datasource": "InfluxDB",
            "fieldConfig": {
                "defaults": {
                    "color": {
                        "mode": "palette-classic"
                    },
                    "custom": {
                        "hideFrom": {
                            "legend": False,
                            "tooltip": False,
                            "viz": False
                        }
                    },
                    "mappings": []
                },
                "overrides": []
            },
            "gridPos": {
                "h": 8,
                "w": 12,
                "x": 0,
                "y": y_pos
            },
            "id": 4,
            "options": {
                "displayLabels": ["percent"],
                "legend": {
                    "displayMode": "list",
                    "placement": "right",
                    "values": ["percent"]
                },
                "pieType": "pie",
                "reduceOptions": {
                    "calcs": ["sum"],
                    "fields": "",
                    "values": False
                },
                "tooltip": {
                    "mode": "single"
                }
            },
            "pluginVersion": "7.5.7",
            "targets": [
                {
                    "groupBy": [
                        {
                            "params": [
                                "exit_type"
                            ],
                            "type": "tag"
                        }
                    ],
                    "measurement": "trades",
                    "orderByTime": "ASC",
                    "policy": "default",
                    "refId": "A",
                    "resultFormat": "time_series",
                    "select": [
                        [
                            {
                                "params": [
                                    "value"
                                ],
                                "type": "field"
                            },
                            {
                                "params": [],
                                "type": "count"
                            }
                        ]
                    ],
                    "tags": [
                        {
                            "key": "trader",
                            "operator": "=~",
                            "value": "/^$trader$/"
                        }
                    ]
                }
            ],
            "title": "Exit Type Distribution",
            "type": "piechart"
        })
        
        # Add emotional state distribution panel
        dashboard["panels"].append({
            "datasource": "InfluxDB",
            "fieldConfig": {
                "defaults": {
                    "color": {
                        "mode": "palette-classic"
                    },
                    "custom": {
                        "hideFrom": {
                            "legend": False,
                            "tooltip": False,
                            "viz": False
                        }
                    },
                    "mappings": []
                },
                "overrides": []
            },
            "gridPos": {
                "h": 8,
                "w": 12,
                "x": 12,
                "y": y_pos
            },
            "id": 5,
            "options": {
                "displayLabels": ["percent"],
                "legend": {
                    "displayMode": "list",
                    "placement": "right",
                    "values": ["percent"]
                },
                "pieType": "pie",
                "reduceOptions": {
                    "calcs": ["sum"],
                    "fields": "",
                    "values": False
                },
                "tooltip": {
                    "mode": "single"
                }
            },
            "pluginVersion": "7.5.7",
            "targets": [
                {
                    "groupBy": [
                        {
                            "params": [
                                "emotional_state"
                            ],
                            "type": "tag"
                        }
                    ],
                    "measurement": "trades",
                    "orderByTime": "ASC",
                    "policy": "default",
                    "refId": "A",
                    "resultFormat": "time_series",
                    "select": [
                        [
                            {
                                "params": [
                                    "value"
                                ],
                                "type": "field"
                            },
                            {
                                "params": [],
                                "type": "count"
                            }
                        ]
                    ],
                    "tags": [
                        {
                            "key": "trader",
                            "operator": "=~",
                            "value": "/^$trader$/"
                        }
                    ]
                }
            ],
            "title": "Emotional State Distribution",
            "type": "piechart"
        })
        
        return dashboard

