
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
🦁 PATOIS LOGGER - RASTA ALERT MODE 🦁
=====================================

Generates spiritually-inspired Patois alerts for market manipulation.
May your warnings be blessed with the truth of JAH! 🌿

JAH BLESS THE TRUTHFUL MARKET VISION! 🙏
"""

from typing import Dict, Any
from omega_ai.mm_trap_detector.core.mm_trap_detector import TrapDetection, TrapType

class PatoisLogger:
    """Patois-style trap alert generator."""
    
    def __init__(self):
        """Initialize the Patois logger."""
        self.rasta_mode = True
        self.alert_history: list[str] = []
    
    def generate_rasta_alert(self, trap: TrapDetection) -> str:
        """Generate a Patois-style alert for a detected trap."""
        # Convert confidence to percentage
        confidence_pct = int(trap.confidence * 100)
        
        # Generate base alert
        alert = self._generate_base_alert(trap, confidence_pct)
        
        # Add trap-specific details
        alert += self._add_trap_details(trap)
        
        # Add spiritual guidance
        alert += self._add_spiritual_guidance(trap)
        
        # Store alert in history
        self.alert_history.append(alert)
        
        return alert
    
    def _generate_base_alert(self, trap: TrapDetection, confidence_pct: int) -> str:
        """Generate the base Patois alert message."""
        trap_type = trap.type.value.replace("_", " ")
        
        if trap_type == "liquidity grab":
            return f"⚠️ Babylon try sneak di stop hunt! Confidence: {confidence_pct}%\n"
        elif trap_type == "fake pump":
            return f"⚠️ Babylon a try pump up di price! Confidence: {confidence_pct}%\n"
        elif trap_type == "fake dump":
            return f"⚠️ Babylon a try dump down di price! Confidence: {confidence_pct}%\n"
        elif trap_type == "stealth accumulation":
            return f"⚠️ Babylon a try accumulate in secret! Confidence: {confidence_pct}%\n"
        elif trap_type == "fractal trap":
            return f"⚠️ Babylon a try create false patterns! Confidence: {confidence_pct}%\n"
        elif trap_type == "time dilation":
            return f"⚠️ Babylon a try manipulate time! Confidence: {confidence_pct}%\n"
        elif trap_type == "order spoofing":
            return f"⚠️ Babylon a try spoof di orders! Confidence: {confidence_pct}%\n"
        elif trap_type == "wash trading":
            return f"⚠️ Babylon a try wash di trades! Confidence: {confidence_pct}%\n"
        elif trap_type == "hidden liquidity":
            return f"⚠️ Babylon a try hide di liquidity! Confidence: {confidence_pct}%\n"
        elif trap_type == "cross exchange":
            return f"⚠️ Babylon a try cross exchange manipulation! Confidence: {confidence_pct}%\n"
        elif trap_type == "flash dump":
            return f"⚠️ Babylon a try flash crash di market! Confidence: {confidence_pct}%\n"
        else:
            return f"⚠️ Babylon a try something wicked! Confidence: {confidence_pct}%\n"
    
    def _add_trap_details(self, trap: TrapDetection) -> str:
        """Add trap-specific details to the alert."""
        details = []
        
        # Add price information
        if trap.price > 0:
            details.append(f"Price: ${trap.price:,.2f}")
        
        # Add volume information
        if trap.volume > 0:
            details.append(f"Volume: {trap.volume:,.2f} BTC")
        
        # Add timestamp
        details.append(f"Time: {trap.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return f"📊 Details: {' | '.join(details)}\n"
    
    def _add_spiritual_guidance(self, trap: TrapDetection) -> str:
        """Add spiritual guidance based on trap type."""
        if trap.confidence > 0.9:
            return "🙏 JAH protect us from Babylon's wicked ways! Stay vigilant, bredren!\n"
        elif trap.confidence > 0.7:
            return "🌿 Trust in JAH's wisdom, but keep your eyes open!\n"
        else:
            return "✨ Let JAH guide your trading decisions!\n"
    
    def get_alert_history(self) -> list[str]:
        """Get the history of generated alerts."""
        return self.alert_history
    
    def clear_history(self) -> None:
        """Clear the alert history."""
        self.alert_history.clear()
    
    def set_rasta_mode(self, enabled: bool) -> None:
        """Enable or disable Rasta mode."""
        self.rasta_mode = enabled 