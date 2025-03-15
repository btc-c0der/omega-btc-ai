import json
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import random
import pytest_asyncio
import redis.asyncio as redis
import requests

from omega_ai.alerts.telegram_market_report import TelegramMarketReporter

# ✅ Divine Test Constants
TEST_PRICE = 87654.32
TEST_PREV_PRICE = 86543.21
TEST_CHANGE_PCT = 1.28
TEST_VOLUME = 0.00214
TEST_CONFIG = {
    'telegram_token': 'test_token',
    'telegram_chat_id': '-1002510049870',
    'redis_host': 'localhost',
    'redis_port': 6379,
    'redis_db': 0,
    'report_interval': 300,
    'debug_mode': True,
    'schumann_enabled': True,  # Enable Schumann resonance integration
    'bio_energy_tracking': True,  # Enable bio-energy state tracking
    'divine_timing': True  # Enable divine timing features
}

# ✅ Test Data for Redis Mock
TEST_MARKET_TRENDS = {
    "1min": "Strongly Bullish",
    "5min": "Moderately Bullish",
    "15min": "Slightly Bearish",
    "1h": "Neutral",
    "4h": "Moderately Bearish"
}

# ✅ Test Movement Data
TEST_MOVEMENT_DATA = {
    "classification": "Stable",
    "stored_price": 11.85,
    "volume": TEST_VOLUME,
    "bias": "Strongly Bullish",
    "signals": {
        "bullish": 3,
        "bearish": 1,
        "sideways": 12
    }
}

# ✅ Divine Bio-Energy States
TEST_BIO_ENERGY_STATES = {
    "vibration_level": 0.85,
    "energy_flow": "HARMONIOUS",
    "market_consciousness": "ELEVATED",
    "confidence_score": 0.92,
    "timestamp": datetime.now().isoformat()
}

# ✅ Schumann Resonance Data
TEST_SCHUMANN_DATA = {
    "base_frequency": 7.83,
    "current_frequency": 7.92,
    "market_harmony": 0.88,
    "resonance_state": "ALIGNED",
    "timestamp": datetime.now().isoformat()
}

# ✅ Divine Market Patterns
TEST_DIVINE_PATTERNS = [
    {
        "name": "GOLDEN RATIO CONFLUENCE",
        "confidence": 0.89,
        "description": "Price approaching major golden ratio level",
        "suggested_action": "OBSERVE WITH DIVINE PATIENCE"
    },
    {
        "name": "FIBONACCI SPIRAL",
        "confidence": 0.78,
        "description": "Formation of ascending Fibonacci spiral",
        "suggested_action": "ALIGN WITH NATURAL FLOW"
    }
]

# ✅ Market Rhythm Data
TEST_MARKET_RHYTHM = {
    "cycle_length": 144,  # Fibonacci number
    "phase": "ACCUMULATION",
    "confidence": 0.83,
    "next_peak": (datetime.now() + timedelta(minutes=89)).isoformat(),  # Fibonacci number
    "harmony_score": 0.618  # Golden ratio
}

TEST_FIBONACCI_LEVELS = {
    "0.236": TEST_PRICE * 0.9,
    "0.382": TEST_PRICE * 0.95,
    "0.5": TEST_PRICE * 0.98,
    "0.618": TEST_PRICE * 1.02,  # Golden ratio level
    "0.786": TEST_PRICE * 1.05,
    "timestamp": datetime.now().isoformat()
}

TEST_MM_TRAPS = [
    {
        "type": "Liquidity Grab",
        "confidence": "0.85",
        "price": str(TEST_PRICE),
        "change": "0.025",
        "timestamp": datetime.now().isoformat()
    },
    {
        "type": "Fake Pump",
        "confidence": "0.72",
        "price": str(TEST_PRICE - 1000),
        "change": "0.018",
        "timestamp": datetime.now().isoformat()
    }
]

