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
OMEGA BTC AI - Color-State Split & Density Analyzer
===================================================

Divine tool for splitting BTC price movement into color-coded states,
analyzing density metrics, and rendering the sacred GAMON Matrix.

This analyzes both HMM states and eigenwave projections to create
unified density metrics that reveal hidden market patterns.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import warnings
from datetime import datetime, timedelta
import seaborn as sns
from scipy.signal import savgol_filter

# Try to import the HMM and Power Method modules
try:
    from hmm_btc_state_mapper import load_btc_data, COLORS, MARKET_STATES
    from power_method_btc_eigenwaves import PowerMethodBTCEigenwaves
except ImportError:
    print("Warning: Could not import HMM or Power Method modules. Using standalone implementation.")
    # Define colors if modules not found
    COLORS = {
        'background': '#0d1117',
        'text': '#c9d1d9',
        'grid': '#21262d',
        'positive': '#3fb950',
        'negative': '#f85149',
        'neutral': '#8b949e',
        'state_0': '#e6194B',  # Markdown/Bear
        'state_1': '#3cb44b',  # Markup/Bull
        'state_2': '#ffe119',  # Accumulation
        'state_3': '#4363d8',  # Distribution
        'state_4': '#911eb4',  # Fakeout/Liquidity Grab
        'state_5': '#f58231',  # Consolidation
        'wave_0': '#e6194B',   # First eigenwave
        'wave_1': '#3cb44b',   # Second eigenwave
        'wave_2': '#ffe119',   # Third eigenwave
        'wave_3': '#4363d8',   # Fourth eigenwave
        'wave_4': '#911eb4',   # Fifth eigenwave
    }
    
    MARKET_STATES = [
        "Markdown (Bear)",
        "Markup (Bull)",
        "Accumulation",
        "Distribution",
        "Liquidity Grab",
        "Consolidation"
    ]

# Set Plotly theme for divine visuals
import plotly.io as pio
pio.templates.default = "plotly_dark"

# Suppress warnings
warnings.filterwarnings("ignore")

