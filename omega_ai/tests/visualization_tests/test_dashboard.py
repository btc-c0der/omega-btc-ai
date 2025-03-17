#!/usr/bin/env python3

"""
DIVINE RASTA DASHBOARD TEST SUITE 🌿📊

"Test the vibes before they manifest in production." - Rastafarian DevOps Wisdom

These sacred tests verify the divine behavior of the OMEGA RASTA BTC DASHBOARD,
ensuring proper Fibonacci alignment, Schumann resonance visualization,
and spiritual market maker trap detection.

JAH BLESS THE UI TESTING! 🙏🌟
"""

import os
import sys
import pytest
import json
import redis
import dash
from dash.testing.application_runners import import_app
from dash.testing.composite import DashComposite
from unittest.mock import patch, MagicMock, ANY
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from freezegun import freeze_time

# Add project root to path for divine module accessibility
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from omega_ai.visualization.dashboard import app, RedisKeys, RASTA_QUOTES
from omega_ai.utils.redis_connection import RedisConnectionManager

# Terminal colors for divine output
RED = "\033[91m"
GREEN = "\033[92m" 
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# =============== DIVINE FIXTURES ===============

@pytest.fixture
def mock_redis():
    """Create a divine mock Redis connection."""
    with patch('redis.Redis') as mock_redis:
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance
        
        # Set up standard mock responses
        mock_data = {
            RedisKeys.LIVE_BATTLE_STATE: json.dumps({
                'btc_price': 50000.0,
                'btc_history': [48500.0, 49000.0, 49500.0, 50000.0],
                'day': 3,
                'session': 2,
            }),
            RedisKeys.LIVE_TRADER_DATA: json.dumps({
                'strategic': {
                    'pnl': 1250.0,
                    'trades': [{'profit': 250}, {'profit': 1000}],
                    'emotional_state': 'confident',
                    'confidence': 0.8,
                    'achievements': ['fibonacci_master', 'zen_trader'],
                },
                'aggressive': {
                    'pnl': -500.0,
                    'trades': [{'profit': 750}, {'profit': -1250}],
                    'emotional_state': 'fearful',
                    'confidence': 0.4,
                    'achievements': ['risk_taker'],
                },
                'newbie': {
                    'pnl': -1000.0,
                    'trades': [{'profit': -500}, {'profit': -500}],
                    'emotional_state': 'panicked',
                    'confidence': 0.2,
                    'achievements': [],
                },
                'scalper': {
                    'pnl': 800.0,
                    'trades': [{'profit': 100}, {'profit': 200}, {'profit': 200}, {'profit': 300}],
                    'emotional_state': 'neutral', 
                    'confidence': 0.7,
                    'achievements': ['quick_scalper'],
                }
            }),
            RedisKeys.MARKET_REGIME: 'UPTREND',
            RedisKeys.SCHUMANN_RESONANCE: '7.83',
            RedisKeys.SCHUMANN_HISTORY: json.dumps([7.83, 7.85, 7.89, 7.92, 8.05, 8.12, 8.0, 7.95, 7.9, 7.83]),
            RedisKeys.LATEST_MOVEMENT_ANALYSIS: json.dumps({
                '1min': 'BULLISH',
                '5min': 'BULLISH',
                '15min': 'NEUTRAL',
                '1h': 'NEUTRAL',
                '4h': 'BULLISH',
            }),
            RedisKeys.LATEST_ORGANIC_ANALYSIS: json.dumps({
                'organic_probability': 0.85,
                'manipulation_signals': ['liquidity_sweep', 'rapid_recovery'],
                'confidence': 'HIGH'
            }),
            RedisKeys.FIBONACCI_CONFLUENCE_ZONES: json.dumps({
                'support': [
                    {'level': '0.618', 'price': 48500, 'timeframes': ['1h', '4h'], 'strength': 'STRONG'},
                    {'level': '0.786', 'price': 47200, 'timeframes': ['4h'], 'strength': 'MEDIUM'}
                ],
                'resistance': [
                    {'level': '1.272', 'price': 52000, 'timeframes': ['1h', '4h', '1d'], 'strength': 'VERY_STRONG'},
                    {'level': '1.618', 'price': 54500, 'timeframes': ['4h'], 'strength': 'STRONG'}
                ]
            }),
            RedisKeys.START_TRADING: '1',
        }
        
        # Set up mock get method
        def mock_get(key):
            if key in mock_data:
                return mock_data[key]
            return None
            
        mock_instance.get.side_effect = mock_get
        
        # Setup mock exists method
        def mock_exists(key):
            return key in mock_data
            
        mock_instance.exists.side_effect = mock_exists
        
        yield mock_instance


