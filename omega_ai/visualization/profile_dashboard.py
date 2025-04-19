#!/usr/bin/env python3

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸


"""
ProfileTrader Dashboard & Gamification System

This dashboard shows real-time performance of different trader profiles,
implementing gamification elements to compare strategies in a competitive format.
"""

import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import datetime
import json
import redis
import asyncio
import websockets
import random
import numpy as np
from collections import deque

# Redis Connection
redis_conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Initialize Dash App with Dark Mode
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Define Dark Mode Styles with Gaming Elements
dark_theme = {
    "background": "#121212",
    "card_bg": "#1E1E1E",
    "text": "#E0E0E0",
    "graph_bg": "#242424",
    "accent": "#FFB300",  # Gold
    "green": "#00E676",
    "red": "#FF3D00",
    "blue": "#2196F3",
    "purple": "#9C27B0",
    "cyan": "#00BCD4",
    "yellow": "#FFEB3B",
    "gray": "#757575"
}

# Profile Colors
profile_colors = {
    "strategic": dark_theme["blue"],
    "aggressive": dark_theme["red"],
    "newbie": dark_theme["yellow"],
    "scalper": dark_theme["purple"]
}

# Trader Profile Badges
profile_badges = {
    "strategic": "🧠",  # Brain (strategic thinking)
    "aggressive": "🔥",  # Fire (aggressive approach)
    "newbie": "🐣",     # Hatching chick (newbie)
    "scalper": "⚡",     # Lightning (fast trading)
}

# Achievement Badges
achievement_badges = {
    "winning_streak": "🏆",
    "big_win": "💰",
    "risk_manager": "🛡️",
    "comeback": "🚀",
    "volume_king": "📊",
    "diamond_hands": "💎",
    "paper_hands": "📄"
}

# ======== DASHBOARD LAYOUT ========

app.layout = html.Div(style={
    "backgroundColor": dark_theme["background"], 
    "color": dark_theme["text"], 
    "padding": "20px",
    "fontFamily": "'Roboto', sans-serif"
}, children=[
    # Header
    html.Div(style={"textAlign": "center", "marginBottom": "30px"}, children=[
        html.H1("🏆 OMEGA BTC AI - TRADER PROFILE ARENA 🏆", 
                style={'color': dark_theme["accent"], 'marginBottom': '10px'}),
        html.Div([
            html.Span("Live BTC: ", style={"fontSize": "20px"}),
            html.Span(id="live-btc-price", style={"fontSize": "24px", "color": dark_theme["green"], "marginRight": "30px"}),
            html.Span("Battle Day: ", style={"fontSize": "20px"}),
            html.Span(id="battle-day", style={"fontSize": "24px", "color": dark_theme["accent"]}),
        ]),
    ]),
    
    html.Div(style={"textAlign": "center", "marginBottom": "20px"}, children=[
        html.Div([
            html.Label("BATTLE MODE: ", style={"marginRight": "10px", "fontWeight": "bold"}),
            dcc.RadioItems(
                id='battle-mode',
                options=[
                    {'label': '🧪 SIMULATION', 'value': 'simulated'},
                    {'label': '🔥 OMEGA ULTIMATE REAL BATTLE 🔥', 'value': 'real'}
                ],
                value='simulated',
                style={"display": "inline-block"},
                labelStyle={"marginRight": "15px", "cursor": "pointer", "fontWeight": "bold"}
            ),
        ]),
    ]),
    
    # Main Content Grid
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 3fr", "gap": "20px"}, children=[
        # Left Column - Trader Leaderboard
        html.Div(style={"backgroundColor": dark_theme["card_bg"], "padding": "15px", "borderRadius": "10px"}, children=[
            html.H2("🏆 TRADER RANKINGS", style={"textAlign": "center", "color": dark_theme["accent"]}),
            html.Div(id="trader-leaderboard"),
            
            html.Hr(style={"margin": "20px 0", "borderColor": dark_theme["gray"]}),
            
            # Battle Stats
            html.H3("⚔️ BATTLE STATS", style={"textAlign": "center", "color": dark_theme["accent"]}),
            html.Div(id="battle-stats"),
            
            # Recent Achievements
            html.H3("🏅 RECENT ACHIEVEMENTS", style={"textAlign": "center", "color": dark_theme["accent"], "marginTop": "20px"}),
            html.Div(id="recent-achievements"),
            
            # Update Controls
            html.Div(style={"marginTop": "30px", "textAlign": "center"}, children=[
                html.Button("Start Battle Simulation", id="start-battle", 
                           style={"backgroundColor": dark_theme["green"], "color": "white", 
                                  "border": "none", "padding": "10px 15px", "borderRadius": "5px",
                                  "cursor": "pointer", "marginRight": "10px"}),
                html.Button("Reset Arena", id="reset-arena", 
                           style={"backgroundColor": dark_theme["red"], "color": "white", 
                                  "border": "none", "padding": "10px 15px", "borderRadius": "5px",
                                  "cursor": "pointer"}),
            ])
        ]),
        
        # Right Column - Trader Details and Charts
        html.Div(style={"backgroundColor": dark_theme["card_bg"], "padding": "15px", "borderRadius": "10px"}, children=[
            # Tabs for different views
            dcc.Tabs(id="trader-view-tabs", value="performance", 
                    style={"color": dark_theme["text"], "backgroundColor": dark_theme["card_bg"]},
                    children=[
                # Performance Tab
                dcc.Tab(label="📈 Performance", value="performance", style={
                    "backgroundColor": dark_theme["graph_bg"],
                    "color": dark_theme["text"],
                }, selected_style={
                    "backgroundColor": dark_theme["accent"],
                    "color": dark_theme["background"],
                    "fontWeight": "bold"
                }),
                
                # Psychology Tab
                dcc.Tab(label="🧠 Psychology", value="psychology", style={
                    "backgroundColor": dark_theme["graph_bg"],
                    "color": dark_theme["text"],
                }, selected_style={
                    "backgroundColor": dark_theme["accent"],
                    "color": dark_theme["background"],
                    "fontWeight": "bold"
                }),
                
                # Positions Tab
                dcc.Tab(label="💰 Positions", value="positions", style={
                    "backgroundColor": dark_theme["graph_bg"],
                    "color": dark_theme["text"],
                }, selected_style={
                    "backgroundColor": dark_theme["accent"],
                    "color": dark_theme["background"],
                    "fontWeight": "bold"
                }),
                
                # Decisions Tab
                dcc.Tab(label="🔍 Decisions", value="decisions", style={
                    "backgroundColor": dark_theme["graph_bg"],
                    "color": dark_theme["text"],
                }, selected_style={
                    "backgroundColor": dark_theme["accent"],
                    "color": dark_theme["background"],
                    "fontWeight": "bold"
                }),
            ]),
            
            # Tab Content Container
            html.Div(id="trader-view-content", style={"marginTop": "20px"}),
        ]),
    ]),
    
    # History Timeline
    html.Div(style={
        "backgroundColor": dark_theme["card_bg"], 
        "padding": "15px", 
        "borderRadius": "10px",
        "marginTop": "20px"
    }, children=[
        html.H2("📜 BATTLE TIMELINE", style={"textAlign": "center", "color": dark_theme["accent"]}),
        html.Div(id="battle-timeline"),
    ]),
    
    # Hidden Divs for Storing State
    html.Div(id="trader-state", style={"display": "none"}),
    html.Div(id="battle-state", style={"display": "none"}),
    
    # Update Interval
    dcc.Interval(id="update-interval", interval=5000, n_intervals=0)  # Update every 5 seconds
])

