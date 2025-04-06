#!/usr/bin/env python3
"""
AIXBT Dashboard Layout Module
--------------------------

Layout components and UI structure for the AIXBT Trading Dashboard.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Dict, List, Any

from .config import DASHBOARD_CONFIG

def create_header() -> html.Div:
    """
    Create the dashboard header.
    
    Returns:
        Header component
    """
    theme = DASHBOARD_CONFIG["theme"]
    
    return html.Div(
        className="container-fluid py-3",
        style={
            'backgroundColor': theme['panel'],
            'borderBottom': f"1px solid {theme['grid']}",
            'boxShadow': f"0 2px 10px {theme['grid']}"
        },
        children=[
            html.Div(
                className="d-flex justify-content-between align-items-center",
                children=[
                    # Left side - Title
                    html.Div(
                        className="d-flex align-items-center",
                        children=[
                            html.H3(
                                "AIXBT Trading Dashboard",
                                className="m-0 me-2",
                                style={'color': theme['text']}
                            ),
                            html.Span(
                                "OMEGA TRAP ZONE™",
                                className="badge bg-primary ms-2",
                                style={
                                    'backgroundColor': theme['accent1'],
                                    'fontSize': '0.8rem',
                                    'fontWeight': 'bold'
                                }
                            )
                        ]
                    ),
                    
                    # Right side - Price Info
                    html.Div(
                        className="d-flex align-items-center",
                        children=[
                            # Risk Status Indicator
                            html.Div(
                                className="me-4",
                                children=[
                                    dbc.Row([
                                        dbc.Col([
                                            html.Span("Status: ", className="me-1"),
                                            html.Span(
                                                "IN TRAP ZONE",
                                                id="risk-status-text",
                                                style={'color': theme['warning'], 'fontWeight': 'bold'}
                                            )
                                        ]),
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Div(
                                                className="mt-1",
                                                style={'width': '100%', 'height': '6px'},
                                                children=[
                                                    html.Div(
                                                        id="risk-status-indicator",
                                                        style={
                                                            'width': '100%',
                                                            'height': '100%',
                                                            'backgroundColor': theme['warning'],
                                                            'borderRadius': '3px'
                                                        }
                                                    )
                                                ]
                                            )
                                        ])
                                    ])
                                ]
                            ),
                            
                            # Token Price
                            html.Div(
                                className="text-end me-4",
                                children=[
                                    html.Div(
                                        "Current Price",
                                        style={'fontSize': '0.8rem', 'opacity': '0.7'}
                                    ),
                                    html.Div(
                                        id="current-price-display",
                                        children=f"${DASHBOARD_CONFIG['token']['current_price']:.5f}",
                                        style={'fontSize': '1.2rem', 'fontWeight': 'bold'}
                                    )
                                ]
                            ),
                            
                            # PnL
                            html.Div(
                                className="text-end me-4",
                                children=[
                                    html.Div(
                                        "Current PnL",
                                        style={'fontSize': '0.8rem', 'opacity': '0.7'}
                                    ),
                                    html.Div(
                                        id="current-pnl-display",
                                        children=f"$0.00",
                                        style={'fontSize': '1.2rem', 'fontWeight': 'bold'}
                                    )
                                ]
                            ),
                            
                            # PnL Percentage
                            html.Div(
                                className="text-end",
                                children=[
                                    html.Div(
                                        "Return %",
                                        style={'fontSize': '0.8rem', 'opacity': '0.7'}
                                    ),
                                    html.Div(
                                        id="current-pnl-percent-display",
                                        children=f"0.00%",
                                        style={'fontSize': '1.2rem', 'fontWeight': 'bold'}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

def create_footer() -> html.Div:
    """
    Create the dashboard footer.
    
    Returns:
        Footer component
    """
    theme = DASHBOARD_CONFIG["theme"]
    
    return html.Div(
        className="container-fluid py-3 mt-4",
        style={
            'backgroundColor': theme['panel'],
            'borderTop': f"1px solid {theme['grid']}",
            'color': theme['text'],
            'opacity': '0.7',
            'fontSize': '0.8rem',
            'textAlign': 'center'
        },
        children=[
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="col-md-6 offset-md-3",
                        children=[
                            html.P("AIXBT Trading Dashboard - OMEGA TRAP ZONE™ Escape Strategy Visualization", className="mb-0"),
                            html.P("Powered by OMEGA BTC AI", className="mb-0"),
                            html.P("© 2024 OMEGA BTC AI - All rights reserved", className="mb-0")
                        ]
                    )
                ]
            )
        ]
    )

def create_token_stats_card() -> dbc.Card:
    """
    Create the token stats card.
    
    Returns:
        Card component with token statistics
    """
    theme = DASHBOARD_CONFIG["theme"]
    token = DASHBOARD_CONFIG["token"]
    liquidation_price = DASHBOARD_CONFIG["liquidation_price"]
    breakeven_price = DASHBOARD_CONFIG["breakeven_price"]
    
    # Calculate PnL
    current_pnl = (token["current_price"] - token["entry_price"]) * token["token_quantity"] * token["leverage"]
    
    # Calculate liquidation distance (percentage)
    liquidation_distance = ((token["current_price"] - liquidation_price) / token["current_price"]) * 100
    
    return dbc.Card(
        className="h-100 border-0 shadow",
        style={
            'backgroundColor': theme['panel'],
            'borderRadius': '10px'
        },
        children=[
            dbc.CardHeader(
                style={
                    'backgroundColor': 'transparent',
                    'borderBottom': f"1px solid {theme['grid']}",
                    'color': theme['accent2']
                },
                children=[
                    html.H5(
                        [
                            html.I(className="fas fa-chart-line me-2"),
                            "AIXBT Position Stats"
                        ],
                        className="mb-0"
                    )
                ]
            ),
            dbc.CardBody(
                [
                    # Token quantity and value
                    html.Div(
                        className="mb-3",
                        children=[
                            html.H6("Position Size", className="mb-2"),
                            dbc.Row([
                                dbc.Col([
                                    html.Small("Quantity", className="d-block text-muted"),
                                    html.Div(
                                        f"{token['token_quantity']:,} AIXBT",
                                        style={'fontWeight': 'bold'}
                                    )
                                ], width=6),
                                dbc.Col([
                                    html.Small("Value", className="d-block text-muted"),
                                    html.Div(
                                        f"${token['token_quantity'] * token['current_price']:,.2f}",
                                        style={'fontWeight': 'bold'}
                                    )
                                ], width=6)
                            ])
                        ]
                    ),
                    
                    # Current PnL
                    html.Div(
                        className="mb-3",
                        children=[
                            html.H6("Profit/Loss", className="mb-2"),
                            dbc.Row([
                                dbc.Col([
                                    html.Small("Unrealized PnL", className="d-block text-muted"),
                                    html.Div(
                                        f"${current_pnl:,.2f}",
                                        style={
                                            'fontWeight': 'bold',
                                            'color': theme['success'] if current_pnl >= 0 else theme['error']
                                        }
                                    )
                                ], width=6),
                                dbc.Col([
                                    html.Small("PnL %", className="d-block text-muted"),
                                    html.Div(
                                        f"{(current_pnl / (token['token_quantity'] * token['entry_price'])) * 100:.2f}%",
                                        style={
                                            'fontWeight': 'bold',
                                            'color': theme['success'] if current_pnl >= 0 else theme['error']
                                        }
                                    )
                                ], width=6)
                            ])
                        ]
                    ),
                    
                    # Critical price levels
                    html.Div(
                        children=[
                            html.H6("Critical Levels", className="mb-2"),
                            dbc.Row([
                                dbc.Col([
                                    html.Small("Liquidation Price", className="d-block text-muted"),
                                    html.Div(
                                        f"${liquidation_price:.5f}",
                                        style={
                                            'fontWeight': 'bold',
                                            'color': theme['error']
                                        }
                                    )
                                ], width=6),
                                dbc.Col([
                                    html.Small("Distance to Liquidation", className="d-block text-muted"),
                                    html.Div(
                                        f"{liquidation_distance:.2f}%",
                                        style={
                                            'fontWeight': 'bold',
                                            'color': theme['warning'] if liquidation_distance < 10 else theme['success']
                                        }
                                    )
                                ], width=6)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Small("Breakeven Price", className="d-block text-muted"),
                                    html.Div(
                                        f"${breakeven_price:.5f}",
                                        style={'fontWeight': 'bold'}
                                    )
                                ], width=6),
                                dbc.Col([
                                    html.Small("Target Price", className="d-block text-muted"),
                                    html.Div(
                                        f"${token['price_target']:.2f}",
                                        style={
                                            'fontWeight': 'bold',
                                            'color': theme['success']
                                        }
                                    )
                                ], width=6)
                            ])
                        ]
                    )
                ]
            )
        ]
    )

def create_escape_plan_card() -> dbc.Card:
    """
    Create the escape plan card.
    
    Returns:
        Card component with escape plan
    """
    theme = DASHBOARD_CONFIG["theme"]
    
    return dbc.Card(
        className="h-100 border-0 shadow",
        style={
            'backgroundColor': theme['panel'],
            'borderRadius': '10px'
        },
        children=[
            dbc.CardHeader(
                style={
                    'backgroundColor': 'transparent',
                    'borderBottom': f"1px solid {theme['grid']}",
                    'color': theme['highlight']
                },
                children=[
                    html.H5(
                        [
                            html.I(className="fas fa-door-open me-2"),
                            "GET OUT THE BTRAP™ MODE"
                        ],
                        className="mb-0"
                    )
                ]
            ),
            dbc.CardBody(
                [
                    # Current situation
                    html.Div(
                        className="mb-3",
                        children=[
                            html.H6(
                                [
                                    html.I(className="fas fa-exclamation-triangle me-2", style={'color': theme['warning']}),
                                    "Current Situation:"
                                ],
                                className="mb-2"
                            ),
                            html.Ul(
                                children=[
                                    html.Li(f"AIXBT = {DASHBOARD_CONFIG['token']['current_price']}"),
                                    html.Li(f"Your Entry = {DASHBOARD_CONFIG['token']['entry_price']}"),
                                    html.Li(f"Leverage = {DASHBOARD_CONFIG['token']['leverage']}x"),
                                    html.Li([
                                        "Liquidation zone is ",
                                        html.Span("getting spicy 🌶️", style={'color': theme['error']})
                                    ])
                                ],
                                className="mb-0",
                                style={'paddingLeft': '1.5rem'}
                            )
                        ]
                    ),
                    
                    # Omega strategies
                    html.Div(
                        className="mb-3",
                        children=[
                            html.H6(
                                [
                                    html.I(className="fas fa-magic me-2", style={'color': theme['accent1']}),
                                    "Omega Strategies to ",
                                    html.Span("ESCAPE THE BTRAP™", style={'color': theme['error']})
                                ],
                                className="mb-2"
                            ),
                            
                            # Strategy 1: Stealth Ladder Orders
                            dbc.Button(
                                className="d-flex align-items-center w-100 mb-2 p-2",
                                style={
                                    'backgroundColor': 'rgba(108, 92, 231, 0.1)',
                                    'border': f'1px solid {theme["accent1"]}',
                                    'color': theme['text'],
                                    'textAlign': 'left'
                                },
                                children=[
                                    html.I(className="fas fa-bolt me-2", style={'color': theme['accent1']}),
                                    html.Div([
                                        html.Strong("⚡ Stealth Ladder Orders"),
                                        html.P("Deploy micro buys every 0.001 from current down — bait bots, control drawdown.", className="mb-0 small")
                                    ])
                                ],
                                id="strategy-stealth-ladder-btn"
                            ),
                            
                            # Strategy 2: Fake Sell Wall
                            dbc.Button(
                                className="d-flex align-items-center w-100 mb-2 p-2",
                                style={
                                    'backgroundColor': 'rgba(0, 206, 201, 0.1)',
                                    'border': f'1px solid {theme["accent2"]}',
                                    'color': theme['text'],
                                    'textAlign': 'left'
                                },
                                children=[
                                    html.I(className="fas fa-magnet me-2", style={'color': theme['accent2']}),
                                    html.Div([
                                        html.Strong("🧲 Fake Sell Wall (simulated)"),
                                        html.P("Place a fake ask just under your liquidation — MM bots tend to reverse.", className="mb-0 small")
                                    ])
                                ],
                                id="strategy-fake-wall-btn"
                            ),
                            
                            # Strategy 3: Positive Flow Spiral
                            dbc.Button(
                                className="d-flex align-items-center w-100 mb-2 p-2",
                                style={
                                    'backgroundColor': 'rgba(116, 185, 255, 0.1)',
                                    'border': f'1px solid {theme["accent3"]}',
                                    'color': theme['text'],
                                    'textAlign': 'left'
                                },
                                children=[
                                    html.I(className="fas fa-sync-alt me-2", style={'color': theme['accent3']}),
                                    html.Div([
                                        html.Strong("🌀 Positive Flow Spiral"),
                                        html.P("Monitor Schumann resonance & Fibonacci price rhythms. If aligned → average in = win.", className="mb-0 small")
                                    ])
                                ],
                                id="strategy-flow-spiral-btn"
                            )
                        ]
                    ),
                    
                    # Escape Path
                    html.Div(
                        children=[
                            html.H6(
                                [
                                    html.I(className="fas fa-location-arrow me-2", style={'color': theme['accent2']}),
                                    "Visualize Your Escape"
                                ],
                                className="mb-2"
                            ),
                            dbc.Card(
                                className="border-0",
                                style={
                                    'backgroundColor': 'rgba(0, 0, 0, 0.2)',
                                    'borderRadius': '5px'
                                },
                                children=[
                                    dbc.CardHeader(
                                        "OMEGA ASCENT PATH",
                                        style={
                                            'backgroundColor': 'rgba(0, 0, 0, 0.3)',
                                            'borderBottom': f'1px solid {theme["grid"]}',
                                            'textAlign': 'center',
                                            'fontWeight': 'bold',
                                            'color': theme['accent2']
                                        }
                                    ),
                                    dbc.CardBody(
                                        [
                                            html.Ul(
                                                children=[
                                                    html.Li(f"0.0768 – Final Bot Wipe"),
                                                    html.Li(f"0.0775 – EMF Reversal"),
                                                    html.Li(f"0.0789 – Fibonacci Arc"),
                                                    html.Li(f"0.08198 – ENTRY BREAKOUT", style={'color': theme['highlight'], 'fontWeight': 'bold'}),
                                                    html.Li(f"0.0850 – Sky Is Open")
                                                ],
                                                className="mb-0",
                                                style={'paddingLeft': '1.5rem'}
                                            )
                                        ],
                                        style={'padding': '1rem'}
                                    )
                                ]
                            ),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button(
                                        "RUN THE ESCAPE VIS",
                                        id="run-escape-vis-btn",
                                        color="success",
                                        className="mt-2 w-100"
                                    )
                                ], width=6),
                                dbc.Col([
                                    dbc.Button(
                                        "SHOW FIBONACCI VORTEX",
                                        id="show-fibonacci-vortex-btn",
                                        color="warning",
                                        className="mt-2 w-100"
                                    )
                                ], width=6)
                            ])
                        ]
                    )
                ]
            )
        ]
    )

def create_pnl_projection_card() -> dbc.Card:
    """
    Create the PnL projection visualization card.
    
    Returns:
        Card component containing the PnL visualization
    """
    theme = DASHBOARD_CONFIG["theme"]
    
    return dbc.Card(
        className="h-100 shadow",
        style={'backgroundColor': theme['panel'], 'border': f"1px solid {theme['grid']}"},
        children=[
            dbc.CardHeader(
                className="d-flex justify-content-between align-items-center",
                style={'backgroundColor': theme['background'], 'borderBottom': f"1px solid {theme['grid']}"},
                children=[
                    html.H5(
                        "PnL Projection & Escape Routes",
                        className="mb-0",
                        style={'color': theme['text']}
                    ),
                    html.Div(
                        className="btn-group",
                        children=[
                            dbc.Button(
                                "Basic",
                                id="basic-pnl-btn",
                                color="primary",
                                outline=True,
                                size="sm",
                                active=True,
                                className="me-1"
                            ),
                            dbc.Button(
                                "Multi Leverage",
                                id="multi-leverage-pnl-btn",
                                color="primary",
                                outline=True,
                                size="sm",
                                className="me-1"
                            ),
                            dbc.Button(
                                "Trap Zone",
                                id="trap-zone-pnl-btn",
                                color="primary",
                                outline=True,
                                size="sm",
                                className="me-1"
                            ),
                            dbc.Button(
                                "Fibonacci Vortex",
                                id="show-fibonacci-vortex-btn",
                                color="primary",
                                outline=True,
                                size="sm",
                                className="me-1"
                            ),
                            dbc.Button(
                                "Run Escape Visualization",
                                id="run-escape-vis-btn",
                                color="success",
                                size="sm"
                            )
                        ]
                    )
                ]
            ),
            dbc.CardBody(
                [
                    dcc.Graph(
                        id='pnl-projection-graph',
                        config={
                            'displayModeBar': False,
                            'responsive': True
                        },
                        style={'height': '400px'}
                    )
                ]
            )
        ]
    )

def create_strategy_card() -> dbc.Card:
    """
    Create the strategy visualization card.
    
    Returns:
        Card component for strategy visualization
    """
    theme = DASHBOARD_CONFIG["theme"]
    
    return dbc.Card(
        className="h-100 shadow",
        style={'backgroundColor': theme['panel'], 'border': f"1px solid {theme['grid']}"},
        children=[
            dbc.CardHeader(
                className="d-flex justify-content-between align-items-center",
                style={'backgroundColor': theme['background'], 'borderBottom': f"1px solid {theme['grid']}"},
                children=[
                    html.H5(
                        id="strategy-vis-title",
                        children="Strategy Visualization",
                        className="mb-0",
                        style={'color': theme['text']}
                    ),
                    html.Div(
                        className="btn-group",
                        children=[
                            dbc.Button(
                                "Stealth Ladder",
                                id="strategy-stealth-ladder-btn",
                                color="primary",
                                outline=True,
                                size="sm",
                                className="me-1"
                            ),
                            dbc.Button(
                                "Fake Sell Wall",
                                id="strategy-fake-wall-btn",
                                color="primary",
                                outline=True,
                                size="sm",
                                className="me-1"
                            ),
                            dbc.Button(
                                "Positive Flow Spiral",
                                id="strategy-flow-spiral-btn",
                                color="primary",
                                outline=True,
                                size="sm"
                            )
                        ]
                    )
                ]
            ),
            dbc.CardBody(
                [
                    # Default content (shown before selecting a strategy)
                    html.Div(
                        id="strategy-default-content",
                        className="text-center py-5",
                        children=[
                            html.I(
                                className="fas fa-chart-line fa-3x mb-3",
                                style={'color': theme['accent1']}
                            ),
                            html.H5(
                                "Select a strategy to visualize",
                                style={'color': theme['text']}
                            ),
                            html.P(
                                "Choose one of the escape strategies above to visualize and analyze its potential effectiveness.",
                                className="text-muted"
                            )
                        ]
                    ),
                    
                    # Strategy visualization (hidden by default)
                    dcc.Graph(
                        id='strategy-visualization-graph',
                        config={
                            'displayModeBar': False,
                            'responsive': True
                        },
                        style={'height': '400px', 'display': 'none'}
                    ),
                    
                    # Strategy details (hidden by default)
                    html.Div(
                        id="strategy-details-container",
                        style={'display': 'none'},
                        children=[
                            dbc.Row(
                                className="mt-3",
                                children=[
                                    dbc.Col(
                                        [
                                            html.Div(
                                                className="d-flex justify-content-between",
                                                children=[
                                                    html.Div(
                                                        className="text-center p-2",
                                                        style={'backgroundColor': theme['background'], 'borderRadius': '5px'},
                                                        children=[
                                                            html.Div("Risk Level", style={'fontSize': '0.8rem', 'opacity': '0.7'}),
                                                            html.Div(id="strategy-risk-level")
                                                        ]
                                                    ),
                                                    html.Div(
                                                        className="text-center p-2",
                                                        style={'backgroundColor': theme['background'], 'borderRadius': '5px'},
                                                        children=[
                                                            html.Div("Success Probability", style={'fontSize': '0.8rem', 'opacity': '0.7'}),
                                                            html.Div(id="strategy-success-probability")
                                                        ]
                                                    ),
                                                    html.Div(
                                                        className="text-center p-2",
                                                        style={'backgroundColor': theme['background'], 'borderRadius': '5px'},
                                                        children=[
                                                            html.Div("Expected PnL", style={'fontSize': '0.8rem', 'opacity': '0.7'}),
                                                            html.Div(id="strategy-expected-pnl")
                                                        ]
                                                    )
                                                ]
                                            )
                                        ],
                                        width=12
                                    )
                                ]
                            ),
                            dbc.Row(
                                className="mt-3",
                                children=[
                                    dbc.Col(
                                        [
                                            html.H6("Strategy Steps:", style={'color': theme['accent2']}),
                                            html.Ul(id="strategy-steps", className="ps-3")
                                        ],
                                        width=12
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

def create_dashboard_layout() -> html.Div:
    """
    Create the main dashboard layout.
    
    Returns:
        Main application layout
    """
    theme = DASHBOARD_CONFIG["theme"]
    
    return html.Div(
        style={
            'backgroundColor': theme['background'],
            'minHeight': '100vh',
            'color': theme['text']
        },
        children=[
            # Header
            create_header(),
            
            # Main content
            html.Div(
                className="container-fluid py-4",
                children=[
                    # First row - PnL Projection and Strategy Visualization
                    dbc.Row(
                        className="mb-4",
                        children=[
                            # PnL Projection
                            dbc.Col(
                                create_pnl_projection_card(),
                                lg=6,
                                md=12,
                                className="mb-4 mb-lg-0"
                            ),
                            
                            # Strategy Visualization
                            dbc.Col(
                                create_strategy_card(),
                                lg=6,
                                md=12
                            )
                        ]
                    )
                ]
            ),
            
            # Footer
            create_footer(),
            
            # Interval for updating data
            dcc.Interval(
                id='interval-component',
                interval=DASHBOARD_CONFIG['ui']['refresh_interval'] * 1000,  # in milliseconds
                n_intervals=0
            ),
            
            # Store components for state management
            dcc.Store(id='selected-strategy-store'),
            dcc.Store(id='selected-chart-type-store', data='basic'),
            dcc.Store(id='simulation-results-store')
        ]
    )