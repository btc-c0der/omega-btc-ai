#!/usr/bin/env python3
"""
Quantum 5D QA Dashboard Callbacks
--------------------------------

This module provides the callback handlers for the Quantum 5D QA Dashboard.
"""

import time
import datetime
import threading
import logging
import json
from dash import Input, Output, State, ctx, no_update, html
from typing import Dict, List, Any, Tuple, Optional

# Import configuration and modules
from .config import DASHBOARD_CONFIG, quantum_theme, ANSI_COLORS
from .metrics import metrics_store, collect_metrics
from .visualization import (
    create_hyperspatial_trend_graph,
    create_dimension_graph,
    create_stability_gauge,
    create_coherence_gauge,
    create_risk_indicator,
    create_entanglement_visualization,
    create_metrics_table,
    create_terminal_output,
    create_health_indicators
)

# Set up logging
logger = logging.getLogger("Quantum5DQADashboard.Callbacks")

# Terminal output storage
terminal_lines = [
    "Initializing Quantum 5D QA Dashboard...",
    "Accessing 5 dimensional metrics...",
    "Calculating quantum entanglement...",
    "Ready."
]


def register_callbacks(app):
    """Register all dashboard callbacks."""
    
    # Metrics collection thread
    metrics_thread = None
    
    # Define metrics update function
    def metrics_collector():
        """Background thread to collect metrics."""
        logger.info("Starting metrics collection thread")
        
        # Add to terminal output
        add_terminal_line("Starting metrics collection...")
        
        while True:
            try:
                # Collect metrics
                logger.info("Collecting metrics")
                add_terminal_line("Collecting quantum metrics...")
                
                # Get new metrics
                metrics = collect_metrics()
                
                # Update metrics store
                metrics_dict = metrics.to_dict()
                
                # Update metrics store
                metrics_store["current"] = metrics_dict
                metrics_store["history"].append(metrics_dict)
                metrics_store["last_update"] = datetime.datetime.now().isoformat()
                
                # Limit history length
                history_limit = DASHBOARD_CONFIG["metrics_history_limit"]
                if len(metrics_store["history"]) > history_limit:
                    metrics_store["history"] = metrics_store["history"][-history_limit:]
                
                # Add to terminal output
                stability = metrics_dict.get("dimensional_stability", 0)
                add_terminal_line(f"Dimensional stability: {stability:.1f}%")
                
                # Check for warnings
                if stability < DASHBOARD_CONFIG["threshold_warning"]:
                    add_terminal_line(f"WARNING: Dimensional stability below warning threshold", "warning")
                
                if stability < DASHBOARD_CONFIG["threshold_critical"]:
                    add_terminal_line(f"CRITICAL: Dimensional stability below critical threshold!", "error")
                
                risk = metrics_dict.get("dimensional_collapse_risk", 0)
                if risk > 50:
                    add_terminal_line(f"WARNING: Collapse risk at {risk:.1f}%", "warning")
                
                # Sleep for the metrics collection interval
                time.sleep(DASHBOARD_CONFIG["metrics_collection_interval"])
                
            except Exception as e:
                # Log error
                logger.error(f"Error collecting metrics: {e}")
                add_terminal_line(f"Error collecting metrics: {e}", "error")
                
                # Sleep for a bit before trying again
                time.sleep(5)
    
    # Start the metrics collection thread when the app starts
    @app.callback(
        Output("metrics-store", "data"),
        Input("metrics-interval", "n_intervals")
    )
    def update_metrics_store(n_intervals):
        """Update the metrics store and start the collection thread if needed."""
        nonlocal metrics_thread
        
        # Start the metrics collection thread if it's not already running
        if metrics_thread is None or not metrics_thread.is_alive():
            metrics_thread = threading.Thread(target=metrics_collector, daemon=True)
            metrics_thread.start()
            logger.info("Started metrics collection thread")
        
        # Return the current metrics
        return metrics_store
    
    # Update hyperspatial trend graph
    @app.callback(
        Output("hyperspatial-trend-graph", "figure"),
        Input("metrics-store", "data")
    )
    def update_hyperspatial_trend_graph(data):
        """Update the hyperspatial trend graph with the latest metrics."""
        if data is None or "history" not in data or not data["history"]:
            return no_update
        
        # Create hyperspatial trend graph
        figure = create_hyperspatial_trend_graph(data["history"])
        
        return figure
    
    # Update dimension graphs
    dimensions = ["quality", "coverage", "performance", "security"]
    for dimension in dimensions:
        @app.callback(
            Output(f"{dimension}-dimension-graph", "figure"),
            Input("metrics-store", "data")
        )
        def update_dimension_graph(data, dimension=dimension):
            """Update the dimension graph with the latest metrics."""
            if data is None or "history" not in data or not data["history"]:
                return no_update
            
            # Create dimension graph
            figure = create_dimension_graph(dimension, data["history"])
            
            return figure
    
    # Update stability gauge
    @app.callback(
        Output("stability-gauge", "figure"),
        Input("metrics-store", "data")
    )
    def update_stability_gauge(data):
        """Update the stability gauge with the latest metrics."""
        if data is None or "current" not in data or not data["current"]:
            return no_update
        
        # Create stability gauge
        figure = create_stability_gauge(data["current"])
        
        return figure
    
    # Update coherence gauge
    @app.callback(
        Output("coherence-gauge", "figure"),
        Input("metrics-store", "data")
    )
    def update_coherence_gauge(data):
        """Update the coherence gauge with the latest metrics."""
        if data is None or "current" not in data or not data["current"]:
            return no_update
        
        # Create coherence gauge
        figure = create_coherence_gauge(data["current"])
        
        return figure
    
    # Update risk indicator
    @app.callback(
        Output("risk-indicator", "figure"),
        Input("metrics-store", "data")
    )
    def update_risk_indicator(data):
        """Update the risk indicator with the latest metrics."""
        if data is None or "current" not in data or not data["current"]:
            return no_update
        
        # Create risk indicator
        figure = create_risk_indicator(data["current"])
        
        return figure
    
    # Update entanglement visualization
    @app.callback(
        Output("entanglement-visualization", "figure"),
        Input("metrics-store", "data")
    )
    def update_entanglement_visualization(data):
        """Update the entanglement visualization with the latest metrics."""
        if data is None or "current" not in data or not data["current"]:
            return no_update
        
        # Create entanglement visualization
        figure = create_entanglement_visualization(data["current"])
        
        return figure
    
    # Update metrics table
    @app.callback(
        Output("metrics-table", "figure"),
        Input("metrics-store", "data")
    )
    def update_metrics_table(data):
        """Update the metrics table with the latest metrics."""
        if data is None or "current" not in data or not data["current"]:
            return no_update
        
        # Create metrics table
        figure = create_metrics_table(data["current"])
        
        return figure
    
    # Update terminal output
    @app.callback(
        Output("terminal-output", "children"),
        Input("metrics-interval", "n_intervals")
    )
    def update_terminal_output(n_intervals):
        """Update the terminal output with the latest lines."""
        global terminal_lines
        
        # Get latest terminal lines (limited to last 20)
        latest_lines = terminal_lines[-20:]
        
        # Create terminal output HTML
        terminal_html = create_terminal_output(latest_lines)
        
        # Use iframe to safely render HTML content
        return html.Iframe(
            srcDoc=terminal_html,
            style={"border": "none", "width": "100%", "height": "100%"},
            sandbox="allow-scripts"
        )
    
    # Update header metrics
    @app.callback(
        [
            Output("header-stability", "children"),
            Output("header-stability", "style"),
            Output("header-risk", "children"),
            Output("header-risk", "style"),
            Output("header-last-update", "children")
        ],
        Input("metrics-store", "data")
    )
    def update_header_metrics(data):
        """Update the header metrics with the latest data."""
        if data is None or "current" not in data or not data["current"]:
            return no_update, no_update, no_update, no_update, no_update
        
        # Get current metrics
        current = data["current"]
        
        # Get stability
        stability = current.get("dimensional_stability", 0)
        
        # Determine stability color
        if stability >= 80:
            stability_color = quantum_theme["success"]
        elif stability >= 50:
            stability_color = quantum_theme["warning"]
        else:
            stability_color = quantum_theme["error"]
        
        # Get risk
        risk = current.get("dimensional_collapse_risk", 0)
        
        # Determine risk color
        if risk <= 20:
            risk_color = quantum_theme["success"]
        elif risk <= 50:
            risk_color = quantum_theme["warning"]
        else:
            risk_color = quantum_theme["error"]
        
        # Get last update
        last_update = data.get("last_update", "Unknown")
        
        # If last update is a timestamp, format it
        if isinstance(last_update, str) and "T" in last_update:
            try:
                dt = datetime.datetime.fromisoformat(last_update)
                last_update = dt.strftime("%H:%M:%S")
            except:
                pass
        
        return (
            f"{stability:.1f}%",
            {"color": stability_color},
            f"{risk:.1f}%",
            {"color": risk_color},
            last_update
        )
    
    # Update dimension indicators
    @app.callback(
        [
            Output("indicator-value-quality", "children"),
            Output("indicator-status-quality", "children"),
            Output("indicator-status-quality", "style"),
            Output("indicator-value-coverage", "children"),
            Output("indicator-status-coverage", "children"),
            Output("indicator-status-coverage", "style"),
            Output("indicator-value-performance", "children"),
            Output("indicator-status-performance", "children"),
            Output("indicator-status-performance", "style"),
            Output("indicator-value-security", "children"),
            Output("indicator-status-security", "children"),
            Output("indicator-status-security", "style")
        ],
        Input("metrics-store", "data")
    )
    def update_dimension_indicators(data):
        """Update the dimension indicators with the latest metrics."""
        if data is None or "current" not in data or not data["current"]:
            return [no_update] * 12
        
        # Get indicators
        indicators = create_health_indicators(data["current"])
        
        # Extract values for each dimension
        outputs = []
        for indicator in indicators:
            outputs.append(f"{indicator['value']:.1f}%")
            outputs.append(indicator["status"])
            outputs.append({"color": indicator["color"]})
        
        return outputs
    
    # Update status
    @app.callback(
        [
            Output("status-value", "children"),
            Output("status-value", "className")
        ],
        Input("metrics-store", "data")
    )
    def update_status(data):
        """Update the status indicator based on metrics."""
        if data is None or "current" not in data or not data["current"]:
            return "Unknown", "status-value status-unknown"
        
        # Get current metrics
        current = data["current"]
        
        # Get stability and risk
        stability = current.get("dimensional_stability", 0)
        risk = current.get("dimensional_collapse_risk", 0)
        
        # Determine status
        if stability >= 80 and risk <= 20:
            return "Stable", "status-value status-stable"
        elif stability >= 50 and risk <= 50:
            return "Warning", "status-value status-warning"
        else:
            return "Critical", "status-value status-critical"


def add_terminal_line(line: str, level: str = "info") -> None:
    """Add a line to the terminal output with an ANSI color.
    
    Args:
        line: The line to add
        level: The log level (info, warning, error, success)
    """
    global terminal_lines
    
    # Get ANSI color
    color = ANSI_COLORS.get(level, "")
    reset = ANSI_COLORS.get("reset", "")
    
    # Create colored line
    colored_line = f"{color}{line}{reset}"
    
    # Add timestamp
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    timestamped_line = f"[{timestamp}] {colored_line}"
    
    # Add to terminal lines
    terminal_lines.append(timestamped_line)
    
    # Limit the number of lines
    if len(terminal_lines) > 100:
        terminal_lines = terminal_lines[-100:] 