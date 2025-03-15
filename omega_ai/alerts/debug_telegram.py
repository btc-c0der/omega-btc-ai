import os
import requests
import json
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
    
    # 2. Try sending a test message
    try:
        print("\n📝 Sending test message...")
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
            
            # Now try with Markdown
            markdown_msg = """🌿 *RASTA DEBUG*: _Markdown_ test
            
*Bold text*
_Italic text_
[OMEGA BTC AI](https://github.com/yourusername/omega-btc-ai)

JAH BLESS! 🔥"""
            
            print("\n📝 Sending markdown test message...")
            md_payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": markdown_msg,
                "parse_mode": "Markdown"
            }
            
            md_response = requests.post(message_url, json=md_payload)
            print(f"📥 Status code: {md_response.status_code}")
            
            if md_response.status_code == 200:
                print("✅ Markdown message sent successfully!")
            else:
                print(f"❌ Markdown message failed: {md_response.text}")
        else:
            print(f"❌ Message sending failed: {response.text}")
    except Exception as e:
        print(f"❌ Message sending error: {e}")

if __name__ == "__main__":
    debug_telegram_connection()