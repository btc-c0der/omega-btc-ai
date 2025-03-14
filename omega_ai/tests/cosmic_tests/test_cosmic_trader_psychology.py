#!/usr/bin/env python3

"""
DIVINE COSMIC TRADER PSYCHOLOGY TESTS 🌿🔥

"In the multitude of dreams and many words, there is also vanity. But fear thou God."
- Ecclesiastes 5:7 with Rastafarian wisdom

These sacred tests verify the divine cosmic influences on trader psychology,
ensuring the holy alignment between natural market rhythms and trader consciousness.

JAH BLESS THIS COSMIC CONSCIOUSNESS! 🙏🌟
"""

import os
import sys
import pytest
import json
import random
import datetime
from unittest.mock import patch, MagicMock
from freezegun import freeze_time

# Add project root to path for divine module accessibility
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from omega_ai.trading.cosmic_trader_psychology import (
    CosmicTraderPsychology, CosmicInfluences,
    MoonPhase, SchumannFrequency, MarketLiquidity, GlobalSentiment, EmotionalState
)

# Terminal colors for divine output
RED = "\033[91m"
GREEN = "\033[92m" 
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# =============== DIVINE TEST FIXTURES ===============

@pytest.fixture
def strategic_trader():
    """Create a blessed strategic trader with cosmic consciousness."""
    return CosmicTraderPsychology(profile_type="strategic", initial_state="neutral")

@pytest.fixture
def aggressive_trader():
    """Create a divine aggressive trader with cosmic consciousness."""
    return CosmicTraderPsychology(profile_type="aggressive", initial_state="confident")

@pytest.fixture
def newbie_trader():
    """Create a novice trader awaiting cosmic enlightenment."""
    return CosmicTraderPsychology(profile_type="newbie", initial_state="euphoric")

@pytest.fixture
def scalper_trader():
    """Create a quick-moving scalper trader with cosmic consciousness."""
    return CosmicTraderPsychology(profile_type="scalper", initial_state="neutral")

# =============== DIVINE TEST CASES ===============

def test_cosmic_trader_initialization():
    """🌿 Test divine initialization of cosmic trader psychology."""
    # Verify each profile has unique divine characteristics
    for profile_type in ["strategic", "aggressive", "newbie", "scalper"]:
        trader = CosmicTraderPsychology(profile_type=profile_type)
        
        # Print divine initialization
        print(f"\n{GREEN}Testing {profile_type.upper()} cosmic initialization{RESET}")
        print(f"Emotional state: {trader.emotional_state}")
        print(f"Confidence: {trader.confidence:.2f}")
        print(f"Risk appetite: {trader.risk_appetite:.2f}")
        print(f"Divine connection: {trader.divine_connection:.2f}")
        
        # Verify profile-specific cosmic attributes
        assert hasattr(trader, "emotional_state")
        assert hasattr(trader, "cosmic")
        assert hasattr(trader, "susceptibilities")
        
        # Verify cosmic susceptibilities are profile-specific
        assert trader.susceptibilities["lunar"] >= 0.0
        assert trader.susceptibilities["schumann"] >= 0.0
        
        # Verify profile-specific settings
        if profile_type == "newbie":
            # Newbies are highly susceptible to cosmic influences
            assert trader.susceptibilities["lunar"] > 0.7
            assert trader.susceptibilities["mercury"] > 0.7
        elif profile_type == "strategic":
            # Strategic traders are less affected by emotional cosmic forces
            assert trader.discipline > 0.7
            assert trader.susceptibilities["lunar"] < 0.5

