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

# -*- coding: utf-8 -*-

"""
🌌 AIXBT Divine Monitor Coverage Report Utilities
--------------------------------------------

This module provides utility functions for coverage report generation.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('coverage_report_utils')

def load_config() -> Optional[Dict[str, Any]]:
    """Load coverage report configuration."""
    try:
        with open('coverage_report_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error('Configuration file not found')
        return None
    except json.JSONDecodeError:
        logger.error('Invalid JSON in configuration file')
        return None

def calculate_divine_metrics(
    coverage: float,
    history_data: Dict[str, Any]
) -> Dict[str, float]:
    """Calculate divine metrics based on coverage and history."""
    config = load_config()
    if not config:
        return {}

    metrics_config = config['report']['metrics']['divine']
    
    # Calculate harmony (balance between coverage and its consistency)
    harmony = min(
        coverage / 100,
        get_coverage_consistency(history_data)
    ) * metrics_config['harmony']['weight']
    
    # Calculate balance (distribution of coverage across modules)
    balance = calculate_coverage_distribution(
        history_data
    ) * metrics_config['balance']['weight']
    
    # Calculate resonance (trend alignment)
    resonance = calculate_trend_alignment(
        history_data
    ) * metrics_config['resonance']['weight']
    
    return {
        'harmony': harmony,
        'balance': balance,
        'resonance': resonance,
        'total': harmony + balance + resonance
    }

def get_coverage_consistency(history_data: Dict[str, Any]) -> float:
    """Calculate coverage consistency from history."""
    entries = history_data.get('history', {}).get('entries', [])
    if not entries:
        return 0.0
    
    coverage_values = [entry['coverage'] for entry in entries]
    if not coverage_values:
        return 0.0
    
    # Calculate standard deviation and normalize
    mean = sum(coverage_values) / len(coverage_values)
    variance = sum((x - mean) ** 2 for x in coverage_values) / len(coverage_values)
    std_dev = variance ** 0.5
    
    # Convert to consistency score (0-1)
    max_std_dev = 20  # Maximum expected standard deviation
    consistency = 1 - min(std_dev / max_std_dev, 1)
    
    return consistency

def calculate_coverage_distribution(history_data: Dict[str, Any]) -> float:
    """Calculate coverage distribution score."""
    latest_entry = history_data.get('history', {}).get('entries', [{}])[0]
    if not latest_entry:
        return 0.0
    
    metrics = latest_entry.get('metrics', {})
    if not metrics:
        return 0.0
    
    # Calculate distribution score based on coverage types
    total_lines = metrics.get('lines', {}).get('total', 0)
    total_branches = metrics.get('branches', {}).get('total', 0)
    total_functions = metrics.get('functions', {}).get('total', 0)
    
    if not (total_lines and total_branches and total_functions):
        return 0.0
    
    lines_coverage = metrics['lines']['covered'] / total_lines
    branches_coverage = metrics['branches']['covered'] / total_branches
    functions_coverage = metrics['functions']['covered'] / total_functions
    
    # Calculate distribution score (0-1)
    distribution = (lines_coverage + branches_coverage + functions_coverage) / 3
    
    return distribution

def calculate_trend_alignment(history_data: Dict[str, Any]) -> float:
    """Calculate trend alignment score."""
    entries = history_data.get('history', {}).get('entries', [])
    if len(entries) < 2:
        return 0.0
    
    # Calculate trend direction and strength
    coverage_values = [entry['coverage'] for entry in entries]
    trend_direction = sum(
        1 if b > a else -1
        for a, b in zip(coverage_values[1:], coverage_values[:-1])
    )
    
    # Calculate trend strength (0-1)
    max_trend = len(coverage_values) - 1
    trend_strength = abs(trend_direction) / max_trend
    
    # Calculate trend consistency
    trend_changes = sum(
        1 if (b - a) * (c - b) < 0 else 0
        for a, b, c in zip(coverage_values[:-2], coverage_values[1:-1], coverage_values[2:])
    )
    trend_consistency = 1 - (trend_changes / (len(coverage_values) - 2) if len(coverage_values) > 2 else 0)
    
    # Combine trend strength and consistency
    alignment = (trend_strength + trend_consistency) / 2
    
    return alignment

def format_coverage_value(value: float) -> str:
    """Format coverage value with appropriate color and symbol."""
    config = load_config()
    if not config:
        return f"{value:.2f}%"
    
    thresholds = config['report']['metrics']['coverage']['thresholds']
    colors = config['report']['metrics']['coverage']['colors']
    
    if value >= thresholds['high']:
        color = colors['high']
        symbol = '🟢'
    elif value >= thresholds['medium']:
        color = colors['medium']
        symbol = '🟡'
    else:
        color = colors['low']
        symbol = '🔴'
    
    return f'<span style="color: {color}">{symbol} {value:.2f}%</span>'

def get_trend_data(
    history_data: Dict[str, Any],
    window: Optional[int] = None
) -> Dict[str, List[Any]]:
    """Get trend data for visualization."""
    entries = history_data.get('history', {}).get('entries', [])
    if not entries:
        return {'dates': [], 'values': []}
    
    if window:
        entries = entries[:window]
    
    dates = [
        datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
        for entry in entries
    ]
    values = [entry['coverage'] for entry in entries]
    
    return {
        'dates': dates,
        'values': values
    }

def create_output_directory(output_dir: str) -> bool:
    """Create output directory if it doesn't exist."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f'Error creating output directory: {e}')
        return False

def copy_assets(output_dir: str) -> bool:
    """Copy static assets to output directory."""
    try:
        config = load_config()
        if not config:
            return False
        
        assets = [
            config['report']['template']['css'],
            'coverage.svg',
            'coverage_badge_template.svg'
        ]
        
        for asset in assets:
            if os.path.exists(asset):
                dest = os.path.join(output_dir, os.path.basename(asset))
                with open(asset, 'r') as src, open(dest, 'w') as dst:
                    dst.write(src.read())
        
        return True
    except Exception as e:
        logger.error(f'Error copying assets: {e}')
        return False 