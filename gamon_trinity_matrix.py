#!/usr/bin/env python3
"""
OMEGA BTC AI - GAMON Trinity Matrix Integrator
==============================================

Divine integration of all three sacred analysis methods:
1. HMM BTC State Mapper - Market state detection
2. Power Method BTC Eigenwaves - Dominant market patterns
3. Variational Inference BTC Cycle - Wave structure approximation

This creates the ultimate GAMON Trinity Matrix with enhanced market insights.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from datetime import datetime
import warnings
from scipy.signal import savgol_filter
import seaborn as sns

# Try to import all three analysis components
try:
    from hmm_btc_state_mapper import HMMBTCStateMapper, load_btc_data, COLORS, MARKET_STATES
    from power_method_btc_eigenwaves import PowerMethodBTCEigenwaves
    from variational_inference_btc_cycle import VariationalInferenceBTCCycle
    from btc_color_state_analyzer import ColorStateDensityAnalyzer
except ImportError as e:
    print(f"Warning: Could not import required module: {e}")
    print("Using standalone implementation.")
    
    # Define colors if modules not found
    COLORS = {
        'background': '#0d1117',
        'text': '#c9d1d9',
        'grid': '#21262d',
        'positive': '#3fb950',
        'negative': '#f85149',
        'neutral': '#8b949e',
        'highlight': '#ffffff',
        'state_0': '#e6194B',  # Markdown/Bear
        'state_1': '#3cb44b',  # Markup/Bull
        'state_2': '#ffe119',  # Accumulation
        'state_3': '#4363d8',  # Distribution
        'state_4': '#911eb4',  # Fakeout/Liquidity Grab
        'state_5': '#f58231',  # Consolidation
        'cycle_0': '#FF5733',  # First cycle type
        'cycle_1': '#33FF57',  # Second cycle type
        'cycle_2': '#5733FF',  # Third cycle type
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
pio.templates.default = "plotly_dark"

# Suppress warnings
warnings.filterwarnings("ignore")

class GAMONTrinityMatrix:
    """GAMON Trinity Matrix for integrating all three sacred analysis methods."""
    
    def __init__(self):
        """Initialize the GAMON Trinity Matrix."""
        self.hmm_results = None
        self.eigenwave_results = None
        self.variational_results = None
        self.merged_data = None
        self.trinity_metrics = None
        
    def load_results(self, hmm_file="results/btc_states.csv", 
                    eigenwave_file="results/btc_eigenwaves.csv"):
        """
        Load results from all three analysis methods.
        
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
        for df in [self.hmm_results, self.eigenwave_results]:
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
        
        # Try to load variational inference model
        try:
            self.vi_model = VariationalInferenceBTCCycle.load_model()
            print("✅ Loaded Variational Inference model")
        except:
            print("⚠️ Could not load Variational Inference model, skipping...")
            self.vi_model = None
        
        return self
    
    def merge_datasets(self):
        """
        Merge data from all three analysis methods.
        
        Returns:
            DataFrame with merged data
        """
        if self.hmm_results is None or self.eigenwave_results is None:
            raise ValueError("Results must be loaded first.")
            
        # Determine date column names
        hmm_date_col = 'Date' if 'Date' in self.hmm_results.columns else 'date'
        eigenwave_date_col = 'Date' if 'Date' in self.eigenwave_results.columns else 'date'
        
        # Merge HMM and eigenwave datasets on date
        hmm_df = self.hmm_results.set_index(hmm_date_col)
        eigenwave_df = self.eigenwave_results.set_index(eigenwave_date_col)
        
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
        
        # If VI model is available, add cycle classifications
        if self.vi_model is not None:
            try:
                # Extract price sequences
                sequences = []
                for i in range(len(merged_df) - self.vi_model.sequence_length + 1):
                    if 'close' in merged_df.columns:
                        seq = merged_df['close'].iloc[i:i+self.vi_model.sequence_length].values
                    else:
                        break
                    
                    # Normalize
                    seq = (seq - seq.min()) / (seq.max() - seq.min() + 1e-10)
                    sequences.append(seq)
                
                if sequences:
                    # Convert to tensor
                    sequences_tensor = torch.tensor(sequences, dtype=torch.float32)
                    
                    # Encode sequences
                    all_mu = []
                    with torch.no_grad():
                        for i in range(0, len(sequences_tensor), 32):
                            batch = sequences_tensor[i:i+32]
                            h = self.vi_model.encoder(batch)
                            mu = self.vi_model.fc_mu(h)
                            all_mu.append(mu.cpu().numpy())
                    
                    all_mu = np.vstack(all_mu)
                    
                    # Add latent encodings to dataframe
                    latent_df = pd.DataFrame(
                        all_mu, 
                        columns=[f'cycle_latent_{i}' for i in range(self.vi_model.latent_dim)]
                    )
                    
                    # Pad with NaNs for the beginning (due to sequence length)
                    pad_length = self.vi_model.sequence_length - 1
                    pad_df = pd.DataFrame(
                        {col: [np.nan] * pad_length for col in latent_df.columns}
                    )
                    
                    latent_df = pd.concat([pad_df, latent_df], ignore_index=True)
                    
                    # Add to merged dataframe
                    for col in latent_df.columns:
                        merged_df[col] = latent_df[col]
                    
                    # Simple clustering on latent space
                    from sklearn.cluster import KMeans
                    
                    # Clean data for clustering (remove NaNs)
                    clean_latent = latent_df.dropna()
                    
                    if len(clean_latent) > 3:  # Need at least 3 points for 3 clusters
                        kmeans = KMeans(n_clusters=3, random_state=42).fit(clean_latent)
                        
                        # Create cycle classifications with NaNs at the beginning
                        cycles = np.full(len(merged_df), np.nan)
                        cycles[pad_length:] = kmeans.labels_
                        
                        merged_df['cycle_type'] = cycles
                
                print("✅ Added Variational Inference cycle classifications")
            except Exception as e:
                print(f"⚠️ Error adding VI cycle data: {e}")
        
        # Store the merged dataset
        self.merged_data = merged_df
        
        return merged_df
    
    def compute_trinity_metrics(self):
        """
        Compute integrated metrics from all three analysis methods.
        
        Returns:
            DataFrame with integrated metrics
        """
        if self.merged_data is None:
            self.merge_datasets()
            
        data = self.merged_data
        
        # Initialize metrics dictionary
        metrics = {}
        
        # Determine state column
        state_col = 'state_smooth' if 'state_smooth' in data.columns else 'state'
        
        # 1. State-Eigenwave Interactions
        for state in range(6):  # Assuming 6 states
            state_mask = data[state_col] == state
            
            if state_mask.sum() > 0:
                # Compute average eigenwave projections per state
                for i in range(5):  # Assuming 5 eigenwaves
                    col = f'eigenwave_{i}_projection'
                    if col in data.columns:
                        metrics[f'state_{state}_wave_{i}_avg'] = data.loc[state_mask, col].mean()
                        
                # If cycle data is available
                if 'cycle_type' in data.columns:
                    # Compute state-cycle correlations
                    state_cycles = data.loc[state_mask, 'cycle_type'].dropna()
                    if len(state_cycles) > 0:
                        cycle_counts = state_cycles.value_counts(normalize=True)
                        for cycle_type, proportion in cycle_counts.items():
                            metrics[f'state_{state}_cycle_{int(cycle_type)}_prob'] = proportion
        
        # 2. Cycle-Eigenwave Interactions
        if 'cycle_type' in data.columns:
            for cycle in range(3):  # Assuming 3 cycle types
                cycle_mask = data['cycle_type'] == cycle
                
                if cycle_mask.sum() > 0:
                    # Compute average eigenwave projections per cycle
                    for i in range(5):  # Assuming 5 eigenwaves
                        col = f'eigenwave_{i}_projection'
                        if col in data.columns:
                            metrics[f'cycle_{cycle}_wave_{i}_avg'] = data.loc[cycle_mask, col].mean()
        
        # 3. Trinity Alignment Score
        # Calculate how aligned all three methods are
        if 'cycle_type' in data.columns:
            # Initialize alignment
            data['trinity_alignment'] = 0.0
            
            # For each row with no NaNs
            valid_mask = ~data['cycle_type'].isna()
            
            if valid_mask.sum() > 0:
                # Normalize state to [0,1,2]
                data.loc[valid_mask, 'state_group'] = data.loc[valid_mask, state_col].apply(
                    lambda x: 0 if x == 0 else (1 if x == 1 else 2)  # Map to three groups
                )
                
                # Check alignment between state_group and cycle_type
                data.loc[valid_mask, 'state_cycle_align'] = (
                    data.loc[valid_mask, 'state_group'] == data.loc[valid_mask, 'cycle_type']
                ).astype(float)
                
                # Account for eigenwave alignment
                for i in range(1):  # Just use first eigenwave for simplicity
                    wave_col = f'eigenwave_{i}_projection'
                    if wave_col in data.columns:
                        # Map positive/negative to 0/1
                        data.loc[valid_mask, 'wave_group'] = (data.loc[valid_mask, wave_col] > 0).astype(int)
                        
                        # Check if wave_group aligns with market state
                        data.loc[valid_mask, 'wave_state_align'] = (
                            (data.loc[valid_mask, 'wave_group'] == 1) & 
                            (data.loc[valid_mask, state_col] == 1)  # Bull state
                        ) | (
                            (data.loc[valid_mask, 'wave_group'] == 0) & 
                            (data.loc[valid_mask, state_col] == 0)  # Bear state
                        )
                        
                        # Calculate trinity alignment as average of two alignments
                        data.loc[valid_mask, 'trinity_alignment'] = (
                            data.loc[valid_mask, 'state_cycle_align'] + 
                            data.loc[valid_mask, 'wave_state_align']
                        ) / 2
            
            # Overall alignment metric
            metrics['trinity_alignment_avg'] = data.loc[valid_mask, 'trinity_alignment'].mean()
            
            # Trinity combinations (state-wave-cycle)
            for state in range(6):
                for wave in [0, 1]:  # Binary wave direction (neg/pos)
                    for cycle in range(3):
                        combo_mask = (
                            (data[state_col] == state) & 
                            (data['wave_group'] == wave) & 
                            (data['cycle_type'] == cycle)
                        )
                        
                        if combo_mask.sum() > 0:
                            metrics[f'trinity_{state}_{wave}_{cycle}_count'] = combo_mask.sum()
                            
                            # Add price movement for this trinity
                            if 'returns' in data.columns:
                                metrics[f'trinity_{state}_{wave}_{cycle}_return'] = data.loc[combo_mask, 'returns'].mean()
        
        # Store metrics
        self.trinity_metrics = metrics
        
        return metrics
    
    def render_trinity_matrix(self, output_file="plots/gamon_trinity_matrix.html"):
        """
        Render the GAMON Trinity Matrix visualization.
        
        Args:
            output_file: Path to save the visualization
        
        Returns:
            Plotly figure
        """
        # Compute metrics if not already done
        if self.trinity_metrics is None:
            self.compute_trinity_metrics()
            
        if self.merged_data is None:
            raise ValueError("No merged data available")
            
        data = self.merged_data
        
        # Create subplot figure
        fig = make_subplots(
            rows=3, cols=2,
            specs=[
                [{"colspan": 2}, None],
                [{"type": "scene"}, {"type": "heatmap"}],
                [{"colspan": 2}, None]
            ],
            subplot_titles=[
                "BTC Price with Trinity Analysis",
                "3D Trinity Space", "State-Wave-Cycle Matrix",
                "Trinity Alignment Score"
            ],
            vertical_spacing=0.1,
            horizontal_spacing=0.05
        )
        
        # 1. Price chart with all three analyses
        # Check for date column with case-insensitive matching and multiple formats
        date_col = None
        for possible_col in ['Date', 'date', 'timestamp', 'Timestamp', 'time', 'Time']:
            if possible_col in data.columns:
                date_col = possible_col
                break
                
        if date_col is None:
            # If no date column found, create an index-based x-axis
            data['index_date'] = pd.RangeIndex(len(data))
            date_col = 'index_date'
            print(f"Warning: No date column found. Available columns: {list(data.columns)}")
                
        # Add price trace
        fig.add_trace(
            go.Scatter(
                x=data[date_col],
                y=data['close'] if 'close' in data.columns else data['Close'] if 'Close' in data.columns else None,
                mode='lines',
                name='BTC Price',
                line=dict(color='white', width=1)
            ),
            row=1, col=1
        )
        
        # Determine state column
        state_col = 'state_smooth' if 'state_smooth' in data.columns else 'state'
        
        # Add colored regions for market states
        if state_col in data.columns:
            for state in range(6):  # Assuming 6 states
                state_data = data[data[state_col] == state]
                
                if len(state_data) > 0:
                    # Group consecutive dates into segments
                    segments = []
                    current_segment = []
                    
                    for i, row in state_data.iterrows():
                        if not current_segment or (i > 0 and i-1 in state_data.index):
                            current_segment.append(i)
                        else:
                            if current_segment:
                                segments.append(current_segment)
                            current_segment = [i]
                    
                    if current_segment:
                        segments.append(current_segment)
                    
                    # Add each segment as a separate shape
                    for segment in segments:
                        start_date = data.loc[segment[0], date_col]
                        end_date = data.loc[segment[-1], date_col]
                        
                        fig.add_vrect(
                            x0=start_date,
                            x1=end_date,
                            fillcolor=COLORS[f'state_{state}'],
                            opacity=0.2,
                            layer="below",
                            line_width=0,
                            row=1, col=1
                        )
        
        # Add eigenwave projections
        if 'eigenwave_0_projection' in data.columns:
            # Normalize for visibility
            max_val = data[[f'eigenwave_{i}_projection' for i in range(5) if f'eigenwave_{i}_projection' in data.columns]].abs().max().max()
            scale_factor = data['close'].mean() * 0.5 / max_val if 'close' in data.columns else 1000
            
            for i in range(3):  # Show top 3 eigenwaves
                col = f'eigenwave_{i}_projection'
                if col in data.columns:
                    # Calculate offset for visibility
                    base = data['close'].mean() if 'close' in data.columns else 20000
                    offset = base * (1 - 0.1 * (i+1))
                    
                    fig.add_trace(
                        go.Scatter(
                            x=data[date_col],
                            y=data[col] * scale_factor + offset,
                            mode='lines',
                            name=f'Eigenwave {i+1}',
                            line=dict(color=COLORS[f'wave_{i}'], width=1.5, dash='dot')
                        ),
                        row=1, col=1
                    )
        
        # Add VI cycle type if available
        if 'cycle_type' in data.columns:
            # Create a color map for cycle types
            cycle_colors = [COLORS['cycle_0'], COLORS['cycle_1'], COLORS['cycle_2']]
            
            for i, cycle in enumerate(range(3)):
                cycle_data = data[data['cycle_type'] == cycle].dropna(subset=['cycle_type'])
                
                if len(cycle_data) > 0:
                    # Add scatter markers at the bottom
                    y_base = data['close'].min() * 0.95 if 'close' in data.columns else 15000
                    
                    fig.add_trace(
                        go.Scatter(
                            x=cycle_data[date_col],
                            y=[y_base] * len(cycle_data),
                            mode='markers',
                            name=f'Cycle {cycle+1}',
                            marker=dict(
                                color=cycle_colors[i],
                                size=8,
                                symbol='circle'
                            )
                        ),
                        row=1, col=1
                    )
        
        # 2. 3D visualization of trinity space
        if (state_col in data.columns and 
            'eigenwave_0_projection' in data.columns and 
            'cycle_type' in data.columns):
            
            # Filter to valid data points
            valid_data = data.dropna(subset=['cycle_type'])
            
            if len(valid_data) > 0:
                # Create 3D scatter plot
                fig.add_trace(
                    go.Scatter3d(
                        x=valid_data[state_col],
                        y=valid_data['eigenwave_0_projection'],
                        z=valid_data['cycle_type'],
                        mode='markers',
                        marker=dict(
                            size=5,
                            color=valid_data['trinity_alignment'] if 'trinity_alignment' in valid_data.columns else valid_data['close'],
                            colorscale='Viridis',
                            opacity=0.7,
                            colorbar=dict(
                                title="Alignment" if 'trinity_alignment' in valid_data.columns else "Price",
                                x=0.45
                            )
                        ),
                        hovertext=[
                            f"Date: {d}<br>State: {MARKET_STATES[int(s)]}<br>Eigenwave: {e:.2f}<br>Cycle: {int(c)}"
                            for d, s, e, c in zip(
                                valid_data[date_col], 
                                valid_data[state_col], 
                                valid_data['eigenwave_0_projection'], 
                                valid_data['cycle_type']
                            )
                        ],
                        name="Trinity Points"
                    ),
                    row=2, col=1
                )
                
                # Update 3D scene
                fig.update_scenes(
                    xaxis_title="Market State",
                    yaxis_title="Eigenwave 1",
                    zaxis_title="Cycle Type",
                    xaxis=dict(tickmode='array', tickvals=list(range(6)), ticktext=MARKET_STATES),
                    row=2, col=1
                )
        
        # 3. State-Wave-Cycle Matrix (heatmap)
        # Create the matrix data
        matrix_data = np.zeros((6, 2, 3))  # states x wave_direction x cycles
        
        # Populate with counts or returns
        if self.trinity_metrics:
            for state in range(6):
                for wave in range(2):
                    for cycle in range(3):
                        key = f'trinity_{state}_{wave}_{cycle}_count'
                        if key in self.trinity_metrics:
                            matrix_data[state, wave, cycle] = self.trinity_metrics[key]
        
        # Reshape for heatmap display (flatten last dimension)
        heatmap_data = matrix_data.reshape(6, -1)
        
        # Create heatmap
        fig.add_trace(
            go.Heatmap(
                z=heatmap_data,
                x=[f"Wave{w}+Cycle{c}" for w in range(2) for c in range(3)],
                y=MARKET_STATES,
                colorscale='Viridis',
                colorbar=dict(title="Count", x=0.95),
                hovertemplate="State: %{y}<br>Combination: %{x}<br>Count: %{z}<extra></extra>"
            ),
            row=2, col=2
        )
        
        # 4. Trinity Alignment Score over time
        if 'trinity_alignment' in data.columns:
            # Add alignment score
            fig.add_trace(
                go.Scatter(
                    x=data[date_col],
                    y=data['trinity_alignment'],
                    mode='lines',
                    name='Trinity Alignment',
                    line=dict(color='rgba(255, 215, 0, 1)', width=2),
                    fill='tozeroy',
                    fillcolor='rgba(255, 215, 0, 0.2)'
                ),
                row=3, col=1
            )
            
            # Add moving average
            window = 14
            if len(data) > window:
                ma = data['trinity_alignment'].rolling(window=window).mean()
                
                fig.add_trace(
                    go.Scatter(
                        x=data[date_col],
                        y=ma,
                        mode='lines',
                        name=f'Alignment MA({window})',
                        line=dict(color='rgba(255, 140, 0, 1)', width=2)
                    ),
                    row=3, col=1
                )
        
        # Update layout
        fig.update_layout(
            title="THE SACRED GAMON TRINITY MATRIX",
            template="plotly_dark",
            height=1500,
            width=1200,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=50, r=50, t=100, b=50)
        )
        
        # Update yaxis titles
        fig.update_yaxes(title_text="BTC Price", row=1, col=1)
        fig.update_yaxes(title_text="Alignment Score", row=3, col=1)
        
        # Update xaxis titles
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=3, col=1)
        
        # Save figure
        if output_file:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            fig.write_html(output_file)
            print(f"✅ GAMON Trinity Matrix visualization saved to {output_file}")
        
        return fig