def test_moon_phase_influence(strategic_trader):
    """🌙 Test divine influence of moon phases on trading psychology."""
    trader = strategic_trader
    
    # Test each moon phase influence
    print(f"\n{YELLOW}Testing MOON PHASE influences on trader psychology{RESET}")
    
    for phase in MoonPhase:
        # Set moon phase and baseline attributes
        trader.cosmic.moon_phase = phase
        baseline_confidence = trader.confidence = 0.5
        baseline_risk = trader.risk_appetite = 0.5
        
        # Apply cosmic influences
        trader._apply_cosmic_influences()
        
        # Print divine moon influence
        print(f"{CYAN}Moon phase {phase.value}:{RESET}")
        print(f"  Confidence: {baseline_confidence:.2f} → {trader.confidence:.2f}")
        print(f"  Risk appetite: {baseline_risk:.2f} → {trader.risk_appetite:.2f}")
        
        # Verify each moon phase has appropriate influence
        if phase == MoonPhase.FULL_MOON:
            # Full moon should affect emotional intensity
            moon_influence = trader.cosmic.get_moon_influence()
            assert moon_influence[0] == "emotional_intensity"
            assert moon_influence[1] > 0.0
        elif phase == MoonPhase.NEW_MOON:
            # New moon should enhance insight for strategic traders
            assert trader.insight_level > 0.5

def test_schumann_frequency_influence(scalper_trader):
    """🌿 Test divine Schumann frequency influence on trading psychology."""
    trader = scalper_trader
    
    # Test each frequency level
    print(f"\n{MAGENTA}Testing SCHUMANN FREQUENCY influences on trader psychology{RESET}")
    
    for freq in SchumannFrequency:
        # Set frequency and baseline attributes
        trader.cosmic.schumann_frequency = freq
        baseline_risk = trader.risk_appetite = 0.5
        baseline_patience = trader.patience = 0.5
        baseline_intuition = trader.intuition = 0.5
        
        # Apply cosmic influences
        trader._apply_cosmic_influences()
        
        # Print divine schumann influence
        print(f"{BLUE}Schumann frequency {freq.value}:{RESET}")
        print(f"  Risk appetite: {baseline_risk:.2f} → {trader.risk_appetite:.2f}")
        print(f"  Patience: {baseline_patience:.2f} → {trader.patience:.2f}")
        print(f"  Intuition: {baseline_intuition:.2f} → {trader.intuition:.2f}")
        
        # Verify each frequency has appropriate influence
        if freq == SchumannFrequency.VERY_HIGH:
            # High frequency should increase risk and intuition for scalpers
            assert trader.intuition > baseline_intuition
        elif freq == SchumannFrequency.VERY_LOW:
            # Low frequency should promote caution
            schumann_influence = trader.cosmic.get_schumann_influence()
            assert schumann_influence[0] == "cautious"
            assert schumann_influence[1] < 0.0

@freeze_time("2025-03-15 12:00:00")
def test_trader_emotional_state_transitions(aggressive_trader):
    """🔥 Test divine emotional state transitions from trade results."""
    trader = aggressive_trader
    
    # Initial emotional state
    initial_state = trader.emotional_state
    print(f"\n{GREEN}Testing emotional transitions from {initial_state}{RESET}")
    
    # Simulate consecutive wins and check emotional states
    print(f"\n{CYAN}Simulating winning streak:{RESET}")
    for i in range(4):
        # Update after winning trade (100 pip profit, 10 minute trade)
        profit = 100.0
        trader.update_after_trade(profit, 10.0)
        print(f"Win #{i+1}: {trader.emotional_state} (confidence: {trader.confidence:.2f})")
        
        # After 3+ consecutive wins, aggressive traders should become greedy or euphoric
        if i >= 2:
            assert trader.emotional_state in [
                EmotionalState.GREEDY.value,
                EmotionalState.EUPHORIC.value, 
                EmotionalState.CONFIDENT.value
            ]
    
    # Simulate consecutive losses and check emotional states
    print(f"\n{RED}Simulating losing streak:{RESET}")
    for i in range(6):
        # Update after losing trade (-50 pip loss, 30 minute trade)
        loss = -50.0
        trader.update_after_trade(loss, 30.0)
        print(f"Loss #{i+1}: {trader.emotional_state} (confidence: {trader.confidence:.2f})")
        
        # Universal law: 5+ consecutive losses = fearful
        if i >= 4:
            assert trader.emotional_state == EmotionalState.FEARFUL.value
            
        # Aggressive traders may enter revenge trading mode after 2+ losses
        if 1 <= i <= 3:
            revenge_potential = (trader.risk_appetite > 0.6 and 
                               trader.emotional_state == EmotionalState.REVENGE.value)
            fearful_potential = trader.emotional_state == EmotionalState.FEARFUL.value
            assert revenge_potential or fearful_potential