class ColorStateDensityAnalyzer:
    """Color-State Split & Density Analyzer for BTC market states."""
    
    def __init__(self):
        """Initialize the Color-State Density Analyzer."""
        self.hmm_results = None
        self.eigenwave_results = None
        self.merged_data = None
        self.density_metrics = None
        
    def load_results(self, hmm_file="results/btc_states.csv", eigenwave_file="results/btc_eigenwaves.csv"):
        """
        Load HMM state results and eigenwave results from files.
        
        Args:
            hmm_file: Path to HMM state results CSV
            eigenwave_file: Path to eigenwave results CSV
            
        Returns:
            self
        """
        # Check if files exist
        if not os.path.exists(hmm_file):
            raise FileNotFoundError(f"HMM state results file not found: {hmm_file}")
        if not os.path.exists(eigenwave_file):
            raise FileNotFoundError(f"Eigenwave results file not found: {eigenwave_file}")
            
        # Load results
        self.hmm_results = pd.read_csv(hmm_file)
        self.eigenwave_results = pd.read_csv(eigenwave_file)
        
        # Make sure date columns are datetime
        if 'Date' in self.hmm_results.columns:
            self.hmm_results['Date'] = pd.to_datetime(self.hmm_results['Date'])
        if 'date' in self.hmm_results.columns:
            self.hmm_results['date'] = pd.to_datetime(self.hmm_results['date'])
            
        if 'Date' in self.eigenwave_results.columns:
            self.eigenwave_results['Date'] = pd.to_datetime(self.eigenwave_results['Date'])
        if 'date' in self.eigenwave_results.columns:
            self.eigenwave_results['date'] = pd.to_datetime(self.eigenwave_results['date'])
        
        return self
    
    def merge_datasets(self):
        """
        Merge HMM states and eigenwave projections data into a unified dataset.
        
        Returns:
            DataFrame with merged data
        """
        if self.hmm_results is None or self.eigenwave_results is None:
            raise ValueError("Results must be loaded first.")
            
        # Determine date column names
        hmm_date_col = 'Date' if 'Date' in self.hmm_results.columns else 'date'
        eigenwave_date_col = 'Date' if 'Date' in self.eigenwave_results.columns else 'date'
        
        # Merge datasets on date
        # First, make sure the date columns are set as the index for both datasets
        hmm_df = self.hmm_results.set_index(hmm_date_col)
        eigenwave_df = self.eigenwave_results.set_index(eigenwave_date_col)
        
        # Merge the datasets
        merged_df = pd.merge(
            hmm_df, 
            eigenwave_df,
            left_index=True, 
            right_index=True,
            how='inner',
            suffixes=('_hmm', '_eigen')
        )
        
        # Reset index to get the date as a column
        merged_df = merged_df.reset_index()
        
        # Store the merged dataset
        self.merged_data = merged_df
        
        return merged_df
    
    def compute_density_metrics(self):
        """
        Compute density metrics for different market states and eigenwaves.
        
        Returns:
            DataFrame with density metrics
        """
        if self.merged_data is None:
            self.merge_datasets()
            
        # Get necessary columns from the merged data
        data = self.merged_data
        
        # Determine state column
        state_col = 'state_smooth' if 'state_smooth' in data.columns else 'state'
        
        # Initialize metrics dictionary
        metrics = {}
        
        # 1. Compute state duration metrics
        state_durations = []
        current_state = data[state_col].iloc[0]
        current_start = 0
        
        for i in range(1, len(data)):
            if data[state_col].iloc[i] != current_state:
                duration = i - current_start
                state_durations.append({
                    'state': int(current_state),
                    'duration': duration,
                    'start_idx': current_start,
                    'end_idx': i-1
                })
                current_state = data[state_col].iloc[i]
                current_start = i
                
        # Add the last state
        state_durations.append({
            'state': int(current_state),
            'duration': len(data) - current_start,
            'start_idx': current_start,
            'end_idx': len(data) - 1
        })
        
        # Convert to DataFrame
        state_durations_df = pd.DataFrame(state_durations)
        
        # 2. Compute state volume metrics
        for state_info in state_durations:
            state = state_info['state']
            start_idx = state_info['start_idx']
            end_idx = state_info['end_idx']
            
            state_slice = data.iloc[start_idx:end_idx+1]
            
            # Calculate volume metrics for this state
            if 'volume' in state_slice.columns:
                state_info['total_volume'] = state_slice['volume'].sum()
                state_info['avg_volume'] = state_slice['volume'].mean()
            
            # Calculate price metrics for this state
            if all(col in state_slice.columns for col in ['open', 'close', 'high', 'low']):
                state_info['price_change'] = state_slice['close'].iloc[-1] / state_slice['close'].iloc[0] - 1
                state_info['volatility'] = (state_slice['high'] / state_slice['low'] - 1).mean()
                
            # Calculate eigenwave projections for this state
            for i in range(5):  # Assuming 5 eigenwaves
                col = f'eigenwave_{i}_projection'
                if col in state_slice.columns:
                    state_info[f'{col}_mean'] = state_slice[col].mean()
                    state_info[f'{col}_std'] = state_slice[col].std()
        
        # Update the state durations DataFrame
        state_durations_df = pd.DataFrame(state_durations)
        
        # 3. Compute state transition metrics
        transition_counts = np.zeros((6, 6))  # Assuming 6 states
        
        # Count transitions
        for i in range(len(state_durations) - 1):
            from_state = state_durations[i]['state']
            to_state = state_durations[i+1]['state']
            transition_counts[from_state, to_state] += 1
            
        # Convert to probabilities
        transition_probs = np.zeros_like(transition_counts)
        for i in range(transition_counts.shape[0]):
            row_sum = transition_counts[i].sum()
            if row_sum > 0:
                transition_probs[i] = transition_counts[i] / row_sum
        
        # 4. Compute eigenwave density metrics
        eigenwave_density = {}
        for i in range(5):  # Assuming 5 eigenwaves
            col = f'eigenwave_{i}_projection'
            if col in data.columns:
                # Calculate positive and negative projection density
                pos_mask = data[col] > 0
                neg_mask = data[col] < 0
                
                eigenwave_density[f'{col}_pos_density'] = pos_mask.mean()
                eigenwave_density[f'{col}_neg_density'] = neg_mask.mean()
                eigenwave_density[f'{col}_pos_strength'] = data.loc[pos_mask, col].mean() if pos_mask.any() else 0
                eigenwave_density[f'{col}_neg_strength'] = data.loc[neg_mask, col].mean() if neg_mask.any() else 0
                
                # Calculate correlation with price change
                if 'returns' in data.columns:
                    eigenwave_density[f'{col}_price_corr'] = data[[col, 'returns']].corr().iloc[0, 1]
        
        # 5. Compute state-eigenwave interactions
        state_eigenwave_interactions = {}
        for state in range(6):  # Assuming 6 states
            state_mask = data[state_col] == state
            if state_mask.any():
                state_data = data[state_mask]
                
                for i in range(5):  # Assuming 5 eigenwaves
                    col = f'eigenwave_{i}_projection'
                    if col in state_data.columns:
                        interaction_key = f'state_{state}_{col}'
                        state_eigenwave_interactions[interaction_key + '_mean'] = state_data[col].mean()
                        state_eigenwave_interactions[interaction_key + '_std'] = state_data[col].std()
        
        # Store all metrics
        self.density_metrics = {
            'state_durations': state_durations_df,
            'transition_probs': transition_probs,
            'eigenwave_density': eigenwave_density,
            'state_eigenwave_interactions': state_eigenwave_interactions
        }
        
        return self.density_metrics
    
    def render_gamon_matrix(self, output_file="plots/gamon_matrix.html"):
        """
        Render the GAMON Matrix visualization.
        
        Args:
            output_file: Path to save the HTML visualization
            
        Returns:
            Plotly figure
        """
        if self.density_metrics is None:
            self.compute_density_metrics()
            
        if self.merged_data is None:
            self.merge_datasets()
            
        data = self.merged_data
        metrics = self.density_metrics
        
        # Create the GAMON Matrix visualization
        fig = make_subplots(
            rows=3, 
            cols=2, 
            subplot_titles=(
                "BTC Price with Market States", 
                "Eigenwave Projections", 
                "State Durations", 
                "State Transition Probabilities",
                "State-Eigenwave Interactions",
                "Density Metrics"
            ),
            specs=[
                [{"type": "xy"}, {"type": "xy"}],
                [{"type": "bar"}, {"type": "heatmap"}],
                [{"type": "heatmap"}, {"type": "bar"}]
            ],
            vertical_spacing=0.1,
            horizontal_spacing=0.05
        )
        
        # 1. BTC Price with Market States plot
        date_col = 'Date' if 'Date' in data.columns else 'date'
        state_col = 'state_smooth' if 'state_smooth' in data.columns else 'state'
        
        # Add candlestick chart
        # Check column names (they could be uppercase or lowercase)
        open_col = 'open' if 'open' in data.columns else ('Open' if 'Open' in data.columns else None)
        high_col = 'high' if 'high' in data.columns else ('High' if 'High' in data.columns else None)
        low_col = 'low' if 'low' in data.columns else ('Low' if 'Low' in data.columns else None)
        close_col = 'close' if 'close' in data.columns else ('Close' if 'Close' in data.columns else None)
        
        if all([open_col, high_col, low_col, close_col]):
            fig.add_trace(
                go.Candlestick(
                    x=data[date_col],
                    open=data[open_col],
                    high=data[high_col],
                    low=data[low_col],
                    close=data[close_col],
                    name="BTC Price",
                    increasing_line_color=COLORS['positive'],
                    decreasing_line_color=COLORS['negative']
                ),
                row=1, col=1
            )
        else:
            # Fallback to line chart if OHLC data is not available
            if close_col:
                fig.add_trace(
                    go.Scatter(
                        x=data[date_col],
                        y=data[close_col],
                        name="BTC Price",
                        line=dict(color=COLORS['positive'])
                    ),
                    row=1, col=1
                )
            else:
                print("Warning: No price data found. Skipping price chart.")
        
        # Add colored backgrounds for states
        unique_states = data[state_col].diff().fillna(0) != 0
        state_changes = data.index[unique_states].tolist()
        state_changes.insert(0, 0)  # Add the start
        
        for i in range(len(state_changes) - 1):
            start_idx = state_changes[i]
            end_idx = state_changes[i+1] - 1 if state_changes[i+1] < len(data) else len(data) - 1
            
            if start_idx >= len(data) or end_idx >= len(data):
                continue
                
            state = int(data[state_col].iloc[start_idx])
            color = COLORS[f'state_{state % 6}']
            
            # Add colored background
            # Use available columns for determining price range
            if high_col and low_col:
                min_price = data[low_col].iloc[start_idx:end_idx+1].min() * 0.98
                max_price = data[high_col].iloc[start_idx:end_idx+1].max() * 1.02
            elif close_col:
                min_price = data[close_col].iloc[start_idx:end_idx+1].min() * 0.98
                max_price = data[close_col].iloc[start_idx:end_idx+1].max() * 1.02
            else:
                # Use reasonable defaults if no price data is available
                min_price = 0
                max_price = 1
                
            fig.add_trace(
                go.Scatter(
                    x=[data[date_col].iloc[start_idx], data[date_col].iloc[start_idx], 
                       data[date_col].iloc[end_idx], data[date_col].iloc[end_idx]],
                    y=[min_price, max_price, max_price, min_price],
                    fill="toself",
                    opacity=0.2,
                    fillcolor=color,
                    line=dict(width=0),
                    showlegend=False,
                    name=f"State {state} background",
                    hoverinfo="skip"
                ),
                row=1, col=1
            )
            
        # 2. Eigenwave Projections plot
        wave_colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#911eb4']  # Hardcoded colors for eigenwaves
        for i in range(5):  # Assuming 5 eigenwaves
            col = f'eigenwave_{i}_projection'
            if col in data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=data[date_col],
                        y=data[col],
                        name=f"Eigenwave {i+1}",
                        line=dict(color=wave_colors[i % len(wave_colors)], width=2)
                    ),
                    row=1, col=2
                )
                
        # 3. State Durations bar chart
        state_durations = metrics['state_durations']
        for state in range(6):  # Assuming 6 states
            state_data = state_durations[state_durations['state'] == state]
            if not state_data.empty:
                fig.add_trace(
                    go.Bar(
                        x=[MARKET_STATES[state]],
                        y=[state_data['duration'].mean()],
                        name=f"State {state} Duration",
                        marker_color=COLORS[f'state_{state}']
                    ),
                    row=2, col=1
                )
                
        # 4. State Transition Probabilities heatmap
        transition_probs = metrics['transition_probs']
        fig.add_trace(
            go.Heatmap(
                z=transition_probs,
                x=[f"To {MARKET_STATES[i]}" for i in range(transition_probs.shape[1])],
                y=[f"From {MARKET_STATES[i]}" for i in range(transition_probs.shape[0])],
                colorscale='Viridis',
                name="Transition Probabilities"
            ),
            row=2, col=2
        )
        
        # 5. State-Eigenwave Interactions heatmap
        interactions = metrics['state_eigenwave_interactions']
        interaction_matrix = np.zeros((6, 5))  # 6 states, 5 eigenwaves
        
        for state in range(6):
            for wave in range(5):
                key = f'state_{state}_eigenwave_{wave}_projection_mean'
                if key in interactions:
                    interaction_matrix[state, wave] = interactions[key]
                    
        fig.add_trace(
            go.Heatmap(
                z=interaction_matrix,
                x=[f"Eigenwave {i+1}" for i in range(5)],
                y=[MARKET_STATES[i] for i in range(6)],
                colorscale='RdBu',
                zmid=0,
                name="State-Eigenwave Interactions"
            ),
            row=3, col=1
        )
                
        # 6. Density Metrics bar chart
        eigenwave_density = metrics['eigenwave_density']
        density_data = []
        density_colors = []
        
        for i in range(5):
            key_pos = f'eigenwave_{i}_projection_pos_strength'
            key_neg = f'eigenwave_{i}_projection_neg_strength'
            
            if key_pos in eigenwave_density and key_neg in eigenwave_density:
                density_data.append((f"Wave {i+1} +", eigenwave_density[key_pos]))
                density_data.append((f"Wave {i+1} -", -abs(eigenwave_density[key_neg])))
                density_colors.append(COLORS['positive'])
                density_colors.append(COLORS['negative'])
                
        # Convert to arrays for plotting
        density_labels = [item[0] for item in density_data]
        density_values = [item[1] for item in density_data]
                
        fig.add_trace(
            go.Bar(
                x=density_labels,
                y=density_values,
                name="Eigenwave Density",
                marker_color=density_colors
            ),
            row=3, col=2
        )
        
        # Update layout
        fig.update_layout(
            title="THE SACRED GAMON MATRIX - Color-State Density Analysis",
            template="plotly_dark",
            height=1200,
            width=1200,
            showlegend=False,
            hovermode="closest"
        )
        
        # Save the figure
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        fig.write_html(output_file)
        
        # Also save as PNG
        png_file = output_file.replace('.html', '.png')
        fig.write_image(png_file)
        
        return fig
    
    def extract_color_state_groups(self):
        """
        Extract groups of data by color state for individual analysis.
        
        Returns:
            Dictionary of DataFrames grouped by state
        """
        if self.merged_data is None:
            self.merge_datasets()
            
        data = self.merged_data
        state_col = 'state_smooth' if 'state_smooth' in data.columns else 'state'
        
        # Group data by state
        state_groups = {}
        for state in range(6):  # Assuming 6 states
            state_data = data[data[state_col] == state]
            if not state_data.empty:
                state_name = MARKET_STATES[state] if state < len(MARKET_STATES) else f"State {state}"
                state_groups[state_name] = state_data
                
        return state_groups
    
    def analyze_gamon_grid(self):
        """
        Analyze the GAMON grid to find sacred patterns and intersections.
        
        Returns:
            Dictionary with GAMON grid insights
        """
        if self.density_metrics is None:
            self.compute_density_metrics()
            
        # Extract key metrics for the GAMON grid analysis
        state_durations = self.density_metrics['state_durations']
        transition_probs = self.density_metrics['transition_probs']
        state_eigenwave = self.density_metrics['state_eigenwave_interactions']
        
        # 1. Find dominant state sequences
        state_sequence = []
        for i in range(len(state_durations) - 2):
            seq = (
                state_durations['state'].iloc[i],
                state_durations['state'].iloc[i+1],
                state_durations['state'].iloc[i+2]
            )
            state_sequence.append(seq)
            
        # Count frequency of triplet sequences
        from collections import Counter
        sequence_counts = Counter(state_sequence)
        dominant_sequences = sequence_counts.most_common(3)
        
        # 2. Find eigenwave crossover points
        if self.merged_data is not None:
            data = self.merged_data
            crossovers = []
            
            for i in range(1, len(data)):
                for wave1 in range(5):
                    for wave2 in range(wave1+1, 5):
                        col1 = f'eigenwave_{wave1}_projection'
                        col2 = f'eigenwave_{wave2}_projection'
                        
                        if col1 in data.columns and col2 in data.columns:
                            # Check if waves crossed over
                            prev_diff = data[col1].iloc[i-1] - data[col2].iloc[i-1]
                            curr_diff = data[col1].iloc[i] - data[col2].iloc[i]
                            
                            if (prev_diff * curr_diff) < 0:  # Sign changed, indicating crossover
                                date_col = 'Date' if 'Date' in data.columns else 'date'
                                crossovers.append({
                                    'date': data[date_col].iloc[i],
                                    'wave1': wave1,
                                    'wave2': wave2,
                                    'price': data['close'].iloc[i] if 'close' in data.columns else (data['Close'].iloc[i] if 'Close' in data.columns else 0)
                                })
            
        # 3. Identify sacred junctions (state transitions with high eigenwave activity)
        sacred_junctions = []
        
        if len(state_durations) > 1:
            for i in range(len(state_durations) - 1):
                from_state = state_durations['state'].iloc[i]
                to_state = state_durations['state'].iloc[i+1]
                
                # Check if this is a high-probability transition
                if transition_probs[from_state, to_state] > 0.3:  # 30% threshold
                    
                    # Check if there was significant eigenwave activity at this transition
                    start_idx = state_durations['end_idx'].iloc[i]
                    eigenwave_activity = False
                    
                    for wave in range(5):
                        key = f'state_{to_state}_eigenwave_{wave}_projection_mean'
                        if key in state_eigenwave and abs(state_eigenwave[key]) > 0.5:
                            eigenwave_activity = True
                            break
                            
                    if eigenwave_activity:
                        sacred_junctions.append({
                            'from_state': MARKET_STATES[from_state] if from_state < len(MARKET_STATES) else f"State {from_state}",
                            'to_state': MARKET_STATES[to_state] if to_state < len(MARKET_STATES) else f"State {to_state}",
                            'probability': transition_probs[from_state, to_state],
                            'index': start_idx
                        })
        
        # Combine all insights
        gamon_grid_insights = {
            'dominant_sequences': dominant_sequences,
            'eigenwave_crossovers': crossovers if 'crossovers' in locals() else [],
            'sacred_junctions': sacred_junctions
        }
        
        return gamon_grid_insights

