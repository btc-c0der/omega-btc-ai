
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
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TEST_CHAT_IDS = [
    "1002510049870",    # Without hyphen
    "-1002510049870",   # With hyphen
    "2510049870"        # Last part only
]

def test_each_chat_id():
    """Test sending a message to each possible chat ID format."""
    for chat_id in TEST_CHAT_IDS:
        try:
            print(f"🧪 Testing chat ID: {chat_id}")
            
            telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": chat_id, 
                "text": f"🌿 RASTA TEST: Testing chat ID: {chat_id}"
            }
            
            response = requests.post(telegram_url, data=payload)
            
            if response.status_code == 200:
                print(f"✅ SUCCESS! Message sent to chat ID: {chat_id}")
                print(f"✅ This is your correct chat ID - update your .env file")
            else:
                print(f"❌ FAILED: Status {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_each_chat_id()