@pytest.fixture
def mock_redis_manager():
    """Create a divine mock Redis connection manager."""
    with patch('omega_ai.utils.redis_connection.RedisConnectionManager') as mock_manager:
        mock_instance = MagicMock()
        mock_manager.return_value = mock_instance
        
        # Setup mock data store
        mock_data = {
            RedisKeys.LIVE_BATTLE_STATE: json.dumps({
                'btc_price': 50000.0,
                'btc_history': [48500.0, 49000.0, 49500.0, 50000.0],
                'day': 3,
                'session': 2,
            }),
            RedisKeys.LIVE_TRADER_DATA: json.dumps({
                'strategic': {
                    'pnl': 1250.0,
                    'trades': [{'profit': 250}, {'profit': 1000}],
                    'emotional_state': 'confident',
                    'confidence': 0.8,
                    'achievements': ['fibonacci_master', 'zen_trader'],
                },
                'aggressive': {
                    'pnl': -500.0, 
                    'trades': [{'profit': 750}, {'profit': -1250}],
                    'emotional_state': 'fearful',
                    'confidence': 0.4,
                    'achievements': ['risk_taker'],
                },
                'newbie': {
                    'pnl': -1000.0,
                    'trades': [{'profit': -500}, {'profit': -500}],
                    'emotional_state': 'panicked',
                    'confidence': 0.2,
                    'achievements': [],
                },
                'scalper': {
                    'pnl': 800.0,
                    'trades': [{'profit': 100}, {'profit': 200}, {'profit': 200}, {'profit': 300}],
                    'emotional_state': 'neutral',
                    'confidence': 0.7,
                    'achievements': ['quick_scalper'],  
                }
            }),
        }
        
        # Setup mock get method
        def mock_get(key):
            if key in mock_data:
                return mock_data[key]
            return None
            
        mock_instance.get.side_effect = mock_get
        
        yield mock_instance


@pytest.fixture
def patched_dash_app(mock_redis, mock_redis_manager):
    """Create a divine patched Dash app for testing."""
    with patch('dash.Dash') as mock_dash:
        # Create mock app
        mock_app = MagicMock()
        mock_dash.return_value = mock_app
        
        # Patch callbacks
        mock_app.callback.return_value = lambda func: func
        
        # Mock layout
        mock_app.layout = MagicMock()
        
        # Import app with patched dependencies
        with patch('redis.Redis', return_value=mock_redis):
            with patch('omega_ai.utils.redis_connection.RedisConnectionManager', return_value=mock_redis_manager):
                from omega_ai.visualization.dashboard import app
                yield app
                

@pytest.fixture
def mock_analysis_functions():
    """Create divine mocks for market analysis functions."""
    with patch('omega_ai.monitor.monitor_market_trends.analyze_price_trend') as mock_analyze:
        with patch('omega_ai.monitor.monitor_market_trends.get_current_fibonacci_levels') as mock_fib_levels:
            with patch('omega_ai.monitor.monitor_market_trends.check_fibonacci_level') as mock_check_fib:
                
                # Set up mock return values
                mock_analyze.return_value = {
                    'trend': 'UPTREND',
                    'strength': 0.85,
                    'oscillation': 'LOW',
                    'confidence': 'HIGH'
                }
                
                mock_fib_levels.return_value = {
                    '0': 45000.0,
                    '0.236': 46500.0,
                    '0.382': 47250.0, 
                    '0.5': 47850.0,
                    '0.618': 48500.0,
                    '0.786': 49200.0,
                    '1.0': 50000.0,
                    '1.272': 52000.0,
                    '1.618': 54500.0
                }
                
                mock_check_fib.return_value = {
                    'current_level': '0.786',
                    'distance_to_next': 800.0,
                    'next_level': '1.0',
                    'probability': 0.75,
                    'suggested_action': 'BUY_DIP'
                }
                
                yield {
                    'analyze': mock_analyze,
                    'fib_levels': mock_fib_levels,
                    'check_fib': mock_check_fib
                }


