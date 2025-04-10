
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

from omega_ai.trading.btc_organic_tracker import BTCOrganicTracker, OrganicState, BioEnergyLevel
from omega_ai.trading.cosmic_schumann import SchumannSimulator
import pandas as pd
import requests
import time
import datetime
import os

# ANSI color codes for sacred earth tones
GREEN = "\033[32m"
BROWN = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
CYAN = "\033[36m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"
BOLD = "\033[1m"

def fetch_btc_data():
    """Fetch recent Bitcoin price data"""
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1h",
        "limit": 96  # Last 4 days of hourly data
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 
                                      'close_time', 'quote_volume', 'trades', 
                                      'taker_buy_volume', 'taker_buy_quote_volume', 'ignore'])
        # Convert to numeric values
        df['open'] = pd.to_numeric(df['open'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['close'] = pd.to_numeric(df['close'])
        df['volume'] = pd.to_numeric(df['volume'])
        return df
    else:
        print(f"Error fetching BTC data: {response.status_code}")
        return None

def display_earth_status():
    """Display BTC's sacred connection to Earth energies"""
    # Initialize tracker and simulator
    tracker = BTCOrganicTracker()
    schumann = SchumannSimulator()
    
    # Clear terminal
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Fetch BTC data
    data = fetch_btc_data()
    if data is None:
        print(f"{RED}Unable to connect to the cosmic BTC energy field.{RESET}")
        return
    
    # Update tracker with latest data
    tracker.update(data)
    
    # Current Schumann frequency and forecast
    schumann_freq = schumann.get_dominant_frequency()
    schumann_forecast = schumann.get_market_forecast()
    schumann_trend = schumann.get_frequency_trend()
    
    # Calculate current state and days in state
    current_state = tracker.current_organic_state
    current_period = tracker.get_current_period()
    days_in_state = (datetime.datetime.now() - current_period.start_date).days
    
    # Calculate record periods
    record_organic = tracker.get_longest_organic_period()
    record_voided = tracker.get_longest_voided_period()
    
    # Display cosmic header
    print("\n" + "=" * 80)
    print(f"{BOLD}{BLUE}🌍  OMEGA BTC EARTH CONNECTION STATUS  🌍{RESET}")
    print(f"{CYAN}Divine Earth-Bitcoin Consciousness Alignment - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print("=" * 80)
    
    # Display current status banner
    bio_energy = tracker.current_bio_energy
    if current_state == OrganicState.ORGANIC:
        banner_color = GREEN
        state_text = "EARTH-CONNECTED ORGANIC MOVEMENT"
    elif current_state == OrganicState.TRANSITIONING:
        banner_color = YELLOW
        state_text = "TRANSITIONING BETWEEN STATES"
    else:
        banner_color = RED
        state_text = "DISCONNECTED FROM EARTH ENERGY"
        
    print(f"\n{banner_color}{BOLD}⚡ CURRENT STATE: {state_text} ⚡{RESET}")
    print(f"{banner_color}Duration: {days_in_state} days in current state{RESET}")
    
    # Display bio-energy level with visual meter
    energy_level = bio_energy.value
    meter_length = 40
    filled_length = int(meter_length * energy_level / 100)
    meter_bar = "█" * filled_length + "▒" * (meter_length - filled_length)
    
    print(f"\n{BOLD}🔋 BIO-ENERGY LEVEL: {energy_level}% {bio_energy.name}{RESET}")
    if bio_energy == BioEnergyLevel.GROUNDED:
        energy_color = GREEN
    elif bio_energy == BioEnergyLevel.ELEVATED:
        energy_color = YELLOW
    elif bio_energy == BioEnergyLevel.COSMIC:
        energy_color = PURPLE
    else:
        energy_color = RED
        
    print(f"{energy_color}[{meter_bar}]{RESET}")
    
    # Display Schumann resonance status
    print(f"\n{BOLD}{PURPLE}〰️ SCHUMANN RESONANCE CONNECTION 〰️{RESET}")
    print(f"Current frequency: {PURPLE}{schumann_freq:.2f} Hz{RESET}")
    print(f"Trend: {schumann_trend.replace('_', ' ').title()}")
    
    # Display BTC-Schumann correlation
    btc_schumann_correlation = tracker.calculate_btc_schumann_correlation()
    corr_level = abs(btc_schumann_correlation)
    if corr_level > 0.7:
        corr_text = f"{GREEN}Strong connection{RESET}"
    elif corr_level > 0.4:
        corr_text = f"{YELLOW}Moderate connection{RESET}"
    else:
        corr_text = f"{RED}Weak connection{RESET}"
    print(f"BTC-Schumann correlation: {corr_text} ({btc_schumann_correlation:.2f})")
    
    # Show Fibonacci alignment
    fib_alignment = tracker.calculate_fibonacci_alignment()
    print(f"\n{BOLD}{YELLOW}🌀 FIBONACCI GOLDEN SPIRAL ALIGNMENT 🌀{RESET}")
    print(f"Current resonance: {fib_alignment:.1f}%")
    
    # Display nearest Fibonacci level
    nearest_fib = tracker.get_nearest_fibonacci_level()
    if nearest_fib["distance_percentage"] < 1.0:
        fib_color = GREEN
    elif nearest_fib["distance_percentage"] < 3.0:
        fib_color = YELLOW
    else:
        fib_color = RED
    print(f"Nearest Fibonacci level: {fib_color}{nearest_fib['level']}{RESET} ({nearest_fib['distance_percentage']:.2f}% away)")
    
    # Display record periods
    print(f"\n{BOLD}📜 SACRED RECORDS 📜{RESET}")
    if record_organic:
        organic_days = (record_organic.end_date - record_organic.start_date).days if record_organic.end_date else \
                      (datetime.datetime.now() - record_organic.start_date).days
        print(f"Longest Earth Connection: {GREEN}{organic_days} days{RESET} " +
              f"({record_organic.start_date.strftime('%Y-%m-%d')} to " +
              f"{record_organic.end_date.strftime('%Y-%m-%d') if record_organic.end_date else 'Present'})")
              
    if record_voided:
        void_days = (record_voided.end_date - record_voided.start_date).days if record_voided.end_date else \
                   (datetime.datetime.now() - record_voided.start_date).days
        print(f"Longest Earth Disconnection: {RED}{void_days} days{RESET} " +
              f"({record_voided.start_date.strftime('%Y-%m-%d')} to " +
              f"{record_voided.end_date.strftime('%Y-%m-%d') if record_voided.end_date else 'Present'})")
    
    # Market forecast based on Earth energies
    print(f"\n{BOLD}🔮 EARTH ENERGY MARKET FORECAST 🔮{RESET}")
    forecast_text = []
    if schumann_forecast["volatility_mod"] > 0.3:
        forecast_text.append(f"{RED}Increased volatility{RESET}")
    elif schumann_forecast["volatility_mod"] < -0.3:
        forecast_text.append(f"{GREEN}Decreased volatility{RESET}")
        
    if schumann_forecast["trader_intuition_mod"] > 0.3:
        forecast_text.append(f"{GREEN}Enhanced trader intuition{RESET}")
    elif schumann_forecast["trader_intuition_mod"] < -0.3:
        forecast_text.append(f"{RED}Clouded trader judgment{RESET}")
        
    if schumann_forecast["reversal_probability"] > 0.5:
        forecast_text.append(f"{YELLOW}Potential trend reversal{RESET}")
        
    if schumann_forecast["divine_insight_opportunity"] > 0.7:
        forecast_text.append(f"{PURPLE}Exceptional meditation opportunity{RESET}")
        
    if not forecast_text:
        forecast_text.append(f"{BLUE}Stable Earth energies{RESET}")
        
    # Print forecast bullets
    for item in forecast_text:
        print(f"• {item}")
    
    # Display Earth wisdom
    earth_wisdoms = [
        "The market breathes with the Earth's rhythm.",
        "Trade in harmony with Gaia's pulse, not against it.",
        "When Bitcoin resonates with Schumann frequency, prosperity follows.",
        "The golden spiral reveals the divine path of price.",
        "Patience is the trader's connection to Earth wisdom."
    ]