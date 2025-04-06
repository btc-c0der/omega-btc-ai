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
                    # Left side - Title and subtitle
                    html.Div(
                        children=[
                            html.H1(
                                children=[
                                    html.Span("AIXBT ", style={'color': theme['accent1']}),
                                    html.Span("Trading Dashboard", style={'color': theme['accent2']}),
                                    html.Span(" v1.0", style={'color': theme['highlight'], 'fontSize': '1.2rem'})
                                ],
                                className="mb-0",
                                style={'fontWeight': 'bold', 'letterSpacing': '1px'}
                            ),
                            html.P(
                                "Escape the OMEGA TRAP ZONE™ with Quantum Strategy",
                                className="mb-0 text-muted",
                                style={'fontSize': '1rem'}
                            )
                        ]
                    ),
                    
                    # Right side - Token stats
                    html.Div(
                        className="d-flex align-items-center",
                        children=[
                            # Current price
                            html.Div(
                                className="me-4 text-end",
                                children=[
                                    html.Small("Current Price", className="d-block text-muted"),
                                    html.Span(
                                        f"${DASHBOARD_CONFIG['token']['current_price']:.5f}",
                                        id="current-price-display",
                                        style={
                                            'color': theme['error'] if DASHBOARD_CONFIG['token']['current_price'] < DASHBOARD_CONFIG['token']['entry_price'] else theme['success'],
                                            'fontWeight': 'bold',
                                            'fontSize': '1.2rem'
                                        }
                                    )
                                ]
                            ),
                            
                            # Entry price
                            html.Div(
                                className="me-4 text-end",
                                children=[
                                    html.Small("Entry Price", className="d-block text-muted"),
                                    html.Span(
                                        f"${DASHBOARD_CONFIG['token']['entry_price']:.5f}",
                                        style={
                                            'fontWeight': 'bold',
                                            'fontSize': '1.2rem'
                                        }
                                    )
                                ]
                            ),
                            
                            # Leverage
                            html.Div(
                                className="text-end",
                                children=[
                                    html.Small("Leverage", className="d-block text-muted"),
                                    html.Span(
                                        f"{DASHBOARD_CONFIG['token']['leverage']}x",
                                        style={
                                            'color': theme['highlight'],
                                            'fontWeight': 'bold',
                                            'fontSize': '1.2rem'
                                        }
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

def create_footer() -> html.Footer:
    """
    Create the dashboard footer.
    
    Returns:
        Footer component
    """
    theme = DASHBOARD_CONFIG["theme"]
    
    return html.Footer(
        className="container-fluid py-3 mt-5",
        style={
            'backgroundColor': theme['panel'],
            'borderTop': f"1px solid {theme['grid']}",
            'textAlign': 'center'
        },
        children=[
            html.P(
                [
                    "Powered by ",
                    html.Span("OMEGA ", style={'color': theme['accent1']}),
                    html.Span("BTC ", style={'color': theme['accent2']}),
                    html.Span("AI", style={'color': theme['accent3']}),
                    html.Span(" © 2025")
                ],
                className="mb-0"
            ),
            html.Small(
                "The blessing is always after the trick.",
                className="text-muted"
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
    Create the PnL projection card.
    
    Returns:
        Card component with PnL projection graph
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
                className="d-flex justify-content-between align-items-center",
                style={
                    'backgroundColor': 'transparent',
                    'borderBottom': f"1px solid {theme['grid']}",
                    'color': theme['accent1']
                },
                children=[
                    html.H5("PnL Projection", className="mb-0"),
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                "Basic",
                                id="basic-pnl-btn",
                                color="dark",
                                size="sm",
                                outline=True,
                                active=True
                            ),
                            dbc.Button(
                                "Multi-Leverage",
                                id="multi-leverage-pnl-btn",
                                color="dark",
                                size="sm",
                                outline=True
                            ),
                            dbc.Button(
                                "Trap Zone",
                                id="trap-zone-pnl-btn",
                                color="dark",
                                size="sm",
                                outline=True
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

def create_strategy_visualization_card() -> dbc.Card:
    """
    Create the strategy visualization card.
    
    Returns:
        Card component with strategy visualization
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
                    'color': theme['accent3']
                },
                children=[
                    html.H5(
                        id="strategy-vis-title",
                        children="Strategy Visualization",
                        className="mb-0"
                    )
                ]
            ),
            dbc.CardBody(
                [
                    # Default content
                    html.Div(
                        id="strategy-default-content",
                        className="text-center py-5",
                        children=[
                            html.I(
                                className="fas fa-chart-line mb-3",
                                style={
                                    'fontSize': '3rem',
                                    'color': theme['accent2'],
                                    'opacity': '0.5'
                                }
                            ),
                            html.H5("Select a strategy to visualize"),
                            html.P(
                                "Click on any strategy above to see detailed visualization and analysis",
                                className="text-muted"
                            )
                        ]
                    ),
                    
                    # Strategy visualization
                    dcc.Graph(
                        id='strategy-visualization-graph',
                        config={
                            'displayModeBar': False,
                            'responsive': True
                        },
                        style={
                            'height': '400px',
                            'display': 'none'
                        }
                    ),
                    
                    # Strategy details
                    html.Div(
                        id="strategy-details-container",
                        style={'display': 'none'},
                        children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Small("Risk Level"),
                                    html.Div(id="strategy-risk-level", className="mb-2")
                                ], width=4),
                                dbc.Col([
                                    html.Small("Success Probability"),
                                    html.Div(id="strategy-success-probability", className="mb-2")
                                ], width=4),
                                dbc.Col([
                                    html.Small("Expected PnL"),
                                    html.Div(id="strategy-expected-pnl", className="mb-2")
                                ], width=4)
                            ]),
                            html.Hr(style={'margin': '0.5rem 0'}),
                            html.Small("Strategy Implementation Steps", className="d-block mt-2"),
                            html.Ol(id="strategy-steps", className="small", style={'paddingLeft': '1rem'})
                        ]
                    )
                ]
            )
        ]
    )

def create_dashboard_layout() -> html.Div:
    """
    Create the complete dashboard layout.
    
    Returns:
        Main layout container
    """
    theme = DASHBOARD_CONFIG["theme"]
    
    return html.Div(
        style={
            'backgroundColor': theme['background'],
            'color': theme['text'],
            'minHeight': '100vh',
            'fontFamily': "'Roboto', sans-serif"
        },
        children=[
            # Header
            create_header(),
            
            # Main content
            html.Div(
                className="container-fluid",
                style={'padding': '20px'},
                children=[
                    # First row: Token stats and escape plan
                    dbc.Row(
                        className="mb-4",
                        children=[
                            # Token stats
                            dbc.Col(
                                width=4,
                                children=[create_token_stats_card()]
                            ),
                            
                            # Escape plan
                            dbc.Col(
                                width=8,
                                children=[create_escape_plan_card()]
                            )
                        ]
                    ),
                    
                    # Second row: PnL projection and strategy visualization
                    dbc.Row(
                        className="mb-4",
                        children=[
                            # PnL projection
                            dbc.Col(
                                width=8,
                                children=[create_pnl_projection_card()]
                            ),
                            
                            # Strategy visualization
                            dbc.Col(
                                width=4,
                                children=[create_strategy_visualization_card()]
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