# ======== CALLBACK FUNCTIONS ========

# Initialize simulated trader data
def generate_initial_trader_data():
    return {
        "strategic": {
            "name": "Strategic Fibonacci Trader",
            "capital": 10000.0,
            "pnl": 0.0,
            "win_rate": 0.0,
            "trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "emotional_state": "neutral",
            "confidence": 0.6,
            "risk_level": 0.4,
            "positions": [],
            "trade_history": [],
            "achievements": []
        },
        "aggressive": {
            "name": "Aggressive Momentum Trader",
            "capital": 10000.0,
            "pnl": 0.0,
            "win_rate": 0.0,
            "trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "emotional_state": "neutral",
            "confidence": 0.7,
            "risk_level": 0.8,
            "positions": [],
            "trade_history": [],
            "achievements": []
        },
        "newbie": {
            "name": "YOLO Crypto Influencer Follower",
            "capital": 10000.0,
            "pnl": 0.0,
            "win_rate": 0.0,
            "trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "emotional_state": "fearful",
            "confidence": 0.4,
            "risk_level": 0.9,
            "positions": [],
            "trade_history": [],
            "achievements": []
        },
        "scalper": {
            "name": "Order Book Scalper",
            "capital": 10000.0,
            "pnl": 0.0,
            "win_rate": 0.0,
            "trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "emotional_state": "neutral",
            "confidence": 0.5,
            "risk_level": 0.5,
            "positions": [],
            "trade_history": [],
            "achievements": []
        }
    }

# Initialize battle state
def initialize_battle_state():
    return {
        "day": 1,
        "session": 1,
        "btc_price": 83000,
        "btc_history": [83000],
        "battle_active": False,
        "start_time": datetime.datetime.now().isoformat(),
        "timeline_events": [],
    }

# Create leaderboard
@app.callback(
    Output("trader-leaderboard", "children"),
    [Input("trader-state", "children")]
)
def update_leaderboard(trader_state_json):
    if not trader_state_json:
        trader_data = generate_initial_trader_data()
    else:
        trader_data = json.loads(trader_state_json)
    
    # Sort traders by performance
    sorted_traders = sorted(
        trader_data.items(),
        key=lambda x: x[1]["capital"] + x[1]["pnl"],
        reverse=True
    )
    
    leaderboard_items = []
    for rank, (profile, data) in enumerate(sorted_traders):
        medal = "🥇" if rank == 0 else "🥈" if rank == 1 else "🥉" if rank == 2 else "🏅"
        
        # Create leaderboard entry
        leaderboard_items.append(html.Div(style={
            "display": "flex",
            "alignItems": "center",
            "backgroundColor": dark_theme["graph_bg"],
            "padding": "10px",
            "borderRadius": "10px",
            "marginBottom": "10px",
            "border": f"2px solid {profile_colors[profile]}"
        }, children=[
            html.Div(f"{medal} #{rank+1}", style={
                "fontWeight": "bold",
                "fontSize": "20px",
                "width": "60px",
                "color": dark_theme["accent"] if rank == 0 else dark_theme["text"]
            }),
            html.Div(profile_badges[profile], style={
                "fontSize": "24px",
                "marginRight": "10px"
            }),
            html.Div(style={"flex": "1"}, children=[
                html.Div(data["name"], style={
                    "fontWeight": "bold",
                    "fontSize": "16px"
                }),
                html.Div([
                    html.Span("Capital: ", style={"fontSize": "14px"}),
                    html.Span(f"${data['capital'] + data['pnl']:.2f}", style={
                        "color": dark_theme["green"] if data["pnl"] >= 0 else dark_theme["red"],
                        "fontWeight": "bold"
                    }),
                    html.Span(f" ({data['pnl']/data['capital']*100:.1f}%)" if data['pnl'] != 0 else "", style={
                        "color": dark_theme["green"] if data["pnl"] >= 0 else dark_theme["red"],
                    })
                ]),
                html.Div(f"Win Rate: {data['win_rate']*100:.1f}%" if data["trades"] > 0 else "No trades yet")
            ])
        ]))
    
    return leaderboard_items

# Update battle stats
@app.callback(
    [Output("battle-stats", "children"),
     Output("live-btc-price", "children"),
     Output("battle-day", "children")],
    [Input("battle-state", "children")]
)
def update_battle_stats(battle_state_json):
    if not battle_state_json:
        battle_state = initialize_battle_state()
    else:
        battle_state = json.loads(battle_state_json)
    
    # Format live price
    live_price = f"${battle_state['btc_price']:.2f}"
    
    # Battle day
    battle_day = f"Day {battle_state['day']} - Session {battle_state['session']}/4"
    
    # Create battle stats
    price_change = 0
    if len(battle_state['btc_history']) > 1:
        price_change = (battle_state['btc_price'] / battle_state['btc_history'][0] - 1) * 100
    
    stats = html.Div(children=[
        html.Div(style={"marginBottom": "10px"}, children=[
            html.Div("Market Conditions:", style={"fontWeight": "bold"}),
            html.Div(f"BTC Change: {price_change:+.2f}%", style={
                "color": dark_theme["green"] if price_change >= 0 else dark_theme["red"]
            }),
        ]),
        html.Div(style={"marginBottom": "10px"}, children=[
            html.Div("Battle Progress:", style={"fontWeight": "bold"}),
            html.Div(f"Day {battle_state['day']} - Session {battle_state['session']}/4"),
            html.Div(f"Status: {'Active' if battle_state['battle_active'] else 'Paused'}", style={
                "color": dark_theme["green"] if battle_state['battle_active'] else dark_theme["red"]
            }),
        ]),
    ])
    
    return stats, live_price, battle_day

