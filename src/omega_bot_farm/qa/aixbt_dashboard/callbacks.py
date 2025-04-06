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

from .config import DASHBOARD_CONFIG
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
            Input("run-escape-vis-btn", "n_clicks")
        ]
    )
    def update_pnl_graph(chart_type, escape_clicks):
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
    
    # Interval update callback
    @app.callback(
        Output("current-price-display", "children"),
        [Input("interval-component", "n_intervals")]
    )
    def update_current_price(n_intervals):
        """Update the current price display (mock implementation)."""
        # This would normally fetch the current price from an API
        # For the demo, we'll just return the static value
        return f"${DASHBOARD_CONFIG['token']['current_price']:.5f}" 