# =============== DIVINE TEST CASES ===============

@patch('redis.Redis')
@patch('omega_ai.utils.redis_connection.RedisConnectionManager')
def test_dashboard_initialization(mock_manager, mock_redis):
    """🌿 Test divine dashboard initialization."""
    # Test app creation and title
    from omega_ai.visualization.dashboard import app
    
    print(f"\n{GREEN}Testing divine dashboard initialization:{RESET}")
    print(f"  App title: {app.title}")
    
    assert app.title == "OMEGA RASTA BTC DASHBOARD"
    assert "rasta" in app.title.lower()
    assert app.layout is not None
    
    # Verify dashboard components
    def count_components(layout):
        """Recursively count components in layout"""
        if not hasattr(layout, 'children'):
            return 1
            
        if not layout.children:
            return 1
            
        count = 1  # Count this component
        
        if isinstance(layout.children, list):
            for child in layout.children:
                count += count_components(child)
        else:
            count += count_components(layout.children)
            
        return count
    
    component_count = count_components(app.layout)
    print(f"  Component count: {component_count}")
    
    # Should have substantial number of components
    assert component_count > 20, "Dashboard should have many divine components"


@freeze_time("2025-03-15 12:00:00")
def test_rasta_quote_callback(patched_dash_app, monkeypatch):
    """🌿 Test divine Rastafarian quote updates."""
    print(f"\n{GREEN}Testing Rasta quote callback:{RESET}")
    
    # Mock random.choice to return a specific quote
    fixed_quote = "JAH provide the herb, mon - Green energy for trading wisdom 🌿"
    monkeypatch.setattr('random.choice', lambda x: fixed_quote)
    
    # Get update_rasta_quote function
    from omega_ai.visualization.dashboard import update_rasta_quote
    
    # Test the callback
    result = update_rasta_quote(5)
    print(f"  Quote result: {result}")
    
    assert result == fixed_quote
    assert "JAH" in result
    

@freeze_time("2025-03-15 12:00:00")
@patch('redis.Redis')
@patch('omega_ai.utils.redis_connection.RedisConnectionManager')
def test_battle_display_callback(mock_manager_class, mock_redis_class, mock_redis, mock_redis_manager, mock_analysis_functions, monkeypatch):
    """🌿 Test divine trading battle display updates."""
    print(f"\n{GREEN}Testing battle display callback:{RESET}")
    
    # Setup mocks
    mock_manager_class.return_value = mock_redis_manager
    mock_redis_class.return_value = mock_redis
    
    # Get update callback
    from omega_ai.visualization.dashboard import update_battle_display
    
    # Run the callback
    results = update_battle_display(10)
    
    # Verify results
    print(f"  Price display: {results[0]}")
    print(f"  Price change: {results[1]}")
    
    # Check that price is correctly formatted
    assert "$" in results[0]
    assert "," in results[0]
    assert isinstance(results[4], go.Figure)  # Price chart
    assert isinstance(results[5], go.Figure)  # Performance chart
    
    print(f"  Figure data traces: {len(results[4].data)}")
    
    # Price chart should include main price line plus Fibonacci levels
    assert len(results[4].data) >= 1, "Price chart should have at least one trace"
    
    # Should have trader components
    assert isinstance(results[6], list), "Should have trader leaderboard"
    assert len(results[6]) > 0, "Leaderboard should contain traders"
    
    assert isinstance(results[7], list), "Should have emotional states"
    assert len(results[7]) > 0, "Emotional states should contain traders"