# ✅ Rasta Market Wisdom
TEST_RASTA_WISDOM = [
    "JAH BLESS THE RIGHTEOUS TRADER WHO FOLLOWS THE GOLDEN RATIO",
    "WHEN BABYLON SYSTEM TRIES TO SHAKE YOU OUT, HOLD FIRM WITH DIVINE CONVICTION",
    "THE NATURAL VIBRATION OF THE MARKET REVEALS THE TRUTH TO THE PATIENT OBSERVER",
    "ONE LOVE, ONE HEART, ONE BLOCKCHAIN - TRUST IN THE DIVINE PATTERN"
]

# ✅ Pytest Fixtures
@pytest_asyncio.fixture
async def mock_redis():
    """Mock Redis with test data."""
    redis_mock = MagicMock(spec=redis.Redis)
    
    # Configure redis mock to return test data
    async def get_side_effect(key):
        if key == "last_btc_price":
            return str(TEST_PRICE)
        elif key == "prev_btc_price":
            return str(TEST_PREV_PRICE)
        elif key == "current_market_regime":
            return "BULLISH"
        elif key == "schumann_resonance":
            return str(TEST_SCHUMANN_DATA["current_frequency"])
        elif key == "market_consciousness":
            return TEST_BIO_ENERGY_STATES["market_consciousness"]
        elif key == "bio_energy_state":
            return json.dumps(TEST_BIO_ENERGY_STATES)
        elif key == "market_rhythm":
            return json.dumps(TEST_MARKET_RHYTHM)
        elif key == "divine_patterns":
            return json.dumps(TEST_DIVINE_PATTERNS)
        elif key == "movement_data":
            return json.dumps(TEST_MOVEMENT_DATA)
        elif key.startswith("latest_trend_"):
            timeframe = key.replace("latest_trend_", "")
            return TEST_MARKET_TRENDS.get(timeframe, "Neutral")
        elif key == "rasta_wisdom":
            return random.choice(TEST_RASTA_WISDOM)
        return None

    redis_mock.get.side_effect = get_side_effect
    
    # Configure hgetall for various data structures
    async def hgetall_side_effect(key):
        if key == "current_fibonacci_levels":
            return TEST_FIBONACCI_LEVELS
        elif key == "schumann_data":
            return TEST_SCHUMANN_DATA
        elif key == "bio_energy_state":
            return TEST_BIO_ENERGY_STATES
        elif key == "market_rhythm":
            return TEST_MARKET_RHYTHM
        elif key == "mm_trap:12345":
            return TEST_MM_TRAPS[0]
        elif key == "mm_trap:67890":
            return TEST_MM_TRAPS[1]
        return {}

    redis_mock.hgetall.side_effect = hgetall_side_effect
    
    # Configure scan for MM traps and divine patterns
    async def scan_side_effect(cursor, match, count=None):
        if match == "mm_trap:*":
            return (0, ["mm_trap:12345", "mm_trap:67890"])
        elif match == "divine_pattern:*":
            return (0, ["divine_pattern:1", "divine_pattern:2"])
        return (0, [])

    redis_mock.scan.side_effect = scan_side_effect
    
    return redis_mock

@pytest_asyncio.fixture
async def market_reporter(mock_redis):
    """Create a TelegramMarketReporter with mocks."""
    with patch('redis.asyncio.Redis', return_value=mock_redis):
        reporter = TelegramMarketReporter(TEST_CONFIG)
        await reporter.initialize()
        yield reporter