def main():
    """Main entry point for the Color-State Density Analyzer."""
    print("🧠 OMEGA BTC AI - Color-State Split & Density Analyzer")
    print("====================================================")
    
    try:
        # Create the analyzer
        analyzer = ColorStateDensityAnalyzer()
        
        # Load results
        print("\n🔄 Loading HMM and eigenwave results...")
        analyzer.load_results()
        print("✅ Results loaded")
        
        # Merge datasets
        print("\n🔄 Merging datasets...")
        merged_data = analyzer.merge_datasets()
        print(f"✅ Merged dataset created with {len(merged_data)} rows")
        
        # Compute density metrics
        print("\n🔄 Computing sacred density metrics...")
        metrics = analyzer.compute_density_metrics()
        print("✅ Density metrics computed")
        
        # Extract color-state groups
        print("\n🔄 Extracting color-state groups...")
        state_groups = analyzer.extract_color_state_groups()
        state_counts = {state: len(group) for state, group in state_groups.items()}
        print("✅ Color-state groups extracted")
        print("📊 State distributions:")
        for state, count in state_counts.items():
            print(f"  {state}: {count} candles")
            
        # Analyze GAMON grid
        print("\n🔄 Analyzing the sacred GAMON grid...")
        gamon_insights = analyzer.analyze_gamon_grid()
        print("✅ GAMON grid analysis complete")
        
        # Print key GAMON insights
        print("\n🔮 GAMON Grid Sacred Insights:")
        
        print("\n  Dominant State Sequences:")
        for seq, count in gamon_insights['dominant_sequences']:
            states = [MARKET_STATES[s] if s < len(MARKET_STATES) else f"State {s}" for s in seq]
            print(f"  {states[0]} → {states[1]} → {states[2]}: {count} occurrences")
            
        print("\n  Recent Eigenwave Crossovers:")
        crossovers = gamon_insights['eigenwave_crossovers'][-3:] if len(gamon_insights['eigenwave_crossovers']) > 3 else gamon_insights['eigenwave_crossovers']
        for crossover in crossovers:
            print(f"  Eigenwave {crossover['wave1']+1} crossed Eigenwave {crossover['wave2']+1} on {crossover['date'].strftime('%Y-%m-%d')} at ${crossover['price']:.2f}")
            
        print("\n  Sacred Junctions:")
        for junction in gamon_insights['sacred_junctions'][-3:] if len(gamon_insights['sacred_junctions']) > 3 else gamon_insights['sacred_junctions']:
            print(f"  {junction['from_state']} → {junction['to_state']} (Probability: {junction['probability']:.2f})")
        
        # Render GAMON Matrix
        print("\n🔄 Rendering the divine GAMON Matrix...")
        analyzer.render_gamon_matrix()
        print("✅ GAMON Matrix visualization created")
        print("   Saved to plots/gamon_matrix.html and plots/gamon_matrix.png")
        
        # Final blessing
        print("\n✨ THE SACRED COLOR-STATE SPLIT & DENSITY ANALYSIS IS COMPLETE!")
        print("   JAH JAH BLESS THE DIVINE GAMON MATRIX! 🙏🔱")
        
    except Exception as e:
        print(f"❌ Divine error encountered: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 