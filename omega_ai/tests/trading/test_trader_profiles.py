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
DIVINE RASTA TRADER PROFILE TESTS 🌿🔥

"Test everything. Keep the good." - 1 Thessalonians 5:21 with Rastafarian wisdom

These sacred tests verify the divine behavior of different trader profiles, ensuring
their holy psychological traits, risk management, and trading decisions are aligned
with cosmic energy and the laws of profitable trading.

JAH BLESS THE TRADING WISDOM! 🙏🌟
"""

import os
import sys
import pytest
import json
import redis
import random
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, ANY
from freezegun import freeze_time

# Add project root to path for divine module accessibility
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from omega_ai.trading.profiled_futures_trader import ProfiledFuturesTrader, TradingPosition
from omega_ai.trading.profiles.strategic_trader import StrategicTrader
from omega_ai.trading.profiles.aggressive_trader import AggressiveTrader
from omega_ai.trading.profiles.newbie_trader import NewbieTrader
from omega_ai.trading.profiles.scalper_trader import ScalperTrader

# Divine Test Configuration
class TestConfig:
    """Holy configuration for RASTA trader tests"""
    TEST_CAPITAL = 10000.0
    TEST_PROFILES = ["strategic", "aggressive", "newbie", "scalper"]
    TEST_PRICE = 50000.0
    TEST_LEVERAGE = [3, 10, 20, 10]  # Expected default leverage by profile
    TEST_TIMEFRAME = "2025-03-15 12:00:00"
    INITIAL_CAPITAL = 10000.0

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
    """Mock Redis for testing."""
    with patch('redis.StrictRedis') as mock_redis:
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        yield mock_client

@pytest.fixture
def mock_redis_conn():
    """Mock Redis connection for testing."""
    with patch('omega_ai.trading.btc_futures_trader.redis_conn') as mock_conn:
        mock_conn.get.return_value = str(TestConfig.TEST_PRICE)
        yield mock_conn

# =============== BLESSED TEST CASES ===============

@pytest.mark.parametrize("profile_type", TestConfig.TEST_PROFILES)
def test_trader_profile_initialization(profile_type):
    """🌿 Test divine initialization of each trader profile."""
    # Create trader with JAH blessing
    trader = ProfiledFuturesTrader(
        profile_type=profile_type,
        initial_capital=TestConfig.TEST_CAPITAL
    )
    
    # Verify divine attributes
    print(f"\n{GREEN}Testing {profile_type.upper()} profile initialization{RESET}")
    assert trader.profile_type == profile_type
    assert trader.initial_capital == TestConfig.TEST_CAPITAL
    assert trader.capital == TestConfig.TEST_CAPITAL
    assert hasattr(trader, "profile")
    assert trader.positions == []
    
    # Verify psychological state initialization
    assert "emotional_state" in trader.state
    assert "confidence" in trader.state
    assert trader.state["emotional_state"] == "neutral"
    assert 0.0 <= trader.state["confidence"] <= 1.0
    
    # Print divine confirmation
    print(f"{GREEN}✓ {profile_type.capitalize()} trader blessed with divine initial state{RESET}")

@pytest.mark.parametrize("profile_type", TestConfig.TEST_PROFILES)
def test_trader_risk_parameters(profile_type):
    """🌿 Test each trader profile has divine risk parameters."""
    # Create trader with specific profile
    trader = ProfiledFuturesTrader(
        profile_type=profile_type,
        initial_capital=TestConfig.TEST_CAPITAL
    )
    
    # Risk parameters should align with profile type
    print(f"\n{GREEN}Testing {profile_type.upper()} risk parameters{RESET}")
    
    # Risk per trade should be divinely appropriate
    if profile_type == "aggressive":
        assert trader.risk_per_trade == 0.4  # 40% - highest risk
        assert trader.max_leverage >= 20  # High leverage
    elif profile_type == "strategic":
        assert trader.risk_per_trade == 0.2  # 20% - measured risk
        assert trader.max_leverage <= 10  # Moderate leverage
    elif profile_type == "newbie":
        assert trader.risk_per_trade == 0.3  # 30% - unbalanced risk
        assert trader.max_leverage >= 30  # Excessive leverage
    elif profile_type == "scalper":
        assert trader.risk_per_trade == 0.2  # 20% - precise risk
        assert trader.max_leverage > 5  # Higher leverage for small moves
        
    # Print divine confirmation
    print(f"{GREEN}✓ {profile_type.capitalize()} trader blessed with divine risk parameters:{RESET}")
    print(f"   Risk per trade: {trader.risk_per_trade}")
    print(f"   Max leverage: {trader.max_leverage}")

@pytest.mark.parametrize("profile_type", TestConfig.TEST_PROFILES)
def test_trader_stop_loss_calculation(profile_type):
    """🌿 Test stop loss calculation has divine alignment across profiles."""
    # Create trader with specific profile
    trader = ProfiledFuturesTrader(
        profile_type=profile_type,
        initial_capital=TestConfig.TEST_CAPITAL
    )
    
    # Set current price
    trader.current_price = TestConfig.TEST_PRICE
    
    # Calculate stop loss for LONG position
    long_stop_loss = trader._calculate_stop_loss("LONG", TestConfig.TEST_PRICE)
    
    # Stop loss should be below entry for longs
    assert long_stop_loss < TestConfig.TEST_PRICE
    
    # Calculate stop loss for SHORT position
    short_stop_loss = trader._calculate_stop_loss("SHORT", TestConfig.TEST_PRICE)
    
    # Stop loss should be above entry for shorts
    assert short_stop_loss > TestConfig.TEST_PRICE
    
    # Profile-specific checks
    print(f"\n{GREEN}Testing {profile_type.upper()} stop loss calculation{RESET}")
    
    # Strategic traders have wider stops
    if profile_type == "strategic":
        assert TestConfig.TEST_PRICE - long_stop_loss > TestConfig.TEST_PRICE * 0.03
    # Aggressive traders have moderate stops
    elif profile_type == "aggressive":
        assert TestConfig.TEST_PRICE - long_stop_loss > TestConfig.TEST_PRICE * 0.01
        assert TestConfig.TEST_PRICE - long_stop_loss < TestConfig.TEST_PRICE * 0.03
    # Newbies have tight stops that get hit often
    elif profile_type == "newbie":
        assert TestConfig.TEST_PRICE - long_stop_loss < TestConfig.TEST_PRICE * 0.02
    # Scalpers have tight but reasonable stops
    elif profile_type == "scalper":
        assert TestConfig.TEST_PRICE - long_stop_loss > TestConfig.TEST_PRICE * 0.005
        assert TestConfig.TEST_PRICE - long_stop_loss < TestConfig.TEST_PRICE * 0.02
    
    # Print divine confirmation
    print(f"{GREEN}✓ {profile_type.capitalize()} trader blessed with divine stop loss placement:{RESET}")
    print(f"   Long stop loss: ${long_stop_loss:.2f} (${TestConfig.TEST_PRICE - long_stop_loss:.2f} away)")
    print(f"   Short stop loss: ${short_stop_loss:.2f} (${short_stop_loss - TestConfig.TEST_PRICE:.2f} away)")

@pytest.mark.parametrize("profile_type", TestConfig.TEST_PROFILES)
def test_trader_take_profit_levels(profile_type):
    """🌿 Test take profit levels are divinely structured based on trader psychology."""
    # Create trader with specific profile
    trader = ProfiledFuturesTrader(
        profile_type=profile_type,
        initial_capital=TestConfig.TEST_CAPITAL
    )
    
    # Set current price
    trader.current_price = TestConfig.TEST_PRICE
    
    # Calculate take profit for LONG position
    long_take_profits = trader._calculate_take_profit_levels("LONG", TestConfig.TEST_PRICE)
    
    # Calculate take profit for SHORT position
    short_take_profits = trader._calculate_take_profit_levels("SHORT", TestConfig.TEST_PRICE)
    
    # Basic assertions
    assert isinstance(long_take_profits, list)
    assert isinstance(short_take_profits, list)
    assert len(long_take_profits) > 0
    assert len(short_take_profits) > 0
    
    # Take profits should be above entry for longs
    for tp in long_take_profits:
        assert tp["price"] > TestConfig.TEST_PRICE
        assert "percentage" in tp
    
    # Take profits should be below entry for shorts
    for tp in short_take_profits:
        assert tp["price"] < TestConfig.TEST_PRICE
        assert "percentage" in tp
    
    # Profile-specific checks
    print(f"\n{GREEN}Testing {profile_type.upper()} take profit levels{RESET}")
    
    # Strategic traders have multiple planned take-profit levels
    if profile_type == "strategic":
        assert len(long_take_profits) >= 2
        total_percentage = sum(tp["percentage"] for tp in long_take_profits)
        assert abs(total_percentage - 1.0) < 0.01  # Should sum to 100%
    
    # Aggressive traders aim for bigger targets
    elif profile_type == "aggressive":
        assert len(long_take_profits) >= 1
        first_tp = long_take_profits[0]["price"]
        assert first_tp > TestConfig.TEST_PRICE * 1.03  # At least 3% target
    
    # Newbies often use unrealistic targets or exit too early
    elif profile_type == "newbie":
        assert len(long_take_profits) >= 1
        if len(long_take_profits) == 1:
            # Either very tight or very wide
            first_tp = long_take_profits[0]["price"]
            assert (first_tp < TestConfig.TEST_PRICE * 1.01) or (first_tp > TestConfig.TEST_PRICE * 1.10)
    
    # Scalpers use quick small targets
    elif profile_type == "scalper":
        assert len(long_take_profits) >= 1
        first_tp = long_take_profits[0]["price"]
        assert first_tp < TestConfig.TEST_PRICE * 1.03  # Less than 3% target
    
    # Print divine confirmation
    print(f"{GREEN}✓ {profile_type.capitalize()} trader blessed with divine take profit strategy:{RESET}")
    print(f"   Long take profits: {len(long_take_profits)} levels")
    for i, tp in enumerate(long_take_profits):
        print(f"     Level {i+1}: ${tp['price']:.2f} ({tp['percentage']*100:.0f}% of position)")

@freeze_time(TestConfig.TEST_TIMEFRAME)
@pytest.mark.parametrize("profile_type", TestConfig.TEST_PROFILES)
def test_trader_position_management(profile_type):
    """🌿 Test divine position management with each trader psychology."""
    # Create trader with specific profile
    trader = ProfiledFuturesTrader(
        profile_type=profile_type,
        initial_capital=TestConfig.TEST_CAPITAL
    )
    
    # Set current price
    trader.current_price = TestConfig.TEST_PRICE
    
    # Open a position with custom stop loss at 2% below entry
    trader.open_position("LONG", "Test divine entry", 2, stop_loss_pct=0.02)  # 2% stop loss
    
    # Verify position was opened with JAH BLESSING
    assert len(trader.positions) == 1
    assert trader.positions[0].direction == "LONG"
    assert trader.positions[0].entry_price == TestConfig.TEST_PRICE
    assert trader.positions[0].stop_loss == TestConfig.TEST_PRICE * 0.98  # 2% below entry
    
    # Change price and manage position - Profitable move
    trader.current_price = TestConfig.TEST_PRICE * 1.01  # 1% increase
    trader.manage_open_positions()
    
    # Position should still be open with profit
    assert len(trader.positions) == 1
    assert trader.positions[0].unrealized_pnl > 0
    
    # Test stop loss - exactly at stop loss should trigger
    trader.current_price = trader.positions[0].stop_loss
    trader.manage_open_positions()
    
    # Position should be closed
    assert len(trader.positions) == 0
    
    # Capital should be reduced due to stop loss hit
    assert trader.capital < TestConfig.TEST_CAPITAL
    
    # Print divine confirmation
    print(f"\n{GREEN}✓ {profile_type.capitalize()} trader blessed with divine position management{RESET}")

@freeze_time(TestConfig.TEST_TIMEFRAME)
@pytest.mark.parametrize("profile_type", TestConfig.TEST_PROFILES)
def test_trader_psychological_changes(profile_type):
    """🌿 Test psychological state changes with divine wisdom."""
    # Create trader with specific profile
    trader = ProfiledFuturesTrader(
        profile_type=profile_type,
        initial_capital=TestConfig.TEST_CAPITAL
    )
    
    # Set current price
    trader.current_price = TestConfig.TEST_PRICE
    
    # Capture initial psychological state
    initial_state = trader.state["emotional_state"]
    initial_confidence = trader.state["confidence"]
    
    # Simulate a profitable trade
    position = TradingPosition(
        direction="LONG",
        entry_price=TestConfig.TEST_PRICE * 0.95,
        size=1000.0,
        leverage=2.0,
        entry_time=datetime.now(),
        stop_loss=TestConfig.TEST_PRICE * 0.90,
        take_profit=[{"percentage": 1.0, "price": TestConfig.TEST_PRICE * 1.05}]
    )
    trader.positions.append(position)
    trader._close_position(position, "Take profit test")
    
    # Psychology should improve after winning trade
    assert trader.state["consecutive_wins"] == 1
    assert trader.state["consecutive_losses"] == 0
    assert trader.state["confidence"] >= initial_confidence
    
    # Simulate a losing trade
    trader.current_price = TestConfig.TEST_PRICE
    position = TradingPosition(
        direction="LONG",
        entry_price=TestConfig.TEST_PRICE * 1.05,
        size=1000.0,
        leverage=2.0,
        entry_time=datetime.now(),
        stop_loss=TestConfig.TEST_PRICE * 0.95
    )
    trader.positions.append(position)
    trader._close_position(position, "Stop loss test")
    
    # Psychology should deteriorate after losing trade
    assert trader.state["consecutive_wins"] == 0
    assert trader.state["consecutive_losses"] == 1
    assert trader.state["confidence"] <= initial_confidence
    
    # Profile-specific checks
    print(f"\n{GREEN}Testing {profile_type.upper()} psychological changes{RESET}")
    
    # Simulate multiple consecutive losses to test psychological resilience
    for i in range(4):
        position = TradingPosition(
            direction="LONG",
            entry_price=TestConfig.TEST_PRICE * 1.05,
            size=1000.0,
            leverage=2.0,
            entry_time=datetime.now(),
            stop_loss=TestConfig.TEST_PRICE * 0.95
        )
        trader.positions.append(position)
        trader._close_position(position, f"Consecutive loss #{i+1}")
    
    # After 5 consecutive losses, emotional state should be fearful
    assert trader.state["consecutive_losses"] == 5
    assert trader.state["emotional_state"] == "fearful"
    assert trader.state["confidence"] < 0.5  # Confidence should be below average
    
    # Print divine confirmation
    print(f"{GREEN}✓ {profile_type.capitalize()} trader shows divine psychological response:{RESET}")
    print(f"   Emotional state: {trader.state['emotional_state']}")
    print(f"   Confidence: {trader.state['confidence']:.2f}")
    print(f"   Consecutive losses: {trader.state['consecutive_losses']}")

@freeze_time(TestConfig.TEST_TIMEFRAME)
def test_trader_redis_integration(mock_redis):
    """🌿 Test divine trader data persistence in Redis."""
    # Patch redis.StrictRedis to use our mock
    with patch('redis.StrictRedis', return_value=mock_redis):
        # Create trader with strategic profile
        trader = ProfiledFuturesTrader(
            profile_type="strategic",
            initial_capital=TestConfig.TEST_CAPITAL
        )
        
        # Set current price
        trader.current_price = TestConfig.TEST_PRICE
        
        # Open a position
        trader.open_position("LONG", "Test Redis integration", 2)
        
        # Verify position was stored in Redis
        assert f"trader:positions:strategic" in mock_redis._list_data
        assert len(mock_redis._list_data[f"trader:positions:strategic"]) == 1
        
        # Make position profitable
        trader.current_price = TestConfig.TEST_PRICE * 1.05  # 5% increase
        position = trader.positions[0]
        trader._close_position(position, "Take profit test")
        
        # Verify trade result was stored in Redis
        assert f"trader:trades:strategic" in mock_redis._list_data
        assert len(mock_redis._list_data[f"trader:trades:strategic"]) == 1
        
        # Verify trader metrics were stored
        assert f"trader:metrics:strategic" in mock_redis._hash_data
        metrics = mock_redis._hash_data[f"trader:metrics:strategic"]
        assert "win_rate" in metrics
        assert "total_trades" in metrics
        assert "capital" in metrics
        assert "emotional_state" in metrics
        
        # Print divine confirmation
        print(f"\n{GREEN}✓ Strategic trader data blessed with divine Redis persistence{RESET}")
        print(f"   Stored positions: {len(mock_redis._list_data['trader:positions:strategic'])}")
        print(f"   Stored trades: {len(mock_redis._list_data['trader:trades:strategic'])}")
        print(f"   Stored metrics: {list(mock_redis._hash_data['trader:metrics:strategic'].keys())}")

@freeze_time(TestConfig.TEST_TIMEFRAME)
@pytest.mark.parametrize("profile_type", TestConfig.TEST_PROFILES)
def test_trader_decision_making(profile_type):
    """🌿 Test divine decision making processes per trader profile."""
    # Create trader with specific profile
    trader = ProfiledFuturesTrader(
        profile_type=profile_type,
        initial_capital=TestConfig.TEST_CAPITAL
    )
    
    # Mock the analyzer to return bullish signals
    with patch.object(trader, 'analyzer') as mock_analyzer:
        mock_analyzer.analyze_trading_opportunity.return_value = (True, "Strong bullish divergence", 3.0)
        
        # Test the decision-making process
        should_trade, reason, leverage = trader.should_open_position()
        
        # All profiles should consider the signal
        print(f"\n{GREEN}Testing {profile_type.upper()} decision making{RESET}")
        
        # Profile-specific assertions
        if profile_type == "strategic":
            # Strategic traders should stick close to the analyst recommendation
            assert leverage <= 3.0 * 1.2  # Should not increase leverage dramatically
        
        elif profile_type == "aggressive":
            # Aggressive traders tend to use higher leverage
            assert leverage >= 3.0
        
        elif profile_type == "newbie":
            # Newbies often make random decisions that may not align with analysis
            pass  # Hard to deterministically test randomness
        
        elif profile_type == "scalper":
            # Scalpers focus on short-term moves with higher leverage
            assert leverage >= 3.0
            
        # Print divine confirmation
        print(f"{GREEN}✓ {profile_type.capitalize()} trader makes decisions with divine wisdom:{RESET}")
        print(f"   Should trade: {should_trade}")
        print(f"   Reason: {reason}")
        print(f"   Leverage: {leverage}x")

@freeze_time(TestConfig.TEST_TIMEFRAME)
def test_linus_torvalds_blessing():
    """🐧🌿 Test that the trader profiles code receives the blessing of Linus Torvalds."""
    # This spiritual test checks if the code follows open source principles
    
    # Find the ProfiledFuturesTrader module
    module_path = os.path.join(project_root, "omega_ai", "trading", "profiled_futures_trader.py")
    file_exists = os.path.isfile(module_path)
    
    # Verify the module exists
    assert file_exists, "The profiled_futures_trader.py file should exist"
    
    # Read the file content
    with open(module_path, 'r') as f:
        content = f.read().lower()
    
    # Check for licensing
    has_license = any(term in content for term in ["license", "mit", "apache", "copyright"])
    assert has_license, "JAH BLESS - Code should have open source licensing"
    
    # Check for proper error handling
    has_error_handling = "try:" in content and "except" in content
    assert has_error_handling, "JAH BLESS - Code should handle errors with divine grace"
    
    # Check for proper documentation
    has_documentation = '"""' in content
    assert has_documentation, "JAH BLESS - Code should be well-documented"
    
    # Check for clean code practices
    clean_code_indicators = [
        "def " in content,  # Functions defined
        "class " in content,  # Classes defined
        ": " in content,     # Type hints
        "return " in content  # Return statements
    ]
    assert all(clean_code_indicators), "JAH BLESS - Code should follow clean coding practices"
    
    # Print divine confirmation
    print(f"\n{GREEN}✓ ProfiledFuturesTrader has received the divine blessing of Linus Torvalds{RESET}")
    print(f"{YELLOW}ONE LOVE, ONE HEART, ONE CODE{RESET}")

