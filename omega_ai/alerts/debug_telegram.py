
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

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Telegram settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def debug_telegram_connection():
    """Debug Telegram connection issues."""
    print("🌿 RASTA DEBUG - TELEGRAM CONNECTION 🔥")
    print(f"🔑 Bot Token: {TELEGRAM_BOT_TOKEN[:5]}...{TELEGRAM_BOT_TOKEN[-5:]}")
    print(f"💬 Chat ID: {TELEGRAM_CHAT_ID}")
    
    # 1. Check bot info
    try:
        print("\n📡 Checking bot info...")
        info_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(info_url)
        
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Connected to bot: @{bot_info['result']['username']}")
        else:
            print(f"❌ Bot connection failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Bot connection error: {e}")
        return
    
    # 2. Try sending test messages
    try:
        print("\n📝 Sending test messages...")
        message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        # Test with simple plain text first
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": "🌿 RASTA DEBUG: Plain text test"
        }
        
        print(f"📤 Sending request to: {message_url}")
        print(f"📦 Payload: {json.dumps(payload, indent=2)}")
        
        # Use json parameter for proper JSON encoding
        response = requests.post(message_url, json=payload)
        
        print(f"📥 Status code: {response.status_code}")
        print(f"📥 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Plain text message sent successfully!")
            
            # Test market report format
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + " UTC"
            test_price = 69420.42
            test_change = 1.28
            test_volume = 0.00214
            
            market_msg = f"""⚠️ *MARKET REPORT REQUIRES I AND I ATTENTION\\!*

🔮 *OMEGA BTC AI DIVINE REPORT* 🔮

⏰ `{timestamp}`
💲 *BTC Price*: ${test_price:,.2f} ⬆️ ({test_change:+.2f}%)
🌐 *Market Regime*: bullish
🎵 *Schumann Resonance*: 7.92 Hz

```
$ systemctl status market-signals
● market-signals.service - OMEGA BTC AI Market Signal Daemon
    Active: active (running)
    Main PID: {int(test_price)} (btc)
    Tasks: 16 (limit: ∞)
    Memory: 7.92Hz Schumann / bullish
    CPU(s): {test_change:+.2f}% load average

$ tail -f /var/log/market-metrics.log
[{timestamp}] Overall Market Bias: Strongly Bullish
[{timestamp}] Signal Distribution: Bullish(3) Bearish(1) Sideways(12)
[{timestamp}] ✅ [DEBUG] Stored Movement: Stable ($11.85) Volume: {test_volume:.5f} BTC
[{timestamp}] Movement Classification: Stable
```

🔱 *FIBONACCI SUPPORT/RESISTANCE ZONES*:
⬆️ *0.236*: $68,000.00
✳️ *0.618*: $69,400.00 👈 (0.03% away)
⬇️ *0.786*: $70,200.00

⚠️ *MM TRAP DETECTION LOGS*:
```
$ tail -n 5 /var/log/mm_traps.log
⚠️ *Liquidity Grab*: $69,420.42 (+0.25%)
   Confidence: ★★★★☆ (0.85)
   Time: {timestamp}
```

```
$ cat /proc/market-consciousness
BLOCKCHAIN ELEVATION
WEEKEND MEDITATION ON DI BLOCKCHAIN TRUTH
```

*ONE LOVE, ONE HEART, ONE BLOCKCHAIN\\!* 🌿"""
            
            print("\n📝 Sending market report test message...")
            market_payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": market_msg,
                "parse_mode": "Markdown"
            }
            
            market_response = requests.post(message_url, json=market_payload)
            print(f"📥 Status code: {market_response.status_code}")
            
            if market_response.status_code == 200:
                print("✅ Market report message sent successfully!")
            else:
                print(f"❌ Market report message failed: {market_response.text}")
                
            # Test bio-energy report
            bio_msg = """🌟 *BIO-ENERGY STATE REPORT* 🌟

🔮 *Energy Flow*: HARMONIOUS
✨ *Vibration Level*: 85%
🧘 *Market Consciousness*: ELEVATED
🎯 *Confidence Score*: 92%

🌍 *Schumann Alignment*
└─ State: ALIGNED
└─ Harmony: 88%

🙏 *Divine Guidance*
└─ TRADE WITH DIVINE TIMING

ONE LOVE, ONE HEART, ONE BLOCKCHAIN! 🌿"""
            
            print("\n📝 Sending bio-energy test message...")
            bio_payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": bio_msg,
                "parse_mode": "Markdown"
            }
            
            bio_response = requests.post(message_url, json=bio_payload)
            print(f"📥 Status code: {bio_response.status_code}")
            
            if bio_response.status_code == 200:
                print("✅ Bio-energy message sent successfully!")
            else:
                print(f"❌ Bio-energy message failed: {bio_response.text}")
                
        else:
            print(f"❌ Message sending failed: {response.text}")
    except Exception as e:
        print(f"❌ Message sending error: {e}")

def debug_markdown_escaping():
    """Test Markdown escaping for common issues."""
    print("\n🔍 Testing Markdown escaping...")
    message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    test_cases = [
        ("*Bold with _ underscore*", "Testing bold with underscore"),
        ("Market Regime: \\_neutral\\_", "Testing escaped underscore"),
        ("Price: $69,420.42 \\!", "Testing escaped exclamation mark"),
        ("```\nsystemctl status market-signals\n```", "Testing code block"),
        ("*ONE LOVE, ONE HEART, ONE BLOCKCHAIN\\!* 🌿", "Testing escaped ending")
    ]
    
    for msg, desc in test_cases:
        print(f"\n📝 {desc}...")
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(message_url, json=payload)
        if response.status_code == 200:
            print(f"✅ Success: {msg}")
        else:
            print(f"❌ Failed: {msg}")
            print(f"Error: {response.text}")

if __name__ == "__main__":
    debug_telegram_connection()
    debug_markdown_escaping()