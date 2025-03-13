# File: visualization/live_dashboard.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import datetime
import json
import pandas as pd
from omega_ai.utils.redis_connection import RedisConnectionManager
from omega_ai.monitor.monitor_market_trends import (
    detect_possible_mm_traps,
    get_current_fibonacci_levels,
    check_fibonacci_level
)

# Initialize Redis connection manager
redis_manager = RedisConnectionManager()

# Constants
class RedisKeys:
    """Redis key constants"""
    LIVE_TRADER_DATA = "omega:live_trader_data"
    LIVE_BATTLE_STATE = "omega:live_battle_state"
    START_TRADING = "omega:start_trading"
    MOVEMENTS_PREFIX = "btc_movements_"

# Initialize Dash app with dark mode
app = dash.Dash(__name__)

# Enhanced dark theme with trend colors
dark_theme = {
    "background": "#121212",
    "paper": "#1E1E1E",
    "text": "#E0E0E0",
    "accent": "#FFB300",
    "green": "#00E676",
    "red": "#FF3D00",
    "blue": "#2196F3",
    "yellow": "#FFD600",
    "orange": "#FF9100"
}

app.layout = html.Div(style={
    "backgroundColor": dark_theme["background"],
    "color": dark_theme["text"],
    "padding": "20px",
    "minHeight": "100vh"
}, children=[
    # Header
    html.Div([
        html.H1("🔱 OMEGA BTC AI - LIVE BATTLE MODE 🔱", 
                style={'textAlign': 'center', 'color': dark_theme["accent"]}),
        html.Div([
            html.H2("💰 BTC Price:", style={'display': 'inline-block', 'marginRight': '10px'}),
            html.H2(id='live-btc-price', style={'display': 'inline-block', 'color': dark_theme["green"]}),
        ], style={'textAlign': 'center'}),
    ]),
    
    # Battle Controls
    html.Div([
        html.Button("▶️ Start Battle", id="start-battle", style={
            'backgroundColor': dark_theme["green"],
            'color': 'white',
            'border': 'none',
            'padding': '10px 20px',
            'margin': '10px',
            'borderRadius': '5px'
        }),
        html.Button("🔄 Reset Arena", id="reset-arena", style={
            'backgroundColor': dark_theme["blue"],
            'color': 'white',
            'border': 'none',
            'padding': '10px 20px',
            'margin': '10px',
            'borderRadius': '5px'
        }),
    ], style={'textAlign': 'center', 'margin': '20px'}),
    
    # Battle Stats
    html.Div([
        html.Div(id="battle-stats", style={
            'backgroundColor': dark_theme["paper"],
            'padding': '20px',
            'borderRadius': '10px',
            'margin': '20px 0'
        }),
        html.Div(id="battle-day", style={
            'textAlign': 'center',
            'fontSize': '24px',
            'margin': '20px 0'
        })
    ]),
    
    # Trader Performance
    html.Div([
        html.H2("📊 Trader Performance", style={'color': dark_theme["accent"]}),
        html.Div(id="trader-leaderboard", style={
            'backgroundColor': dark_theme["paper"],
            'padding': '20px',
            'borderRadius': '10px'
        })
    ]),
    
    # Market Trends Analysis
    html.Div([
        html.H2("📊 Market Trends Analysis", style={'color': dark_theme["accent"]}),
        html.Div([
            # Timeframe Analysis
            html.Div([
                html.H3("Timeframe Analysis", style={'color': dark_theme["text"]}),
                html.Div(id='timeframe-analysis', style={
                    'backgroundColor': dark_theme["paper"],
                    'padding': '15px',
                    'borderRadius': '10px',
                    'marginBottom': '15px'
                })
            ]),
            
            # MM Trap Alerts
            html.Div([
                html.H3("Market Maker Trap Alerts", style={'color': dark_theme["text"]}),
                html.Div(id='mm-trap-alerts', style={
                    'backgroundColor': dark_theme["paper"],
                    'padding': '15px',
                    'borderRadius': '10px',
                    'marginBottom': '15px'
                })
            ]),
            
            # Fibonacci Levels
            html.Div([
                html.H3("Fibonacci Levels", style={'color': dark_theme["text"]}),
                html.Div(id='fibonacci-levels', style={
                    'backgroundColor': dark_theme["paper"],
                    'padding': '15px',
                    'borderRadius': '10px'
                })
            ])
        ])
    ]),
    
    # Charts
    html.Div([
        dcc.Graph(id='price-chart'),
        dcc.Graph(id='performance-chart')
    ]),
    
    # Hidden states
    dcc.Store(id='trader-state'),
    dcc.Store(id='battle-state'),
    
    # Update interval
    dcc.Interval(id='update-interval', interval=2000, n_intervals=0)
])