# ✅ Divine Tests for Data Retrieval Functions
class TestMarketReporterDataRetrieval:
    """Test data retrieval functions of the TelegramMarketReporter."""
    
    @pytest.mark.asyncio
    async def test_get_market_data(self, market_reporter, mock_redis):
        """Test getting market data from Redis."""
        price, schumann = await market_reporter.get_market_data()
        assert price == TEST_PRICE
        assert schumann == TEST_SCHUMANN_DATA["current_frequency"]
    
    @pytest.mark.asyncio
    async def test_get_market_trends(self, market_reporter, mock_redis):
        """Test retrieving market trends for multiple timeframes."""
        trends = await market_reporter.get_market_trends()
        assert trends == TEST_MARKET_TRENDS
        assert "1min" in trends
        assert "5min" in trends
        assert trends["1min"] == "Strongly Bullish"
    
    @pytest.mark.asyncio
    async def test_movement_classification(self, market_reporter, mock_redis):
        """Test movement classification and metrics."""
        summary = await market_reporter.get_market_summary()
        
        # Check movement metrics are present
        assert "Overall Market Bias: Strongly Bullish" in summary
        assert "Signal Distribution: Bullish(3) Bearish(1) Sideways(12)" in summary
        assert f"Stored Movement: Stable (${TEST_MOVEMENT_DATA['stored_price']:.2f})" in summary
        assert f"Volume: {TEST_VOLUME:.5f} BTC" in summary
        assert "Movement Classification: Stable" in summary
    
    @pytest.mark.asyncio
    async def test_market_metrics_format(self, market_reporter, mock_redis):
        """Test market metrics log format."""
        summary = await market_reporter.get_market_summary()
        
        # Check log-style formatting
        assert "$ tail -f /var/log/market-metrics.log" in summary
        assert "[" in summary and "] Overall Market Bias:" in summary
        assert "✅ [DEBUG]" in summary
    
    @pytest.mark.asyncio
    async def test_get_fibonacci_levels(self, market_reporter, mock_redis):
        """Test retrieving Fibonacci levels from Redis."""
        levels = await market_reporter.get_fibonacci_levels()
        assert isinstance(levels, dict)
        assert "0.618" in levels  # Golden ratio must be present
    
    @pytest.mark.asyncio
    async def test_get_market_regime(self, market_reporter, mock_redis):
        """Test retrieving market regime from Redis."""
        regime = await market_reporter.get_market_regime()
        assert regime == "BULLISH"
    
    @pytest.mark.asyncio
    async def test_missing_fibonacci_levels(self, market_reporter, mock_redis):
        """Test behavior when Fibonacci levels are missing."""
        mock_redis.hgetall.return_value = {}
        levels = await market_reporter.get_fibonacci_levels()
        assert levels == {}  # Should return empty dict, not fail
    
    @pytest.mark.asyncio
    async def test_get_mm_traps(self, market_reporter, mock_redis):
        """Test retrieving MM traps from Redis."""
        traps = await market_reporter.get_mm_traps()
        assert len(traps) > 0
        assert traps[0]["type"] == "Liquidity Grab"
        assert "confidence" in traps[0]

# ✅ Divine Tests for Formatting Functions
class TestMarketReporterFormatting:
    """Test formatting functions of the TelegramMarketReporter."""
    
    def test_format_trend_insights(self, market_reporter):
        """Test formatting trend insights with emojis."""
        trends = {
            "1min": "Strongly Bullish",
            "5min": "Moderately Bearish",
            "15min": "Neutral"
        }
        result = market_reporter.format_trend_insights(trends)
        assert "🚀" in result  # Strong bull emoji
        assert "🔻" in result  # Bear emoji
        assert "➡️" in result  # Neutral emoji
        assert "*1min*" in result  # Markdown formatting
        assert "Strongly Bullish" in result
    
    def test_format_fibonacci_levels(self, market_reporter):
        """Test formatting Fibonacci levels with proximity indicators."""
        fib_levels = {
            "0.236": 80000.0,
            "0.382": 82000.0,
            "0.5": 85000.0,
            "0.618": 88000.0,  # Closest to TEST_PRICE
            "0.786": 92000.0
        }
        result = market_reporter.format_fibonacci_levels(fib_levels, TEST_PRICE)
        assert "0.618" in result  # Golden ratio must be present
        assert "👈" in result  # Pointer to closest level
        assert "% away" in result  # Shows proximity
    
    def test_format_fibonacci_levels_empty(self, market_reporter):
        """Test formatting empty Fibonacci levels."""
        result = market_reporter.format_fibonacci_levels({}, TEST_PRICE)
        assert "_No Fibonacci levels available_" in result  # Fallback message
    
    def test_format_mm_traps(self, market_reporter):
        """Test formatting MM trap information."""
        result = market_reporter.format_mm_traps(TEST_MM_TRAPS)
        assert "Liquidity Grab" in result
        assert "Fake Pump" in result
        assert "★" in result  # Confidence stars
        assert str(TEST_PRICE) in result  # Formatted price

