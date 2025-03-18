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
from omega_ai.visualization.hyper_dimension import (
    create_3d_fibonacci_sphere,
    create_4d_trader_energy_field
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
    
    # Add a 3D scatter plot for trading data visualization
    html.Div([
        dcc.Graph(id='3d-scatter-plot')
    ], style={
        'backgroundColor': rasta_theme["paper"],
        'borderRadius': '10px',
        'padding': '15px',
        'marginBottom': '20px'
    }),
    
    # Add 5D Fibonacci Energy Sphere Visualization
    html.Div([
        html.H3("5D Fibonacci Energy Sphere", style={'color': rasta_theme["accent"]}),
        dcc.Graph(id='fibonacci-sphere', style={'height': '50vh'}),
    ], style={'backgroundColor': rasta_theme["panel"], 'padding': '15px', 'borderRadius': '10px', 'marginBottom': '20px'}),
    
    # Add 4D Trader Energy Field Visualization
    html.Div([
        html.H3("4D Trader Energy Field", style={'color': rasta_theme["accent"]}),
        dcc.Graph(id='trader-energy-field', style={'height': '50vh'}),
    ], style={'backgroundColor': rasta_theme["panel"], 'padding': '15px', 'borderRadius': '10px'}),
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
     Output('trading-suggestions', 'children'),
     Output('market-regime', 'children'),
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
        if not price_history:  # Add mock data for testing
            price_history = [50000] * 100
            for i in range(100):
                price_history[i] = 50000 + random.uniform(-500, 500)
                
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
        
        # Get Schumann resonance to influence chart appearance
        schumann_raw = redis_conn.get(RedisKeys.SCHUMANN_RESONANCE)
        schumann_value = 7.83  # Default to base Schumann frequency
        
        if schumann_raw:
            try:
                schumann_raw_str = str(schumann_raw)  # Convert Redis response to string
                try:
                    schumann_data = json.loads(schumann_raw_str)
                    if isinstance(schumann_data, dict) and "value" in schumann_data:
                        schumann_value = float(schumann_data["value"])
                    else:
                        schumann_value = float(schumann_data)
                except json.JSONDecodeError:
                    schumann_value = float(schumann_raw_str)
            except (ValueError, TypeError, AttributeError):
                logger.warning(f"Could not parse Schumann value from {schumann_raw}, using default")
        
        # Adjust colors based on Schumann resonance
        if schumann_value > 10.0:
            # High resonance - more intense colors
            price_color = "#FF5722"  # Bright orange for high resonance
            bg_color = "#1A0F0F"     # Darker background
            fib_color = "#FFD54F"    # Brighter yellow
            accent_fib = "#FF9800"   # Bright orange
            plot_bgcolor = "#0D0D0D"  # Very dark background
            paper_bgcolor = "#1A0F0F"  # Dark red tint
            title_text = "🔥 ELEVATED BTC ENERGY 🔥"
            line_width = 3
        elif schumann_value > 8.5:
            # Medium resonance - warmer colors
            price_color = "#4CAF50"  # Green
            bg_color = "#1E1E1E"     # Standard dark
            fib_color = "#3D5AFE"    # Blue
            accent_fib = "#FFB300"   # Amber
            plot_bgcolor = "#1A1A1A"  # Dark background
            paper_bgcolor = "#1E1E1E"  # Standard dark
            title_text = "✨ HARMONIC BTC FLOW ✨"
            line_width = 2
        else:
            # Normal resonance - standard colors
            price_color = rasta_theme["green"]
            bg_color = rasta_theme["paper"]
            fib_color = rasta_theme["secondary"]
            accent_fib = rasta_theme["accent"]
            plot_bgcolor = rasta_theme["paper"]
            paper_bgcolor = rasta_theme["paper"]
            title_text = "🌿 BTC PRICE JOURNEY 🌿"
            line_width = 2
            
        # Add price line with Schumann-influenced color
        price_fig.add_trace(go.Scatter(
            y=price_history,
            mode='lines',
            name='BTC Price',
            line=dict(color=price_color, width=line_width)
        ))
        
        # Add Fibonacci levels if available
        logger.debug("Fetching Fibonacci levels")
        fib_levels = get_current_fibonacci_levels()
        
        # If no Fibonacci levels available, create some for testing
        if not fib_levels:
            base_price = 50000
            fib_levels = {
                "0.0": base_price,
                "0.236": base_price * 0.95,
                "0.382": base_price * 0.93,
                "0.5": base_price * 0.9,
                "0.618": base_price * 0.87,
                "0.786": base_price * 0.85,
                "1.0": base_price * 0.8
            }
            
        logger.debug(f"Found {len(fib_levels) if fib_levels else 0} Fibonacci levels")
        
        if fib_levels and price_history:
            for level, price in fib_levels.items():
                if isinstance(level, str) and 0.1 < float(level) < 0.9:  # Only show primary levels
                    logger.debug(f"Adding Fibonacci level {level} at price ${price:.2f}")
                    price_fig.add_trace(go.Scatter(
                        y=[float(price)] * len(price_history),
                        mode='lines',
                        name=f'Fib {level}',
                        line=dict(
                            color=accent_fib if level == "0.618" else fib_color,
                            width=1,
                            dash='dash'
                        )
                    ))
        
        # Apply Schumann-influenced chart styling
        price_fig.update_layout(
            title=title_text,
            template='plotly_dark',
            paper_bgcolor=paper_bgcolor,
            plot_bgcolor=plot_bgcolor,
            font=dict(color=rasta_theme["text"]),
            height=300,
            margin=dict(l=10, r=10, t=30, b=10),
            showlegend=True,
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
        
        # If no traders in data, add default traders for testing
        if not sorted_traders:
            default_profiles = ["strategic", "aggressive", "newbie", "scalper"]
            for i, profile in enumerate(default_profiles):
                pnl = random.uniform(-1000, 2000)
                win_rate = random.uniform(30, 80)
                sorted_traders.append((profile, {'pnl': pnl, 'win_rate': win_rate}))
        
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
        
        perf_fig.update_layout(
            title="💰 TRADER PERFORMANCE 💰",
            plot_bgcolor=rasta_theme["paper"],
            paper_bgcolor=rasta_theme["paper"],
            font=dict(color=rasta_theme["text"]),
            margin=dict(l=10, r=10, t=30, b=10),
            height=300
        )
        
        # Enhanced leaderboard with Rasta styling
        logger.debug("Creating trader leaderboard")
        leaderboard = []
        for i, (profile, data) in enumerate(sorted_traders):
            logger.debug(f"Processing leaderboard entry for {profile} (position {i+1})")
            
            # Determine ranking badge
            if i == 0:
                badge = "🥇"
                badge_color = rasta_theme["accent"]
            elif i == 1:
                badge = "🥈"
                badge_color = "#C0C0C0"
            elif i == 2:
                badge = "🥉"
                badge_color = "#CD7F32"
            else:
                badge = f"{i+1}."
                badge_color = rasta_theme["text"]
            
            # Calculate trader stats
            pnl = data.get('pnl', 0)
            win_rate = data.get('win_rate', 50.0)
            
            leaderboard.append(html.Div([
                html.Div([
                    html.Span(badge, style={'fontSize': '22px', 'color': badge_color, 'marginRight': '8px'}),
                    html.Span(profile.capitalize(), style={'fontWeight': 'bold', 'fontSize': '18px'})
                ], style={'display': 'flex', 'alignItems': 'center'}),
                
                html.Div([
                    html.Div([
                        html.Span("P&L: "),
                        html.Span(f"${pnl:+,.2f}", style={
                            'color': rasta_theme["green"] if pnl >= 0 else rasta_theme["red"],
                            'fontWeight': 'bold'
                        })
                    ]),
                    html.Div([
                        html.Span("Win Rate: "),
                        html.Span(f"{win_rate:.1f}%", style={
                            'color': rasta_theme["accent"],
                            'fontWeight': 'bold'
                        })
                    ])
                ])
            ], style={
                'backgroundColor': rasta_theme["panel"],
                'padding': '10px 15px',
                'borderRadius': '8px',
                'marginBottom': '10px',
                'borderLeft': f'4px solid {rasta_theme["green"] if pnl >= 0 else rasta_theme["red"]}'
            }))
        
        # Create emotional states for traders
        logger.debug("Creating emotional states display")
        emotional_states = []
        
        # Generate emotional states if not in data
        emotions = ['confident', 'calm', 'anxious', 'fearful', 'zen', 'euphoric', 'greedy']
        
        # Ensure we have the required trader profiles for testing
        required_profiles = ["strategic", "aggressive", "newbie", "scalper"]
        trader_profiles = [profile for profile, _ in sorted_traders]
        
        # Add missing profiles if needed
        for profile in required_profiles:
            if profile not in trader_profiles:
                sorted_traders.append((profile, {'emotional_state': random.choice(emotions), 'bio_energy': random.randint(40, 95)}))
                logger.debug(f"Added missing trader profile: {profile} for emotional states")
        
        # Ensure we create at least one state for each required profile
        for profile in required_profiles:
            # Find the profile in sorted_traders or use default values
            trader_data = next((data for p, data in sorted_traders if p == profile), 
                              {'emotional_state': random.choice(emotions), 'bio_energy': random.randint(40, 95)})
            
            emotional_state = trader_data.get('emotional_state', random.choice(emotions))
            bio_energy = int(trader_data.get('bio_energy', random.randint(40, 95)))
            
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
                    html.Span(f"{bio_energy}%", 
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
        
        # Generate achievements
        achievements = html.Div([
            html.Div([
                html.Img(src="https://i.ibb.co/Cn5xnGz/rasta-lion.png", height="30px", style={"marginRight": "10px"}),
                html.Span("🌟 Fibonacci Master", style={'fontWeight': 'bold', 'color': rasta_theme["accent"]}),
            ], style={
                'backgroundColor': rasta_theme["panel"],
                'padding': '10px',
                'borderRadius': '5px',
                'margin': '5px',
                'display': 'flex',
                'alignItems': 'center'
            }),
            html.Div([
                html.Img(src="https://i.ibb.co/Cn5xnGz/rasta-lion.png", height="30px", style={"marginRight": "10px"}),
                html.Span("💰 Profit Prophet", style={'fontWeight': 'bold', 'color': rasta_theme["green"]}),
            ], style={
                'backgroundColor': rasta_theme["panel"],
                'padding': '10px',
                'borderRadius': '5px',
                'margin': '5px',
                'display': 'flex',
                'alignItems': 'center'
            }),
            html.Div([
                html.Img(src="https://i.ibb.co/Cn5xnGz/rasta-lion.png", height="30px", style={"marginRight": "10px"}),
                html.Span("🧘‍♂️ Zen Trader", style={'fontWeight': 'bold', 'color': rasta_theme["yellow"]}),
            ], style={
                'backgroundColor': rasta_theme["panel"],
                'padding': '10px',
                'borderRadius': '5px',
                'margin': '5px',
                'display': 'flex',
                'alignItems': 'center'
            })
        ])
        
        # Trading suggestions
        suggestions = html.Div([
            html.Div("🔮 JAH ORACLE RECOMMENDATIONS", style={
                'textAlign': 'center',
                'fontSize': '18px',
                'fontWeight': 'bold',
                'marginBottom': '15px',
                'color': rasta_theme["accent"]
            }),
            html.Div([
                html.Div("🟢 BUY OPPORTUNITY", style={'fontWeight': 'bold', 'color': rasta_theme["green"], 'marginBottom': '5px'}),
                html.Div(f"Next Fibonacci support at ${current_price * 0.95:.0f} with strong confluence")
            ], style={
                'backgroundColor': rasta_theme["panel"],
                'padding': '10px',
                'borderRadius': '5px',
                'marginBottom': '10px'
            }),
            html.Div([
                html.Div("⚠️ RISK WARNING", style={'fontWeight': 'bold', 'color': rasta_theme["orange"], 'marginBottom': '5px'}),
                html.Div(f"Watch for potential bear trap below ${current_price * 0.98:.0f}")
            ], style={
                'backgroundColor': rasta_theme["panel"],
                'padding': '10px',
                'borderRadius': '5px',
                'marginBottom': '10px'
            }),
            html.Div([
                html.Div("🔄 STRATEGY ADVICE", style={'fontWeight': 'bold', 'color': rasta_theme["yellow"], 'marginBottom': '5px'}),
                html.Div(f"Scale in gradually as price approaches the 0.618 golden ratio (${current_price * 0.91:.0f})")
            ], style={
                'backgroundColor': rasta_theme["panel"],
                'padding': '10px',
                'borderRadius': '5px'
            })
        ])
        
        # Market regime and time analysis
        market_regime_raw = redis_conn.get(RedisKeys.MARKET_REGIME)
        market_regime = str(market_regime_raw) if market_regime_raw else "NEUTRAL"
        logger.debug(f"Current market regime: {market_regime}")
        
        # Get Schumann resonance data
        schumann_raw = redis_conn.get(RedisKeys.SCHUMANN_RESONANCE)
        schumann_value = 7.83  # Default to base Schumann frequency
        
        if schumann_raw:
            try:
                schumann_raw_str = str(schumann_raw)  # Convert Redis response to string
                try:
                    schumann_data = json.loads(schumann_raw_str)
                    if isinstance(schumann_data, dict) and "value" in schumann_data:
                        schumann_value = float(schumann_data["value"])
                    else:
                        schumann_value = float(schumann_data)
                except json.JSONDecodeError:
                    schumann_value = float(schumann_raw_str)
            except (ValueError, TypeError, AttributeError):
                logger.warning(f"Could not parse Schumann value from {schumann_raw}, using default")
            
        logger.debug(f"Current Schumann value: {schumann_value} Hz")
        
        # Create gauge with proper color format
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
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 30.0
                },
                'steps': [
                    {'range': [0, 7.0], 'color': 'rgba(51, 102, 204, 0.15)'},
                    {'range': [7.0, 8.5], 'color': 'rgba(51, 204, 51, 0.15)'},
                    {'range': [8.5, 15.0], 'color': 'rgba(255, 191, 0, 0.15)'},
                    {'range': [15.0, 40.0], 'color': 'rgba(255, 0, 0, 0.15)'}
                ]
            }
        ))
        
        gauge_fig.update_layout(
            paper_bgcolor=rasta_theme["paper"],
            font={'color': rasta_theme["text"], 'family': "'Montserrat', sans-serif"},
            margin=dict(l=20, r=20, t=50, b=20),
            height=250,
        )
        
        # Define placeholders for missing variables
        regime_display = html.Div([
            html.H3("Current Market Regime:", style={'color': rasta_theme["accent"]}),
            html.H4(str(market_regime), style={'color': rasta_theme["green"] if market_regime == "UPTREND" else rasta_theme["red"]})
        ])
        
        tf_analysis = html.Div("Analysis in progress...")
        fib_display = html.Div("Calculating Fibonacci levels...")
        confluence_display = html.Div("Checking confluence zones...")
        trap_alerts = html.Div("Scanning for market maker traps...")
        schumann_current = html.Div([
            html.H3(f"Current Frequency: {schumann_value:.2f} Hz"),
            html.Div("🌍 Earth's Heartbeat", style={'color': rasta_theme["accent"]})
        ])
        schumann_status = html.Div(
            "Baseline Harmony" if 7.5 <= schumann_value <= 8.5 else
            "Elevated Consciousness" if schumann_value > 8.5 else
            "Deep Meditation",
            style={'color': rasta_theme["green"]}
        )
        news_items = [
            html.Div([
                html.Div("Bitcoin ETF inflows reach new highs", style={'fontWeight': 'bold'}),
                html.Div("March 15, 2025", style={'fontSize': '12px', 'color': rasta_theme["secondary"]})
            ], style={'backgroundColor': rasta_theme["panel"], 'padding': '10px', 'borderRadius': '5px', 'marginBottom': '10px'}),
            html.Div([
                html.Div("Fibonacci patterns indicate strong support at $48,500", style={'fontWeight': 'bold'}),
                html.Div("March 14, 2025", style={'fontSize': '12px', 'color': rasta_theme["secondary"]})
            ], style={'backgroundColor': rasta_theme["panel"], 'padding': '10px', 'borderRadius': '5px', 'marginBottom': '10px'}),
            html.Div([
                html.Div("Schumann resonance spikes correlate with market volatility", style={'fontWeight': 'bold'}),
                html.Div("March 13, 2025", style={'fontSize': '12px', 'color': rasta_theme["secondary"]})
            ], style={'backgroundColor': rasta_theme["panel"], 'padding': '10px', 'borderRadius': '5px'})
        ]

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
            suggestions,
            regime_display,
            tf_analysis,
            fib_display,
            confluence_display,
            trap_alerts,
            schumann_current,
            schumann_status,
            gauge_fig,
            news_items
        )
    except Exception as e:
        logger.error(f"Error updating display: {e}", exc_info=True)
        # Return default values instead of no_update to prevent TypeErrors
        default_display = html.Div("Data unavailable")
        default_figure = go.Figure()
        default_figure.update_layout(
            paper_bgcolor=rasta_theme["paper"],
            font=dict(color=rasta_theme["text"]),
            height=250,
        )
        default_style = {'color': rasta_theme["text"]}
        
        return (
            "$0.00", 
            "+0.00%", 
            default_style,
            default_display,
            default_figure,
            default_figure,
            [default_display],
            [default_display],
            default_display,
            default_display,
            default_display,
            default_display,
            default_display,
            default_display,
            default_figure,
            default_display
        )

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
        redis_manager.set(RedisKeys.START_TRADING, "1")
        return {'status': 'running'}
    elif button_id == 'pause-battle':
        logger.info("⏸️ Pausing trading simulation")
        redis_manager.set(RedisKeys.START_TRADING, "0")
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

