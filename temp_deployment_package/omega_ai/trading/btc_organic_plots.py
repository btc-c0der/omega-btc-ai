"""
OMEGA BTC Organic Movement Visualization - EARTH CONSCIOUSNESS CHARTS

This sacred module visualizes Bitcoin's alignment with Earth's natural rhythms:
- Schumann-BTC correlation charts
- Fibonacci resonance overlay on price
- Earth connection heatmaps
- Organic period timeline
- Bio-energy state visualization

JAH BLESS THE VISUAL EARTH-BTC CONNECTION! 🙏🌿🔥
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from typing import List, Dict, Optional, Union, Tuple
from omega_ai.trading.btc_organic_tracker import BTCOrganicTracker, OrganicState, BioEnergyLevel

# Create custom earth-colored colormaps
earth_cmap = LinearSegmentedColormap.from_list(
    "earth_tones", ["#8C4B2A", "#D0AE6D", "#567D46", "#186048", "#073B4C"]
)
schumann_cmap = LinearSegmentedColormap.from_list(
    "schumann", ["#25064C", "#4B1D69", "#722F7E", "#8E4F9F", "#F2E8C9"]
)

def plot_organic_timeline(tracker: BTCOrganicTracker, days_back: int = 90):
    """Plot the timeline of organic vs non-organic periods"""
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Prepare data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Filter periods in the selected timeframe
    periods = [p for p in tracker.organic_periods 
              if p.start_date > start_date or 
              (p.end_date and p.end_date > start_date)]
    
    # Create plot data
    dates = []
    scores = []
    colors = []
    states = []
    
    # Generate daily data points
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        
        # Find if this date is in an organic period
        in_period = False
        for period in periods:
            if period.start_date <= current_date and (not period.end_date or period.end_date >= current_date):
                scores.append(period.avg_organic_score)
                states.append("Organic")
                in_period.append("#567D46")  # Green for organic
                in_period = True
                break
        
        if not in_period:
            scores.append(0.3)  # Low score for non-organic
            states.append("Non-Organic")
            colors.append("#8C4B2A")  # Brown for non-organic
            
        current_date += timedelta(days=1)
    
    # Plot
    plt.bar(dates, scores, color=colors, width=0.8)
    
    # Add current day marker
    plt.axvline(end_date, color='#073B4C', linestyle='--', alpha=0.7)
    
    # Add record line
    if tracker.longest_organic_period:
        record_duration = tracker.longest_organic_period.duration_hours / 24  # days
        plt.ax# filepath: /Users/fsiqueira/Desktop/GitHub/omega-btc-ai/omega_ai/trading/btc_organic_plots.py

"""
OMEGA BTC Organic Movement Visualization - EARTH CONSCIOUSNESS CHARTS

This sacred module visualizes Bitcoin's alignment with Earth's natural rhythms:
- Schumann-BTC correlation charts
- Fibonacci resonance overlay on price
- Earth connection heatmaps
- Organic period timeline
- Bio-energy state visualization

JAH BLESS THE VISUAL EARTH-BTC CONNECTION! 🙏🌿🔥
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from typing import List, Dict, Optional, Union, Tuple
from omega_ai.trading.btc_organic_tracker import BTCOrganicTracker, OrganicState, BioEnergyLevel

# Create custom earth-colored colormaps
earth_cmap = LinearSegmentedColormap.from_list(
    "earth_tones", ["#8C4B2A", "#D0AE6D", "#567D46", "#186048", "#073B4C"]
)
schumann_cmap = LinearSegmentedColormap.from_list(
    "schumann", ["#25064C", "#4B1D69", "#722F7E", "#8E4F9F", "#F2E8C9"]
)

def plot_organic_timeline(tracker: BTCOrganicTracker, days_back: int = 90):
    """Plot the timeline of organic vs non-organic periods"""
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Prepare data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Filter periods in the selected timeframe
    periods = [p for p in tracker.organic_periods 
              if p.start_date > start_date or 
              (p.end_date and p.end_date > start_date)]
    
    # Create plot data
    dates = []
    scores = []
    colors = []
    states = []
    
    # Generate daily data points
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        
        # Find if this date is in an organic period
        in_period = False
        for period in periods:
            if period.start_date <= current_date and (not period.end_date or period.end_date >= current_date):
                scores.append(period.avg_organic_score)
                states.append("Organic")
                in_period.append("#567D46")  # Green for organic
                in_period = True
                break
        
        if not in_period:
            scores.append(0.3)  # Low score for non-organic
            states.append("Non-Organic")
            colors.append("#8C4B2A")  # Brown for non-organic
            
        current_date += timedelta(days=1)
    
    # Plot
    plt.bar(dates, scores, color=colors, width=0.8)
    
    # Add current day marker
    plt.axvline(end_date, color='#073B4C', linestyle='--', alpha=0.7)
    
    # Add record line
    if tracker.longest_organic_period:
        record_duration = tracker.longest_organic_period.duration_hours / 24  # days
        plt.ax