@freeze_time("2025-03-15 12:00:00") 
@patch('redis.Redis')
@patch('omega_ai.utils.redis_connection.RedisConnectionManager')
def test_market_analysis_callback(mock_manager_class, mock_redis_class, mock_redis, mock_redis_manager, mock_analysis_functions, monkeypatch):
    """🔥 Test divine market analysis updates."""
    print(f"\n{GREEN}Testing market analysis callback:{RESET}")
    
    # Setup mocks
    mock_manager_class.return_value = mock_redis_manager
    mock_redis_class.return_value = mock_redis
    
    # Get analysis callback
    from omega_ai.visualization.dashboard import update_market_analysis
    
    # Run the callback
    results = update_market_analysis(10)
    
    # Verify results
    print(f"  Market regime: {results[0]}")
    print(f"  Schumann current: {results[5]}")
    
    # Schumann resonance chart
    assert isinstance(results[7], go.Figure)
    assert len(results[7].data) >= 1, "Schumann chart should have at least one trace"
    
    # News feed
    assert isinstance(results[8], list), "News feed should be a list"


def test_battle_controls_callback(patched_dash_app, mock_redis, mock_redis_manager):
    """⚔️ Test divine battle control buttons."""
    print(f"\n{GREEN}Testing battle control callback:{RESET}")
    
    # Import dash for callback context
    import dash
    
    # Get control callback
    from omega_ai.visualization.dashboard import handle_battle_controls
    
    # Test start button
    with patch('dash.callback_context') as mock_ctx:
        mock_ctx.triggered = [{'prop_id': 'start-battle.n_clicks'}]
        result = handle_battle_controls(1, None, None)
        print(f"  Start button result: {result}")
        assert result['status'] == 'running'
        mock_redis.set.assert_called_with(RedisKeys.START_TRADING, 1)
    
    # Test pause button
    with patch('dash.callback_context') as mock_ctx:
        mock_ctx.triggered = [{'prop_id': 'pause-battle.n_clicks'}]  
        result = handle_battle_controls(None, 1, None)
        print(f"  Pause button result: {result}")
        assert result['status'] == 'paused'
        mock_redis.set.assert_called_with(RedisKeys.START_TRADING, 0)
    
    # Test reset button  
    with patch('dash.callback_context') as mock_ctx:
        mock_ctx.triggered = [{'prop_id': 'reset-arena.n_clicks'}]
        result = handle_battle_controls(None, None, 1)
        print(f"  Reset button result: {result}")
        assert result['status'] == 'reset'


@patch('redis.Redis')
@patch('omega_ai.utils.redis_connection.RedisConnectionManager')
def test_fibonacci_visualization(mock_manager_class, mock_redis_class, mock_redis, mock_redis_manager, mock_analysis_functions):
    """🌀 Test divine Fibonacci level visualization."""
    print(f"\n{GREEN}Testing Fibonacci level visualization:{RESET}")
    
    # Setup mocks
    mock_manager_class.return_value = mock_redis_manager
    mock_redis_class.return_value = mock_redis
    
    # Get update callback
    from omega_ai.visualization.dashboard import update_battle_display
    
    # Run the callback to get chart
    results = update_battle_display(10)
    price_fig = results[4]  # Price chart with Fibonacci levels
    
    assert isinstance(price_fig, go.Figure)
    
    # Extract trace names to find Fibonacci levels
    trace_names = [trace.name for trace in price_fig.data]
    print(f"  Chart traces: {trace_names}")
    
    # Check for Fibonacci traces
    fib_traces = [t for t in trace_names if 'Fib' in str(t)]
    print(f"  Fibonacci traces: {fib_traces}")
    
    # Assume at least one Fibonacci level is displayed
    assert any('Fib' in str(t) for t in trace_names), "Chart should contain Fibonacci levels"


def test_schumann_resonance_display(patched_dash_app, mock_redis, mock_redis_manager):
    """🌍 Test divine Schumann resonance display."""
    print(f"\n{GREEN}Testing Schumann resonance display:{RESET}")
    
    # Get market analysis callback
    from omega_ai.visualization.dashboard import update_market_analysis
    
    # Run the callback
    with patch('redis.Redis', return_value=mock_redis):
        with patch('omega_ai.utils.redis_connection.RedisConnectionManager', return_value=mock_redis_manager):
            results = update_market_analysis(10)
    
    # Check Schumann resonance display
    schumann_current = results[5]
    schumann_status = results[6]
    schumann_chart = results[7]
    
    print(f"  Schumann current: {schumann_current}")
    print(f"  Schumann status: {schumann_status}")
    
    # Verify chart
    assert isinstance(schumann_chart, go.Figure)
    assert len(schumann_chart.data) >= 1, "Schumann chart should have at least one trace"