# ✅ Divine Tests for Report Generation and Sending
class TestMarketReporterSending:
    """Test report generation and sending functionality."""
    
    @pytest.mark.asyncio
    async def test_generate_market_summary(self, market_reporter):
        """Test generating a comprehensive market summary."""
        summary = await market_reporter.get_market_summary()
        assert "OMEGA BTC AI DIVINE REPORT" in summary
        assert "BTC Price" in summary
        assert "FIBONACCI LEVELS" in summary
        assert "MULTI-TIMEFRAME TRENDS" in summary
        assert "RECENT MM TRAP DETECTIONS" in summary
    
    @pytest.mark.asyncio
    @patch('omega_ai.alerts.telegram_market_report.RastaVibes')
    async def test_generate_divine_market_report(self, mock_rasta_vibes, market_reporter):
        """Test generating a divine market report with RastaVibes enhancement."""
        mock_rasta_vibes.enhance_alert.return_value = "ENHANCED REPORT"
        report = await market_reporter.generate_divine_market_report()
        assert "ENHANCED REPORT" in report
        mock_rasta_vibes.enhance_alert.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_telegram_message(self, market_reporter):
        """Test sending a message to Telegram."""
        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_post.return_value.__aenter__.return_value.status = 200
            result = await market_reporter.send_telegram_message("Test message")
            assert result is True
    
    @pytest.mark.asyncio
    async def test_send_telegram_error(self, market_reporter):
        """Test handling Telegram API errors."""
        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_post.return_value.__aenter__.return_value.status = 400
            mock_post.return_value.__aenter__.return_value.text = lambda: "Bad Request"
            result = await market_reporter.send_telegram_message("Test message")
            assert result is False

# ✅ Divine Tests for Schumann Resonance Integration
class TestSchumannResonanceIntegration:
    """Test the integration of Schumann resonance with market analysis."""
    
    @pytest.mark.asyncio
    async def test_schumann_resonance_retrieval(self, market_reporter, mock_redis):
        """Test retrieving current Schumann resonance frequency."""
        resonance = await market_reporter.get_schumann_resonance()
        assert float(resonance) == TEST_SCHUMANN_DATA["current_frequency"]
    
    @pytest.mark.asyncio
    async def test_market_schumann_alignment(self, market_reporter):
        """Test market alignment with Schumann resonance."""
        alignment = await market_reporter.check_schumann_market_alignment()
        assert isinstance(alignment, dict)
        assert "resonance_state" in alignment
        assert "market_harmony" in alignment
        assert "suggested_action" in alignment
    
    @pytest.mark.asyncio
    async def test_schumann_alert_enhancement(self, market_reporter):
        """Test enhancement of alerts with Schumann resonance data."""
        alert = await market_reporter.enhance_alert_with_schumann("Test alert")
        assert "Schumann Resonance" in alert
        assert "Market Harmony" in alert
        assert "🌿" in alert  # Spiritual alignment indicator