# Update achievements
@app.callback(
    Output("recent-achievements", "children"),
    [Input("trader-state", "children")]
)
def update_achievements(trader_state_json):
    if not trader_state_json:
        trader_data = generate_initial_trader_data()
    else:
        trader_data = json.loads(trader_state_json)
    
    # Collect all achievements
    all_achievements = []
    for profile, data in trader_data.items():
        for achievement in data["achievements"]:
            all_achievements.append({
                "profile": profile,
                "badge": achievement["badge"],
                "text": achievement["text"],
                "timestamp": achievement["timestamp"]
            })
    
    # Sort by timestamp (newest first) and take only 5 most recent
    all_achievements.sort(key=lambda x: x["timestamp"], reverse=True)
    recent = all_achievements[:5]
    
    if not recent:
        return html.Div("No achievements yet", style={"fontStyle": "italic", "textAlign": "center"})
    
    achievement_items = []
    for item in recent:
        achievement_items.append(html.Div(style={
            "display": "flex",
            "alignItems": "center",
            "marginBottom": "10px"
        }, children=[
            html.Div(item["badge"], style={"fontSize": "24px", "marginRight": "10px"}),
            html.Div(style={"flex": "1"}, children=[
                html.Div(f"{profile_badges[item['profile']]} {trader_data[item['profile']]['name']}", style={
                    "fontWeight": "bold",
                    "color": profile_colors[item["profile"]]
                }),
                html.Div(item["text"])
            ])
        ]))
    
    return achievement_items

# Update timeline
@app.callback(
    Output("battle-timeline", "children"),
    [Input("battle-state", "children")]
)
def update_timeline(battle_state_json):
    if not battle_state_json:
        battle_state = initialize_battle_state()
    else:
        battle_state = json.loads(battle_state_json)
    
    events = battle_state["timeline_events"]
    
    if not events:
        return html.Div("No events yet", style={"fontStyle": "italic", "textAlign": "center"})
    
    # Sort events by timestamp (newest first)
    events.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Create timeline items
    timeline_items = []
    for event in events:
        icon = "📈" if "position" in event["type"].lower() else "🏆" if "achievement" in event["type"].lower() else "📊"
        
        timeline_items.append(html.Div(style={
            "display": "flex",
            "alignItems": "flex-start",
            "marginBottom": "15px"
        }, children=[
            html.Div(icon, style={"fontSize": "24px", "marginRight": "15px", "marginTop": "5px"}),
            html.Div(style={"flex": "1"}, children=[
                html.Div(style={"display": "flex", "justifyContent": "space-between"}, children=[
                    html.Div(event["title"], style={"fontWeight": "bold"}),
                    html.Div(event["time"], style={"color": dark_theme["gray"], "fontSize": "14px"})
                ]),
                html.Div(event["description"]),
                html.Div(f"BTC: ${event['btc_price']:.2f}", style={"fontSize": "14px", "color": dark_theme["accent"]})
            ])
        ]))
    
    return timeline_items

# Update trader view content based on selected tab
@app.callback(
    Output("trader-view-content", "children"),
    [Input("trader-view-tabs", "value"),
     Input("trader-state", "children"),
     Input("battle-state", "children")]
)
def update_trader_view(tab, trader_state_json, battle_state_json):
    if not trader_state_json or not battle_state_json:
        return html.Div("Loading data...")
    
    trader_data = json.loads(trader_state_json)
    battle_state = json.loads(battle_state_json)
    
    if tab == "performance":
        return create_performance_view(trader_data, battle_state)
    elif tab == "psychology":
        return create_psychology_view(trader_data)
    elif tab == "positions":
        return create_positions_view(trader_data, battle_state)
    elif tab == "decisions":
        return create_decisions_view(trader_data)
    else:
        return html.Div("Select a tab to view trader data")

# Create performance view
def create_performance_view(trader_data, battle_state):
    # Prepare performance data for chart
    performance_data = []
    for profile, data in trader_data.items():
        performance_data.append({
            "profile": profile,
            "name": data["name"],
            "capital": data["capital"] + data["pnl"],
            "pnl_pct": (data["pnl"] / data["capital"]) * 100 if data["capital"] > 0 else 0,
            "win_rate": data["win_rate"] * 100,
            "trades": data["trades"]
        })
    
    # Create DataFrame for Plotly
    df = pd.DataFrame(performance_data)
    
    # Create charts
    return html.Div(children=[
        # Capital comparison chart
        dcc.Graph(
            figure=px.bar(
                df, x="name", y="capital", color="profile",
                color_discrete_map=profile_colors,
                title="Trader Capital Comparison",
                labels={"capital": "Current Capital ($)", "name": "Trader", "profile": "Profile"},
                text_auto='.2f'
            ).update_layout(
                plot_bgcolor=dark_theme["graph_bg"],
                paper_bgcolor=dark_theme["card_bg"],
                font=dict(color=dark_theme["text"]),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor=dark_theme["gray"]),
                showlegend=False
            )
        ),
        
        # Stats grid
        html.Div(style={
            "display": "grid",
            "gridTemplateColumns": "repeat(2, 1fr)",
            "gap": "20px",
            "marginTop": "20px"
        }, children=[
            # PnL percentage chart
            dcc.Graph(
                figure=px.bar(
                    df, x="name", y="pnl_pct", color="profile",
                    color_discrete_map=profile_colors,
                    title="Profit & Loss (%)",
                    labels={"pnl_pct": "P&L (%)", "name": "Trader", "profile": "Profile"},
                    text_auto='.1f'
                ).update_layout(
                    plot_bgcolor=dark_theme["graph_bg"],
                    paper_bgcolor=dark_theme["card_bg"],
                    font=dict(color=dark_theme["text"]),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor=dark_theme["gray"]),
                    showlegend=False
                )
            ),
            
            # Win rate chart
            dcc.Graph(
                figure=px.bar(
                    df, x="name", y="win_rate", color="profile",
                    color_discrete_map=profile_colors,
                    title="Win Rate (%)",
                    labels={"win_rate": "Win Rate (%)", "name": "Trader", "profile": "Profile"},
                    text_auto='.1f'
                ).update_layout(
                    plot_bgcolor=dark_theme["graph_bg"],
                    paper_bgcolor=dark_theme["card_bg"],
                    font=dict(color=dark_theme["text"]),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor=dark_theme["gray"]),
                    showlegend=False
                )
            )
        ]),
        
        # BTC price chart
        dcc.Graph(
            figure=px.line(
                x=list(range(len(battle_state["btc_history"]))),
                y=battle_state["btc_history"],
                title="BTC Price History",
                labels={"x": "Time", "y": "BTC Price ($)"}
            ).update_layout(
                plot_bgcolor=dark_theme["graph_bg"],
                paper_bgcolor=dark_theme["card_bg"],
                font=dict(color=dark_theme["text"]),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor=dark_theme["gray"])
            )
        )
    ])

