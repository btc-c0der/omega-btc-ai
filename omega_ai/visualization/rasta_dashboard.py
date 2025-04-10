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
RASTA DASHBOARD - Divine Web Visualization for OMEGA BTC AI System
Provides a sacred web-based dashboard for visualizing BTC price movements,
Fibonacci alignments, Schumann resonance harmonics, and Exodus Flow.

Matthew 5:14-16
"You are the light of the world. A city set on a hill cannot be hidden.
Nor do people light a lamp and put it under a basket, but on a stand,
and it gives light to all in the house. In the same way, let your light
shine before others, so that they may see your good works."
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import redis
import json
import time
import datetime
from typing import Dict, List, Optional, Tuple, Union
import logging
import os
import sys

# Configure logging with RASTA COLORS
class ColoredFormatter(logging.Formatter):
    """Custom formatter with RASTA colors for logging"""
    
    COLORS = {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[32m',   # Green
        'WARNING': '\033[33m', # Yellow
        'ERROR': '\033[31m',   # Red
        'CRITICAL': '\033[41m', # Red background
        'RESET': '\033[0m',    # Reset
    }
    
    def format(self, record):
        log_message = super().format(record)
        if hasattr(record, 'levelname'):
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            reset = self.COLORS['RESET']
            log_message = f"{color}{log_message}{reset}"
        return log_message

# Setup logger
logger = logging.getLogger("RASTA_DASHBOARD")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

class RastaDashboard:
    """Sacred dashboard for visualizing divine market insights from OMEGA BTC AI"""
    
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379, 
                 redis_db: int = 0, history_length: int = 144):
        """
        Initialize the sacred dashboard
        
        Args:
            redis_host: Redis server host
            redis_port: Redis server port
            redis_db: Redis database number
            history_length: Length of history to maintain (144 is sacred Fibonacci number)
        """
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.history_length = history_length
        
        # Initialize Redis connection
        try:
            self.redis_client = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                db=self.redis_db,
                decode_responses=True
            )
            logger.info("✅ Connected to Redis divine data stream")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            raise
        
        # Initialize data structures
        self.price_history = []
        self.volume_history = []
        self.exodus_flow_history = []
        self.fibonacci_alignment_history = []
        self.schumann_resonance_history = []
        self.trap_alerts = []
        
        # Streamlit page configuration
        self._configure_streamlit()
    
    def _configure_streamlit(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="RASTA DASHBOARD - OMEGA BTC AI",
            page_icon="🔱",
            layout="wide",
            initial_sidebar_state="expanded",
        )
    
    def _display_header(self):
        """Display the sacred header of the dashboard"""
        st.title("🔱 OMEGA BTC AI - RASTA DASHBOARD 🔱")
        st.markdown("""
        > *"In divine vibration, we see the true nature of the market"*
        
        This sacred dashboard visualizes the cosmic rhythms of Bitcoin price movements,
        aligned with Fibonacci sequences and Schumann resonance harmonics.
        """)
        
        # Display current time
        now = datetime.datetime.now()
        st.sidebar.markdown(f"### 🕒 Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def _fetch_latest_data(self):
        """Fetch the latest data from Redis"""
        try:
            # Fetch BTC price data
            btc_data = self.redis_client.get("btc_price_data")
            if btc_data:
                btc_data = json.loads(btc_data)
                self.price_history.append(btc_data.get("price", 0))
                self.volume_history.append(btc_data.get("volume", 0))
                
            # Fetch Exodus flow data
            exodus_data = self.redis_client.get("exodus_flow")
            if exodus_data:
                exodus_data = json.loads(exodus_data)
                self.exodus_flow_history.append(exodus_data.get("flow_strength", 0))
                
            # Fetch Fibonacci alignment data
            fib_data = self.redis_client.get("fibonacci_alignment")
            if fib_data:
                fib_data = json.loads(fib_data)
                self.fibonacci_alignment_history.append(fib_data.get("alignment_score", 0))
                
            # Fetch Schumann resonance data
            schumann_data = self.redis_client.get("schumann_resonance")
            if schumann_data:
                schumann_data = json.loads(schumann_data)
                self.schumann_resonance_history.append(schumann_data.get("resonance_strength", 0))
                
            # Fetch trap alerts
            trap_alert = self.redis_client.get("trap_alert")
            if trap_alert:
                trap_alert = json.loads(trap_alert)
                if trap_alert.get("active", False):
                    self.trap_alerts.append({
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "type": trap_alert.get("type", "Unknown"),
                        "confidence": trap_alert.get("confidence", 0),
                        "price": trap_alert.get("price", 0)
                    })
            
            # Maintain history length
            self.price_history = self.price_history[-self.history_length:]
            self.volume_history = self.volume_history[-self.history_length:]
            self.exodus_flow_history = self.exodus_flow_history[-self.history_length:]
            self.fibonacci_alignment_history = self.fibonacci_alignment_history[-self.history_length:]
            self.schumann_resonance_history = self.schumann_resonance_history[-self.history_length:]
            self.trap_alerts = self.trap_alerts[-21:]  # Keep only recent alerts
            
            logger.info("✅ Successfully updated divine data streams")
        except Exception as e:
            logger.error(f"❌ Error fetching data from Redis: {e}")
    
    def _plot_price_chart(self):
        """Plot the sacred BTC price chart with Fibonacci levels"""
        st.subheader("📈 Divine Price Flow")
        
        if not self.price_history:
            st.info("Awaiting divine price data...")
            return
        
        # Create figure
        fig = go.Figure()
        
        # Add price line
        fig.add_trace(go.Scatter(
            y=self.price_history,
            mode='lines',
            name='BTC Price',
            line=dict(color='#FFD700', width=2),
            fill='tozeroy',
            fillcolor='rgba(255, 215, 0, 0.1)'
        ))
        
        # Calculate Fibonacci levels if we have enough data
        if len(self.price_history) > 2:
            min_price = min(self.price_history)
            max_price = max(self.price_history)
            price_range = max_price - min_price
            
            # Add Fibonacci retracement levels
            fib_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
            fib_colors = ['rgba(255,0,0,0.3)', 'rgba(255,165,0,0.3)', 
                          'rgba(255,255,0,0.3)', 'rgba(0,128,0,0.3)',
                          'rgba(0,0,255,0.3)', 'rgba(75,0,130,0.3)',
                          'rgba(238,130,238,0.3)']
            
            for i, level in enumerate(fib_levels):
                fib_price = max_price - price_range * level
                fig.add_shape(
                    type="line",
                    x0=0,
                    y0=fib_price,
                    x1=len(self.price_history),
                    y1=fib_price,
                    line=dict(color=fib_colors[i], width=1, dash="dot"),
                )
                fig.add_annotation(
                    x=len(self.price_history),
                    y=fib_price,
                    text=f"Fib {level}",
                    showarrow=False,
                    xshift=10,
                    font=dict(size=10, color="#FFD700")
                )
        
        # Update layout
        fig.update_layout(
            title="BTC Price with Sacred Fibonacci Levels",
            xaxis_title="Time (144-period window)",
            yaxis_title="Price (USD)",
            template="plotly_dark",
            height=400,
            margin=dict(l=0, r=0, t=40, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _plot_exodus_flow(self):
        """Plot the divine EXODUS flow"""
        st.subheader("⚡ EXODUS Flow Strength")
        
        if not self.exodus_flow_history:
            st.info("Awaiting divine EXODUS flow data...")
            return
        
        # Create figure
        fig = go.Figure()
        
        # Add exodus flow line
        fig.add_trace(go.Scatter(
            y=self.exodus_flow_history,
            mode='lines',
            name='EXODUS Flow',
            line=dict(color='#FF0000', width=2),
            fill='tozeroy',
            fillcolor='rgba(255, 0, 0, 0.1)'
        ))
        
        # Add threshold lines
        fig.add_shape(
            type="line",
            x0=0,
            y0=0.618,  # Golden ratio threshold
            x1=len(self.exodus_flow_history),
            y1=0.618,
            line=dict(color="green", width=1, dash="dash"),
        )
        
        fig.add_shape(
            type="line",
            x0=0,
            y0=-0.618,  # Negative golden ratio threshold
            x1=len(self.exodus_flow_history),
            y1=-0.618,
            line=dict(color="red", width=1, dash="dash"),
        )
        
        # Update layout
        fig.update_layout(
            title="Sacred EXODUS Flow Strength",
            xaxis_title="Time (144-period window)",
            yaxis_title="Flow Strength",
            template="plotly_dark",
            height=300,
            margin=dict(l=0, r=0, t=40, b=0),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _plot_resonance_dashboard(self):
        """Plot the combined Schumann and Fibonacci resonance"""
        st.subheader("🌊 Divine Resonance Dashboard")
        
        if not self.schumann_resonance_history or not self.fibonacci_alignment_history:
            st.info("Awaiting divine resonance data...")
            return
        
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add Schumann resonance line
        fig.add_trace(
            go.Scatter(
                y=self.schumann_resonance_history,
                mode='lines',
                name='Schumann Resonance',
                line=dict(color='#9370DB', width=2)
            ),
            secondary_y=False,
        )
        
        # Add Fibonacci alignment line
        fig.add_trace(
            go.Scatter(
                y=self.fibonacci_alignment_history,
                mode='lines',
                name='Fibonacci Alignment',
                line=dict(color='#32CD32', width=2)
            ),
            secondary_y=True,
        )
        
        # Update layout
        fig.update_layout(
            title="Schumann Resonance & Fibonacci Alignment",
            template="plotly_dark",
            height=300,
            margin=dict(l=0, r=0, t=40, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Set x-axis and y-axis titles
        fig.update_xaxes(title_text="Time (144-period window)")
        fig.update_yaxes(title_text="Schumann Resonance", secondary_y=False)
        fig.update_yaxes(title_text="Fibonacci Alignment", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _display_trap_alerts(self):
        """Display market maker trap alerts"""
        st.subheader("⚠️ Market Maker Trap Alerts")
        
        if not self.trap_alerts:
            st.info("No divine trap alerts detected...")
            return
        
        # Create a dataframe for the alerts
        df = pd.DataFrame(self.trap_alerts)
        
        # Style the dataframe
        st.dataframe(
            df,
            column_config={
                "timestamp": "Timestamp",
                "type": "Trap Type",
                "confidence": st.column_config.ProgressColumn(
                    "Confidence",
                    min_value=0,
                    max_value=1,
                    format="%.2f",
                ),
                "price": "Price at Alert"
            },
            use_container_width=True,
            hide_index=True,
        )
    
    def _display_system_status(self):
        """Display the system status in the sidebar"""
        st.sidebar.subheader("🔄 System Status")
        
        # Check Redis connection
        redis_status = "✅ Connected" if self.redis_client.ping() else "❌ Disconnected"
        st.sidebar.markdown(f"**Redis:** {redis_status}")
        
        # Display update frequency
        st.sidebar.markdown(f"**Update Frequency:** Every 13 seconds")
        
        # Display history length
        st.sidebar.markdown(f"**History Length:** {self.history_length} periods")
        
        # Display data points available
        data_points = {
            "Price Data": len(self.price_history),
            "EXODUS Flow": len(self.exodus_flow_history),
            "Fibonacci Alignment": len(self.fibonacci_alignment_history),
            "Schumann Resonance": len(self.schumann_resonance_history),
            "Trap Alerts": len(self.trap_alerts)
        }
        
        st.sidebar.markdown("**Data Points Available:**")
        for key, value in data_points.items():
            st.sidebar.markdown(f"- {key}: {value}")
    
    def _display_sidebar_controls(self):
        """Display control options in the sidebar"""
        st.sidebar.subheader("🛠️ Dashboard Controls")
        
        # History length slider
        history_length = st.sidebar.slider(
            "History Length", 
            min_value=21, 
            max_value=377, 
            value=self.history_length,
            step=21
        )
        if history_length != self.history_length:
            self.history_length = history_length
            st.sidebar.success(f"History length updated to {history_length}")
        
        # Refresh button
        if st.sidebar.button("🔄 Manual Refresh"):
            self._fetch_latest_data()
            st.sidebar.success("Divine data manually refreshed!")
        
        # Redis connection settings
        st.sidebar.subheader("🔌 Redis Connection")
        redis_host = st.sidebar.text_input("Redis Host", value=self.redis_host)
        redis_port = st.sidebar.number_input("Redis Port", value=self.redis_port)
        redis_db = st.sidebar.number_input("Redis DB", value=self.redis_db)
        
        if st.sidebar.button("Reconnect to Redis"):
            try:
                self.redis_host = redis_host
                self.redis_port = redis_port
                self.redis_db = redis_db
                
                self.redis_client = redis.Redis(
                    host=self.redis_host,
                    port=self.redis_port,
                    db=self.redis_db,
                    decode_responses=True
                )
                if self.redis_client.ping():
                    st.sidebar.success("✅ Successfully reconnected to Redis!")
                else:
                    st.sidebar.error("❌ Redis ping failed!")
            except Exception as e:
                st.sidebar.error(f"❌ Redis connection failed: {e}")
    
    def render_dashboard(self):
        """Render the entire sacred dashboard"""
        # Display header
        self._display_header()
        
        # Display sidebar
        self._display_system_status()
        self._display_sidebar_controls()
        
        # Fetch data
        self._fetch_latest_data()
        
        # Main dashboard components
        self._plot_price_chart()
        
        # Two column layout for EXODUS flow and resonance
        col1, col2 = st.columns(2)
        
        with col1:
            self._plot_exodus_flow()
        
        with col2:
            self._plot_resonance_dashboard()
        
        # Trap alerts at the bottom
        self._display_trap_alerts()

def main():
    """Main function to run the Rasta Dashboard"""
    dashboard = RastaDashboard()
    dashboard.render_dashboard()

if __name__ == "__main__":
    main() 