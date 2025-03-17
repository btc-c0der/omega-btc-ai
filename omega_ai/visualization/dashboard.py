#!/usr/bin/env python3

"""
OMEGA RASTA BTC DASHBOARD - Bio-Energy Emotional Futures Trading Interface

A spiritually-aligned dashboard for monitoring Bitcoin trading with Rastafarian vibrations,
Fibonacci harmony, and Schumann resonance energy integration.
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import datetime
import json
import pandas as pd
import random
import redis
import logging
import time
import sys
import os
from omega_ai.utils.redis_connection import RedisConnectionManager
from omega_ai.monitor.monitor_market_trends import (
    analyze_price_trend,
    get_current_fibonacci_levels,
    check_fibonacci_level
)

# Setup enhanced debug logging
# Configure logging with detailed formatting and terminal colors
class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for terminal output"""
    
    # Terminal colors
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    RESET = "\033[0m"
    
    FORMATS = {
        logging.DEBUG: f"{CYAN}%(asctime)s - [%(name)s] - %(levelname)s - %(message)s{RESET}",
        logging.INFO: f"{GREEN}%(asctime)s - [%(name)s] - %(levelname)s - %(message)s{RESET}",
        logging.WARNING: f"{YELLOW}%(asctime)s - [%(name)s] - %(levelname)s - %(message)s{RESET}",
        logging.ERROR: f"{RED}%(asctime)s - [%(name)s] - %(levelname)s - %(message)s{RESET}",
        logging.CRITICAL: f"{MAGENTA}%(asctime)s - [%(name)s] - %(levelname)s - %(message)s{RESET}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S.%f")
        return formatter.format(record)

# Setup logger
logger = logging.getLogger("OMEGA_RASTA_DASHBOARD")
logger.setLevel(logging.DEBUG)  # Set to DEBUG for maximum verbosity

# Console handler with colors
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(ColoredFormatter())
logger.addHandler(console_handler)

# File handler for persistent logs
os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/dashboard.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

logger.info("🌟🌟🌟 STARTING OMEGA RASTA BTC DASHBOARD 🌟🌟🌟")

# Initialize Redis connection manager
logger.debug("Initializing Redis Connection Manager")
redis_manager = RedisConnectionManager()
redis_conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
logger.info("Redis connection established")

# Rasta quotes for inspiration
RASTA_QUOTES = [
    "JAH provide the herb, mon - Green energy for trading wisdom 🌿",
    "One love, one heart, one BTC position 🚀",
    "Every little thing gonna be alright with proper risk management 💚",
    "Who feels it knows it, market maker traps clear to the wise ⚠️",
    "The market is a mighty river, flowing with natural Fibonacci rhythms 📈",
    "Lion of Judah watches over your trades with divine strength 🦁",
    "Positive vibration, positive profit, yeah! Rise up this morning! 🌞",
    "Get up, stand up, don't give up the trade 💰",
    "Bitcoin burnin' and lootin' the old financial system 🔥",
    "No monkey business with these trading strategies mon 🐒",
    "Exodus movement of JAH profitable people 📊",
    "Babylon system cannot predict these Fibonacci levels 🔮",
    "Them belly full but we hungry for gainz 💪",
    "Three little birds pitch by my BTC charts 🐦🐦🐦"
]

# Constants
class RedisKeys:
    """Redis key constants"""
    LIVE_TRADER_DATA = "omega:live_trader_data"
    LIVE_BATTLE_STATE = "omega:live_battle_state"
    START_TRADING = "omega:start_trading"
    MOVEMENTS_PREFIX = "btc_movements_"
    SCHUMANN_RESONANCE = "schumann_resonance"
    SCHUMANN_HISTORY = "schumann_history"
    BTC_MOVEMENT_HISTORY = "btc_movement_history"
    MARKET_REGIME = "market_regime" 
    LATEST_MOVEMENT_ANALYSIS = "latest_movement_analysis"
    LATEST_ORGANIC_ANALYSIS = "latest_organic_analysis"
    FIBONACCI_CONFLUENCE_ZONES = "fibonacci_confluence_zones"

