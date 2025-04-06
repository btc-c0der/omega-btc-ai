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
import plotly.graph_objects as go
from . import config
from .visualization import (
    create_terminal_output,
    create_health_indicators,
    create_empty_figure
)
from .test_runner import TestDimension


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
                "color": config.quantum_theme["text"],
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
                    className="terminal-output terminal-container",
                    children=[
                        html.Div(
                            className="terminal-header",
                            children=[
                                html.Div(className="terminal-button red"),
                                html.Div(className="terminal-button yellow"),
                                html.Div(className="terminal-button green"),
                                html.Span("Quantum QA Terminal", className="terminal-title")
                            ]
                        ),
                        html.Div(
                            className="terminal-body",
                            children=html.Pre(
                                id="terminal-text",
                                className="terminal-text",
                                children=[
                                    html.Span("$", className="prompt"), " ",
                                    html.Span("quantum-dashboard --start", className="command"),
                                    html.Br(),
                                    html.Br(),
                                    "Initializing Quantum 5D QA Dashboard...",
                                    html.Br(),
                                    "Accessing 5 dimensional metrics...",
                                    html.Br(),
                                    "Calculating quantum entanglement...",
                                    html.Br(),
                                    "Ready.",
                                    html.Br(),
                                    html.Span("$", className="prompt"), " ",
                                    html.Span("█", className="cursor")
                                ]
                            )
                        )
                    ]
                )
            )
        ]
    )
    
    return card