@freeze_time(TestConfig.TEST_TIMEFRAME)
@pytest.mark.parametrize("profile_type", TestConfig.TEST_PROFILES)
def test_trader_edge_cases(profile_type):
    """🌿 Test divine handling of extreme market conditions."""
    # Create trader with specific profile
    trader = ProfiledFuturesTrader(
        profile_type=profile_type,
        initial_capital=TestConfig.TEST_CAPITAL
    )
    
    # Test extreme price movements
    print(f"\n{GREEN}Testing {profile_type.upper()} edge cases{RESET}")
    
    # Test extreme volatility
    trader.update_price(TestConfig.TEST_PRICE)
    trader.open_position("LONG", "Test extreme volatility", 2)
    
    # Simulate extreme price movement
    trader.update_price(TestConfig.TEST_PRICE * 1.5)  # 50% increase
    trader.manage_open_positions()
    
    # Position should be closed with significant profit
    assert len(trader.positions) == 0
    assert trader.capital > TestConfig.TEST_CAPITAL
    
    # Test position size limits
    max_position_size = trader.capital * trader.max_leverage
    trader.open_position("LONG", "Test position size limit", max_position_size)
    assert len(trader.positions) == 1
    assert trader.positions[0].size <= max_position_size
    
    # Test multiple positions
    for _ in range(3):
        trader.open_position("LONG", "Test multiple positions", 1000.0)
    
    # Should respect max positions limit
    assert len(trader.positions) <= trader.max_positions
    
    print(f"{GREEN}✓ {profile_type.capitalize()} trader handles edge cases with divine grace{RESET}")

