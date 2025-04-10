
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

from omega_ai.alerts.rasta_vibes import RastaVibes
from omega_ai.alerts.alerts_orchestrator import send_alert

# Test different alert types
alert_types = [
    "Liquidity Grab",
    "Fake Pump",
    "Half-Fake Dump",
    "Market Manipulation"
]

# Generate and send an example of each alert type
for alert_type in alert_types:
    print(f"\n{'='*50}")
    print(f"Testing {alert_type} alert:")
    print(f"{'='*50}")
    
    base_message = f"BTC price moved suspiciously at $87,654.32 with 2.5% change"
    
    # Generate enhanced message
    enhanced = RastaVibes.enhance_alert(alert_type, base_message)
    
    # Print the enhanced message
    print(enhanced)
    
    # Uncomment to actually send the alerts
    # send_alert(base_message, alert_type)
    
    print(f"{'='*50}\n")

print("🌿 JAH BLESS THE DIVINE RASTA VIBES! 🌿")