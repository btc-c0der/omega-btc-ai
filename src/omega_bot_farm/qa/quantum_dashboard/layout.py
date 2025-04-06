#!/usr/bin/env python3
"""
Quantum 5D QA Dashboard Layout
-----------------------------

This module provides the layout components for the Quantum 5D QA Dashboard.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Dict, List, Any, Optional

# Import configuration and visualization functions
from .config import DASHBOARD_CONFIG, quantum_theme
from .visualization import (
    create_terminal_output,
    create_health_indicators
)


def create_header() -> html.Div:
    """Create dashboard header component with title and status."""
    header = html.Div(
        className="quantum-header",
        children=[
            html.Div(
                className="title-container",
                children=[
                    html.H1("Quantum 5D QA Dashboard", className="dashboard-title"),
                    html.Div(
                        className="status-container",
                        children=[
                            html.Span("Status: ", className="status-label"),
                            html.Span("Online", id="status-value", className="status-value")
                        ]
                    )
                ]
            ),
            html.Div(
                className="header-metrics",
                children=[
                    html.Div(
                        className="header-metric",
                        children=[
                            html.Span("Dimensional Stability:", className="metric-label"),
                            html.Span("--", id="header-stability", className="metric-value")
                        ]
                    ),
                    html.Div(
                        className="header-metric",
                        children=[
                            html.Span("Collapse Risk:", className="metric-label"),
                            html.Span("--", id="header-risk", className="metric-value")
                        ]
                    ),
                    html.Div(
                        className="header-metric",
                        children=[
                            html.Span("Last Update:", className="metric-label"),
                            html.Span("--", id="header-last-update", className="metric-value")
                        ]
                    )
                ]
            )
        ]
    )
    
    return header


def create_dimension_indicators(metrics: Optional[Dict[str, Any]] = None) -> html.Div:
    """Create dimension health indicators component."""
    # Get indicators
    indicators = []
    if metrics:
        indicators = create_health_indicators(metrics)
    else:
        # Create default indicators
        for dim in ["Quality", "Coverage", "Performance", "Security"]:
            indicators.append({
                "name": dim,
                "value": 0,
                "status": "UNKNOWN",
                "color": quantum_theme["text"],
                "icon": "?",
                "description": f"{dim} dimension status"
            })
    
    # Create indicator cards
    indicator_cards = []
    for indicator in indicators:
        card = dbc.Card(
            className="dimension-indicator",
            style={"borderColor": indicator["color"]},
            children=[
                dbc.CardBody([
                    html.Div(
                        className="indicator-header",
                        children=[
                            html.Span(indicator["icon"], className="indicator-icon"),
                            html.H4(indicator["name"], className="indicator-title")
                        ]
                    ),
                    html.Div(
                        className="indicator-value-container",
                        children=[
                            html.Span(
                                f"{indicator['value']:.1f}%", 
                                id=f"indicator-value-{indicator['name'].lower()}", 
                                className="indicator-value"
                            ),
                            html.Span(
                                indicator["status"], 
                                id=f"indicator-status-{indicator['name'].lower()}", 
                                className="indicator-status",
                                style={"color": indicator["color"]}
                            )
                        ]
                    ),
                    html.P(indicator["description"], className="indicator-description")
                ])
            ]
        )
        indicator_cards.append(card)
    
    # Create indicators container
    indicators_container = html.Div(
        className="dimension-indicators-container",
        children=indicator_cards
    )
    
    return indicators_container


def create_hyperspatial_trend_card() -> dbc.Card:
    """Create hyperspatial trend visualization card."""
    card = dbc.Card(
        className="visualization-card",
        children=[
            dbc.CardHeader(
                html.H3("5D Hyperspatial Trend", className="card-title")
            ),
            dbc.CardBody(
                dcc.Graph(
                    id="hyperspatial-trend-graph",
                    figure={},
                    config={'displayModeBar': False},
                    className="visualization-graph"
                )
            )
        ]
    )
    
    return card


def create_dimension_graph_card(dimension: str, label: str) -> dbc.Card:
    """Create dimension graph card for time series visualization."""
    card = dbc.Card(
        className="visualization-card",
        children=[
            dbc.CardHeader(
                html.H3(f"{label} Dimension", className="card-title")
            ),
            dbc.CardBody(
                dcc.Graph(
                    id=f"{dimension}-dimension-graph",
                    figure={},
                    config={'displayModeBar': False},
                    className="visualization-graph"
                )
            )
        ]
    )
    
    return card


def create_stability_card() -> dbc.Card:
    """Create stability gauge card."""
    card = dbc.Card(
        className="visualization-card",
        children=[
            dbc.CardHeader(
                html.H3("Dimensional Stability", className="card-title")
            ),
            dbc.CardBody(
                dcc.Graph(
                    id="stability-gauge",
                    figure={},
                    config={'displayModeBar': False},
                    className="visualization-graph"
                )
            )
        ]
    )
    
    return card


def create_coherence_card() -> dbc.Card:
    """Create quantum coherence gauge card."""
    card = dbc.Card(
        className="visualization-card",
        children=[
            dbc.CardHeader(
                html.H3("Quantum Coherence", className="card-title")
            ),
            dbc.CardBody(
                dcc.Graph(
                    id="coherence-gauge",
                    figure={},
                    config={'displayModeBar': False},
                    className="visualization-graph"
                )
            )
        ]
    )
    
    return card


def create_risk_card() -> dbc.Card:
    """Create dimensional collapse risk gauge card."""
    card = dbc.Card(
        className="visualization-card",
        children=[
            dbc.CardHeader(
                html.H3("Dimensional Collapse Risk", className="card-title")
            ),
            dbc.CardBody(
                dcc.Graph(
                    id="risk-indicator",
                    figure={},
                    config={'displayModeBar': False},
                    className="visualization-graph"
                )
            )
        ]
    )
    
    return card


def create_entanglement_card() -> dbc.Card:
    """Create entanglement factor visualization card."""
    card = dbc.Card(
        className="visualization-card",
        children=[
            dbc.CardHeader(
                html.H3("Entanglement Factor", className="card-title")
            ),
            dbc.CardBody(
                dcc.Graph(
                    id="entanglement-visualization",
                    figure={},
                    config={'displayModeBar': False},
                    className="visualization-graph"
                )
            )
        ]
    )
    
    return card


def create_metrics_table_card() -> dbc.Card:
    """Create metrics table card."""
    card = dbc.Card(
        className="visualization-card",
        children=[
            dbc.CardHeader(
                html.H3("Quantum Metrics Summary", className="card-title")
            ),
            dbc.CardBody(
                dcc.Graph(
                    id="metrics-table",
                    figure={},
                    config={'displayModeBar': False},
                    className="visualization-graph"
                )
            )
        ]
    )
    
    return card


def create_terminal_card() -> dbc.Card:
    """Create terminal output card with matrix-like visualization."""
    card = dbc.Card(
        className="visualization-card terminal-card",
        children=[
            dbc.CardHeader(
                html.H3("Quantum Matrix Monitor", className="card-title")
            ),
            dbc.CardBody(
                html.Div(
                    id="terminal-output",
                    className="terminal-output",
                    children=html.Iframe(
                        srcDoc=create_terminal_output(),
                        style={"border": "none", "width": "100%", "height": "100%"},
                        sandbox="allow-scripts"
                    )
                )
            )
        ]
    )
    
    return card


def create_dashboard_layout() -> html.Div:
    """Create the main dashboard layout."""
    # Create header
    header = create_header()
    
    # Create dimension indicators
    indicators = create_dimension_indicators()
    
    # Create hyperspatial trend card
    hyperspatial_trend_card = create_hyperspatial_trend_card()
    
    # Create dimension graph cards
    quality_card = create_dimension_graph_card("quality", "Quality")
    coverage_card = create_dimension_graph_card("coverage", "Coverage")
    performance_card = create_dimension_graph_card("performance", "Performance")
    security_card = create_dimension_graph_card("security", "Security")
    
    # Create gauge cards
    stability_card = create_stability_card()
    coherence_card = create_coherence_card()
    risk_card = create_risk_card()
    
    # Create entanglement card
    entanglement_card = create_entanglement_card()
    
    # Create metrics table card
    metrics_table_card = create_metrics_table_card()
    
    # Create terminal card
    terminal_card = create_terminal_card()
    
    # Create dashboard layout
    dashboard = html.Div(
        className="quantum-dashboard",
        children=[
            # Header
            header,
            
            # Main content
            html.Div(
                className="dashboard-content",
                children=[
                    # Dimension indicators
                    indicators,
                    
                    # First row
                    html.Div(
                        className="dashboard-row",
                        children=[
                            html.Div(
                                className="card-container large",
                                children=hyperspatial_trend_card
                            ),
                            html.Div(
                                className="card-container medium",
                                children=stability_card
                            ),
                            html.Div(
                                className="card-container medium",
                                children=risk_card
                            )
                        ]
                    ),
                    
                    # Second row
                    html.Div(
                        className="dashboard-row",
                        children=[
                            html.Div(
                                className="card-container medium",
                                children=quality_card
                            ),
                            html.Div(
                                className="card-container medium",
                                children=coverage_card
                            ),
                            html.Div(
                                className="card-container medium",
                                children=entanglement_card
                            )
                        ]
                    ),
                    
                    # Third row
                    html.Div(
                        className="dashboard-row",
                        children=[
                            html.Div(
                                className="card-container medium",
                                children=performance_card
                            ),
                            html.Div(
                                className="card-container medium",
                                children=security_card
                            ),
                            html.Div(
                                className="card-container medium",
                                children=coherence_card
                            )
                        ]
                    ),
                    
                    # Fourth row
                    html.Div(
                        className="dashboard-row",
                        children=[
                            html.Div(
                                className="card-container medium",
                                children=metrics_table_card
                            ),
                            html.Div(
                                className="card-container large",
                                children=terminal_card
                            )
                        ]
                    )
                ]
            ),
            
            # Hidden elements for storing data
            dcc.Store(id="metrics-store"),
            dcc.Interval(
                id="metrics-interval",
                interval=DASHBOARD_CONFIG["ui_refresh_interval"] * 1000,  # Convert to milliseconds
                n_intervals=0
            )
        ]
    )
    
    return dashboard 