# Add a 3D scatter plot for trading data visualization
@app.callback(
    Output('3d-scatter-plot', 'figure'),
    [Input('update-interval', 'n_intervals')]
)
def update_3d_scatter_plot(n_intervals):
    """Update the 3D scatter plot with trading data."""
    logger.debug(f"Updating 3D scatter plot - interval: {n_intervals}")
    
    # Sample data for demonstration
    price = [random.uniform(30000, 60000) for _ in range(100)]
    volume = [random.uniform(100, 1000) for _ in range(100)]
    time = list(range(100))
    
    # Create 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=price,
        y=volume,
        z=time,
        mode='markers',
        marker=dict(
            size=5,
            color=price,  # Color by price
            colorscale='Viridis',
            opacity=0.8
        )
    )])
    
    fig.update_layout(
        title="3D Trading Data Visualization 🌐",
        scene=dict(
            xaxis_title='Price 💰',
            yaxis_title='Volume 📊',
            zaxis_title='Time ⏰'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    
    return fig

# Add callback for the 5D Fibonacci Energy Sphere
@app.callback(
    Output('fibonacci-sphere', 'figure'),
    [Input('update-interval', 'n_intervals')]
)
def update_fibonacci_sphere(n_intervals):
    """Update the 5D Fibonacci Energy Sphere visualization"""
    # Get price history from Redis
    try:
        battle_state_raw = redis_manager.get(RedisKeys.LIVE_BATTLE_STATE)
        if battle_state_raw:
            battle_state = json.loads(battle_state_raw)
            price_history = battle_state.get('btc_history', [])
        else:
            # Mock data if not available
            price_history = [random.uniform(45000, 56000) for _ in range(100)]
        
        # Get Schumann resonance value
        schumann_raw = redis_conn.get(RedisKeys.SCHUMANN_RESONANCE)
        schumann_value = 7.83  # Default to base Schumann frequency
        
        if schumann_raw:
            try:
                schumann_value = float(schumann_raw)
            except (ValueError, TypeError):
                logger.warning(f"Could not parse Schumann value from {schumann_raw}, using default")
        
        # Create the visualization
        fig = create_3d_fibonacci_sphere(price_history, schumann_value)
        return fig
    except Exception as e:
        logger.error(f"Error updating Fibonacci sphere: {e}")
        # Return empty figure on error
        return go.Figure()

# Add callback for the 4D Trader Energy Field
@app.callback(
    Output('trader-energy-field', 'figure'),
    [Input('update-interval', 'n_intervals')]
)
def update_trader_energy_field(n_intervals):
    """Update the 4D Trader Energy Field visualization"""
    try:
        # Get trader data from Redis
        trader_data_raw = redis_manager.get(RedisKeys.LIVE_TRADER_DATA)
        trader_data = {}
        
        if trader_data_raw:
            trader_data = json.loads(trader_data_raw)
        
        # Get Schumann resonance value
        schumann_raw = redis_conn.get(RedisKeys.SCHUMANN_RESONANCE)
        schumann_value = 7.83  # Default to base Schumann frequency
        
        if schumann_raw:
            try:
                schumann_value = float(schumann_raw)
            except (ValueError, TypeError):
                logger.warning(f"Could not parse Schumann value from {schumann_raw}, using default")
        
        # Create the visualization
        fig = create_4d_trader_energy_field(trader_data, schumann_value)
        return fig
    except Exception as e:
        logger.error(f"Error updating trader energy field: {e}")
        # Return empty figure on error
        return go.Figure()

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
        app.run(debug=True, host='0.0.0.0', port=8051)
    except Exception as e:
        logger.critical(f"Fatal error starting dashboard: {e}", exc_info=True)
        raise