def update_price_safely(trader: ProfiledFuturesTrader, mock_redis_conn: MagicMock, price: float) -> None:
    """Update price safely, ensuring it's never 0.0."""
    if price <= 0:
        raise ValueError(f"Price must be positive, got {price}")
    mock_redis_conn.get.return_value = str(price)
    result = trader.update_current_price()
    if result <= 0:
        raise ValueError(f"Failed to update price to {price}")
    assert trader.current_price > 0, "Price update failed"

@freeze_time(TestConfig.TEST_TIMEFRAME)
def test_trader_performance_metrics(mock_redis_conn):
    """Test trader performance metrics calculation."""
    # Initialize trader with test configuration
    trader = ProfiledFuturesTrader(profile_type="strategic", initial_capital=TestConfig.INITIAL_CAPITAL)
    
    # Set initial price in Redis mock
    initial_price = float(TestConfig.TEST_PRICE)
    update_price_safely(trader, mock_redis_conn, initial_price)
    
    # Open a long position
    trader.open_position("LONG", "Test trade", leverage=1.0)
    
    # Simulate price movement up
    new_price = initial_price * 1.02  # 2% increase
    update_price_safely(trader, mock_redis_conn, new_price)
    
    # Close position with profit
    for pos in trader.positions:
        trader._close_position(pos, "Test close")  # Use internal method to handle TradingPosition
    
    # Open a short position
    update_price_safely(trader, mock_redis_conn, new_price)
    trader.open_position("SHORT", "Test trade", leverage=1.0)
    
    # Simulate price movement down
    final_price = new_price * 0.98  # 2% decrease
    update_price_safely(trader, mock_redis_conn, final_price)
    
    # Close position with profit
    for pos in trader.positions:
        trader._close_position(pos, "Test close")  # Use internal method to handle TradingPosition
    
    # Verify performance metrics
    assert trader.win_rate > 0.0, "Win rate should be positive"
    assert trader.total_pnl > 0.0, "Total PnL should be positive"
    assert trader.calculate_sharpe_ratio() >= 0.0, "Sharpe ratio should be non-negative"
    assert trader.calculate_max_drawdown() >= 0.0, "Max drawdown should be non-negative"