def test_newbie_cosmic_susceptibility(newbie_trader):
    """🌿 Test divine newbie susceptibility to cosmic influences."""
    trader = newbie_trader
    
    # Newbies should be highly susceptible to cosmic influences
    print(f"\n{YELLOW}Testing NEWBIE trader cosmic susceptibility:{RESET}")
    for influence, value in trader.susceptibilities.items():
        print(f"  {influence}: {value:.2f}")
        assert value > 0.7  # Newbies highly susceptible
    
    # Test extreme cosmic conditions
    trader.set_cosmic_conditions(
        moon_phase=MoonPhase.FULL_MOON,
        schumann_freq=SchumannFrequency.VERY_HIGH,
        mercury_retrograde=True,
        global_sentiment=GlobalSentiment.EUPHORIC
    )
    
    # Verify newbie psychology is strongly affected
    print(f"{CYAN}After extreme cosmic conditions:{RESET}")
    print(f"  Emotional state: {trader.emotional_state}")
    print(f"  Confidence: {trader.confidence:.2f}")
    print(f"  Risk appetite: {trader.risk_appetite:.2f}")
    print(f"  Stress level: {trader.stress_level:.2f}")
    
    # Newbie should have elevated risk due to high susceptibility
    assert trader.risk_appetite > 0.6
    
    # Psychological state should be extreme
    assert trader.emotional_state in [
        EmotionalState.EUPHORIC.value,
        EmotionalState.FOMO.value,
        EmotionalState.GREEDY.value
    ]

def test_trading_decision_influence(strategic_trader):
    """🔥 Test how cosmic psychology influences trading decisions."""
    trader = strategic_trader
    
    # Test decision influences with different emotional states
    print(f"\n{GREEN}Testing TRADING DECISION influences by emotional state:{RESET}")
    
    emotional_states = [
        EmotionalState.NEUTRAL.value,
        EmotionalState.FEARFUL.value, 
        EmotionalState.GREEDY.value,
        EmotionalState.ZEN.value,
        EmotionalState.ENLIGHTENED.value
    ]
    
    for state in emotional_states:
        trader.emotional_state = state
        influences = trader.get_trading_decision_influence()
        
        print(f"\n{CYAN}Emotional state: {state}{RESET}")
        for factor, value in influences.items():
            print(f"  {factor}: {value:.2f}")
        
        # Verify emotional state influences decisions appropriately
        if state == EmotionalState.FEARFUL.value:
            assert influences["entry_threshold_mod"] > 0.0  # Higher threshold
            assert influences["position_size_mod"] < 0.0    # Smaller positions
            
        elif state == EmotionalState.GREEDY.value:
            assert influences["entry_threshold_mod"] < 0.0  # Lower threshold
            assert influences["position_size_mod"] > 0.0    # Larger positions
            
        elif state == EmotionalState.ZEN.value:
            assert influences["entry_patience"] > 0.0       # More patient
            assert influences["exit_impulse"] < 0.0         # Less impulsive exits
            
        elif state == EmotionalState.ENLIGHTENED.value:
            assert influences["entry_patience"] > 0.0       # More patient
            assert abs(influences["stop_loss_mod"]) < 0.1   # Balanced risk

