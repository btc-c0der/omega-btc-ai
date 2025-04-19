
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
Test suite for the OMEGA RASTA FIBONACCI ALERT SYSTEM 🌟

JAH BLESS THE TESTING! 🔥
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
from omega_ai.alerts.omega_rasta_alerts import OmegaRastaAlerts

@pytest.fixture
def mock_telegram_config():
    return {
        "bot_token": "test_token",
        "chat_id": "test_chat_id"
    }

@pytest.fixture
def mock_smtp_config():
    return {
        "host": "smtp.test.com",
        "port": 587,
        "username": "test_user",
        "password": "test_pass",
        "from_email": "test@test.com",
        "to_email": "alerts@test.com"
    }

@pytest.fixture
def mock_webhook_config():
    return {
        "url": "https://test.webhook.com",
        "secret": "test_secret",
        "enabled": True
    }

@pytest.fixture
def alert_system(mock_telegram_config, mock_smtp_config, mock_webhook_config):
    return OmegaRastaAlerts(
        telegram_config=mock_telegram_config,
        smtp_config=mock_smtp_config,
        webhook_config=mock_webhook_config
    )

@pytest.mark.asyncio
async def test_fibonacci_confidence_calculation(alert_system):
    """Test the AI-enhanced Fibonacci confidence calculation"""
    # Test perfect alignment
    confidence = alert_system.calculate_fibonacci_confidence(
        level_price=100.0,
        current_price=100.0,
        volume=2000.0,
        market_trend="strong_bullish"
    )
    assert confidence > 0.9
    
    # Test with price deviation
    confidence = alert_system.calculate_fibonacci_confidence(
        level_price=100.0,
        current_price=101.0,
        volume=2000.0,
        market_trend="strong_bullish"
    )
    assert 0.7 < confidence < 0.9
    
    # Test with low volume
    confidence = alert_system.calculate_fibonacci_confidence(
        level_price=100.0,
        current_price=100.0,
        volume=100.0,
        market_trend="strong_bullish"
    )
    assert confidence < 0.8

@pytest.mark.asyncio
async def test_alert_cooldown_adjustment(alert_system):
    """Test dynamic alert cooldown adjustment"""
    # Test high volatility
    alert_system.adjust_alert_cooldown(volatility=2.5, trend="neutral")
    assert alert_system.alert_cooldown == 900  # 15 minutes
    
    # Test medium volatility
    alert_system.adjust_alert_cooldown(volatility=1.5, trend="neutral")
    assert alert_system.alert_cooldown == 1800  # 30 minutes
    
    # Test low volatility
    alert_system.adjust_alert_cooldown(volatility=0.5, trend="neutral")
    assert alert_system.alert_cooldown == 3600  # 1 hour
    
    # Test strong trend adjustment
    alert_system.adjust_alert_cooldown(volatility=0.5, trend="strong_bullish")
    assert alert_system.alert_cooldown == 3300  # 55 minutes

@pytest.mark.asyncio
async def test_telegram_commands(alert_system):
    """Test Telegram command handling"""
    # Test Fibonacci status command
    response = await alert_system.handle_telegram_command("/fibonacci_status", 123456)
    assert response is not None
    assert "FIBONACCI LEVELS" in response
    
    # Test MM traps command
    response = await alert_system.handle_telegram_command("/mm_traps", 123456)
    assert response is not None
    assert "MARKET MAKER TRAPS" in response
    
    # Test Schumann status command
    response = await alert_system.handle_telegram_command("/schumann_status", 123456)
    assert response is not None
    assert "SCHUMANN RESONANCE" in response
    
    # Test help command
    response = await alert_system.handle_telegram_command("/help", 123456)
    assert response is not None
    assert "COMMANDS" in response
    
    # Test unknown command
    response = await alert_system.handle_telegram_command("/unknown", 123456)
    assert response is None