@freeze_time(TestConfig.TEST_TIMEFRAME)
def test_trader_error_handling(mock_redis_conn):
    """Test trader error handling for invalid inputs."""
    trader = ProfiledFuturesTrader(profile_type="strategic", initial_capital=TestConfig.INITIAL_CAPITAL)
    
    # Set initial price in Redis mock
    initial_price = float(TestConfig.TEST_PRICE)
    update_price_safely(trader, mock_redis_conn, initial_price)
    
    # Test invalid position size
    with pytest.raises(Exception):
        trader.open_position("LONG", "Invalid size", leverage=-1.0)
    
    # Test invalid direction
    with pytest.raises(Exception):
        trader.open_position("INVALID", "Invalid direction", leverage=1.0)
    
    # Test excessive leverage
    with pytest.raises(Exception):
        trader.open_position("LONG", "Excessive leverage", leverage=101.0)
        
    # Test invalid price update
    with pytest.raises(ValueError):
        update_price_safely(trader, mock_redis_conn, 0.0)
        
    # Test Redis error handling
    mock_redis_conn.get.return_value = None
    with pytest.raises(ValueError):
        update_price_safely(trader, mock_redis_conn, initial_price)
        
    mock_redis_conn.get.side_effect = redis.RedisError("Connection error")
    with pytest.raises(ValueError):
        update_price_safely(trader, mock_redis_conn, initial_price)
        
    # Test price update with invalid string
    mock_redis_conn.get.side_effect = None
    mock_redis_conn.get.return_value = "invalid_price"
    with pytest.raises(ValueError):
        update_price_safely(trader, mock_redis_conn, initial_price)
        
    # Test direct price update
    with pytest.raises(ValueError):
        trader.update_price(0.0)
        
    with pytest.raises(ValueError):
        trader.update_price(-1.0)
        
    # Test successful price update
    trader.update_price(initial_price)
    assert trader.current_price == initial_price, "Price update failed"
    
    # Test price update with None
    with pytest.raises(ValueError):
        trader.update_price(None)
        
    # Test price update with invalid type
    with pytest.raises(ValueError):
        trader.update_price("invalid_price")

if __name__ == "__main__":
    # Running this file directly will execute the tests with divine energy
    import pytest
    pytest.main(["-xvs", __file__])