def test_trader_psychological_states(patched_dash_app, mock_redis, mock_redis_manager):
    """🧠 Test divine trader psychological state display."""
    print(f"\n{GREEN}Testing trader psychological states:{RESET}")
    
    # Get battle display callback
    from omega_ai.visualization.dashboard import update_battle_display
    
    # Run the callback
    with patch('redis.Redis', return_value=mock_redis):
        with patch('omega_ai.utils.redis_connection.RedisConnectionManager', return_value=mock_redis_manager):
            results = update_battle_display(10)
    
    # Get emotional states
    emotional_states = results[7]
    
    print(f"  Number of emotional states: {len(emotional_states)}")
    
    # Should have emotional states for all traders
    assert len(emotional_states) == 4, "Should display 4 trader emotional states"
    
    # Check trader-specific emotions
    trader_names = ['strategic', 'aggressive', 'newbie', 'scalper']
    for state in emotional_states:
        # Each state should be a Div containing trader info
        assert any(name in str(state).lower() for name in trader_names)


def test_trading_suggestions(patched_dash_app, mock_redis, mock_redis_manager, mock_analysis_functions):
    """🌿 Test divine trading suggestions generation."""
    print(f"\n{GREEN}Testing trading suggestions:{RESET}")
    
    # Get battle display callback
    from omega_ai.visualization.dashboard import update_battle_display
    
    # Run the callback
    with patch('redis.Redis', return_value=mock_redis):
        with patch('omega_ai.utils.redis_connection.RedisConnectionManager', return_value=mock_redis_manager):
            results = update_battle_display(10)
    
    # Get trading suggestions
    suggestions = results[9]
    
    print(f"  Suggestions type: {type(suggestions)}")
    
    # Should have trading suggestions
    assert suggestions is not None, "Should have trading suggestions"


@freeze_time("2025-03-15 12:00:00")
def test_market_maker_trap_detection(patched_dash_app, mock_redis, mock_redis_manager):
    """⚠️ Test divine market maker trap detection display."""
    print(f"\n{GREEN}Testing market maker trap detection:{RESET}")
    
    # Setup mock data for traps
    trap_data = json.dumps({
        'detected_traps': [
            {
                'trap_type': 'liquidity_grab',
                'confidence': 0.85,
                'price_level': 49500,
                'timeframe': '5min',
                'description': 'Rapid price spike followed by reversal',
                'severity': 'HIGH'
            },
            {
                'trap_type': 'stop_hunt',
                'confidence': 0.75,
                'price_level': 48200,
                'timeframe': '15min',
                'description': 'Brief move below support with rapid recovery',
                'severity': 'MEDIUM'
            }
        ],
        'last_updated': '2025-03-15 11:45:00'
    })
    
    # Update mock Redis
    mock_redis.get.return_value = trap_data
    
    # Get market analysis callback
    from omega_ai.visualization.dashboard import update_market_analysis
    
    # Run the callback
    with patch('redis.Redis', return_value=mock_redis):
        with patch('omega_ai.utils.redis_connection.RedisConnectionManager', return_value=mock_redis_manager):
            results = update_market_analysis(10)
    
    # Get trap alerts
    trap_alerts = results[4]
    
    print(f"  Trap alerts: {trap_alerts}")
    
    # Should have trap alerts
    assert trap_alerts is not None, "Should have market maker trap alerts"