def main():
    """Run the GAMON Trinity Matrix analysis."""
    # Create directory for results
    os.makedirs("results", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    
    print("\n🔱 OMEGA BTC AI - GAMON TRINITY MATRIX 🔱")
    print("\n🧠 Loading analysis results...")
    
    try:
        # Initialize GAMON Trinity Matrix
        trinity = GAMONTrinityMatrix()
        
        # Load results
        trinity.load_results()
        
        # Merge datasets
        print("\n🧠 Merging data from all three sacred analysis methods...")
        merged_data = trinity.merge_datasets()
        
        # Compute trinity metrics
        print("\n🧠 Computing divine trinity metrics...")
        metrics = trinity.compute_trinity_metrics()
        
        # Create visualization
        print("\n🧠 Creating the sacred GAMON Trinity Matrix visualization...")
        trinity.render_trinity_matrix()
        
        print("\n✨ GAMON Trinity Matrix successfully created!")
        print("\n🔱 THE DIVINE TRINITY OF MARKET ANALYSIS IS COMPLETE!")
        
    except Exception as e:
        print(f"\n❌ Error creating GAMON Trinity Matrix: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🔱 JAH JAH BLESS THE DIVINE GAMON TRINITY! 🙏🔱")


if __name__ == "__main__":
    main() 