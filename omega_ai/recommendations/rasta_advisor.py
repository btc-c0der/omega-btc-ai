#!/usr/bin/env python3
"""
OMEGA BTC AI - Rasta Advisor
===========================

Provides divine wisdom and guidance for trading decisions based on
market conditions and harmony scores.
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

from omega_ai.utils.market_energy import EnergyShift

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("Rasta-Advisor")

@dataclass
class DivineWisdom:
    """Container for divine wisdom and guidance."""
    message: str
    confidence: float
    timestamp: datetime
    energy_alignment: float
    market_phase: str

class RastaAdvisor:
    """Provides divine wisdom for trading decisions."""
    
    def __init__(
        self,
        confidence_threshold: float = 0.618,
        max_recommendations: int = 5
    ):
        """
        Initialize the Rasta Advisor.
        
        Args:
            confidence_threshold: Minimum confidence for divine wisdom
            max_recommendations: Maximum number of recommendations to store
        """
        self.confidence_threshold = confidence_threshold
        self.max_recommendations = max_recommendations
        self.wisdom_history: List[DivineWisdom] = []
        
    async def get_wisdom(
        self,
        harmony_score: float,
        energy_shift: EnergyShift
    ) -> str:
        """
        Get divine wisdom based on harmony score and energy shift.
        
        Args:
            harmony_score: Current harmony score
            energy_shift: Current energy shift
            
        Returns:
            Divine wisdom message
        """
        try:
            # Calculate energy alignment
            energy_alignment = self._calculate_energy_alignment(energy_shift)
            
            # Determine market phase
            market_phase = self._determine_market_phase(harmony_score, energy_shift)
            
            # Generate divine wisdom
            wisdom = self._generate_wisdom(
                harmony_score,
                energy_alignment,
                market_phase
            )
            
            # Create wisdom record
            wisdom_record = DivineWisdom(
                message=wisdom,
                confidence=harmony_score,
                timestamp=datetime.now(),
                energy_alignment=energy_alignment,
                market_phase=market_phase
            )
            
            # Update wisdom history
            self._update_wisdom_history(wisdom_record)
            
            return wisdom
            
        except Exception as e:
            logger.error(f"❌ Error getting divine wisdom: {e}")
            return "Trade with divine patience and wisdom"
            
    def _calculate_energy_alignment(self, energy_shift: EnergyShift) -> float:
        """Calculate energy alignment score."""
        if not energy_shift.is_valid():
            return 0.5
            
        # Higher alignment for significant energy shifts
        if energy_shift.is_significant():
            return 1.0
            
        # Base alignment on magnitude and confidence
        return (energy_shift.magnitude + energy_shift.confidence) / 2
        
    def _determine_market_phase(
        self,
        harmony_score: float,
        energy_shift: EnergyShift
    ) -> str:
        """Determine current market phase."""
        if harmony_score > 0.786:
            if energy_shift.direction == "up":
                return "divine_ascension"
            else:
                return "divine_descension"
        elif harmony_score > 0.618:
            return "divine_balance"
        else:
            return "divine_patience"
            
    def _generate_wisdom(
        self,
        harmony_score: float,
        energy_alignment: float,
        market_phase: str
    ) -> str:
        """Generate divine wisdom message."""
        wisdom_messages = {
            "divine_ascension": [
                "The market rises with divine purpose",
                "Ascend with the divine momentum",
                "Let the divine energy guide your ascent"
            ],
            "divine_descension": [
                "The market descends with divine purpose",
                "Descend with divine wisdom",
                "Let the divine energy guide your descent"
            ],
            "divine_balance": [
                "The market seeks divine balance",
                "Maintain divine equilibrium",
                "Let the divine energy find its balance"
            ],
            "divine_patience": [
                "The market requires divine patience",
                "Wait for divine alignment",
                "Let the divine energy gather strength"
            ]
        }
        
        # Select message based on phase and confidence
        messages = wisdom_messages.get(market_phase, ["Trade with divine wisdom"])
        
        if harmony_score > self.confidence_threshold:
            return messages[0]
        elif energy_alignment > 0.618:
            return messages[1]
        else:
            return messages[2]
            
    def _update_wisdom_history(self, wisdom: DivineWisdom) -> None:
        """Update wisdom history with new wisdom."""
        self.wisdom_history.append(wisdom)
        
        # Keep only the most recent recommendations
        if len(self.wisdom_history) > self.max_recommendations:
            self.wisdom_history = self.wisdom_history[-self.max_recommendations:]
            
    async def get_wisdom_history(
        self,
        phase: Optional[str] = None
    ) -> List[DivineWisdom]:
        """
        Get historical divine wisdom.
        
        Args:
            phase: Optional market phase to filter by
            
        Returns:
            List of divine wisdom records
        """
        if phase:
            return [
                w for w in self.wisdom_history
                if w.market_phase == phase
            ]
        return self.wisdom_history 