def test_fibonacci_sensitivity(strategic_trader, newbie_trader):
    """🌿 Test how cosmic factors affect Fibonacci pattern recognition."""
    # Strategic traders should have higher base Fibonacci sensitivity
    strategic_base = strategic_trader.get_fibonacci_sensitivity()
    newbie_base = newbie_trader.get_fibonacci_sensitivity()
    
    print(f"\n{YELLOW}Testing FIBONACCI SENSITIVITY:{RESET}")
    print(f"  Strategic trader: {strategic_base:.2f}")
    print(f"  Newbie trader: {newbie_base:.2f}")
    
    assert strategic_base > newbie_base
    
    # Test cosmic alignment enhancing Fibonacci sensitivity
    strategic_trader.cosmic.moon_phase = MoonPhase.NEW_MOON
    strategic_trader.emotional_state = EmotionalState.ENLIGHTENED.value
    strategic_trader.insight_level = 0.9
    
    enhanced_sensitivity = strategic_trader.get_fibonacci_sensitivity()
    print(f"  Strategic trader with cosmic alignment: {enhanced_sensitivity:.2f}")
    
    assert enhanced_sensitivity > strategic_base
    assert enhanced_sensitivity > 0.8  # Should be highly sensitive with alignment

def test_pip_satisfaction_threshold():
    """🔥 Test how emotional states affect profit satisfaction thresholds."""
    # Test each trader type's pip satisfaction threshold
    print(f"\n{MAGENTA}Testing PIP SATISFACTION THRESHOLDS:{RESET}")
    
    for profile in ["strategic", "aggressive", "newbie", "scalper"]:
        trader = CosmicTraderPsychology(profile_type=profile)
        
        # Test neutral state
        trader.emotional_state = EmotionalState.NEUTRAL.value
        neutral_threshold = trader.get_pip_satisfaction_threshold()
        
        # Test greedy state
        trader.emotional_state = EmotionalState.GREEDY.value
        greedy_threshold = trader.get_pip_satisfaction_threshold()
        
        # Test fearful state
        trader.emotional_state = EmotionalState.FEARFUL.value
        fearful_threshold = trader.get_pip_satisfaction_threshold()
        
        print(f"\n{CYAN}{profile.capitalize()} trader thresholds:{RESET}")
        print(f"  Neutral: {neutral_threshold:.0f} pips")
        print(f"  Greedy: {greedy_threshold:.0f} pips")
        print(f"  Fearful: {fearful_threshold:.0f} pips")
        
        # Greedy traders want more pips
        assert greedy_threshold > neutral_threshold
        # Fearful traders settle for fewer pips
        assert fearful_threshold < neutral_threshold
        
        # Different profiles have different baseline expectations
        if profile == "scalper":
            assert neutral_threshold < 100  # Scalpers target small moves
        if profile == "strategic":
            assert neutral_threshold > 300  # Strategic traders want bigger moves

def test_persistence(strategic_trader):
    """🌿 Test divine persistence of trader psychology to/from dictionary."""
    trader = strategic_trader
    
    # Set some cosmic conditions and psychological state
    trader.set_cosmic_conditions(
        moon_phase=MoonPhase.WAXING_CRESCENT,
        schumann_freq=SchumannFrequency.ELEVATED,
        market_liquidity=MarketLiquidity.FLOWING,
        global_sentiment=GlobalSentiment.OPTIMISTIC
    )
    trader.emotional_state = EmotionalState.CONFIDENT.value
    trader.confidence = 0.8
    trader.consecutive_wins = 3
    
    # Convert to dictionary
    data = trader.to_dict()
    
    # Verify dictionary contains all attributes
    print(f"\n{GREEN}Testing persistence of cosmic trader psychology:{RESET}")
    for key, value in data.items():
        if key != "cosmic_conditions":
            print(f"  {key}: {value}")
    
    print(f"\n{CYAN}Cosmic conditions:{RESET}")
    for key, value in data["cosmic_conditions"].items():
        print(f"  {key}: {value}")
    
    # Recreate from dictionary
    recreated = CosmicTraderPsychology.from_dict(data)
    
    # Verify recreated trader has same attributes
    assert recreated.profile_type == trader.profile_type
    assert recreated.emotional_state == trader.emotional_state
    assert recreated.confidence == trader.confidence
    assert recreated.consecutive_wins == trader.consecutive_wins
    assert recreated.cosmic.moon_phase.value == trader.cosmic.moon_phase.value
    assert recreated.cosmic.schumann_frequency.value == trader.cosmic.schumann_frequency.value

