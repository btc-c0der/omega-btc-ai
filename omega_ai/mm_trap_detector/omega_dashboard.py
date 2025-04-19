
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

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional
from sklearn.decomposition import PCA
from .advanced_pattern_recognition import AdvancedPatternRecognition, Pattern

class OmegaDashboard:
    def __init__(self, pattern_recognition: AdvancedPatternRecognition):
        self.app = dash.Dash(__name__)
        self.pattern_recognition = pattern_recognition
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        """Set up the dashboard layout with a modern, dark theme."""
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1("Omega AI Market Maker Trap Dashboard", 
                       className="dashboard-title"),
                html.Div([
                    html.Button("Refresh Data", id="refresh-button", n_clicks=0),
                    html.Button("Export Analysis", id="export-button", n_clicks=0)
                ], className="button-container")
            ], className="header"),
            
            # Main Content
            html.Div([
                # Left Column - Pattern Analysis
                html.Div([
                    html.H2("Pattern Analysis"),
                    dcc.Graph(id="pattern-clusters-3d"),
                    dcc.Graph(id="pattern-evolution"),
                    dcc.Graph(id="pattern-impact")
                ], className="left-column"),
                
                # Right Column - Market Insights
                html.Div([
                    html.H2("Market Insights"),
                    dcc.Graph(id="pattern-distribution"),
                    dcc.Graph(id="confidence-timeline"),
                    dcc.Graph(id="persistent-patterns")
                ], className="right-column")
            ], className="main-content"),
            
            # Footer with Stats
            html.Div([
                html.Div([
                    html.H3("Pattern Statistics"),
                    html.Div(id="pattern-stats")
                ], className="stats-container"),
                html.Div([
                    html.H3("Market Conditions"),
                    html.Div(id="market-conditions")
                ], className="stats-container")
            ], className="footer")
        ], className="dashboard-container")
        
        # Add custom CSS
        self.app.index_string = '''
        <!DOCTYPE html>
        <html>
            <head>
                <title>Omega AI Dashboard</title>
                <style>
                    body {
                        background-color: #1a1a1a;
                        color: #ffffff;
                        font-family: 'Arial', sans-serif;
                    }
                    .dashboard-container {
                        padding: 20px;
                    }
                    .header {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 30px;
                    }
                    .dashboard-title {
                        color: #00ff00;
                        font-size: 2.5em;
                        margin: 0;
                    }
                    .button-container {
                        display: flex;
                        gap: 10px;
                    }
                    button {
                        background-color: #00ff00;
                        color: #000000;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                        font-weight: bold;
                    }
                    button:hover {
                        background-color: #00cc00;
                    }
                    .main-content {
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 20px;
                        margin-bottom: 30px;
                    }
                    .left-column, .right-column {
                        background-color: #2a2a2a;
                        padding: 20px;
                        border-radius: 10px;
                    }
                    .footer {
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 20px;
                    }
                    .stats-container {
                        background-color: #2a2a2a;
                        padding: 20px;
                        border-radius: 10px;
                    }
                    h2 {
                        color: #00ff00;
                        margin-bottom: 20px;
                    }
                    h3 {
                        color: #00ff00;
                        margin-bottom: 15px;
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
    
    def setup_callbacks(self):
        """Set up interactive callbacks for the dashboard."""
        
        @self.app.callback(
            [Output("pattern-clusters-3d", "figure"),
             Output("pattern-evolution", "figure"),
             Output("pattern-impact", "figure"),
             Output("pattern-distribution", "figure"),
             Output("confidence-timeline", "figure"),
             Output("persistent-patterns", "figure"),
             Output("pattern-stats", "children"),
             Output("market-conditions", "children")],
            [Input("refresh-button", "n_clicks")]
        )
        def update_dashboard(n_clicks):
            # Get pattern history
            patterns = self.pattern_recognition.get_pattern_history()
            
            # 1. 3D Pattern Clusters
            clusters_fig = self.create_clusters_3d(patterns)
            
            # 2. Pattern Evolution
            evolution_fig = self.create_pattern_evolution(patterns)
            
            # 3. Pattern Impact
            impact_fig = self.create_pattern_impact(patterns)
            
            # 4. Pattern Distribution
            distribution_fig = self.create_pattern_distribution(patterns)
            
            # 5. Confidence Timeline
            confidence_fig = self.create_confidence_timeline(patterns)
            
            # 6. Persistent Patterns
            persistent_fig = self.create_persistent_patterns(patterns)
            
            # 7. Pattern Statistics
            stats = self.create_pattern_stats(patterns)
            
            # 8. Market Conditions
            market_conditions = self.create_market_conditions(patterns)
            
            return clusters_fig, evolution_fig, impact_fig, distribution_fig, \
                   confidence_fig, persistent_fig, stats, market_conditions
    
    def create_clusters_3d(self, patterns: List[Pattern]) -> go.Figure:
        """Create 3D visualization of pattern clusters."""
        if len(patterns) < 3:
            return go.Figure()
        
        # Extract features and perform PCA
        features = np.array([p.features for p in patterns])
        pca = PCA(n_components=3).fit_transform(features)
        
        # Get cluster labels
        labels = self.pattern_recognition.cluster_patterns(5)
        
        fig = go.Figure(data=[go.Scatter3d(
            x=pca[:, 0],
            y=pca[:, 1],
            z=pca[:, 2],
            mode='markers+text',
            marker=dict(
                size=8,
                color=[self.pattern_recognition.visualization_settings['cluster_colors'][l] for l in labels],
                opacity=0.8
            ),
            text=[f"{p.pattern_type}<br>Conf: {p.confidence:.2f}" for p in patterns],
            textposition="top center",
            name="Pattern Clusters"
        )])
        
        fig.update_layout(
            title="Pattern Clusters in 3D Space",
            scene=dict(
                xaxis_title="First Principal Component",
                yaxis_title="Second Principal Component",
                zaxis_title="Third Principal Component"
            ),
            height=500
        )
        return fig
    
    def create_pattern_evolution(self, patterns: List[Pattern]) -> go.Figure:
        """Create animated visualization of pattern evolution."""
        if len(patterns) < 10:
            return go.Figure()
        
        sorted_patterns = sorted(patterns, key=lambda x: x.timestamp)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[p.timestamp for p in sorted_patterns],
            y=[p.confidence for p in sorted_patterns],
            mode='markers+lines',
            marker=dict(
                size=10,
                color=[self.pattern_recognition.visualization_settings['color_scheme'][p.pattern_type] for p in sorted_patterns]
            ),
            name="Pattern Evolution"
        ))
        
        fig.update_layout(
            title="Pattern Evolution Over Time",
            xaxis_title="Time",
            yaxis_title="Confidence",
            height=400
        )
        return fig
    
    def create_pattern_impact(self, patterns: List[Pattern]) -> go.Figure:
        """Create visualization of market condition impacts."""
        if not patterns:
            return go.Figure()
        
        fig = make_subplots(rows=2, cols=2,
                           specs=[[{"type": "scatter"}, {"type": "scatter"}],
                                 [{"type": "scatter"}, {"type": "scatter"}]])
        
        # Extract market conditions and weights
        market_conditions = []
        weights = []
        for pattern in patterns:
            if 'market_conditions' in pattern.metadata:
                market_conditions.append(pattern.metadata['market_conditions'])
                weights.append({
                    'volume': pattern.metadata.get('volume_weight', 1.0),
                    'fibo': pattern.metadata.get('fibo_weight', 1.0),
                    'volatility': pattern.metadata.get('volatility_weight', 1.0),
                    'time': pattern.metadata.get('time_weight', 1.0)
                })
        
        if not market_conditions:
            return fig
        
        # Add traces for each impact type
        fig.add_trace(
            go.Scatter(
                x=[mc.get('volume', 0) for mc in market_conditions],
                y=[w['volume'] for w in weights],
                mode='markers',
                marker=dict(
                    size=8,
                    color=[self.pattern_recognition.visualization_settings['color_scheme'][p.pattern_type] for p in patterns]
                ),
                name="Volume Impact"
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=[1 if mc.get('near_fibo', False) else 0 for mc in market_conditions],
                y=[w['fibo'] for w in weights],
                mode='markers',
                marker=dict(
                    size=8,
                    color=[self.pattern_recognition.visualization_settings['color_scheme'][p.pattern_type] for p in patterns]
                ),
                name="Fibonacci Impact"
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=[1 if mc.get('high_volatility', False) else 0 for mc in market_conditions],
                y=[w['volatility'] for w in weights],
                mode='markers',
                marker=dict(
                    size=8,
                    color=[self.pattern_recognition.visualization_settings['color_scheme'][p.pattern_type] for p in patterns]
                ),
                name="Volatility Impact"
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=[(datetime.now() - p.timestamp).total_seconds() / 3600 for p in patterns],
                y=[w['time'] for w in weights],
                mode='markers',
                marker=dict(
                    size=8,
                    color=[self.pattern_recognition.visualization_settings['color_scheme'][p.pattern_type] for p in patterns]
                ),
                name="Time Decay"
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=True)
        return fig
    
    def create_pattern_distribution(self, patterns: List[Pattern]) -> go.Figure:
        """Create heatmap of pattern type distribution."""
        if not patterns:
            return go.Figure()
        
        pattern_types = [p.pattern_type for p in patterns]
        labels = self.pattern_recognition.cluster_patterns(5)
        
        heatmap_data = np.zeros((3, 5))
        for pt, cl in zip(pattern_types, labels):
            pt_idx = ['bullish_trap', 'bearish_trap', 'neutral'].index(pt)
            heatmap_data[pt_idx, cl] += 1
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            colorscale='Viridis',
            name="Pattern Distribution"
        ))
        
        fig.update_layout(
            title="Pattern Type Distribution",
            xaxis_title="Cluster",
            yaxis_title="Pattern Type",
            height=400
        )
        return fig
    
    def create_confidence_timeline(self, patterns: List[Pattern]) -> go.Figure:
        """Create timeline of pattern confidences."""
        if not patterns:
            return go.Figure()
        
        fig = go.Figure()
        for pattern_type in ['bullish_trap', 'bearish_trap', 'neutral']:
            type_patterns = [p for p in patterns if p.pattern_type == pattern_type]
            if type_patterns:
                fig.add_trace(go.Scatter(
                    x=[p.timestamp for p in type_patterns],
                    y=[p.confidence for p in type_patterns],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=self.pattern_recognition.visualization_settings['color_scheme'][pattern_type]
                    ),
                    name=pattern_type
                ))
        
        fig.update_layout(
            title="Pattern Confidence Timeline",
            xaxis_title="Time",
            yaxis_title="Confidence",
            height=400
        )
        return fig
    
    def create_persistent_patterns(self, patterns: List[Pattern]) -> go.Figure:
        """Create visualization of persistent patterns."""
        persistent_patterns = [p for p in patterns if p.metadata.get("persistent", False)]
        if not persistent_patterns:
            return go.Figure()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[p.timestamp for p in persistent_patterns],
            y=[p.metadata.get("occurrences", 0) for p in persistent_patterns],
            mode='markers',
            marker=dict(
                size=10,
                color='#ff00ff',
                symbol='star'
            ),
            name="Persistent Patterns"
        ))
        
        fig.update_layout(
            title="Persistent Pattern Occurrences",
            xaxis_title="Time",
            yaxis_title="Occurrences",
            height=400
        )
        return fig
    
    def create_pattern_stats(self, patterns: List[Pattern]) -> html.Div:
        """Create statistics summary for patterns."""
        if not patterns:
            return html.Div("No patterns detected yet.")
        
        # Calculate statistics
        total_patterns = len(patterns)
        pattern_types = [p.pattern_type for p in patterns]
        avg_confidence = np.mean([p.confidence for p in patterns])
        persistent_count = sum(1 for p in patterns if p.metadata.get("persistent", False))
        
        # Create stats display
        return html.Div([
            html.P(f"Total Patterns: {total_patterns}"),
            html.P(f"Average Confidence: {avg_confidence:.2f}"),
            html.P(f"Persistent Patterns: {persistent_count}"),
            html.P("Pattern Types:"),
            html.Ul([
                html.Li(f"{pt}: {pattern_types.count(pt)}")
                for pt in ['bullish_trap', 'bearish_trap', 'neutral']
            ])
        ])
    
    def create_market_conditions(self, patterns: List[Pattern]) -> html.Div:
        """Create summary of market conditions."""
        if not patterns:
            return html.Div("No market conditions data available.")
        
        # Extract market conditions
        conditions = []
        for pattern in patterns:
            if 'market_conditions' in pattern.metadata:
                conditions.append(pattern.metadata['market_conditions'])
        
        if not conditions:
            return html.Div("No market conditions data available.")
        
        # Calculate statistics
        high_vol_count = sum(1 for c in conditions if c.get('high_volatility', False))
        fibo_count = sum(1 for c in conditions if c.get('near_fibo', False))
        avg_volume = np.mean([c.get('volume', 0) for c in conditions])
        
        return html.Div([
            html.P(f"High Volatility Periods: {high_vol_count}"),
            html.P(f"Near Fibonacci Levels: {fibo_count}"),
            html.P(f"Average Volume: {avg_volume:.2f}")
        ])
    
    def run_server(self, debug: bool = True, port: int = 8050):
        """Run the dashboard server."""
        self.app.run(debug=debug, port=port) 