class TestEarthVibrationIntegration:
    """Divine test class for earth vibration integration with trading."""
    
    @patch('redis.Redis')
    @patch('omega_ai.utils.redis_connection.RedisConnectionManager') 
    def test_schumann_resonance_correlation(self, mock_manager_class, mock_redis_class, mock_redis, mock_redis_manager):
        """🌍 Test divine correlation between Schumann resonance and trading."""
        print(f"\n{GREEN}Testing Schumann resonance correlation with trading:{RESET}")
        
        # Create Schumann history with different frequencies
        normal_freq = 7.83
        elevated_freq = 12.5  # Higher resonance
        
        # Create price histories that correlate with resonance
        normal_prices = [49000.0, 49200.0, 49500.0, 49800.0, 50000.0]
        elevated_prices = [50000.0, 51000.0, 52000.0, 53000.0, 55000.0]  # More volatile
        
        # First test with normal frequency
        mock_redis.get = MagicMock(side_effect=lambda key: {
            RedisKeys.SCHUMANN_RESONANCE: str(normal_freq),
            RedisKeys.SCHUMANN_HISTORY: json.dumps([normal_freq] * 10),
            RedisKeys.LIVE_BATTLE_STATE: json.dumps({
                'btc_price': 50000.0,
                'btc_history': normal_prices,
                'day': 1,
                'session': 1,
            }),
            RedisKeys.LIVE_TRADER_DATA: mock_redis_manager.get(RedisKeys.LIVE_TRADER_DATA),
            RedisKeys.MARKET_REGIME: 'NEUTRAL',
        }.get(key, mock_redis_manager.get(key)))
        
        from omega_ai.visualization.dashboard import update_market_analysis, update_battle_display
        
        normal_results = update_market_analysis(10)
        normal_battle = update_battle_display(10)
        
        print(f"  Normal Schumann: {normal_freq} Hz")
        print(f"  Normal price volatility: {max(normal_prices) - min(normal_prices)}")
        
        # Then test with elevated frequency
        mock_redis.get = MagicMock(side_effect=lambda key: {
            RedisKeys.SCHUMANN_RESONANCE: str(elevated_freq),
            RedisKeys.SCHUMANN_HISTORY: json.dumps([elevated_freq] * 10),
            RedisKeys.LIVE_BATTLE_STATE: json.dumps({
                'btc_price': 55000.0,
                'btc_history': elevated_prices,
                'day': 1,
                'session': 1,
            }),
            RedisKeys.LIVE_TRADER_DATA: mock_redis_manager.get(RedisKeys.LIVE_TRADER_DATA),
            RedisKeys.MARKET_REGIME: 'UPTREND',
        }.get(key, mock_redis_manager.get(key)))
        
        elevated_results = update_market_analysis(10)
        elevated_battle = update_battle_display(10)
        
        print(f"  Elevated Schumann: {elevated_freq} Hz")
        print(f"  Elevated price volatility: {max(elevated_prices) - min(elevated_prices)}")
        
        # Check that elevated resonance creates different display
        assert normal_results[5] != elevated_results[5], "Schumann display should differ"
        assert normal_results[6] != elevated_results[6], "Schumann status should differ"
        
        # Price chart should be different
        normal_chart = normal_battle[4]
        elevated_chart = elevated_battle[4]
        
        assert normal_chart != elevated_chart, "Price charts should differ with Schumann changes"
        
        print(f"  {YELLOW}JAH BLESS! Earth vibrations affect divine trading patterns{RESET}")


def test_rasta_color_scheme():
    """🌈 Test divine Rastafarian color scheme application."""
    print(f"\n{GREEN}Testing Rastafarian color theme:{RESET}")
    
    # Import the dashboard module to access theme
    from omega_ai.visualization.dashboard import rasta_theme
    
    # Verify essential Rasta colors are present
    assert 'green' in rasta_theme
    assert 'red' in rasta_theme
    assert 'yellow' in rasta_theme
    
    # Print the color scheme
    print(f"  Background: {rasta_theme['background']}")
    print(f"  Rasta Green: {rasta_theme['green']}")
    print(f"  Rasta Yellow: {rasta_theme['yellow']}")
    print(f"  Rasta Red: {rasta_theme['red']}")
    
    # Verify colors match Rastafarian theme
    assert rasta_theme['green'] == "#00B52D" or rasta_theme['green'].lower() == "#006400".lower()
    assert rasta_theme['yellow'] == "#FFDD00" or rasta_theme['yellow'].lower() == "#ffb300".lower()
    assert rasta_theme['red'] == "#FF3D00" or rasta_theme['red'].lower() == "#ff0000".lower()


if __name__ == "__main__":
    # Run the divine tests with Rastafarian blessing
    print(f"\n{GREEN}🌿 JAH BLESS THE OMEGA DASHBOARD TEST SUITE! 🌿{RESET}")
    pytest.main(["-v", __file__])