@freeze_time("2025-06-21 12:00:00")  # Summer solstice
def test_seasonal_cosmic_influences():
    """🌙 Test divine seasonal influences based on geographic location."""
    # Test northern hemisphere trader in summer
    north_trader = CosmicTraderPsychology(profile_type="strategic")
    north_trader.cosmic.trader_latitude = 40.0  # New York
    north_influence = north_trader.cosmic.get_geographic_influence()
    
    # Test southern hemisphere trader in winter
    south_trader = CosmicTraderPsychology(profile_type="strategic")
    south_trader.cosmic.trader_latitude = -33.0  # Sydney
    south_influence = south_trader.cosmic.get_geographic_influence()
    
    print(f"\n{BLUE}Testing SEASONAL GEOGRAPHIC influences:{RESET}")
    print(f"  Northern hemisphere (summer): {north_influence}")
    print(f"  Southern hemisphere (winter): {south_influence}")
    
    # Summer solstice should create opposite effects in different hemispheres
    assert north_influence["vitality"] > 0.0
    assert south_influence["vitality"] < 0.0
    
    # Verify winter brings introspection in southern hemisphere
    assert south_influence["introspection"] > 0.0
    # Verify summer brings extroversion in northern hemisphere
    assert north_influence["extroversion"] > 0.0
    
    # Test equatorial trader (minimal seasonal effects)
    equator_trader = CosmicTraderPsychology(profile_type="strategic")
    equator_trader.cosmic.trader_latitude = 1.0  # Near Singapore
    equator_influence = equator_trader.cosmic.get_geographic_influence()
    
    print(f"  Equatorial region: {equator_influence}")
    
    # Equatorial regions should have minimal seasonal psychological variations
    assert abs(equator_influence["vitality"]) < 0.2
    assert abs(equator_influence["introspection"]) < 0.2


@pytest.mark.parametrize("hour", [3, 12, 18, 22])
def test_circadian_trading_rhythm(hour):
    """🌞 Test divine circadian influences on trading psychology."""
    with freeze_time(f"2025-03-15 {hour:02d}:00:00"):
        print(f"\n{MAGENTA}Testing CIRCADIAN RHYTHM at {hour:02d}:00 hours:{RESET}")
        
        # Create traders of different profiles
        traders = {
            profile: CosmicTraderPsychology(profile_type=profile)
            for profile in ["strategic", "aggressive", "newbie", "scalper"]
        }
        
        # Get circadian influences for each trader
        for profile, trader in traders.items():
            rhythm = trader.cosmic.get_circadian_influence()
            print(f"  {profile.capitalize()} trader: {rhythm}")
            
            # Test profile-specific circadian effects
            if hour >= 1 and hour <= 4:  # Early morning hours (1-4 AM)
                # Most should have lower alertness except night owls
                if profile != "aggressive":  # Aggressive traders often work late/early
                    assert rhythm["alertness"] < 0.0
                
                # Intuition often higher during theta-wave state hours
                assert rhythm["intuition"] > 0.1
                    
            elif hour >= 10 and hour <= 14:  # Midday (10 AM - 2 PM)
                # Higher alertness for most profiles
                assert rhythm["alertness"] > 0.0
                
                # Strategic traders have better analysis skills midday
                if profile == "strategic":
                    assert rhythm["analysis"] > 0.2
                    
            elif hour >= 21:  # Evening (9 PM+)
                # Fatigue affects discipline
                if profile != "scalper":  # Scalpers often work nights
                    assert rhythm["discipline"] < 0.0