# Create psychology view
def create_psychology_view(trader_data):
    # Prepare psychology data
    psychology_data = []
    for profile, data in trader_data.items():
        psychology_data.append({
            "profile": profile,
            "name": data["name"],
            "emotional_state": data["emotional_state"],
            "confidence": data["confidence"] * 100,  # Convert to percentage
            "risk_level": data["risk_level"] * 100   # Convert to percentage
        })
    
    df = pd.DataFrame(psychology_data)
    
    # Emotional state pie chart data
    emotional_counts = df["emotional_state"].value_counts().reset_index()
    emotional_counts.columns = ["state", "count"]
    
    # Create emotion color map
    emotion_colors = {
        "neutral": dark_theme["blue"],
        "greedy": dark_theme["green"],
        "fearful": dark_theme["red"],
        "confident": dark_theme["accent"],
        "stressed": dark_theme["purple"]
    }
    
    return html.Div(children=[
        # Trader Psychology Cards
        html.Div(style={
            "display": "grid",
            "gridTemplateColumns": "repeat(2, 1fr)",
            "gap": "20px",
            "marginBottom": "20px"
        }, children=[
            # Create a card for each trader profile
            *[create_psychology_card(profile, data) for profile, data in trader_data.items()]
        ]),
        
        # Charts Row
        html.Div(style={
            "display": "grid",
            "gridTemplateColumns": "repeat(2, 1fr)",
            "gap": "20px",
        }, children=[
            # Confidence Levels
            dcc.Graph(
                figure=px.bar(
                    df, x="name", y="confidence", color="profile",
                    color_discrete_map=profile_colors,
                    title="Trader Confidence Levels",
                    labels={"confidence": "Confidence (%)", "name": "Trader"},
                    text_auto='.1f'
                ).update_layout(
                    plot_bgcolor=dark_theme["graph_bg"],
                    paper_bgcolor=dark_theme["card_bg"],
                    font=dict(color=dark_theme["text"]),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor=dark_theme["gray"]),
                    showlegend=False
                )
            ),
            
            # Risk Levels
            dcc.Graph(
                figure=px.bar(
                    df, x="name", y="risk_level", color="profile",
                    color_discrete_map=profile_colors,
                    title="Trader Risk Appetite",
                    labels={"risk_level": "Risk Level (%)", "name": "Trader"},
                    text_auto='.1f'
                ).update_layout(
                    plot_bgcolor=dark_theme["graph_bg"],
                    paper_bgcolor=dark_theme["card_bg"],
                    font=dict(color=dark_theme["text"]),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor=dark_theme["gray"]),
                    showlegend=False
                )
            )
        ]),
        
        # Emotional State Pie Chart
        dcc.Graph(
            figure=px.pie(
                emotional_counts, values="count", names="state", title="Emotional State Distribution",
                color="state", color_discrete_map=emotion_colors
            ).update_layout(
                plot_bgcolor=dark_theme["graph_bg"],
                paper_bgcolor=dark_theme["card_bg"],
                font=dict(color=dark_theme["text"])
            ).update_traces(
                textinfo="percent+label"
            )
        )
    ])

# Helper function to create psychology card
def create_psychology_card(profile, data):
    # Determine emotion icon and color
    emotion_icon = "😐"  # Neutral default
    emotion_color = dark_theme["blue"]
    
    if data["emotional_state"] == "greedy":
        emotion_icon = "🤑"
        emotion_color = dark_theme["green"]
    elif data["emotional_state"] == "fearful":
        emotion_icon = "😨"
        emotion_color = dark_theme["red"]
    elif data["emotional_state"] == "confident":
        emotion_icon = "😎"
        emotion_color = dark_theme["accent"]
    elif data["emotional_state"] == "stressed":
        emotion_icon = "😰"
        emotion_color = dark_theme["purple"]
    
    return html.Div(style={
        "backgroundColor": dark_theme["graph_bg"],
        "borderRadius": "10px",
        "padding": "15px",
        "border": f"2px solid {profile_colors[profile]}"
    }, children=[
        # Header with name and badge
        html.Div(style={
            "display": "flex",
            "alignItems": "center",
            "marginBottom": "10px"
        }, children=[
            html.Div(profile_badges[profile], style={"fontSize": "24px", "marginRight": "10px"}),
            html.Div(data["name"], style={"fontWeight": "bold", "fontSize": "18px"})
        ]),
        
        # Emotional state
        html.Div(style={
            "display": "flex",
            "alignItems": "center",
            "marginBottom": "10px"
        }, children=[
            html.Div(emotion_icon, style={"fontSize": "32px", "marginRight": "10px"}),
            html.Div(style={"flex": "1"}, children=[
                html.Div("Emotional State", style={"fontWeight": "bold"}),
                html.Div(data["emotional_state"].capitalize(), style={"color": emotion_color})
            ])
        ]),
        
        # Confidence level
        html.Div(style={
            "display": "flex",
            "alignItems": "center",
            "marginBottom": "10px"
        }, children=[
            html.Div("🧠", style={"fontSize": "20px", "marginRight": "10px"}),
            html.Div(style={"flex": "1"}, children=[
                html.Div("Confidence Level", style={"fontWeight": "bold"}),
                html.Div([
                    html.Div(style={
                        "width": f"{data['confidence']*100}%",
                        "backgroundColor": profile_colors[profile],
                        "height": "10px",
                        "borderRadius": "5px"
                    }),
                    html.Div(f"{data['confidence']*100:.0f}%", style={"marginTop": "2px"})
                ])
            ])
        ]),
        
        # Risk level
        html.Div(style={
            "display": "flex",
            "alignItems": "center"
        }, children=[
            html.Div("🎯", style={"fontSize": "20px", "marginRight": "10px"}),
            html.Div(style={"flex": "1"}, children=[
                html.Div("Risk Appetite", style={"fontWeight": "bold"}),
                html.Div([
                    html.Div(style={
                        "width": f"{data['risk_level']*100}%", 
                        "backgroundColor": dark_theme["red"] if data['risk_level'] > 0.7 else 
                                          dark_theme["yellow"] if data['risk_level'] > 0.4 else
                                          dark_theme["green"],
                        "height": "10px",
                        "borderRadius": "5px"
                    }),
                    html.Div(f"{data['risk_level']*100:.0f}%", style={"marginTop": "2px"})
                ])
            ])
        ])
    ])

