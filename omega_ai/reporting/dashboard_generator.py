#!/usr/bin/env python3

"""
Dashboard generator for OmegaBTC AI Grafana visualizations.
Provides reusable templates for panel creation with proper positioning.
"""

import json
from typing import Dict, List, Any

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
            # Create trader-specific panels...
            # Add 2-4 panels per row
            self.current_y += 8
        
        return dashboard

    def export_dashboard(self, dashboard: Dict, output_file: str) -> bool:
        """Export dashboard to a JSON file."""
        try:
            with open(output_file, 'w') as f:
                json.dump(dashboard, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting dashboard: {e}")
            return False