@pytest.mark.parametrize("event", [
    "major_rate_decision", "crypto_hack", "elon_tweet", 
    "regulatory_news", "black_swan_event"
])
def test_market_event_emotional_resilience(event, strategic_trader, newbie_trader):
    """🔥 Test divine emotional resilience to market shock events."""
    print(f"\n{YELLOW}Testing trader emotional resilience to: {event.upper()}{RESET}")
    
    # Setup: Both traders start in neutral emotional state
    strategic_trader.emotional_state = EmotionalState.NEUTRAL.value
    newbie_trader.emotional_state = EmotionalState.NEUTRAL.value
    strategic_baseline = strategic_trader.stress_level
    newbie_baseline = newbie_trader.stress_level
    
    # Apply market shock event
    strategic_trader.process_market_event(event)
    newbie_trader.process_market_event(event)
    
    # Print results
    print(f"  Strategic trader: {strategic_trader.emotional_state} (stress: {strategic_trader.stress_level:.2f})")
    print(f"  Newbie trader: {newbie_trader.emotional_state} (stress: {newbie_trader.stress_level:.2f})")
    
    # Strategic traders should be more resilient to emotional shocks
    assert strategic_trader.stress_level - strategic_baseline < newbie_trader.stress_level - newbie_baseline
    
    # Black swan events should affect everyone
    if event == "black_swan_event":
        assert strategic_trader.stress_level > strategic_baseline
        assert strategic_trader.emotional_state in [
            EmotionalState.FEARFUL.value,
            EmotionalState.STRESSED.value,
            EmotionalState.ANXIOUS.value,  # Replace UNCERTAIN with ANXIOUS
            EmotionalState.PANIC.value     # Add PANIC as another possible state
        ]
    
    # Elon's tweets affect newbies more than strategic traders
    if event == "elon_tweet":
        assert newbie_trader.emotional_state != EmotionalState.NEUTRAL.value


def test_schumann_resonance_pattern_recognition():
    """🌿 Test divine pattern recognition enhancement from Schumann frequencies."""
    print(f"\n{GREEN}Testing SCHUMANN RESONANCE pattern recognition effects:{RESET}")
    
    # Test different Schumann resonance levels
    freq_levels = [
        SchumannFrequency.VERY_LOW,
        SchumannFrequency.BASELINE,
        SchumannFrequency.ELEVATED,
        SchumannFrequency.HIGH,
        SchumannFrequency.VERY_HIGH
    ]
    
    # Test pattern recognition scores at different frequencies
    for freq in freq_levels:
        # Create trader with this Schumann frequency
        trader = CosmicTraderPsychology(profile_type="strategic")
        trader.cosmic.schumann_frequency = freq
        
        # Get pattern recognition scores for different chart patterns
        patterns = ["double_top", "head_shoulders", "fibonacci_retrace", "hidden_divergence"]
        rec_scores = trader.get_pattern_recognition_scores(patterns)
        
        print(f"\n{CYAN}Schumann {freq.value}:{RESET}")
        for pattern, score in rec_scores.items():
            print(f"  {pattern}: {score:.2f}")
        
        # Very high Schumann should enhance recognition of complex patterns
        if freq == SchumannFrequency.VERY_HIGH:
            assert rec_scores["hidden_divergence"] > 0.7
            assert rec_scores["fibonacci_retrace"] > 0.7
            
        # Very low Schumann may enhance foundational patterns
        if freq == SchumannFrequency.VERY_LOW:
            assert rec_scores["double_top"] > 0.6