def create_matrix_test_runner_card() -> dbc.Card:
    """Create a cyberpunk Matrix-style card for running tests."""
    card = dbc.Card(
        className="visualization-card matrix-test-runner-card",
        children=[
            dbc.CardHeader(
                html.H3("F0R3ST RUN 5D TEST MATRIX", className="card-title")
            ),
            dbc.CardBody([
                html.Div(
                    className="matrix-test-controls",
                    children=[
                        html.Div(
                            className="matrix-control-section",
                            children=[
                                html.H4("⚡ TEST DIMENSIONS", className="matrix-section-title"),
                                dbc.Checklist(
                                    id="test-dimensions-checklist",
                                    options=[
                                        {"label": "UNIT 〔 Core Functionality 〕", "value": TestDimension.UNIT.name},
                                        {"label": "INTEGRATION 〔 System Coherence 〕", "value": TestDimension.INTEGRATION.name},
                                        {"label": "PERFORMANCE 〔 Quantum Efficiency 〕", "value": TestDimension.PERFORMANCE.name},
                                        {"label": "SECURITY 〔 Dimensional Shield 〕", "value": TestDimension.SECURITY.name},
                                        {"label": "QUANTUM 〔 Hyperspatial Integrity 〕", "value": TestDimension.QUANTUM.name}
                                    ],
                                    value=[d.name for d in TestDimension],  # All selected by default
                                    className="test-dimensions-list",
                                    switch=True
                                )
                            ]
                        ),
                        html.Div(
                            className="matrix-control-section",
                            children=[
                                html.H4("🌀 EXECUTION OPTIONS", className="matrix-section-title"),
                                dbc.Switch(
                                    id="fancy-visuals-switch",
                                    label="QUANTUM VISUALS",
                                    value=True,
                                    className="matrix-switch"
                                ),
                                dbc.Switch(
                                    id="celebration-switch",
                                    label="CELEBRATION SEQUENCE",
                                    value=True,
                                    className="matrix-switch"
                                )
                            ]
                        ),
                        html.Div(
                            className="matrix-control-section",
                            children=[
                                html.H4("🧬 0M3G4 MODE", className="matrix-section-title"),
                                dbc.Button(
                                    "INITIATE 0M3G4 MODE",
                                    id="omega-mode-btn",
                                    color="success",
                                    className="matrix-btn",
                                    style={"marginBottom": "10px"}
                                ),
                                dbc.Button(
                                    "ACTIVATE 0M3G4-K8s MATRIX",
                                    id="omega-k8s-btn",
                                    color="info",
                                    className="matrix-btn"
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className="matrix-separator",
                    children=html.Div(className="matrix-line")
                ),
                html.Div(
                    className="matrix-test-execution",
                    children=[
                        dbc.Button(
                            [
                                html.I(className="fas fa-play-circle me-2"),
                                "RUN S0NN3T TEST MATRIX"
                            ],
                            id="run-tests-btn",
                            color="danger",
                            size="lg",
                            className="matrix-run-btn"
                        ),
                        html.Div(
                            className="matrix-progress-container",
                            id="test-progress-container",
                            style={"display": "none"},
                            children=[
                                dbc.Progress(
                                    id="test-progress-bar",
                                    value=0,
                                    color="info",
                                    striped=True,
                                    animated=True,
                                    className="matrix-progress"
                                ),
                                html.P(
                                    "Initializing tests...",
                                    id="test-progress-text",
                                    className="matrix-progress-text"
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className="matrix-separator",
                    children=html.Div(className="matrix-line")
                ),
                html.Div(
                    className="matrix-test-output",
                    children=[
                        html.H4("5D MATRIX OUTPUT", className="matrix-section-title"),
                        html.Div(
                            id="test-terminal-output",
                            className="matrix-terminal",
                            children=html.Div(
                                className="terminal-container",
                                children=html.Div(
                                    className="terminal-body",
                                    children=html.Pre(
                                        id="test-terminal-text",
                                        className="terminal-text",
                                        children=[
                                            html.Span("$", className="prompt"), " ",
                                            html.Span("s0nn3t-test-runner --ready", className="command"),
                                            html.Br(), html.Br(),
                                            "[Awaiting commands...]",
                                            html.Br(),
                                            html.Span("$", className="prompt"), " ",
                                            html.Span("█", className="cursor")
                                        ]
                                    )
                                )
                            )
                        )
                    ]
                ),
                html.Div(
                    className="matrix-separator",
                    children=html.Div(className="matrix-line")
                ),
                html.Div(
                    className="matrix-test-results",
                    children=[
                        html.H4("LATEST TEST RESULTS", className="matrix-section-title"),
                        html.Div(
                            id="test-results-container",
                            className="test-results",
                            children=[
                                html.P("No test results available", className="no-results-message")
                            ]
                        )
                    ]
                )
            ])
        ]
    )
    
    return card


def create_dimension_card(title, value, subtitle, dimension_class):
    """Create a dimension card component to display key metrics."""
    return html.Div(
        className=f"card dimension-card {dimension_class}",
        children=[
            html.H3(title, className="dimension-title"),
            html.P(value, className="dimension-value"),
            html.P(subtitle, className="dimension-subtitle")
        ]
    )


def create_visualization_card(title, graph_id, figure=None):
    """Create a visualization card with a header and plot area."""
    if figure is None:
        figure = create_empty_figure()
        
    return html.Div(
        className="card visualization-card",
        children=[
            html.Div(
                className="card-header",
                children=[
                    html.H3(title, className="card-title")
                ]
            ),
            html.Div(
                className="card-body",
                children=[
                    dcc.Graph(
                        id=graph_id,
                        figure=figure,
                        className="visualization-graph",
                        config={'displayModeBar': False}
                    )
                ]
            )
        ]
    )


def create_terminal_card(title, content_id):
    """Create a terminal-style card for displaying text output."""
    return html.Div(
        className="card terminal-card",
        children=[
            html.Div(
                className="card-header",
                children=[
                    html.H3(title, className="card-title")
                ]
            ),
            html.Div(
                className="card-body",
                children=[
                    html.Div(
                        className="terminal-container",
                        children=[
                            html.Div(
                                className="terminal-header",
                                children=[
                                    html.Div(className="terminal-button red"),
                                    html.Div(className="terminal-button yellow"),
                                    html.Div(className="terminal-button green"),
                                    html.Div("quantum-terminal", className="terminal-title")
                                ]
                            ),
                            html.Div(
                                className="terminal-body",
                                children=[
                                    html.Pre(id=content_id, className="terminal-text")
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )


def create_test_runner_card():
    """Create the Matrix Test Runner card with cyberpunk styling."""
    return html.Div(
        className="card matrix-test-runner",
        children=[
            html.Div(
                className="matrix-header",
                children=[
                    html.Div(
                        children=[
                            html.H3("S0NN3T 5D Matrix Test Runner", className="matrix-title"),
                            html.P("Advanced Quantum Test Execution System", className="matrix-subtitle")
                        ]
                    )
                ]
            ),
            html.Div(
                className="matrix-grid",
                children=[
                    html.Div(
                        className="matrix-left-panel",
                        children=[
                            html.Div(
                                className="matrix-section",
                                children=[
                                    html.H4("Test Dimensions", className="matrix-section-title"),
                                    html.Div(
                                        className="matrix-control-items",
                                        children=[
                                            dcc.Checklist(
                                                id="test-dimensions",
                                                options=[
                                                    {"label": "Quality", "value": "quality"},
                                                    {"label": "Coverage", "value": "coverage"},
                                                    {"label": "Performance", "value": "performance"},
                                                    {"label": "Security", "value": "security"}
                                                ],
                                                value=["quality", "coverage"],
                                                labelClassName="matrix-control-label"
                                            )
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                className="matrix-section",
                                children=[
                                    html.H4("Control Panel", className="matrix-section-title"),
                                    html.Div(
                                        className="matrix-control-items",
                                        children=[
                                            html.Div(
                                                className="matrix-control-item",
                                                children=[
                                                    html.Label("Deep Mode:", className="matrix-control-label"),
                                                    dcc.RadioItems(
                                                        id="deep-mode",
                                                        options=[
                                                            {"label": "On", "value": "on"},
                                                            {"label": "Off", "value": "off"}
                                                        ],
                                                        value="off",
                                                        labelClassName="matrix-control-label",
                                                        inline=True
                                                    )
                                                ]
                                            ),
                                            html.Button("Run Tests", id="run-tests-button", className="matrix-btn"),
                                            html.Button("Stop Execution", id="stop-tests-button", className="matrix-btn matrix-btn-danger"),
                                            html.Button("Clear Results", id="clear-results-button", className="matrix-btn")
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        className="matrix-right-panel",
                        children=[
                            html.Div(
                                className="matrix-section matrix-test-output",
                                children=[
                                    html.H4("Test Progress", className="matrix-section-title"),
                                    html.Div(
                                        className="progress-container",
                                        children=[
                                            html.Div(id="test-progress-bar", className="progress-bar", style={"width": "0%"}),
                                            html.Div(id="test-progress-text", className="progress-text", children="0%")
                                        ]
                                    ),
                                    html.Div(
                                        id="test-results-container",
                                        className="test-results-container",
                                        children=[
                                            html.Div(
                                                className="no-results-message",
                                                children="No test results available. Run tests to see results."
                                            )
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                className="matrix-section matrix-code-inspection",
                                children=[
                                    html.H4("Test Output", className="matrix-section-title"),
                                    html.Div(
                                        className="matrix-terminal",
                                        children=[
                                            html.Div(
                                                className="terminal-container",
                                                children=[
                                                    html.Div(
                                                        className="terminal-header",
                                                        children=[
                                                            html.Div(className="terminal-button red"),
                                                            html.Div(className="terminal-button yellow"),
                                                            html.Div(className="terminal-button green"),
                                                            html.Div("matrix-console", className="terminal-title")
                                                        ]
                                                    ),
                                                    html.Div(
                                                        className="terminal-body",
                                                        children=[
                                                            html.Pre(
                                                                id="test-output",
                                                                className="terminal-text",
                                                                children=[
                                                                    html.Span("matrix> ", className="prompt"),
                                                                    html.Span("Initializing S0NN3T 5D Matrix Test Runner...", className="command"),
                                                                    html.Span("█", className="cursor")
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )


def create_dashboard_header():
    """Create the dashboard header with title and status indicators."""
    return html.Div(
        className="header",
        children=[
            html.Div(
                className="header-title-container",
                children=[
                    html.H1("Quantum 5D QA Dashboard", className="header-title"),
                    html.Div("MATRIX", className="header-matrix-badge")
                ]
            ),
            html.Div(
                className="header-status-container",
                children=[
                    html.Div(
                        className="header-metric",
                        children=[
                            html.Span("Status: ", className="header-metric-label"),
                            html.Span(id="system-status", className="status-value status-stable", children="Stable")
                        ]
                    ),
                    html.Div(
                        className="header-metric",
                        children=[
                            html.Span("Stability: ", className="header-metric-label"),
                            html.Span(id="stability-metric", children="99.98%")
                        ]
                    ),
                    html.Div(
                        className="header-metric",
                        children=[
                            html.Span("Coverage: ", className="header-metric-label"),
                            html.Span(id="coverage-metric", children="87.5%")
                        ]
                    ),
                    html.Div(
                        className="header-time",
                        children=[
                            html.Div(id="current-date", className="header-date"),
                            html.Div(id="current-time", className="header-time-value"),
                            html.Div(id="last-update-time", className="header-update-time", children="Last update: Just now")
                        ]
                    )
                ]
            )
        ]
    )


def create_dashboard_footer():
    """Create the dashboard footer with additional information."""
    return html.Div(
        className="footer",
        children=[
            html.Div(
                className="footer-content",
                children=[
                    html.Div(
                        className="footer-section",
                        children=[
                            html.Span("Version: ", className="footer-label"),
                            html.Span("3.7.1", className="footer-value")
                        ]
                    ),
                    html.Div(
                        className="footer-section",
                        children=[
                            html.Span("Omega-BTC-AI ", className="footer-license"),
                            html.Span("© 2023 S0NN3T Advanced Systems")
                        ]
                    ),
                    html.Div(
                        className="footer-section",
                        children=[
                            html.Span("Environment: ", className="footer-label"),
                            html.Span("Production", className="footer-value")
                        ]
                    )
                ]
            )
        ]
    )


def create_dashboard_layout() -> html.Div:
    """Create the main dashboard layout with all components."""
    return html.Div(
        className="dashboard-container",
        children=[
            # Header
            create_dashboard_header(),
            
            # Main Grid
            html.Div(
                className="main-grid",
                children=[
                    # Dimension Cards Row
                    html.Div(
                        className="dimension-row",
                        children=[
                            html.Div(
                                className="dimension-card-container",
                                children=[
                                    create_dimension_card(
                                        "Quality",
                                        "98.7%",
                                        "Test Reliability Index",
                                        "quality-card"
                                    )
                                ]
                            ),
                            html.Div(
                                className="dimension-card-container",
                                children=[
                                    create_dimension_card(
                                        "Coverage",
                                        "87.5%",
                                        "Codebase Coverage Ratio",
                                        "coverage-card"
                                    )
                                ]
                            ),
                            html.Div(
                                className="dimension-card-container",
                                children=[
                                    create_dimension_card(
                                        "Performance",
                                        "342ms",
                                        "Average Response Time",
                                        "performance-card"
                                    )
                                ]
                            ),
                            html.Div(
                                className="dimension-card-container",
                                children=[
                                    create_dimension_card(
                                        "Security",
                                        "94.2%",
                                        "Vulnerability Protection",
                                        "security-card"
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # Visualization Row 1
                    html.Div(
                        className="visualization-row",
                        children=[
                            html.Div(
                                className="visualization-card-container large",
                                children=[
                                    create_visualization_card(
                                        "Hyperspatial Trend Analysis",
                                        "hyperspatial-trend-graph"
                                    )
                                ]
                            ),
                            html.Div(
                                className="visualization-card-container medium",
                                children=[
                                    create_visualization_card(
                                        "Dimension Distribution",
                                        "dimension-distribution-graph"
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    # Visualization Row 2
                    html.Div(
                        className="visualization-row",
                        children=[
                            html.Div(
                                className="visualization-card-container medium",
                                children=[
                                    create_terminal_card(
                                        "Matrix Monitoring",
                                        "matrix-output"
                                    )
                                ]
                            ),
                            html.Div(
                                className="visualization-card-container large",
                                children=[
                                    create_test_runner_card()
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # Footer
            create_dashboard_footer()
        ]
    ) 