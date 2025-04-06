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
from dash import Input, Output, State, ctx, no_update, html, dcc, callback_context
from typing import Dict, List, Any, Tuple, Optional
import dash_bootstrap_components as dbc
import random
import plotly.graph_objects as go
import pandas as pd
import numpy as np

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
    create_health_indicators,
    create_empty_figure
)
from .test_runner import S0NN3TTestRunner

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
    
    # Test runner instance
    test_runner = S0NN3TTestRunner()
    
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
        if not ctx.triggered or data is None or "history" not in data or not data["history"]:
            # Return an empty figure on first load
            return {}
        
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
            if not ctx.triggered or data is None or "history" not in data or not data["history"]:
                # Return an empty figure on first load
                return {}
            
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
        if not ctx.triggered or data is None or "current" not in data or not data["current"]:
            # Return an empty figure on first load
            return {}
        
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
        if not ctx.triggered or data is None or "current" not in data or not data["current"]:
            # Return an empty figure on first load
            return {}
        
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
        if not ctx.triggered or data is None or "current" not in data or not data["current"]:
            # Return an empty figure on first load
            return {}
        
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
        if not ctx.triggered or data is None or "current" not in data or not data["current"]:
            # Return an empty figure on first load
            return {}
        
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
        if not ctx.triggered or data is None or "current" not in data or not data["current"]:
            # Return an empty figure on first load
            return {}
        
        # Create metrics table
        figure = create_metrics_table(data["current"])
        
        return figure
    
    # Update terminal output
    @app.callback(
        Output("terminal-text", "children"),
        Input("metrics-interval", "n_intervals")
    )
    def update_terminal_output(n_intervals):
        """Update the terminal output with the latest lines."""
        global terminal_lines
        
        # Get latest terminal lines (limited to last 20)
        latest_lines = terminal_lines[-20:]
        
        # Create terminal output children elements
        terminal_children = [
            html.Span("$", className="prompt"), " ",
            html.Span("quantum-dashboard --start", className="command"),
            html.Br(),
            html.Br()
        ]
        
        # Add each line
        for line in latest_lines:
            terminal_children.append(line)
            terminal_children.append(html.Br())
        
        # Add prompt and cursor at the end
        terminal_children.extend([
            html.Span("$", className="prompt"), " ",
            html.Span("█", className="cursor")
        ])
        
        return terminal_children
    
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
    
    # Setup test runner callbacks
    @app.callback(
        [
            Output("test-terminal-text", "children"),
            Output("test-progress-container", "style"),
            Output("test-progress-bar", "value", allow_duplicate=True),
            Output("test-progress-text", "children", allow_duplicate=True),
            Output("test-results-container", "children"),
            Output("test-runner-store", "data")
        ],
        [
            Input("run-tests-btn", "n_clicks"),
            Input("omega-mode-btn", "n_clicks"),
            Input("omega-k8s-btn", "n_clicks")
        ],
        [
            State("test-dimensions-checklist", "value"),
            State("fancy-visuals-switch", "value"),
            State("celebration-switch", "value"),
            State("test-runner-store", "data")
        ],
        prevent_initial_call=True
    )
    def handle_test_runner_actions(
        run_clicks, omega_clicks, omega_k8s_clicks,
        test_dimensions, fancy_visuals, celebration, store_data
    ):
        """Handle test runner button actions."""
        # Initialize store data if not present
        if store_data is None:
            store_data = {
                "last_run": None,
                "running": False,
                "progress": 0,
                "latest_results": None
            }
        
        # Check which button was clicked
        triggered = ctx.triggered_id
        
        # If no button was clicked, return current state
        if triggered is None:
            # Return empty terminal with initial prompt
            terminal_children = [
                html.Span("$", className="prompt"), " ",
                html.Span("s0nn3t-test-runner --ready", className="command"),
                html.Br(), html.Br(),
                "[Awaiting commands...]",
                html.Br(),
                html.Span("$", className="prompt"), " ",
                html.Span("█", className="cursor")
            ]
            
            return (
                terminal_children,
                {"display": "none"},
                0,
                "Initializing tests...",
                html.P("No test results available", className="no-results-message"),
                store_data
            )
        
        # Start progress indicators
        progress_style = {"display": "block"}
        progress_value = 10
        progress_text = "Initializing S0NN3T Test Runner..."
        
        # Handle run tests button
        if triggered == "run-tests-btn" and run_clicks:
            # Update progress
            progress_value = 20
            progress_text = f"Running tests in dimensions: {', '.join(test_dimensions)}"
            store_data["running"] = True
            store_data["progress"] = progress_value
            
            # Create a thread to run tests
            import threading
            
            def run_tests_thread():
                nonlocal test_runner
                # Run tests
                result = test_runner.run_tests(
                    dimensions=test_dimensions,
                    fancy_visuals=fancy_visuals,
                    celebration=celebration
                )
                
                # Update store with results
                store_data["latest_results"] = {
                    "success": result.success,
                    "duration": result.duration,
                    "timestamp": result.timestamp,
                    "dimensions": result.test_dimensions
                }
                store_data["running"] = False
                store_data["progress"] = 100
                store_data["last_run"] = result.timestamp
            
            # Start the thread
            test_thread = threading.Thread(target=run_tests_thread)
            test_thread.daemon = True
            test_thread.start()
        
        # Handle OMEGA mode button
        elif triggered == "omega-mode-btn" and omega_clicks:
            # Update progress
            progress_value = 15
            progress_text = "Initializing 0M3G4 Mode..."
            store_data["running"] = True
            store_data["progress"] = progress_value
            
            # Run OMEGA mode in a thread
            test_runner.run_omega_mode(k8s_mode=False)
        
        # Handle OMEGA-K8s mode button
        elif triggered == "omega-k8s-btn" and omega_k8s_clicks:
            # Update progress
            progress_value = 15
            progress_text = "Initializing 0M3G4-K8s Matrix Mode..."
            store_data["running"] = True
            store_data["progress"] = progress_value
            
            # Run OMEGA-K8s mode in a thread
            test_runner.run_omega_mode(k8s_mode=True)
        
        # Get terminal output
        terminal_lines = test_runner.get_terminal_output(50)
        if not terminal_lines:
            terminal_lines = ["[Awaiting command execution...]"]
        
        # Create terminal children elements
        terminal_children = [
            html.Span("$", className="prompt"), " ",
            html.Span("s0nn3t-test-runner --executing", className="command"),
            html.Br(), html.Br()
        ]
        
        # Add each line from the test runner output
        for line in terminal_lines:
            terminal_children.append(line)
            terminal_children.append(html.Br())
        
        # Add prompt and cursor at the end
        terminal_children.extend([
            html.Span("$", className="prompt"), " ",
            html.Span("█", className="cursor")
        ])
        
        # Create test results display
        if store_data.get("latest_results"):
            results = store_data["latest_results"]
            results_display = html.Div([
                html.Div(
                    className="test-result-item",
                    children=[
                        html.Span("Status:", className="test-result-label"),
                        html.Span(
                            "SUCCESS" if results["success"] else "FAILURE",
                            className=f"test-result-value {'test-result-success' if results['success'] else 'test-result-failure'}"
                        )
                    ]
                ),
                html.Div(
                    className="test-result-item",
                    children=[
                        html.Span("Execution Time:", className="test-result-label"),
                        html.Span(f"{results['duration']:.2f}s", className="test-result-value")
                    ]
                ),
                html.Div(
                    className="test-result-item",
                    children=[
                        html.Span("Dimensions Tested:", className="test-result-label"),
                        html.Span(", ".join(results["dimensions"]), className="test-result-value")
                    ]
                ),
                html.Div(
                    className="test-result-item",
                    children=[
                        html.Span("Timestamp:", className="test-result-label"),
                        html.Span(results["timestamp"], className="test-result-value")
                    ]
                )
            ])
        else:
            results_display = html.P("No test results available", className="no-results-message")
        
        # Return updated components
        return (
            terminal_children,
            progress_style,
            progress_value,
            progress_text,
            results_display,
            store_data
        )
    
    # Setup progress bar update callback
    @app.callback(
        [
            Output("test-progress-bar", "value"),
            Output("test-progress-text", "children")
        ],
        Input("metrics-interval", "n_intervals"),
        State("test-runner-store", "data")
    )
    def update_test_progress(n_intervals, store_data):
        """Update the test progress bar."""
        if store_data is None or not store_data.get("running", False):
            return no_update, no_update
        
        # Simulate progress by incrementing current progress
        current_progress = store_data.get("progress", 0)
        if current_progress < 95:
            new_progress = min(95, current_progress + 5)
        else:
            new_progress = current_progress
        
        # Update text based on progress
        if new_progress < 30:
            text = "Initializing tests..."
        elif new_progress < 50:
            text = "Running test cases..."
        elif new_progress < 70:
            text = "Analyzing results..."
        elif new_progress < 90:
            text = "Generating report..."
        else:
            text = "Finalizing..."
        
        # Store updated progress
        store_data["progress"] = new_progress
        
        return new_progress, text


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