#!/usr/bin/env python3
"""
AIXBT Dashboard Callbacks Module
-----------------------------

Dash callbacks for the AIXBT Trading Dashboard, implementing the interactivity
and dynamic content updates.
"""

import dash
from dash import Input, Output, State, ctx, html
import plotly.graph_objects as go
from typing import Dict, List, Any, Tuple, Optional
import logging

from .config import (
    DASHBOARD_CONFIG, 
    get_current_price, 
    get_current_pnl, 
    get_current_pnl_percentage
)
from .visualizations import (
    create_basic_pnl_projection,
    create_multi_leverage_pnl,
    create_omega_trap_zone_pnl,
    create_fibonacci_vortex_pnl,
    create_escape_visualization
)
from .strategies import (
    StealthLadderStrategy,
    FakeWallStrategy,
    PositiveFlowStrategy,
    get_all_strategies
)

# Configure logging
logger = logging.getLogger("AIXBTDashboard.Callbacks")

def register_callbacks(app: dash.Dash) -> None:
    """
    Register all callbacks for the AIXBT Dashboard.
    
    Args:
        app: Dash application instance
    """
    # PnL Projection chart type selector callbacks
    @app.callback(
        [
            Output("basic-pnl-btn", "active"),
            Output("multi-leverage-pnl-btn", "active"),
            Output("trap-zone-pnl-btn", "active"),
            Output("selected-chart-type-store", "data"),
        ],
        [
            Input("basic-pnl-btn", "n_clicks"),
            Input("multi-leverage-pnl-btn", "n_clicks"),
            Input("trap-zone-pnl-btn", "n_clicks"),
            Input("show-fibonacci-vortex-btn", "n_clicks")
        ],
        [State("selected-chart-type-store", "data")]
    )
    def update_pnl_chart_type(
        basic_clicks, multi_clicks, trap_clicks, fibo_clicks, current_type
    ):
        """Update the active PnL chart type button and store the selection."""
        # Default values
        basic_active = False
        multi_active = False
        trap_active = False
        chart_type = current_type
        
        # Determine which button was clicked
        if ctx.triggered_id == "basic-pnl-btn":
            basic_active = True
            chart_type = "basic"
        elif ctx.triggered_id == "multi-leverage-pnl-btn":
            multi_active = True
            chart_type = "multi"
        elif ctx.triggered_id == "trap-zone-pnl-btn":
            trap_active = True
            chart_type = "trap"
        elif ctx.triggered_id == "show-fibonacci-vortex-btn":
            trap_active = True
            chart_type = "fibonacci"
        else:
            # Set active button based on current type
            if chart_type == "basic":
                basic_active = True
            elif chart_type == "multi":
                multi_active = True
            elif chart_type in ["trap", "fibonacci"]:
                trap_active = True
        
        return basic_active, multi_active, trap_active, chart_type
    
    # PnL Projection graph callback
    @app.callback(
        Output("pnl-projection-graph", "figure"),
        [
            Input("selected-chart-type-store", "data"),
            Input("run-escape-vis-btn", "n_clicks"),
            Input("interval-component", "n_intervals")
        ]
    )
    def update_pnl_graph(chart_type, escape_clicks, n_intervals):
        """Update the PnL projection graph based on selected chart type."""
        # If escape button was clicked, show escape visualization
        if ctx.triggered_id == "run-escape-vis-btn":
            return create_escape_visualization()
        
        # Otherwise, show the selected chart type
        if chart_type == "basic":
            return create_basic_pnl_projection()
        elif chart_type == "multi":
            return create_multi_leverage_pnl()
        elif chart_type == "trap":
            return create_omega_trap_zone_pnl()
        elif chart_type == "fibonacci":
            return create_fibonacci_vortex_pnl()
        
        # Default
        return create_basic_pnl_projection()
    
    # Strategy selection callbacks
    @app.callback(
        [
            Output("selected-strategy-store", "data"),
            Output("simulation-results-store", "data"),
            Output("strategy-vis-title", "children"),
            Output("strategy-default-content", "style"),
            Output("strategy-visualization-graph", "figure"),
            Output("strategy-visualization-graph", "style"),
            Output("strategy-details-container", "style"),
            Output("strategy-risk-level", "children"),
            Output("strategy-success-probability", "children"),
            Output("strategy-expected-pnl", "children"),
            Output("strategy-steps", "children")
        ],
        [
            Input("strategy-stealth-ladder-btn", "n_clicks"),
            Input("strategy-fake-wall-btn", "n_clicks"),
            Input("strategy-flow-spiral-btn", "n_clicks")
        ],
        [
            State("selected-strategy-store", "data")
        ]
    )
    def update_strategy_visualization(stealth_clicks, fake_wall_clicks, flow_clicks, current_strategy):
        """Update the strategy visualization based on selected strategy."""
        # Default return values
        strategy_id = current_strategy
        simulation_results = {}
        strategy_name = "Strategy Visualization"
        default_content_style = {'display': 'block'}
        vis_figure = go.Figure()
        vis_style = {'height': '400px', 'display': 'none'}
        details_style = {'display': 'none'}
        risk_level = ""
        success_prob = ""
        expected_pnl = ""
        steps = []
        
        # Theme for styling
        theme = DASHBOARD_CONFIG["theme"]
        
        # Determine which strategy was selected
        selected_strategy = None
        
        if ctx.triggered_id == "strategy-stealth-ladder-btn":
            strategy_id = "stealth_ladder"
            selected_strategy = StealthLadderStrategy()
        elif ctx.triggered_id == "strategy-fake-wall-btn":
            strategy_id = "fake_wall"
            selected_strategy = FakeWallStrategy()
        elif ctx.triggered_id == "strategy-flow-spiral-btn":
            strategy_id = "flow_spiral"
            selected_strategy = PositiveFlowStrategy()
        elif strategy_id == "stealth_ladder":
            selected_strategy = StealthLadderStrategy()
        elif strategy_id == "fake_wall":
            selected_strategy = FakeWallStrategy()
        elif strategy_id == "flow_spiral":
            selected_strategy = PositiveFlowStrategy()
        
        # If a strategy is selected, update the visualization
        if selected_strategy:
            # Update strategy name
            strategy_name = selected_strategy.name
            
            # Simulate the strategy
            simulation_results = selected_strategy.simulate()
            
            # Generate visualization
            vis_figure = selected_strategy.visualize()
            
            # Update styles
            default_content_style = {'display': 'none'}
            vis_style = {'height': '400px', 'display': 'block'}
            details_style = {'display': 'block'}
            
            # Update strategy details
            risk_level = html.Span(
                selected_strategy.risk_level,
                style={
                    'fontWeight': 'bold',
                    'color': theme['error'] if selected_strategy.risk_level == "High" else
                            theme['warning'] if selected_strategy.risk_level == "Medium" else
                            theme['success']
                }
            )
            
            success_prob = html.Span(
                f"{selected_strategy.success_probability * 100:.1f}%",
                style={
                    'fontWeight': 'bold',
                    'color': theme['success'] if selected_strategy.success_probability >= 0.7 else
                            theme['warning'] if selected_strategy.success_probability >= 0.5 else
                            theme['error']
                }
            )
            
            # Expected PnL calculation
            if 'pnl_change' in simulation_results:
                pnl_value = simulation_results['pnl_change']
                expected_pnl = html.Span(
                    f"${pnl_value:,.2f}",
                    style={
                        'fontWeight': 'bold',
                        'color': theme['success'] if pnl_value > 0 else theme['error']
                    }
                )
            
            # Create steps list
            if 'steps' in simulation_results:
                steps = [
                    html.Li(step['action']) for step in simulation_results['steps']
                ]
        
        return (
            strategy_id,
            simulation_results,
            strategy_name,
            default_content_style,
            vis_figure,
            vis_style,
            details_style,
            risk_level,
            success_prob,
            expected_pnl,
            steps
        )
    
    # Realtime price and PnL updates
    @app.callback(
        [
            Output("current-price-display", "children"),
            Output("current-pnl-display", "children"),
            Output("current-pnl-percent-display", "children")
        ],
        [Input("interval-component", "n_intervals")]
    )
    def update_price_and_pnl(n_intervals):
        """Update the price, PnL, and PnL percentage displays with real-time data."""
        # Get current values
        current_price = get_current_price()
        current_pnl = get_current_pnl()
        current_pnl_percentage = get_current_pnl_percentage()
        
        # Theme for styling
        theme = DASHBOARD_CONFIG["theme"]
        
        # Format price display
        price_display = f"${current_price:.5f}"
        
        # Format PnL display with color
        pnl_color = theme['success'] if current_pnl >= 0 else theme['error']
        pnl_display = html.Span(
            f"${current_pnl:,.2f}",
            style={'color': pnl_color, 'fontWeight': 'bold'}
        )
        
        # Format PnL percentage display with color
        pnl_percent_color = theme['success'] if current_pnl_percentage >= 0 else theme['error']
        pnl_percent_display = html.Span(
            f"{current_pnl_percentage:+.2f}%",
            style={'color': pnl_percent_color, 'fontWeight': 'bold'}
        )
        
        return price_display, pnl_display, pnl_percent_display
    
    # Risk status indicator
    @app.callback(
        [
            Output("risk-status-indicator", "color"),
            Output("risk-status-text", "children"),
            Output("risk-status-text", "style")
        ],
        [Input("interval-component", "n_intervals")]
    )
    def update_risk_status(n_intervals):
        """Update the risk status indicator based on current price."""
        # Get current values
        current_price = get_current_price()
        
        # Get configuration
        token_config = DASHBOARD_CONFIG["token"]
        trap_config = DASHBOARD_CONFIG["trap"]
        theme = DASHBOARD_CONFIG["theme"]
        
        # Determine risk level
        entry_price = token_config["entry_price"]
        trap_start = trap_config["trap_start"]
        trap_end = trap_config["trap_end"]
        emergency_alert = trap_config["emergency_alert"]
        liquidation_price = DASHBOARD_CONFIG["liquidation_price"]
        
        if current_price < liquidation_price * 1.05:
            # Near liquidation - critical
            status_color = theme["error"]
            status_text = "CRITICAL - NEAR LIQUIDATION"
            status_style = {'color': theme["error"], 'fontWeight': 'bold'}
        elif current_price < trap_start:
            # Below trap zone - high danger
            status_color = theme["error"]
            status_text = "HIGH RISK - BELOW TRAP"
            status_style = {'color': theme["error"], 'fontWeight': 'bold'}
        elif current_price < emergency_alert:
            # In trap zone, below emergency alert level
            status_color = theme["error"]
            status_text = "DANGER - DEEP IN TRAP"
            status_style = {'color': theme["error"], 'fontWeight': 'bold'}
        elif current_price < trap_end:
            # In trap zone but above emergency level
            status_color = theme["warning"]
            status_text = "WARNING - IN TRAP ZONE"
            status_style = {'color': theme["warning"], 'fontWeight': 'bold'}
        elif current_price < entry_price:
            # Between trap zone and entry price
            status_color = theme["warning"]
            status_text = "CAUTION - BELOW ENTRY"
            status_style = {'color': theme["warning"], 'fontWeight': 'bold'}
        else:
            # Above entry price - safe
            status_color = theme["success"]
            status_text = "SAFE - ABOVE ENTRY"
            status_style = {'color': theme["success"], 'fontWeight': 'bold'}
        
        return status_color, status_text, status_style 