@freeze_time("2025-01-21 09:45:00")  # Full moon phase
def test_moon_liquidity_sentiment_interaction():
    """🌙 Test divine interaction between moon, market liquidity and global sentiment."""
    print(f"\n{BLUE}Testing MOON-LIQUIDITY-SENTIMENT interaction effects:{RESET}")
    
    # Test combinations of moon phase, liquidity and sentiment
    combinations = [
        # Moon Phase, Market Liquidity, Global Sentiment
        (MoonPhase.FULL_MOON, MarketLiquidity.FLOWING, GlobalSentiment.EUPHORIC),
        (MoonPhase.FULL_MOON, MarketLiquidity.RESTRICTED, GlobalSentiment.FEARFUL),  # Fixed from CONSTRICTED
        (MoonPhase.NEW_MOON, MarketLiquidity.FLOWING, GlobalSentiment.OPTIMISTIC),
        (MoonPhase.NEW_MOON, MarketLiquidity.RESTRICTED, GlobalSentiment.FEARFUL)    # Fixed from CONSTRICTED
    ]
    
    for moon, liquidity, sentiment in combinations:
        # Create traders with these cosmic conditions
        strategic = CosmicTraderPsychology(profile_type="strategic")
        newbie = CosmicTraderPsychology(profile_type="newbie")
        
        # Set cosmic conditions
        for trader in [strategic, newbie]:
            trader.set_cosmic_conditions(
                moon_phase=moon,
                market_liquidity=liquidity,
                global_sentiment=sentiment
            )
            
        # Get decision influences
        strategic_inf = strategic.get_trading_decision_influence()
        newbie_inf = newbie.get_trading_decision_influence()
        
        # Print results
        moon_name = moon.value.replace("_", " ").title()
        liquidity_name = liquidity.value.title()
        sentiment_name = sentiment.value.title()
        print(f"\n{CYAN}{moon_name} + {liquidity_name} Liquidity + {sentiment_name} Sentiment:{RESET}")
        print(f"  Strategic risk mod: {strategic_inf['position_size_mod']:.2f}")
        print(f"  Newbie risk mod: {newbie_inf['position_size_mod']:.2f}")
        
        # Dangerous combination: Full moon + flowing liquidity + euphoria
        # This leads to excessive risk-taking especially in newbies
        if moon == MoonPhase.FULL_MOON and liquidity == MarketLiquidity.FLOWING and \
           sentiment == GlobalSentiment.EUPHORIC:
            assert newbie_inf['position_size_mod'] > 0.3  # Significantly increased position sizing
            assert newbie_inf['entry_threshold_mod'] < -0.2  # Lower entry standards
            
            # Strategic traders should resist this influence better
            assert strategic_inf['position_size_mod'] < newbie_inf['position_size_mod']
            
        # Protective combination: New moon + restricted liquidity + fearful sentiment
        # Creates excessive caution
        if moon == MoonPhase.NEW_MOON and liquidity == MarketLiquidity.RESTRICTED and \
           sentiment == GlobalSentiment.FEARFUL:
            assert strategic_inf['position_size_mod'] < 0  # Reduced position sizing
            assert strategic_inf['entry_threshold_mod'] > 0  # Higher entry standards
            assert newbie_inf['exit_impulse'] > 0.3  # Newbies exit quickly when scared


@pytest.fixture
def yolo_trader():
    """Create the divine YOLO crypto trader with extreme psychological traits."""
    yolo = CosmicTraderPsychology(profile_type="yolo")
    yolo.susceptibilities = {
        "fomo": 1.0,
        "lunar": 0.95,
        "schumann": 0.9,
        "social_media": 1.0,
        "celebrity_tweets": 0.99,
        "market_sentiment": 0.98,
        "mercury": 0.85
    }
    yolo.discipline = 0.1
    yolo.fomo_threshold = 0.2
    yolo.patience = 0.1
    return yolo


