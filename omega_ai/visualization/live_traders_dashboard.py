"""
OMEGA BTC AI - Live Traders Dashboard
====================================

A real-time monitoring dashboard for the OMEGA BTC AI Live Traders system.
Provides live updates on trader performance, positions, and system status.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import json
import logging
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Dash app
app = dash.Dash(__name__, title="OMEGA BTC AI - Live Traders Dashboard")

# Terminal colors for blessed output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

def create_layout():
    """Create the main dashboard layout."""
    return html.Div([
        # Header
        html.Div([
            html.H1("OMEGA BTC AI - Live Traders Dashboard", 
                   className="header-title"),
            html.Div(id="last-update", className="last-update")
        ], className="header"),
        
        # Main Grid
        html.Div([
            # Left Column - Trader Stats
            html.Div([
                html.H2("Trader Performance", className="section-title"),
                html.Div(id="trader-stats", className="stats-grid"),
                
                html.H2("Active Positions", className="section-title"),
                html.Div(id="active-positions", className="positions-grid"),
                
                html.H2("System Status", className="section-title"),
                html.Div(id="system-status", className="status-grid")
            ], className="left-column"),
            
            # Right Column - Charts
            html.Div([
                html.H2("Performance Metrics", className="section-title"),
                dcc.Graph(id="performance-chart"),
                
                html.H2("Position Distribution", className="section-title"),
                dcc.Graph(id="position-chart"),
                
                html.H2("Risk Metrics", className="section-title"),
                dcc.Graph(id="risk-chart")
            ], className="right-column")
        ], className="main-grid"),
        
        # Update Interval
        dcc.Interval(
            id='interval-component',
            interval=1*1000,  # Update every second
            n_intervals=0
        )
    ])

def create_trader_stats(traders: Dict) -> html.Div:
    """Create trader performance statistics cards."""
    stats = []
    for profile, trader in traders.items():
        stats.append(html.Div([
            html.H3(profile.title(), className="trader-name"),
            html.Div([
                html.Div([
                    html.Span("PnL", className="metric-label"),
                    html.Span(f"${trader.total_pnl:.2f}", 
                             className=f"metric-value {'positive' if trader.total_pnl >= 0 else 'negative'}")
                ], className="metric-card"),
                html.Div([
                    html.Span("Win Rate", className="metric-label"),
                    html.Span(f"{trader.win_rate:.1%}", className="metric-value")
                ], className="metric-card"),
                html.Div([
                    html.Span("Sharpe", className="metric-label"),
                    html.Span(f"{trader.calculate_sharpe_ratio():.2f}", className="metric-value")
                ], className="metric-card")
            ], className="metrics-grid")
        ], className="trader-card"))
    return html.Div(stats, className="trader-stats")

def create_active_positions(traders: Dict) -> html.Div:
    """Create active positions display."""
    positions = []
    for profile, trader in traders.items():
        for position in trader.get_positions():
            if position['status'] == 'OPEN':
                positions.append(html.Div([
                    html.H4(f"{profile.title()} - {position['side']}", className="position-title"),
                    html.Div([
                        html.Div([
                            html.Span("Entry", className="position-label"),
                            html.Span(f"${position['entry_price']:.2f}", className="position-value")
                        ], className="position-detail"),
                        html.Div([
                            html.Span("Current", className="position-label"),
                            html.Span(f"${trader.current_price:.2f}", className="position-value")
                        ], className="position-detail"),
                        html.Div([
                            html.Span("PnL", className="position-label"),
                            html.Span(f"${position['unrealized_pnl']:.2f}", 
                                     className=f"position-value {'positive' if position['unrealized_pnl'] >= 0 else 'negative'}")
                        ], className="position-detail")
                    ], className="position-details")
                ], className="position-card"))
    return html.Div(positions, className="active-positions")

def create_system_status(traders: Dict) -> html.Div:
    """Create system status display."""
    total_pnl = sum(trader.total_pnl for trader in traders.values())
    active_positions = sum(
        len([p for p in trader.get_positions() if p['status'] == 'OPEN'])
        for trader in traders.values()
    )
    
    return html.Div([
        html.Div([
            html.Span("Total PnL", className="status-label"),
            html.Span(f"${total_pnl:.2f}", 
                     className=f"status-value {'positive' if total_pnl >= 0 else 'negative'}")
        ], className="status-card"),
        html.Div([
            html.Span("Active Positions", className="status-label"),
            html.Span(str(active_positions), className="status-value")
        ], className="status-card"),
        html.Div([
            html.Span("System Health", className="status-label"),
            html.Span("OPERATIONAL", className="status-value positive")
        ], className="status-card")
    ], className="system-status")

def create_performance_chart(traders: Dict) -> go.Figure:
    """Create performance chart."""
    df = pd.DataFrame()
    for profile, trader in traders.items():
        df[profile] = [trader.total_pnl]
    
    fig = go.Figure()
    for column in df.columns:
        fig.add_trace(go.Bar(
            name=column.title(),
            y=[df[column].iloc[0]],
            text=[f"${df[column].iloc[0]:.2f}"],
            textposition='auto',
        ))
    
    fig.update_layout(
        title="Trader Performance",
        yaxis_title="PnL (USDT)",
        showlegend=True,
        height=400
    )
    return fig

def create_position_chart(traders: Dict) -> go.Figure:
    """Create position distribution chart."""
    positions = []
    for trader in traders.values():
        for position in trader.get_positions():
            if position['status'] == 'OPEN':
                positions.append({
                    'side': position['side'],
                    'size': position['size'],
                    'leverage': position['leverage']
                })
    
    if not positions:
        return go.Figure()
    
    df = pd.DataFrame(positions)
    fig = px.pie(df, names='side', values='size', title="Position Distribution")
    fig.update_layout(height=400)
    return fig

def create_risk_chart(traders: Dict) -> go.Figure:
    """Create risk metrics chart."""
    risk_data = []
    for profile, trader in traders.values():
        risk_data.append({
            'profile': profile.title(),
            'sharpe': trader.calculate_sharpe_ratio(),
            'drawdown': trader.calculate_max_drawdown(),
            'win_rate': trader.win_rate
        })
    
    df = pd.DataFrame(risk_data)
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['profile'],
        y=df['sharpe'],
        name='Sharpe Ratio',
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['profile'],
        y=df['drawdown'],
        name='Max Drawdown',
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title="Risk Metrics",
        yaxis_title="Value",
        showlegend=True,
        height=400
    )
    return fig

# Initialize live traders
live_traders = BitGetLiveTraders(use_testnet=True)

@app.callback(
    [Output("trader-stats", "children"),
     Output("active-positions", "children"),
     Output("system-status", "children"),
     Output("performance-chart", "figure"),
     Output("position-chart", "figure"),
     Output("risk-chart", "figure"),
     Output("last-update", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_dashboard(n):
    """Update dashboard with latest data."""
    try:
        # Update trader states
        for trader in live_traders.traders.values():
            trader.update_price(trader.get_market_ticker("BTCUSDT_UMCBL")['last'])
            trader.manage_open_positions()
        
        # Create dashboard components
        trader_stats = create_trader_stats(live_traders.traders)
        active_positions = create_active_positions(live_traders.traders)
        system_status = create_system_status(live_traders.traders)
        performance_chart = create_performance_chart(live_traders.traders)
        position_chart = create_position_chart(live_traders.traders)
        risk_chart = create_risk_chart(live_traders.traders)
        
        # Update timestamp
        last_update = f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return (trader_stats, active_positions, system_status, 
                performance_chart, position_chart, risk_chart, last_update)
                
    except Exception as e:
        logger.error(f"Error updating dashboard: {str(e)}")
        return dash.no_update

# Add custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>OMEGA BTC AI - Live Traders Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #1a1a1a;
                color: #ffffff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .header {
                background-color: #2d2d2d;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 10px;
            }
            
            .header-title {
                color: #00ff00;
                margin: 0;
                font-size: 24px;
            }
            
            .last-update {
                color: #888;
                font-size: 14px;
                margin-top: 5px;
            }
            
            .main-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                padding: 20px;
            }
            
            .section-title {
                color: #00ff00;
                margin: 20px 0 10px;
                font-size: 18px;
            }
            
            .trader-card {
                background-color: #2d2d2d;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 8px;
            }
            
            .trader-name {
                color: #00ff00;
                margin: 0 0 10px 0;
            }
            
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
            }
            
            .metric-card {
                background-color: #3d3d3d;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
            }
            
            .metric-label {
                display: block;
                color: #888;
                font-size: 12px;
            }
            
            .metric-value {
                display: block;
                font-size: 16px;
                font-weight: bold;
            }
            
            .positive {
                color: #00ff00;
            }
            
            .negative {
                color: #ff0000;
            }
            
            .position-card {
                background-color: #2d2d2d;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 8px;
            }
            
            .position-title {
                color: #00ff00;
                margin: 0 0 10px 0;
            }
            
            .position-details {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
            }
            
            .position-detail {
                background-color: #3d3d3d;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
            }
            
            .position-label {
                display: block;
                color: #888;
                font-size: 12px;
            }
            
            .position-value {
                display: block;
                font-size: 16px;
                font-weight: bold;
            }
            
            .status-card {
                background-color: #2d2d2d;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 8px;
                text-align: center;
            }
            
            .status-label {
                display: block;
                color: #888;
                font-size: 12px;
            }
            
            .status-value {
                display: block;
                font-size: 18px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Set the layout
app.layout = create_layout()

if __name__ == '__main__':
    app.run_server(debug=True, port=8050) 