# ✅ Divine Tests for Bio-Energy Market States
class TestBioEnergyMarketStates:
    """Test bio-energetic market state analysis and reporting."""
    
    @pytest.mark.asyncio
    async def test_bio_energy_state_calculation(self, market_reporter):
        """Test calculation of market's bio-energy state."""
        energy_state = await market_reporter.calculate_bio_energy_state()
        assert isinstance(energy_state, dict)
        assert "vibration_level" in energy_state
        assert "energy_flow" in energy_state
        assert "market_consciousness" in energy_state
    
    @pytest.mark.asyncio
    async def test_market_consciousness_levels(self, market_reporter):
        """Test market consciousness level detection."""
        consciousness = await market_reporter.get_market_consciousness()
        assert consciousness in ["ELEVATED", "BALANCED", "SEEKING", "TRANSITIONING"]
    
    @pytest.mark.asyncio
    async def test_bio_energy_report_formatting(self, market_reporter):
        """Test formatting of bio-energy market reports."""
        report = await market_reporter.format_bio_energy_report()
        assert "🌟 BIO-ENERGY STATE" in report
        assert "Market Consciousness" in report
        assert "Energy Flow" in report
        assert "Divine Guidance" in report

# ✅ Divine Tests for Enhanced RastaVibes Integration
class TestEnhancedRastaVibes:
    """Test enhanced Rastafarian message generation and spiritual alignment."""
    
    @pytest.mark.asyncio
    async def test_rasta_market_wisdom(self, market_reporter):
        """Test generation of Rasta market wisdom."""
        wisdom = await market_reporter.get_rasta_market_wisdom()
        assert wisdom.startswith("JAH BLESS")
        assert "DIVINE MARKET" in wisdom
        assert wisdom.endswith("ONE LOVE 🌿")
    
    @pytest.mark.asyncio
    async def test_divine_pattern_recognition(self, market_reporter):
        """Test recognition of divine market patterns."""
        patterns = await market_reporter.identify_divine_patterns()
        assert isinstance(patterns, list)
        assert all(p["confidence"] >= 0.7 for p in patterns)
        assert any("GOLDEN RATIO" in p["name"] for p in patterns)

# ✅ Divine Tests for Market Harmony Patterns
class TestMarketHarmonyPatterns:
    """Test detection and reporting of harmonic market patterns."""
    
    @pytest.mark.asyncio
    async def test_fibonacci_harmony_detection(self, market_reporter):
        """Test detection of Fibonacci harmony in price movements."""
        harmony = await market_reporter.detect_fibonacci_harmony()
        assert isinstance(harmony, dict)
        assert "harmony_level" in harmony
        assert "golden_ratio_alignment" in harmony
        assert harmony["confidence"] >= 0.0
    
    @pytest.mark.asyncio
    async def test_divine_timing_analysis(self, market_reporter):
        """Test analysis of divine market timing."""
        timing = await market_reporter.analyze_divine_timing()
        assert isinstance(timing, dict)
        assert "cycle_phase" in timing
        assert "next_alignment" in timing
        assert "confidence" in timing
    
    @pytest.mark.asyncio
    async def test_market_vibration_analysis(self, market_reporter):
        """Test analysis of market vibration patterns."""
        vibrations = await market_reporter.analyze_market_vibrations()
        assert isinstance(vibrations, dict)
        assert "frequency" in vibrations
        assert "amplitude" in vibrations
        assert "harmony_score" in vibrations
        assert 0.0 <= vibrations["harmony_score"] <= 1.0

# ✅ Divine Tests for Alert Timing
class TestDivineAlertTiming:
    """Test divine timing of market alerts."""
    
    @pytest.mark.asyncio
    async def test_schumann_cycle_alignment(self, market_reporter):
        """Test alignment with Schumann resonance cycles."""
        alignment = await market_reporter.check_schumann_cycle_alignment()
        assert isinstance(alignment, float)
        assert 0.0 <= alignment <= 1.0
    
    @pytest.mark.asyncio
    async def test_market_rhythm_detection(self, market_reporter):
        """Test detection of natural market rhythms."""
        rhythm = await market_reporter.detect_market_rhythm()
        assert isinstance(rhythm, dict)
        assert "cycle_length" in rhythm
        assert "phase" in rhythm
        assert "confidence" in rhythm
        assert 0.0 <= rhythm["confidence"] <= 1.0