# Create positions view
def create_positions_view(trader_data, battle_state):
    # If no one has any positions
    has_positions = any(len(data["positions"]) > 0 for _, data in trader_data.items())
    if not has_positions:
        return html.Div(
            "No active positions", 
            style={"textAlign": "center", "fontSize": "24px", "marginTop": "50px", "color": dark_theme["gray"]}
        )
    
    # Create position cards for each trader with positions
    position_cards = []
    for profile, data in trader_data.items():
        if len(data["positions"]) > 0:
            # Trader header
            position_cards.append(html.Div(style={
                "backgroundColor": dark_theme["graph_bg"],
                "borderRadius": "10px",
                "padding": "15px",
                "marginBottom": "20px",
                "border": f"2px solid {profile_colors[profile]}"
            }, children=[
                # Trader name
                html.Div(style={
                    "display": "flex",
                    "alignItems": "center",
                    "marginBottom": "10px"
                }, children=[
                    html.Div(profile_badges[profile], style={"fontSize": "24px", "marginRight": "10px"}),
                    html.Div(data["name"], style={"fontWeight": "bold", "fontSize": "18px"})
                ]),
                
                # Position list
                html.Div([
                    create_position_card(position, battle_state["btc_price"]) 
                    for position in data["positions"]
                ])
            ]))
    
    return html.Div(position_cards)

# Helper to create a position card
def create_position_card(position, current_price):
    # Calculate position PnL
    price_diff = current_price - position["entry_price"] if position["direction"] == "LONG" else position["entry_price"] - current_price
    pnl = price_diff * position["size"] * position["leverage"]
    pnl_pct = (price_diff / position["entry_price"]) * 100 * position["leverage"]
    
    # Calculate distance to stop loss and take profit
    if "stop_loss" in position:
        sl_distance = abs(position["stop_loss"] - current_price) / current_price * 100
    else:
        sl_distance = None
    
    if "take_profit" in position:
        tp_distance = abs(position["take_profit"] - current_price) / current_price * 100
    else:
        tp_distance = None
    
    return html.Div(style={
        "backgroundColor": dark_theme["card_bg"],
        "padding": "10px",
        "borderRadius": "5px",
        "marginBottom": "10px",
        "border": f"1px solid {dark_theme['green'] if position['direction'] == 'LONG' else dark_theme['red']}"
    }, children=[
        # Position header
        html.Div(style={
            "display": "flex",
            "justifyContent": "space-between",
            "marginBottom": "5px"
        }, children=[
            # Direction and size
            html.Div([
                html.Span(
                    f"{position['direction']} {position['size']:.4f} BTC", 
                    style={
                        "fontWeight": "bold", 
                        "color": dark_theme["green"] if position["direction"] == "LONG" else dark_theme["red"]
                    }
                ),
                html.Span(f" ({position['leverage']}x)", style={"color": dark_theme["accent"]})
            ]),
            
            # Entry time and price
            html.Div(f"@ ${position['entry_price']:.2f}", style={"color": dark_theme["gray"]})
        ]),
        
        # PnL
        html.Div(style={
            "display": "flex",
            "justifyContent": "space-between",
            "marginBottom": "5px"
        }, children=[
            html.Div("PnL:"),
            html.Div([
                html.Span(
                    f"${pnl:.2f}", 
                    style={"color": dark_theme["green"] if pnl >= 0 else dark_theme["red"]}
                ),
                html.Span(
                    f" ({pnl_pct:+.2f}%)", 
                    style={"color": dark_theme["green"] if pnl >= 0 else dark_theme["red"]}
                )
            ])
        ]),
        
        # Stop Loss and Take Profit
        html.Div(style={
            "display": "flex",
            "justifyContent": "space-between"
        }, children=[
            html.Div([
                html.Span("SL: ", style={"fontWeight": "bold"}),
                html.Span(
                    f"${position['stop_loss']:.2f} ({sl_distance:.1f}%)" if sl_distance else "None",
                    style={"color": dark_theme["red"]}
                )
            ]),
            html.Div([
                html.Span("TP: ", style={"fontWeight": "bold"}),
                html.Span(
                    f"${position['take_profit']:.2f} ({tp_distance:.1f}%)" if tp_distance else "None",
                    style={"color": dark_theme["green"]}
                )
            ])
        ])
    ])