@app.callback(
    [Output('live-btc-price', 'children'),
     Output('battle-stats', 'children'),
     Output('battle-day', 'children'),
     Output('price-chart', 'figure'),
     Output('performance-chart', 'figure'),
     Output('trader-leaderboard', 'children')],
    [Input('update-interval', 'n_intervals')]
)
def update_battle_display(n_intervals):
    """Update all battle display components"""
    try:
        # Fetch latest data from Redis
        battle_state = json.loads(redis_manager.get(RedisKeys.LIVE_BATTLE_STATE) or "{}")
        trader_data = json.loads(redis_manager.get(RedisKeys.LIVE_TRADER_DATA) or "{}")
        
        # Current price display
        current_price = battle_state.get('btc_price', 0)
        price_display = f"${current_price:,.2f}"
        
        # Battle stats
        stats = html.Div([
            html.H3("Battle Statistics", style={'color': dark_theme["accent"]}),
            html.Div([
                html.Div(f"Day {battle_state.get('day', 1)} - Session {battle_state.get('session', 1)}/4"),
                html.Div(f"Total Trades: {sum(t.get('trades', 0) for t in trader_data.values())}"),
                html.Div("Status: " + ("🟢 Active" if battle_state.get('battle_active') else "🔴 Paused"))
            ])
        ])
        
        # Battle day
        battle_day = f"Day {battle_state.get('day', 1)} | Session {battle_state.get('session', 1)}/4"
        
        # Price chart
        price_history = battle_state.get('btc_history', [])
        price_fig = go.Figure()
        price_fig.add_trace(go.Scatter(
            y=price_history,
            mode='lines',
            name='BTC Price',
            line=dict(color=dark_theme["green"])
        ))
        price_fig.update_layout(
            title="BTC Price History",
            plot_bgcolor=dark_theme["paper"],
            paper_bgcolor=dark_theme["background"],
            font=dict(color=dark_theme["text"]),
            showlegend=False
        )
        
        # Performance chart
        perf_fig = go.Figure()
        for profile, data in trader_data.items():
            perf_fig.add_trace(go.Bar(
                name=profile.capitalize(),
                y=[data.get('pnl', 0)],
                marker_color=dark_theme["green"] if data.get('pnl', 0) >= 0 else dark_theme["red"]
            ))
        perf_fig.update_layout(
            title="Trader PnL Comparison",
            plot_bgcolor=dark_theme["paper"],
            paper_bgcolor=dark_theme["background"],
            font=dict(color=dark_theme["text"])
        )
        
        # Leaderboard
        leaderboard = html.Div([
            html.Div([
                html.H3(data['name']),
                html.Div([
                    html.Span(f"${data['capital'] + data.get('pnl', 0):,.2f}"),
                    html.Span(f" ({data.get('pnl', 0)/data['capital']*100:+.1f}%)")
                ], style={'color': dark_theme["green"] if data.get('pnl', 0) >= 0 else dark_theme["red"]}),
                html.Div(f"Win Rate: {data.get('win_rate', 0)*100:.1f}%")
            ], style={
                'backgroundColor': dark_theme["background"],
                'padding': '10px',
                'margin': '5px',
                'borderRadius': '5px'
            }) for profile, data in sorted(
                trader_data.items(),
                key=lambda x: x[1].get('pnl', 0),
                reverse=True
            )
        ])
        
        return price_display, stats, battle_day, price_fig, perf_fig, leaderboard
        
    except Exception as e:
        print(f"Error updating display: {e}")
        return "N/A", "Error loading stats", "Day 1", {}, {}, "Error loading leaderboard"