def test_yolo_cosmic_influences(yolo_trader):
    """🔥 Test divine YOLO trader susceptibility to extreme cosmic influences."""
    print(f"\n{RED}Testing YOLO TRADER cosmic vulnerability:{RESET}")
    
    # Test reaction to Elon Musk tweet
    initial_state = yolo_trader.emotional_state
    tweet_influence = yolo_trader.process_social_influence("elon_tweet_dogecoin")
    
    print(f"  Initial state: {initial_state}")
    print(f"  After Elon tweet: {yolo_trader.emotional_state}")
    print(f"  Tweet influence strength: {tweet_influence:.2f}")
    
    # YOLO traders are extremely influenced by social media
    assert tweet_influence > 0.8
    assert yolo_trader.emotional_state in [
        EmotionalState.FOMO.value,
        EmotionalState.EUPHORIC.value,
        EmotionalState.MANIC.value
    ]
    
    # Test with full cosmic alignment for maximum effect
    yolo_trader.set_cosmic_conditions(
        moon_phase=MoonPhase.FULL_MOON,
        schumann_freq=SchumannFrequency.VERY_HIGH,
        mercury_retrograde=False,  # Direct motion
        market_liquidity=MarketLiquidity.FLOWING,
        global_sentiment=GlobalSentiment.EUPHORIC
    )
    
    # Get risk parameters
    risk_appetite = yolo_trader.risk_appetite
    leverage = yolo_trader.get_preferred_leverage()
    patience = yolo_trader.patience
    
    print(f"  YOLO risk appetite: {risk_appetite:.2f}")
    print(f"  YOLO preferred leverage: {leverage:.1f}x")
    print(f"  YOLO patience: {patience:.2f}")
    
    # YOLO traders with cosmic alignment should have extreme risk parameters
    assert risk_appetite > 0.9
    assert leverage > 20.0  # Extremely high leverage
    assert patience < 0.2


@pytest.mark.parametrize("profile_type", [
    "strategic", "aggressive", "newbie", "scalper", "yolo"
])
def test_divine_enlightenment_trader_evolution(profile_type):
    """🌿 Test divine trader evolution toward enlightened trading consciousness."""
    # Use fixed seed for consistent test results
    random.seed(42)  # Fixed seed for reproducible tests
    
    print(f"\n{GREEN}Testing {profile_type.upper()} TRADER path to enlightenment:{RESET}")
    
    # Create trader of specified profile
    trader = CosmicTraderPsychology(profile_type=profile_type)
    trader.consecutive_enlightened_trades = 0
    
    # Initial enlightenment level
    initial_enlightenment = trader.divine_connection
    print(f"  Initial divine connection: {initial_enlightenment:.2f}")
    
    # Simulate series of balanced trades (modest profits, mindful exits)
    for i in range(7):
        # Update trader psychology with balanced profit (not too greedy)
        profit = 25.0  # Modest profit
        trader.update_after_trade(profit, 60.0, balanced_exit=True)
        
        # Practice gratitude and mindfulness after trade
        if random.random() > 0.3:  # 70% chance of practicing mindfulness
            trader.practice_mindful_trading()
            
        # Apply cosmic meditation if conditions align
        if i % 2 == 0:  # Every other trade
            trader.apply_cosmic_meditation()
    
    # Final enlightenment level
    final_enlightenment = trader.divine_connection
    print(f"  Final divine connection: {final_enlightenment:.2f}")
    print(f"  Enlightened trades: {trader.consecutive_enlightened_trades}")
    
    # Trader should progress toward enlightenment
    assert final_enlightenment > initial_enlightenment
    
    # Different profiles progress at different rates
    if profile_type == "strategic":
        assert trader.consecutive_enlightened_trades >= 3
    elif profile_type == "yolo":
        # YOLO traders struggle more with enlightenment
        assert trader.consecutive_enlightened_trades <= 2
        
    # Check for state of zen achieving after many enlightened trades
    if trader.consecutive_enlightened_trades >= 5:
        assert trader.emotional_state in [
            EmotionalState.ZEN.value,
            EmotionalState.ENLIGHTENED.value,
            EmotionalState.MINDFUL.value
        ]


if __name__ == "__main__":
    # Run the divine tests with Rastafarian blessing
    print(f"\n{GREEN}🌿 JAH BLESS THE COSMIC TEST SUITE! 🌿{RESET}")
    pytest.main(["-v", __file__])