# Create decisions view
def create_decisions_view(trader_data):
    # Create decision analysis for each trader
    decision_cards = []
    
    for profile, data in trader_data.items():
        # Count number of trades
        total_trades = data["trades"]
        if total_trades == 0:
            trade_summary = "No trades yet"
        else:
            win_rate = data["winning_trades"] / total_trades * 100
            trade_summary = f"{data['winning_trades']}/{total_trades} trades won ({win_rate:.1f}%)"
        
        # Create decision card
        decision_cards.append(html.Div(style={
            "backgroundColor": dark_theme["graph_bg"],
            "borderRadius": "10px",
            "padding": "15px",
            "marginBottom": "20px",
            "border": f"2px solid {profile_colors[profile]}"
        }, children=[
            # Trader name
            html.Div(style={
                "display": "flex",
                "alignItems": "center",
                "marginBottom": "10px"
            }, children=[
                html.Div(profile_badges[profile], style={"fontSize": "24px", "marginRight": "10px"}),
                html.Div(data["name"], style={"fontWeight": "bold", "fontSize": "18px"})
            ]),
            
            # Trade stats
            html.Div(style={"marginBottom": "10px"}, children=[
                html.Div("Trade Statistics:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                html.Div(trade_summary),
                html.Div(f"Average Win: ${data.get('avg_win', 0):.2f}" if data.get('avg_win') else "No winning trades"),
                html.Div(f"Average Loss: ${data.get('avg_loss', 0):.2f}" if data.get('avg_loss') else "No losing trades")
            ]),
            
            # Decision metrics
            html.Div(style={"marginBottom": "10px"}, children=[
                html.Div("Decision Metrics:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                
                # Accuracy meter
                html.Div(style={"marginBottom": "10px"}, children=[
                    html.Div("Decision Accuracy", style={"marginBottom": "2px"}),
                    html.Div(style={
                        "height": "10px",
                        "backgroundColor": dark_theme["card_bg"],
                        "borderRadius": "5px"
                    }, children=[
                        html.Div(style={
                            "width": f"{data['win_rate']*100 if 'win_rate' in data else 0}%",
                            "height": "100%",
                            "backgroundColor": profile_colors[profile],
                            "borderRadius": "5px"
                        })
                    ]),
                    html.Div(f"{data['win_rate']*100 if 'win_rate' in data else 0:.1f}%", 
                             style={"marginTop": "2px"})
                ]),
                
                # Discipline meter
                html.Div(children=[
                    html.Div("Trading Discipline", style={"marginBottom": "2px"}),
                    html.Div(style={
                        "height": "10px",
                        "backgroundColor": dark_theme["card_bg"],
                        "borderRadius": "5px"
                    }, children=[
                        html.Div(style={
                            # For simplicity, use inverse of risk level as discipline proxy
                            "width": f"{(1 - data['risk_level'])*100}%",
                            "height": "100%",
                            "backgroundColor": 
                                dark_theme["green"] if data['risk_level'] < 0.3 else
                                dark_theme["yellow"] if data['risk_level'] < 0.7 else
                                dark_theme["red"],
                            "borderRadius": "5px"
                        })
                    ]),
                    html.Div(f"{(1 - data['risk_level'])*100:.1f}%", style={"marginTop": "2px"})
                ])
            ]),
            
            # Recent decisions/trade history
            html.Div(children=[
                html.Div("Recent Decisions:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                html.Div("No trade history available" if not data["trade_history"] else "",
                        style={"fontStyle": "italic"})
            ])
        ]))
    
    return html.Div(decision_cards)

# Handle simulation updates
@app.callback(
    [Output("trader-state", "children"),
     Output("battle-state", "children"),
     Output("start-battle", "disabled")],
    [Input("battle-mode", "value"),
     Input("update-interval", "n_intervals"),
     Input("start-battle", "n_clicks"),
     Input("reset-arena", "n_clicks")],
    [State("trader-state", "children"),
     State("battle-state", "children")]
)
def update_data_based_on_mode(mode, n_intervals, start_clicks, reset_clicks, trader_state_json, battle_state_json):
    # Get the triggered button
    ctx = callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
    
    if mode == 'real':
        # Get data from Redis
        try:
            real_trader_data = redis_conn.get("omega:live_trader_data")
            real_battle_state = redis_conn.get("omega:live_battle_state")
            start_trading = redis_conn.get("omega:start_trading")
            
            if real_trader_data and real_battle_state:
                # Data exists in Redis, use it
                print("Using real trading data from Redis")
                battle_state = json.loads(real_battle_state)
                
                # Handle start button
                if triggered_id == "start-battle":
                    redis_conn.set("omega:start_trading", "1")
                    print("Sent start signal for real trading")
                
                # Handle reset button
                if triggered_id == "reset-arena":
                    redis_conn.delete("omega:start_trading")
                    print("Removed start signal for real trading")
                
                # Update battle_active based on start_trading key
                battle_state["battle_active"] = start_trading == "1"
                
                return real_trader_data, json.dumps(battle_state), False  # Enable start button in real mode
            else:
                # Fallback to simulation if Redis data not available
                print("No real data in Redis, falling back to simulation")
                if not trader_state_json:
                    trader_data = generate_initial_trader_data()
                else:
                    trader_data = json.loads(trader_state_json)
                
                if not battle_state_json:
                    battle_state = initialize_battle_state()
                else:
                    battle_state = json.loads(battle_state_json)
                    
                return json.dumps(trader_data), json.dumps(battle_state), False
        except Exception as e:
            print(f"Error fetching real trader data: {e}")
            # Fallback to simulation
            return trader_state_json or json.dumps(generate_initial_trader_data()), \
                   battle_state_json or json.dumps(initialize_battle_state()), \
                   False
    else:
        # Simulated mode - use the existing flow
        if not trader_state_json:
            trader_data = generate_initial_trader_data()
        else:
            trader_data = json.loads(trader_state_json)
        
        if not battle_state_json:
            battle_state = initialize_battle_state()
        else:
            battle_state = json.loads(battle_state_json)
        
        # Handle reset button
        if triggered_id == "reset-arena":
            trader_data = generate_initial_trader_data()
            battle_state = initialize_battle_state()
            return json.dumps(trader_data), json.dumps(battle_state), False
        
        # Handle start button
        if triggered_id == "start-battle":
            battle_state["battle_active"] = True
        
        # Only update the simulation if battle is active
        if battle_state["battle_active"]:
            # Advance the simulation
            simulate_trading_step(trader_data, battle_state)
        
        return json.dumps(trader_data), json.dumps(battle_state), False

# Simulate a single trading step
def simulate_trading_step(trader_data, battle_state):
    # Update BTC price
    old_price = battle_state["btc_price"]
    price_change_pct = random.normalvariate(0, 0.005)  # 0.5% standard deviation
    new_price = old_price * (1 + price_change_pct)
    battle_state["btc_price"] = new_price
    battle_state["btc_history"].append(new_price)
    
    # Limit history length
    if len(battle_state["btc_history"]) > 100:
        battle_state["btc_history"] = battle_state["btc_history"][-100:]
    
    # Advance session/day counters
    battle_state["session"] += 1
    if battle_state["session"] > 4:
        battle_state["session"] = 1
        battle_state["day"] += 1
        
        # Add a day completed event
        battle_state["timeline_events"].append({
            "type": "day_end",
            "title": f"Day {battle_state['day']-1} Completed",
            "description": f"BTC price moved {((new_price/old_price)-1)*100:+.2f}% today",
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "timestamp": datetime.datetime.now().timestamp(),
            "btc_price": new_price
        })
    
    # For each trader, simulate trading decisions
    for profile, data in trader_data.items():
        # First, update open positions
        update_positions(profile, data, new_price, battle_state)
        
        # Sometimes make trading decisions
        if random.random() < get_trade_probability(profile):
            make_trading_decision(profile, data, new_price, battle_state)
        
        # Update psychological state
        update_psychological_state(profile, data)
        
        # Check for achievements
        check_achievements(profile, data, battle_state)

# Get probability of making a trade based on profile
def get_trade_probability(profile):
    if profile == "scalper":
        return 0.3  # High frequency
    elif profile == "aggressive":
        return 0.2  # Medium-high frequency
    elif profile == "newbie":
        return 0.15  # Random decision-making
    else:  # strategic
        return 0.1  # More selective

# Update trader psychological state
def update_psychological_state(profile, data):
    # Update confidence based on recent performance
    pnl_pct = data["pnl"] / data["capital"] if data["capital"] > 0 else 0
    
    # Different profiles have different psychological characteristics
    if profile == "aggressive":
        # Aggressive traders have volatile emotions
        if pnl_pct > 0.05:  # Big win
            data["emotional_state"] = "greedy"
            data["confidence"] = min(1.0, data["confidence"] + 0.1)
        elif pnl_pct < -0.05:  # Big loss
            data["emotional_state"] = "fearful"
            data["confidence"] = max(0.1, data["confidence"] - 0.2)
            
        # They also tend to increase risk when winning
        if data["emotional_state"] == "greedy":
            data["risk_level"] = min(1.0, data["risk_level"] + 0.05)
        
    elif profile == "strategic":
        # Strategic traders are more stable
        if pnl_pct > 0.1:  # Bigger win needed to affect emotions
            data["emotional_state"] = "confident"
            data["confidence"] = min(0.9, data["confidence"] + 0.05)
        elif pnl_pct < -0.1:  # Bigger loss needed to affect emotions
            data["emotional_state"] = "neutral"  # They stay composed
            data["confidence"] = max(0.3, data["confidence"] - 0.05)
            
        # Their risk level is more stable
        data["risk_level"] = 0.4 + (data["confidence"] - 0.5) * 0.2  # Small adjustments
        
    elif profile == "newbie":
        # Newbies have extremely volatile emotions
        if pnl_pct > 0.02:  # Small win makes them greedy
            data["emotional_state"] = "greedy"
            data["confidence"] = min(1.0, data["confidence"] + 0.15)
        elif pnl_pct < -0.02:  # Small loss makes them fearful
            data["emotional_state"] = "fearful"
            data["confidence"] = max(0.1, data["confidence"] - 0.3)
            
        # Their risk level is very emotional
        if data["emotional_state"] == "greedy":
            data["risk_level"] = min(1.0, data["risk_level"] + 0.1)
        elif data["emotional_state"] == "fearful":
            data["risk_level"] = min(1.0, data["risk_level"] + 0.1)  # Counterintuitively increase risk
            
    elif profile == "scalper":
        # Scalpers are mechanical
        data["emotional_state"] = "neutral"
        
        # They adjust confidence based on very recent performance
        if data["trades"] > 0 and data["winning_trades"] / data["trades"] > 0.5:
            data["confidence"] = min(0.8, data["confidence"] + 0.02)
        else:
            data["confidence"] = max(0.3, data["confidence"] - 0.02)
            
        # Their risk level is tied to their confidence
        data["risk_level"] = 0.3 + data["confidence"] * 0.3

# Update existing positions
def update_positions(profile, data, current_price, battle_state):
    if not data["positions"]:
        return
    
    # Check each position
    positions_to_remove = []
    for i, position in enumerate(data["positions"]):
        # Calculate current PnL
        price_diff = current_price - position["entry_price"] if position["direction"] == "LONG" else position["entry_price"] - current_price
        pnl = price_diff * position["size"] * position["leverage"]
        pnl_pct = (price_diff / position["entry_price"]) * 100 * position["leverage"]
        
        # Check for stop loss hit
        if "stop_loss" in position:
            if (position["direction"] == "LONG" and current_price <= position["stop_loss"]) or \
               (position["direction"] == "SHORT" and current_price >= position["stop_loss"]):
                # Close position at stop loss
                close_position(profile, data, position, "stop_loss", battle_state)
                positions_to_remove.append(i)
                continue
        
        # Check for take profit hit
        if "take_profit" in position:
            if (position["direction"] == "LONG" and current_price >= position["take_profit"]) or \
               (position["direction"] == "SHORT" and current_price <= position["take_profit"]):
                # Close position at take profit
                close_position(profile, data, position, "take_profit", battle_state)
                positions_to_remove.append(i)
                continue
        
        # Random chance to close position based on profile
        if random.random() < get_exit_probability(profile, pnl_pct):
            # Close position based on trader decision
            reason = "profit_taking" if pnl >= 0 else "cut_loss"
            close_position(profile, data, position, reason, battle_state)
            positions_to_remove.append(i)
    
    # Remove closed positions
    for i in sorted(positions_to_remove, reverse=True):
        data["positions"].pop(i)

# Get probability of exiting a position based on profile and PnL
def get_exit_probability(profile, pnl_pct):
    if profile == "scalper":
        # Scalpers exit quickly whether in profit or loss
        return 0.3
    elif profile == "aggressive":
        # Aggressive traders let profits run but cut losses quickly
        return 0.1 if pnl_pct > 0 else 0.3
    elif profile == "strategic":
        # Strategic traders stick to their plan
        return 0.05
    else:  # newbie
        # Newbies cut profits quickly but let losses run
        return 0.3 if pnl_pct > 0 else 0.1

# Make trading decision
def make_trading_decision(profile, data, current_price, battle_state):
    # Decide whether to open a new position
    if random.random() < data["risk_level"]:
        # Determine trade parameters based on profile
        direction = random.choice(["LONG", "SHORT"])
        leverage = random.uniform(1, 10)
        size = random.uniform(0.01, 0.1)  # BTC amount
        
        if profile == "strategic":
            sl_pct = random.uniform(0.02, 0.05)
            tp_pct = random.uniform(0.05, 0.1)
        elif profile == "aggressive":
            sl_pct = random.uniform(0.05, 0.1)
            tp_pct = random.uniform(0.1, 0.2)
        elif profile == "newbie":
            # Newbies often have no stop loss or inappropriate ones
            sl_pct = random.uniform(0.05, 0.1) if random.random() < 0.5 else None
            tp_pct = random.uniform(0.01, 0.03)  # Small targets
        else:  # scalper
            sl_pct = random.uniform(0.005, 0.01)  # Tight stops
            tp_pct = random.uniform(0.005, 0.015)  # Small targets
        
        # Calculate actual stop loss and take profit prices
        if sl_pct:
            stop_loss = current_price * (1 - sl_pct) if direction == "LONG" else current_price * (1 + sl_pct)
        else:
            stop_loss = None
    
    if tp_pct:
        take_profit = current_price * (1 + tp_pct) if direction == "LONG" else current_price * (1 - tp_pct)
    else:
        take_profit = None
    
    # Create position
    position = {
        "direction": direction,
        "entry_price": current_price,
        "size": size,
        "leverage": leverage,
        "entry_time": datetime.datetime.now().isoformat(),
        "stop_loss": stop_loss,
        "take_profit": take_profit
    }
    
    # Add position to trader's portfolio
    data["positions"].append(position)
    
    # Add event to timeline
    battle_state["timeline_events"].append({
        "type": "position_open",
        "title": f"{profile_badges[profile]} {data['name']} opened {direction}",
        "description": f"{direction} {size:.4f} BTC ({leverage:.1f}x) @ ${current_price:.2f}",
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "timestamp": datetime.datetime.now().timestamp(),
        "btc_price": current_price
    })

# Close a position
def close_position(profile, data, position, reason, battle_state):
    current_price = battle_state["btc_price"]
    
    # Calculate PnL
    price_diff = current_price - position["entry_price"] if position["direction"] == "LONG" else position["entry_price"] - current_price
    pnl = price_diff * position["size"] * position["leverage"]
    pnl_pct = (price_diff / position["entry_price"]) * 100 * position["leverage"]
    
    # Update trader stats
    data["pnl"] += pnl
    data["trades"] += 1
    
    if pnl >= 0:
        data["winning_trades"] += 1
        
        # Update average win
        if not data.get("avg_win"):
            data["avg_win"] = pnl
        else:
            data["avg_win"] = (data["avg_win"] * (data["winning_trades"] - 1) + pnl) / data["winning_trades"]
    else:
        data["losing_trades"] += 1
        
        # Update average loss
        if not data.get("avg_loss"):
            data["avg_loss"] = abs(pnl)
        else:
            data["avg_loss"] = (data["avg_loss"] * (data["losing_trades"] - 1) + abs(pnl)) / data["losing_trades"]
    
    # Update win rate
    data["win_rate"] = data["winning_trades"] / data["trades"]
    
    # Add to trade history
    trade_record = {
        "direction": position["direction"],
        "entry_price": position["entry_price"],
        "exit_price": current_price,
        "size": position["size"],
        "leverage": position["leverage"],
        "pnl": pnl,
        "pnl_pct": pnl_pct,
        "exit_reason": reason,
        "entry_time": position["entry_time"],
        "exit_time": datetime.datetime.now().isoformat()
    }
    
    data["trade_history"].insert(0, trade_record)
    
    # Limit trade history length
    if len(data["trade_history"]) > 20:
        data["trade_history"] = data["trade_history"][:20]
    
    # Add event to timeline
    result_text = f"profit ${pnl:.2f}" if pnl >= 0 else f"loss ${abs(pnl)::.2f}"
    reason_text = {
        "stop_loss": "Stop Loss",
        "take_profit": "Take Profit",
        "profit_taking": "Manual Profit",
        "cut_loss": "Manual Exit"
    }.get(reason, reason)
    
    battle_state["timeline_events"].append({
        "type": "position_close",
        "title": f"{profile_badges[profile]} {data['name']} closed {position['direction']}",
        "description": f"{reason_text}: {result_text} ({pnl_pct:+.2f}%)",
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "timestamp": datetime.datetime.now().timestamp(),
        "btc_price": current_price
    })

# Check for achievements
def check_achievements(profile, data, battle_state):
    # Check if trader already has this achievement
    def has_achievement(badge):
        return any(a["badge"] == badge for a in data["achievements"])
    
    # 3+ winning trades in a row
    if data["winning_trades"] >= 3 and not has_achievement(achievement_badges["winning_streak"]):
        data["achievements"].append({
            "badge": achievement_badges["winning_streak"],
            "text": f"Achieved 3+ consecutive winning trades",
            "timestamp": datetime.datetime.now().timestamp()
        })
        
        # Add timeline event
        battle_state["timeline_events"].append({
            "type": "achievement",
            "title": f"{profile_badges[profile]} {data['name']} Achievement Unlocked!",
            "description": f"🏆 Winning Streak: 3+ consecutive winning trades",
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "timestamp": datetime.datetime.now().timestamp(),
            "btc_price": battle_state["btc_price"]
        })
    
    # Big win (>5% on a single trade)
    if data["trade_history"] and data["trade_history"][0]["pnl_pct"] > 5 and not has_achievement(achievement_badges["big_win"]):
        data["achievements"].append({
            "badge": achievement_badges["big_win"],
            "text": f"Scored a big win with over 5% profit on a single trade",
            "timestamp": datetime.datetime.now().timestamp()
        })
        
        # Add timeline event
        battle_state["timeline_events"].append({
            "type": "achievement",
            "title": f"{profile_badges[profile]} {data['name']} Achievement Unlocked!",
            "description": f"💰 Big Win: Over 5% profit on a single trade",
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "timestamp": datetime.datetime.now().timestamp(),
            "btc_price": battle_state["btc_price"]
        })
    
    # Risk Manager (win rate > 60% after 10+ trades)
    if data["trades"] >= 10 and data["win_rate"] > 0.6 and not has_achievement(achievement_badges["risk_manager"]):
        data["achievements"].append({
            "badge": achievement_badges["risk_manager"],
            "text": f"Maintained a win rate above 60% after 10+ trades",
            "timestamp": datetime.datetime.now().timestamp()
        })
        
        # Add timeline event
        battle_state["timeline_events"].append({
            "type": "achievement",
            "title": f"{profile_badges[profile]} {data['name']} Achievement Unlocked!",
            "description": f"🛡️ Risk Manager: Win rate above 60% after 10+ trades",
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "timestamp": datetime.datetime.now().timestamp(),
            "btc_price": battle_state["btc_price"]
        })
    
    # Comeback (recover from 10%+ drawdown)
    if data["pnl"] / data["capital"] > 0.1 and not has_achievement(achievement_badges["comeback"]):
        data["achievements"].append({
            "badge": achievement_badges["comeback"],
            "text": f"Recovered from a drawdown of over 10%",
            "timestamp": datetime.datetime.now().timestamp()
        })
        
        # Add timeline event
        battle_state["timeline_events"].append({
            "type": "achievement",
            "title": f"{profile_badges[profile]} {data['name']} Achievement Unlocked!",
            "description": f"🚀 Comeback: Recovered from a drawdown of over 10%",
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "timestamp": datetime.datetime.now().timestamp(),
            "btc_price": battle_state["btc_price"]
        })
    
    # Volume King (highest trading volume)
    if data["trades"] > 20 and not has_achievement(achievement_badges["volume_king"]):
        data["achievements"].append({
            "badge": achievement_badges["volume_king"],
            "text": f"Executed the highest trading volume",
            "timestamp": datetime.datetime.now().timestamp()
        })
        
        # Add timeline event
        battle_state["timeline_events"].append({
            "type": "achievement",
            "title": f"{profile_badges[profile]} {data['name']} Achievement Unlocked!",
            "description": f"📊 Volume King: Executed the highest trading volume",
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "timestamp": datetime.datetime.now().timestamp(),
            "btc_price": battle_state["btc_price"]
        })
    
    # Diamond Hands (hold position for 5+ days)
    if any((datetime.datetime.now() - datetime.datetime.fromisoformat(pos["entry_time"])).days >= 5 for pos in data["positions"]) and not has_achievement(achievement_badges["diamond_hands"]):
        data["achievements"].append({
            "badge": achievement_badges["diamond_hands"],
            "text": f"Held a position for 5+ days",
            "timestamp": datetime.datetime.now().timestamp()
        })
        
        # Add timeline event
        battle_state["timeline_events"].append({
            "type": "achievement",
            "title": f"{profile_badges[profile]} {data['name']} Achievement Unlocked!",
            "description": f"💎 Diamond Hands: Held a position for 5+ days",
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "timestamp": datetime.datetime.now().timestamp(),
            "btc_price": battle_state["btc_price"]
        })
    
    # Paper Hands (close position within 1 hour)
    if any((datetime.datetime.now() - datetime.datetime.fromisoformat(pos["entry_time"])).seconds < 3600 for pos in data["positions"]) and not has_achievement(achievement_badges["paper_hands"]):
        data["achievements"].append({
            "badge": achievement_badges["paper_hands"],
            "text": f"Closed a position within 1 hour",
            "timestamp": datetime.datetime.now().timestamp()
        })
        
        # Add timeline event
        battle_state["timeline_events"].append({
            "type": "achievement",
            "title": f"{profile_badges[profile]} {data['name']} Achievement Unlocked!",
            "description": f"📄 Paper Hands: Closed a position within 1 hour",
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "timestamp": datetime.datetime.now().timestamp(),
            "btc_price": battle_state["btc_price"]
        })

if __name__ == "__main__":
    app.run_server(debug=True)