# Add new callback for market trends
@app.callback(
    [Output('timeframe-analysis', 'children'),
     Output('mm-trap-alerts', 'children'),
     Output('fibonacci-levels', 'children')],
    [Input('update-interval', 'n_intervals')]
)
def update_market_trends(n_intervals):
    """Update market trends analysis display"""
    try:
        # Get latest price and movements data
        battle_state = json.loads(redis_manager.get(RedisKeys.LIVE_BATTLE_STATE) or "{}")
        current_price = battle_state.get('btc_price', 0)
        
        # Timeframe Analysis
        timeframes = {
            "1min": {"trend": None, "change": 0},
            "5min": {"trend": None, "change": 0},
            "10min": {"trend": None, "change": 0}
        }
        
        timeframe_analysis = []
        for timeframe, data in timeframes.items():
            trend_color = dark_theme["green"] if "Bullish" in str(data["trend"]) else \
                         dark_theme["red"] if "Bearish" in str(data["trend"]) else \
                         dark_theme["text"]
            
            timeframe_analysis.append(
                html.Div([
                    html.Span(f"{timeframe}: ", style={'color': dark_theme["accent"]}),
                    html.Span(f"{data['trend'] or 'Analyzing...'} ", 
                             style={'color': trend_color}),
                    html.Span(f"({data['change']:+.2f}%)" if data['change'] else "")
                ])
            )
        
        # MM Trap Detection
        mm_traps = []
        for timeframe, data in timeframes.items():
            if data["trend"] and data["change"]:
                trap_type, confidence = detect_possible_mm_traps(
                    timeframe, data["trend"], data["change"], 
                    abs(data["change"] * current_price / 100)
                )
                if trap_type:
                    mm_traps.append(html.Div([
                        html.Span("⚠️ ", style={'marginRight': '5px'}),
                        html.Span(f"{timeframe}: {trap_type} ", 
                                style={'color': dark_theme["orange"]}),
                        html.Span(f"(Confidence: {confidence:.0%})")
                    ]))
        
        if not mm_traps:
            mm_traps = [html.Div("No MM traps detected", 
                               style={'color': dark_theme["green"]})]
        
        # Fibonacci Analysis
        fib_levels = get_current_fibonacci_levels()
        fib_hit = check_fibonacci_level(current_price)
        
        fibonacci_display = []
        if fib_hit:
            fibonacci_display.append(html.Div([
                html.Span("⭐ Current Price at ", style={'color': dark_theme["accent"]}),
                html.Span(f"Fibonacci {fib_hit['level']} ", 
                         style={'color': dark_theme["green"]}),
                html.Span(f"(${fib_hit['price']:,.2f})")
            ]))
        
        if fib_levels:
            for level, price in fib_levels.items():
                color = dark_theme["green"] if price < current_price else \
                        dark_theme["red"] if price > current_price else \
                        dark_theme["text"]
                fibonacci_display.append(html.Div([
                    html.Span(f"{level}: ", style={'color': dark_theme["accent"]}),
                    html.Span(f"${price:,.2f}", style={'color': color})
                ]))
        
        return timeframe_analysis, mm_traps, fibonacci_display
        
    except Exception as e:
        print(f"Error updating market trends: {e}")
        return (
            [html.Div("Error loading timeframe analysis")],
            [html.Div("Error loading MM trap alerts")],
            [html.Div("Error loading Fibonacci levels")]
        )

if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host="0.0.0.0")