@pytest.mark.asyncio
async def test_webhook_alerts(alert_system):
    """Test webhook alert sending"""
    alert_data = {
        "type": "test_alert",
        "message": "Test message",
        "priority": "normal"
    }
    
    with patch("aiohttp.ClientSession") as mock_session:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
        
        await alert_system.send_webhook_alert(alert_data)
        
        # Verify webhook was called with correct data
        mock_session.return_value.__aenter__.return_value.post.assert_called_once()
        call_args = mock_session.return_value.__aenter__.return_value.post.call_args
        assert "test.webhook.com" in call_args[0][0]
        assert "X-Webhook-Signature" in call_args[1]["headers"]

@pytest.mark.asyncio
async def test_alert_history(alert_system):
    """Test alert history tracking"""
    # Send some test alerts
    await alert_system.send_alert("Test alert 1", "test_type_1")
    await alert_system.send_alert("Test alert 2", "test_type_2")
    
    # Get history
    history = alert_system.get_alert_history()
    assert len(history) == 2
    assert history[0]["message"] == "Test alert 2"  # Most recent first
    assert history[1]["message"] == "Test alert 1"
    
    # Test limit
    history = alert_system.get_alert_history(limit=1)
    assert len(history) == 1
    assert history[0]["message"] == "Test alert 2"

@pytest.mark.asyncio
async def test_alert_cooldown(alert_system):
    """Test alert cooldown functionality"""
    # Send first alert
    await alert_system.send_alert("Test alert", "test_type")
    
    # Try to send another alert immediately
    await alert_system.send_alert("Test alert 2", "test_type")
    
    # Verify only one alert was sent
    history = alert_system.get_alert_history()
    assert len(history) == 1
    
    # Move time forward past cooldown
    alert_system.last_alert_time["test_type"] = datetime.now() - timedelta(hours=2)
    
    # Try to send another alert
    await alert_system.send_alert("Test alert 3", "test_type")
    
    # Verify new alert was sent
    history = alert_system.get_alert_history()
    assert len(history) == 2

@pytest.mark.asyncio
async def test_fibonacci_alerts(alert_system):
    """Test Fibonacci level alerts"""
    with patch("omega_ai.monitor.monitor_market_trends.get_current_fibonacci_levels") as mock_get_levels:
        # Mock Fibonacci levels
        mock_get_levels.return_value = {
            "61.8%": 100.0,
            "38.2%": 90.0,
            "50%": 95.0,
            "78.6%": 110.0
        }
        
        # Test Golden Ratio alert
        await alert_system.check_fibonacci_alerts(current_price=100.0, volume=2000.0)
        history = alert_system.get_alert_history()
        assert any("GOLDEN RATIO ALERT" in alert["message"] for alert in history)
        
        # Test other Fibonacci levels
        await alert_system.check_fibonacci_alerts(current_price=90.0, volume=2000.0)
        history = alert_system.get_alert_history()
        assert any("FIBONACCI LEVEL ALERT" in alert["message"] for alert in history)

@pytest.mark.asyncio
async def test_mm_trap_alerts(alert_system):
    """Test market maker trap alerts"""
    with patch("omega_ai.monitor.monitor_market_trends.detect_possible_mm_traps") as mock_detect:
        # Mock trap detection
        mock_detect.return_value = ("liquidity_grab", 0.85)
        
        await alert_system.check_mm_trap_alerts(
            timeframe="1h",
            trend="bullish",
            price_change=2.5,
            price_move=100.0
        )
        
        history = alert_system.get_alert_history()
        assert any("MARKET MAKER TRAP ALERT" in alert["message"] for alert in history)
        assert any("liquidity_grab" in alert["message"].lower() for alert in history)

@pytest.mark.asyncio
async def test_schumann_alignment(alert_system):
    """Test Schumann resonance alignment alerts"""
    # Test perfect alignment
    await alert_system.check_schumann_alignment(7.83)
    history = alert_system.get_alert_history()
    assert any("COSMIC ALIGNMENT ALERT" in alert["message"] for alert in history)
    
    # Test slight deviation
    await alert_system.check_schumann_alignment(7.90)
    history = alert_system.get_alert_history()
    assert any("COSMIC ALIGNMENT ALERT" in alert["message"] for alert in history)
    
    # Test large deviation
    await alert_system.check_schumann_alignment(8.00)
    history = alert_system.get_alert_history()
    assert not any("COSMIC ALIGNMENT ALERT" in alert["message"] for alert in history) 