# Enhanced Rasta theme colors
rasta_theme = {
    "background": "#121212",
    "paper": "#1E1E1E",
    "text": "#E0E0E0",
    "accent": "#FFD700",  # Gold
    "green": "#00B52D",   # Rasta Green
    "red": "#FF3D00",
    "yellow": "#FFDD00",  # Rasta Yellow
    "orange": "#FF9100",
    "darkgreen": "#006400",
    "headings": "#FFB300",
    "secondary": "#3D5AFE",
    "panel": "#242424",
    "highlight": "#388E3C"
}

# Initialize Dash app with Rasta theme
app = dash.Dash(
    __name__, 
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
app.title = "OMEGA RASTA BTC DASHBOARD"

# App Layout with Enhanced Rasta Design
app.layout = html.Div(style={
    "backgroundColor": rasta_theme["background"],
    "color": rasta_theme["text"],
    "padding": "20px",
    "minHeight": "100vh",
    "fontFamily": "'Montserrat', sans-serif"
}, children=[
    # Banner with Rasta colors
    html.Div([
        html.Div([
            html.Img(src="https://i.ibb.co/Cn5xnGz/rasta-lion.png", height="80px", style={"marginRight": "20px"}),
            html.H1("🔱 OMEGA RASTA BTC DASHBOARD 🔱", style={'color': rasta_theme["accent"]}),
            html.Img(src="https://i.ibb.co/Cn5xnGz/rasta-lion.png", height="80px", style={"marginLeft": "20px", "transform": "scaleX(-1)"}),
        ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
        
        # Inspiration quote
        html.Div(id='rasta-quote', style={
            'textAlign': 'center',
            'fontStyle': 'italic',
            'margin': '10px 0',
            'color': rasta_theme["yellow"]
        }),
        
        # BTC Price with color indication
        html.Div([
            html.H2("💰 BTC PRICE:", style={'display': 'inline-block', 'marginRight': '10px'}),
            html.H2(id='live-btc-price', style={'display': 'inline-block', 'color': rasta_theme["green"]}),
            html.Span(id='price-change', style={'marginLeft': '10px', 'fontSize': '1.2rem'})
        ], style={'textAlign': 'center'}),
        
    ], style={
        'textAlign': 'center',
        'padding': '20px',
        'backgroundImage': 'linear-gradient(to right, #006400, #000000, #FF0000)',
        'borderRadius': '10px',
        'marginBottom': '20px'
    }),
    
    # Battle Controls with Rasta styling
    html.Div([
        html.Button("▶️ START JAH TRADING", id="start-battle", style={
            'backgroundColor': rasta_theme["green"],
            'color': 'white',
            'border': 'none',
            'padding': '15px 25px',
            'margin': '10px',
            'borderRadius': '5px',
            'fontSize': '16px',
            'fontWeight': 'bold',
            'cursor': 'pointer'
        }),
        html.Button("⏹️ BABYLON PAUSE", id="pause-battle", style={
            'backgroundColor': rasta_theme["red"],
            'color': 'white',
            'border': 'none',
            'padding': '15px 25px',
            'margin': '10px',
            'borderRadius': '5px',
            'fontSize': '16px',
            'fontWeight': 'bold',
            'cursor': 'pointer'
        }),
        html.Button("🔄 ITAL RESET", id="reset-arena", style={
            'backgroundColor': rasta_theme["secondary"],
            'color': 'white',
            'border': 'none',
            'padding': '15px 25px',
            'margin': '10px',
            'borderRadius': '5px',
            'fontSize': '16px',
            'fontWeight': 'bold',
            'cursor': 'pointer'
        }),
    ], style={'textAlign': 'center', 'margin': '20px'}),
    
    # Main dashboard content - 2 columns layout
    html.Div([
        # Left Column - Trading Profiles and Performance
        html.Div([
            # Trader Battle Section
            html.Div([
                html.Div([
                    html.H2("🏆 TRADER BABYLON BATTLE", style={'color': rasta_theme["accent"], 'textAlign': 'center'}),
                    html.Div(id="battle-day", style={
                        'textAlign': 'center',
                        'fontSize': '20px',
                        'padding': '10px',
                        'backgroundColor': rasta_theme["panel"],
                        'borderRadius': '5px',
                        'margin': '10px 0'
                    }),
                ]),
                
                # Trader Leaderboard with Achievement Badges
                html.Div([
                    html.H3("💰 TRADER RANKINGS", style={'color': rasta_theme["green"]}),
                    html.Div(id="trader-leaderboard")
                ], style={
                    'backgroundColor': rasta_theme["paper"],
                    'borderRadius': '10px',
                    'padding': '15px',
                    'marginBottom': '20px'
                }),
                
                # Trader Performance Chart
                html.Div([
                    html.H3("📈 PERFORMANCE", style={'color': rasta_theme["green"]}),
                    dcc.Graph(id='performance-chart', config={'displayModeBar': False})
                ], style={
                    'backgroundColor': rasta_theme["paper"],
                    'borderRadius': '10px',
                    'padding': '15px',
                    'marginBottom': '20px'
                }),
                
                # Trader Emotional States
                html.Div([
                    html.H3("🧘‍♂️ TRADER VIBES", style={'color': rasta_theme["yellow"]}),
                    html.Div(id='emotional-states', style={
                        'display': 'flex',
                        'justifyContent': 'space-around',
                        'flexWrap': 'wrap'
                    })
                ], style={
                    'backgroundColor': rasta_theme["paper"],
                    'borderRadius': '10px',
                    'padding': '15px',
                    'marginBottom': '20px'
                })
            ], style={'marginBottom': '20px'}),
            
            # RASTA POWER OMEGA SUGGESTIONS PANEL
            html.Div([
                html.H2("🌟 RASTA POWER TRADING SUGGESTIONS 🌟", style={
                    'color': rasta_theme["accent"], 
                    'textAlign': 'center',
                    'backgroundImage': 'linear-gradient(to right, #006400, #000000, #FF0000)',
                    'padding': '10px',
                    'borderRadius': '5px'
                }),
                html.Div(id='trading-suggestions', style={
                    'backgroundColor': rasta_theme["paper"],
                    'padding': '15px',
                    'borderRadius': '10px',
                    'border': f'2px solid {rasta_theme["accent"]}',
                })
            ], style={'marginBottom': '20px'}),
            
            # Achievements and Gamification
            html.Div([
                html.H3("🏅 TRADER ACHIEVEMENTS", style={'color': rasta_theme["yellow"]}),
                html.Div(id='achievements-panel', style={
                    'backgroundColor': rasta_theme["paper"],
                    'padding': '15px',
                    'borderRadius': '10px',
                })
            ]),
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        # Right Column - Market Analysis
        html.Div([
            # Market Trends Section
            html.Div([
                html.H2("🌊 MARKET VIBRATIONS", style={'color': rasta_theme["accent"], 'textAlign': 'center'}),
                
                # Price Chart with Fibonacci Levels
                html.Div([
                    html.H3("📊 PRICE HISTORY", style={'color': rasta_theme["green"]}),
                    dcc.Graph(id='price-chart', config={'displayModeBar': False})
                ], style={
                    'backgroundColor': rasta_theme["paper"],
                    'borderRadius': '10px',
                    'padding': '15px',
                    'marginBottom': '20px'
                }),
                
                # Market Regime and Timeframe Analysis
                html.Div([
                    html.H3("⏱️ TIMEFRAME ANALYSIS", style={'color': rasta_theme["green"]}),
                    html.Div(id='market-regime', style={
                        'backgroundColor': rasta_theme["panel"],
                        'padding': '10px',
                        'borderRadius': '5px',
                        'marginBottom': '10px',
                        'textAlign': 'center',
                        'fontSize': '18px'
                    }),
                    html.Div(id='timeframe-analysis', style={
                        'backgroundColor': rasta_theme["panel"],
                        'padding': '10px',
                        'borderRadius': '5px'
                    })
                ], style={
                    'backgroundColor': rasta_theme["paper"],
                    'borderRadius': '10px',
                    'padding': '15px',
                    'marginBottom': '20px'
                }),
                
                # Fibonacci Analysis Panel
                html.Div([
                    html.H3("🌀 FIBONACCI COSMIC ALIGNMENT", style={'color': rasta_theme["yellow"]}),
                    html.Div(id='fibonacci-levels', style={
                        'backgroundColor': rasta_theme["panel"],
                        'padding': '10px',
                        'borderRadius': '5px',
                        'marginBottom': '10px'
                    }),
                    html.Div(id='fibonacci-confluence', style={
                        'backgroundColor': rasta_theme["panel"],
                        'padding': '10px',
                        'borderRadius': '5px'
                    })
                ], style={
                    'backgroundColor': rasta_theme["paper"],
                    'borderRadius': '10px',
                    'padding': '15px',
                    'marginBottom': '20px'
                }),
                
                # MM Trap Detection
                html.Div([
                    html.H3("⚠️ BABYLON MARKET MAKER TRAPS", style={'color': rasta_theme["red"]}),
                    html.Div(id='mm-trap-alerts', style={
                        'backgroundColor': rasta_theme["panel"],
                        'padding': '10px',
                        'borderRadius': '5px'
                    })
                ], style={
                    'backgroundColor': rasta_theme["paper"],
                    'borderRadius': '10px',
                    'padding': '15px',
                    'marginBottom': '20px'
                }),
                
                # Schumann Resonance Panel
                html.Div([
                    html.H3("🌍 SCHUMANN RESONANCE", style={'color': rasta_theme["accent"]}),
                    html.Div([
                        html.Div(id='schumann-current', style={
                            'fontSize': '24px',
                            'textAlign': 'center',
                            'padding': '10px'
                        }),
                        html.Div(id='schumann-status', style={
                            'textAlign': 'center',
                            'padding': '5px',
                            'marginBottom': '10px'
                        }),
                        dcc.Graph(id='schumann-chart', config={'displayModeBar': False})
                    ])
                ], style={
                    'backgroundColor': rasta_theme["paper"],
                    'borderRadius': '10px',
                    'padding': '15px'
                }),
                
                # FUD and FOMO News Feed
                html.Div([
                    html.H3("📰 BABYLON NEWS FEED", style={'color': rasta_theme["red"]}),
                    html.Div(id='news-feed', style={
                        'backgroundColor': rasta_theme["panel"],
                        'padding': '10px',
                        'borderRadius': '5px',
                        'maxHeight': '200px',
                        'overflow': 'auto'
                    })
                ], style={
                    'backgroundColor': rasta_theme["paper"],
                    'borderRadius': '10px',
                    'padding': '15px',
                    'marginTop': '20px'
                }),
            ])
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'}),
    ]),
    
    # Hidden states
    dcc.Store(id='trader-state'),
    dcc.Store(id='battle-state'),
    
    # Update interval
    dcc.Interval(id='update-interval', interval=2500, n_intervals=0),
    dcc.Interval(id='quote-interval', interval=20000, n_intervals=0),  # Rasta quote updates
])

@app.callback(
    Output('rasta-quote', 'children'),
    [Input('quote-interval', 'n_intervals')]
)
def update_rasta_quote(n_intervals):
    """Update the Rastafarian inspiration quote"""
    logger.debug(f"Updating Rasta quote - interval: {n_intervals}")
    quote = random.choice(RASTA_QUOTES)
    logger.debug(f"Selected quote: {quote}")
    return quote

@app.callback(
    [Output('live-btc-price', 'children'),
     Output('price-change', 'children'),
     Output('price-change', 'style'),
     Output('battle-day', 'children'),
     Output('price-chart', 'figure'),
     Output('performance-chart', 'figure'),
     Output('trader-leaderboard', 'children'),
     Output('emotional-states', 'children'),
     Output('achievements-panel', 'children'),
     Output('trading-suggestions', 'children')],
    [Input('update-interval', 'n_intervals')]
)
def update_battle_display(n_intervals):
    """Update battle display components"""
    start_time = time.time()
    logger.debug(f"Starting update_battle_display - interval: {n_intervals}")
    
    try:
        # Fetch latest data from Redis
        logger.debug("Fetching battle state from Redis")
        battle_state_raw = redis_manager.get(RedisKeys.LIVE_BATTLE_STATE)
        logger.debug(f"Raw battle state: {battle_state_raw[:100]}..." if battle_state_raw and len(battle_state_raw) > 100 else battle_state_raw)
        
        battle_state = json.loads(battle_state_raw or "{}")
        logger.debug(f"Parsed battle state keys: {list(battle_state.keys())}")
        
        logger.debug("Fetching trader data from Redis")
        trader_data_raw = redis_manager.get(RedisKeys.LIVE_TRADER_DATA)
        trader_data = json.loads(trader_data_raw or "{}")
        logger.debug(f"Found {len(trader_data)} traders: {list(trader_data.keys())}")
        
        # Current price display
        current_price = battle_state.get('btc_price', 0)
        logger.debug(f"Current BTC price: ${current_price:,.2f}")
        price_display = f"${current_price:,.2f}"
        
        # Price change calculation
        price_history = battle_state.get('btc_history', [])
        logger.debug(f"Price history length: {len(price_history)}")
        
        if len(price_history) > 1:
            logger.debug(f"First price: {price_history[0]}, Latest price: {price_history[-1]}")
            price_change = (price_history[-1] - price_history[0]) / price_history[0] * 100
            logger.debug(f"Calculated price change: {price_change:+.2f}%")
            price_change_text = f"{price_change:+.2f}%"
            price_change_style = {
                'color': rasta_theme["green"] if price_change >= 0 else rasta_theme["red"],
                'marginLeft': '10px',
                'fontSize': '1.2rem'
            }
        else:
            logger.debug("Insufficient price history, using default values")
            price_change_text = "+0.00%"
            price_change_style = {'color': rasta_theme["text"], 'marginLeft': '10px', 'fontSize': '1.2rem'}
        
        # Battle day with Rastafarian styling
        logger.debug(f"Battle day: {battle_state.get('day', 1)}, Session: {battle_state.get('session', 1)}")
        battle_day = html.Div([
            html.Span("JAH DAY ", style={'color': rasta_theme["yellow"]}),
            html.Span(f"{battle_state.get('day', 1)}", style={'color': rasta_theme["green"]}),
            html.Span(" | TRADING SESSION ", style={'color': rasta_theme["yellow"]}),
            html.Span(f"{battle_state.get('session', 1)}/4", style={'color': rasta_theme["green"]})
        ])
        
        # Price chart with Fibonacci levels
        logger.debug("Creating price chart")
        price_fig = go.Figure()
        
        # Add price line
        price_fig.add_trace(go.Scatter(
            y=price_history,
            mode='lines',
            name='BTC Price',
            line=dict(color=rasta_theme["green"], width=2)
        ))
        
        # Add Fibonacci levels if available
        logger.debug("Fetching Fibonacci levels")
        fib_levels = get_current_fibonacci_levels()
        logger.debug(f"Found {len(fib_levels) if fib_levels else 0} Fibonacci levels")
        
        if fib_levels and price_history:
            for level, price in fib_levels.items():
                if 0.1 < float(level) < 0.9:  # Only show primary levels
                    logger.debug(f"Adding Fibonacci level {level} at price ${price:.2f}")
                    price_fig.add_trace(go.Scatter(
                        y=[price] * len(price_history),
                        mode='lines',
                        name=f'Fib {level}',
                        line=dict(
                            color=rasta_theme["accent" if level == "0.618" else "secondary"],
                            width=1,
                            dash='dash'
                        )
                    ))
        
        price_fig.update_layout(
            title="🌿 BTC PRICE JOURNEY 🌿",
            plot_bgcolor=rasta_theme["paper"],
            paper_bgcolor=rasta_theme["paper"],
            font=dict(color=rasta_theme["text"]),
            margin=dict(l=10, r=10, t=30, b=10),
            showlegend=False,
            height=300,
            xaxis=dict(showticklabels=False)
        )
        
        # Performance chart with Rasta styling
        logger.debug("Creating performance chart")
        perf_fig = go.Figure()
        
        # Sort traders by PnL
        logger.debug("Sorting traders by PnL")
        sorted_traders = sorted(
            trader_data.items(),
            key=lambda x: x[1].get('pnl', 0),
            reverse=True
        )
        logger.debug(f"Sorted trader order: {[profile for profile, _ in sorted_traders]}")
        
        for profile, data in sorted_traders:
            pnl = data.get('pnl', 0)
            logger.debug(f"Trader {profile} PnL: ${pnl:+,.2f}")
            perf_fig.add_trace(go.Bar(
                name=profile.capitalize(),
                x=[profile.capitalize()],
                y=[pnl],
                marker_color=rasta_theme["green"] if pnl >= 0 else rasta_theme["red"],
                text=[f"${pnl:+,.2f}"],
                textposition='auto'
            ))
        
        # More logging for other components
        # Continue with similar logging for other components
        logger.debug("Creating trader leaderboard")
        # ... rest of your logic with additional logging

        # Log execution time
        execution_time = time.time() - start_time
        logger.debug(f"update_battle_display completed in {execution_time:.3f} seconds")
        
        # Continue with existing code for all other components
        # ... existing code ...

        # Enhanced leaderboard with Rasta styling
        leaderboard = []
        for i, (profile, data) in enumerate(sorted_traders):
            logger.debug(f"Processing leaderboard entry for {profile} (position {i+1})")
            # ... existing leaderboard code ...

        # Remaining components (emotional_states, achievements, suggestions)
        # ... existing code with added logging ...
        
        logger.debug(f"Completed battle display update in {time.time() - start_time:.2f} seconds")
        return (
            price_display,
            price_change_text,
            price_change_style,
            battle_day,
            price_fig,
            perf_fig,
            leaderboard,
            emotional_states,
            achievements,
            suggestions
        )
    except Exception as e:
        logger.error(f"Error updating display: {e}", exc_info=True)
        return dash.no_update

# Add similar logging to other callbacks
@app.callback(
    [Output('market-regime', 'children'),
     Output('timeframe-analysis', 'children'),
     Output('fibonacci-levels', 'children'),
     Output('fibonacci-confluence', 'children'),
     Output('mm-trap-alerts', 'children'),
     Output('schumann-current', 'children'),
     Output('schumann-status', 'children'),
     Output('schumann-chart', 'figure'),
     Output('news-feed', 'children')],
    [Input('update-interval', 'n_intervals')]
)
def update_market_analysis(n_intervals):
    """Update market analysis components"""
    start_time = time.time()
    logger.debug(f"Starting update_market_analysis - interval: {n_intervals}")
    
    try:
        # Get market regime
        logger.debug("Fetching market regime from Redis")
        market_regime = redis_conn.get(RedisKeys.MARKET_REGIME) or "NEUTRAL"
        logger.debug(f"Current market regime: {market_regime}")
        
        # Continue with existing code, adding debug logs
        # ...

        logger.debug(f"Completed market analysis update in {time.time() - start_time:.2f} seconds")
        return (
            regime_display,
            tf_analysis,
            fib_display,
            confluence_display,
            trap_alerts,
            schumann_current,
            schumann_status,
            schumann_fig,
            news_items
        )
    except Exception as e:
        logger.error(f"Error updating market analysis: {e}", exc_info=True)
        return dash.no_update

# Add logging to any battle state handling
@app.callback(
    Output('trader-state', 'data'),
    [Input('start-battle', 'n_clicks'),
     Input('pause-battle', 'n_clicks'),
     Input('reset-arena', 'n_clicks')]
)
def handle_battle_controls(start_clicks, pause_clicks, reset_clicks):
    """Handle battle control buttons"""
    logger.debug("Battle control button clicked")
    ctx = dash.callback_context
    if not ctx.triggered:
        logger.debug("No context trigger, skipping action")
        return dash.no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    logger.debug(f"Triggered by button: {button_id}")
    
    if button_id == 'start-battle':
        logger.info("🚀 Starting trading simulation")
        redis_conn.set(RedisKeys.START_TRADING, 1)
        return {'status': 'running'}
    elif button_id == 'pause-battle':
        logger.info("⏸️ Pausing trading simulation")
        redis_conn.set(RedisKeys.START_TRADING, 0)
        return {'status': 'paused'}
    elif button_id == 'reset-arena':
        logger.info("🔄 Resetting trading arena")
        # Reset traders to initial state
        trader_data = json.loads(redis_manager.get(RedisKeys.LIVE_TRADER_DATA) or "{}")
        for profile in trader_data:
            trader_data[profile]['pnl'] = 0
            trader_data[profile]['trades'] = []
        redis_manager.set(RedisKeys.LIVE_TRADER_DATA, json.dumps(trader_data))
        logger.debug(f"Reset {len(trader_data)} traders to initial state")
        return {'status': 'reset'}
    
    return dash.no_update

# Add this function below the existing update_market_analysis function
@app.callback(
    Output('schumann-chart', 'figure'),
    [Input('update-interval', 'n_intervals')]
)
def update_schumann_gauge():
    """Update the divine Schumann resonance gauge visualization."""
    logger.debug("Updating Schumann resonance gauge")
    
    try:
        # Get current Schumann resonance value from Redis
        schumann_raw = redis_conn.get(RedisKeys.SCHUMANN_RESONANCE)
        if schumann_raw:
            if isinstance(schumann_raw, bytes):
                schumann_raw = schumann_raw.decode('utf-8')
                
            # Check if it's JSON or plain value
            try:
                schumann_data = json.loads(schumann_raw)
                schumann_value = float(schumann_data.get("value", 7.83))
            except json.JSONDecodeError:
                schumann_value = float(schumann_raw)
        else:
            schumann_value = 7.83  # Default baseline Schumann frequency
            
        logger.debug(f"Current Schumann value: {schumann_value} Hz")
        
        # Create gauge figure
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=schumann_value,
            title={'text': "Schumann Resonance (Hz)"},
            gauge={
                'axis': {'range': [0, 40], 'tickwidth': 1},
                'bar': {'color': rasta_theme["accent"]},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'threshold': {
                    'line': {'color': [
                        "#3366CC",  # Blue: low frequency (< 7.0)
                        "#33CC33",  # Green: baseline (~7.83)
                        "#FFBF00",  # Orange: elevated (> 10)
                        "#FF0000"   # Red: high (> 20)
                    ], 'width': 4},
                    'thickness': 0.75,
                    'value': [7.0, 7.83, 15.0, 30.0]
                },
                'steps': [
                    {'range': [0, 7.0], 'color': 'rgba(51, 102, 204, 0.15)'},    # Light blue
                    {'range': [7.0, 8.5], 'color': 'rgba(51, 204, 51, 0.15)'},   # Light green
                    {'range': [8.5, 15.0], 'color': 'rgba(255, 191, 0, 0.15)'},  # Light orange
                    {'range': [15.0, 40.0], 'color': 'rgba(255, 0, 0, 0.15)'}    # Light red
                ]
            }
        ))
        
        gauge_fig.update_layout(
            paper_bgcolor=rasta_theme["paper"],
            font={'color': rasta_theme["text"], 'family': "'Montserrat', sans-serif"},
            margin=dict(l=20, r=20, t=50, b=20),
            height=250,
        )
        
        logger.debug("Schumann gauge updated successfully")
        return gauge_fig
        
    except Exception as e:
        logger.error(f"Error updating Schumann gauge: {e}", exc_info=True)
        # Return empty figure on error
        empty_fig = go.Figure()
        empty_fig.update_layout(
            paper_bgcolor=rasta_theme["paper"],
            font={'color': rasta_theme["text"]},
            margin=dict(l=20, r=20, t=50, b=20),
            height=250,
        )
        return empty_fig


# Add this function as well since it appears to be imported in the test file
@app.callback(
    Output('emotional-states', 'children'),
    [Input('update-interval', 'n_intervals')]
)
def update_trader_psychology(n_intervals):
    """Update trader psychology emotional states with cosmic influences."""
    logger.debug("Updating trader psychology display")
    
    try:
        # Fetch trader data from Redis
        trader_data_raw = redis_manager.get(RedisKeys.LIVE_TRADER_DATA)
        trader_data = json.loads(trader_data_raw or "{}")
        
        # Create emotional state displays for each trader
        emotional_states = []
        for profile, data in trader_data.items():
            emotional_state = data.get('emotional_state', 'neutral')
            
            # Determine color based on emotional state
            if emotional_state in ['confident', 'calm', 'zen', 'focused', 'mindful', 'inspired']:
                state_color = rasta_theme["green"]
            elif emotional_state in ['anxious', 'fearful', 'panic', 'frozen', 'revenge']:
                state_color = rasta_theme["red"]
            elif emotional_state in ['greedy', 'fomo', 'euphoric']:
                state_color = rasta_theme["orange"]
            else:
                state_color = rasta_theme["yellow"]
                
            emotional_states.append(html.Div([
                html.Div(profile.capitalize(), style={'fontWeight': 'bold'}),
                html.Div([
                    html.Span("Mood: "),
                    html.Span(emotional_state.capitalize(), style={'color': state_color, 'fontWeight': 'bold'})
                ]),
                html.Div([
                    html.Span("Bio-Energy: "),
                    html.Span(f"{data.get('bio_energy', 50):.0f}%", 
                             style={'color': rasta_theme["accent"], 'fontWeight': 'bold'})
                ])
            ], style={
                'backgroundColor': rasta_theme["panel"],
                'padding': '10px',
                'borderRadius': '5px',
                'margin': '5px',
                'width': '120px',
                'textAlign': 'center'
            }))
        
        logger.debug(f"Updated psychology display for {len(emotional_states)} traders")
        return emotional_states
        
    except Exception as e:
        logger.error(f"Error updating trader psychology: {e}", exc_info=True)
        return [html.Div("Error loading trader psychology")]

# Main entry point with initialization logging
if __name__ == '__main__':
    try:
        # Set up initial Schumann resonance (mock data for demo)
        if not redis_conn.exists(RedisKeys.SCHUMANN_RESONANCE):
            logger.info("Initializing Schumann resonance data in Redis")
            redis_conn.set(RedisKeys.SCHUMANN_RESONANCE, 7.83)
            redis_conn.set(RedisKeys.SCHUMANN_HISTORY, json.dumps([7.83] * 50))
        
        # Run the dashboard
        logger.info("🌿 OMEGA RASTA BTC DASHBOARD STARTING - JAH BLESS 🌿")
        app.run_server(debug=True, host='0.0.0.0', port=8050)
    except Exception as e:
        logger.critical(f"Fatal error starting dashboard: {e}", exc_info=True)
        raise
