# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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
Rarity Calculator Module

Calculates rarity scores and tiers for hacker archive NFTs.
"""

from typing import Dict, Any, List, Tuple, Optional
import random
import math

class RarityCalculator:
    """Calculates rarity scores and tiers for NFTs."""
    
    # Rarity tiers
    RARITY_TIERS = {
        'Common': (0, 40),
        'Uncommon': (40, 70),
        'Rare': (70, 85),
        'Epic': (85, 95),
        'Legendary': (95, 100)
    }
    
    # Crew rarity weights
    CREW_WEIGHTS = {
        'bl0w': 0.8,
        'Masters of Deception': 0.9,
        'Legion of Doom': 0.9,
        'Chaos Computer Club': 0.7,
        'L0pht Heavy Industries': 0.85,
        'cDc': 0.95,
        'Global Hell': 0.8,
        'The 414s': 0.9,
        'Phonemasters': 0.85,
        
        # Default for any other crew
        'DEFAULT': 0.5
    }
    
    # Year weights (older = rarer)
    YEAR_WEIGHTS = {
        '1995': 0.95,
        '1996': 0.9,
        '1997': 0.85,
        '1998': 0.8,
        '1999': 0.75,
        '2000': 0.7,
        '2001': 0.65,
        '2002': 0.6,
        '2003': 0.55,
        '2004': 0.5,
        '2005': 0.45,
        '2006': 0.4,
        
        # Default for any other year
        'DEFAULT': 0.3
    }
    
    # Defacement type weights
    TYPE_WEIGHTS = {
        'Political': 0.8,
        'Hacktivism': 0.85,
        'For Fun': 0.5,
        'Challenge': 0.7,
        'Revenge': 0.75,
        
        # Default for any other type
        'DEFAULT': 0.4
    }
    
    def __init__(self, random_factor: float = 0.1):
        """
        Initialize the rarity calculator.
        
        Args:
            random_factor: Amount of randomness to introduce (0.0 to 1.0)
        """
        self.random_factor = max(0.0, min(1.0, random_factor))
    
    def calculate_rarity(self, 
                        metadata: Dict[str, Any],
                        include_randomness: bool = True) -> Tuple[float, str]:
        """
        Calculate rarity score and tier for an NFT.
        
        Args:
            metadata: NFT metadata containing crew, year, type, etc.
            include_randomness: Whether to include a random factor
            
        Returns:
            Tuple of (rarity_score, rarity_tier)
        """
        base_score = 0.0
        score_count = 0
        
        # Check for crew
        crew = metadata.get('crew')
        if crew:
            crew_weight = self.CREW_WEIGHTS.get(crew, self.CREW_WEIGHTS['DEFAULT'])
            base_score += crew_weight
            score_count += 1
        
        # Check for year
        year = metadata.get('year')
        if year:
            year_weight = self.YEAR_WEIGHTS.get(str(year), self.YEAR_WEIGHTS['DEFAULT'])
            base_score += year_weight
            score_count += 1
            
        # Check for defacement type
        defacement_type = metadata.get('defacement_type')
        if defacement_type:
            type_weight = self.TYPE_WEIGHTS.get(defacement_type, self.TYPE_WEIGHTS['DEFAULT'])
            base_score += type_weight
            score_count += 1
            
        # Calculate average base score
        avg_score = base_score / max(1, score_count)
        
        # Add random factor if requested
        final_score = avg_score
        if include_randomness and self.random_factor > 0:
            # Random value between -random_factor and +random_factor
            random_value = (random.random() * 2 - 1) * self.random_factor
            final_score = max(0.0, min(1.0, avg_score + random_value))
            
        # Convert to 0-100 scale
        rarity_score = final_score * 100
        
        # Determine rarity tier
        rarity_tier = 'Common'  # Default
        for tier, (min_val, max_val) in self.RARITY_TIERS.items():
            if min_val <= rarity_score < max_val:
                rarity_tier = tier
                break
                
        return rarity_score, rarity_tier
    
    def get_rarity_distribution(self, 
                               num_samples: int = 1000) -> Dict[str, float]:
        """
        Calculate the expected distribution of rarity tiers.
        
        Args:
            num_samples: Number of random samples to use
            
        Returns:
            Dictionary with percentage distribution by tier
        """
        distribution: Dict[str, float] = {tier: 0.0 for tier in self.RARITY_TIERS}
        
        # Generate random metadata
        crews = list(self.CREW_WEIGHTS.keys())
        crews.remove('DEFAULT')
        
        years = list(self.YEAR_WEIGHTS.keys())
        years.remove('DEFAULT')
        
        types = list(self.TYPE_WEIGHTS.keys())
        types.remove('DEFAULT')
        
        for _ in range(num_samples):
            metadata = {
                'crew': random.choice(crews),
                'year': random.choice(years),
                'defacement_type': random.choice(types)
            }
            
            _, tier = self.calculate_rarity(metadata)
            distribution[tier] += 1.0
            
        # Convert to percentages
        for tier in distribution:
            distribution[tier] = (distribution[tier] / num_samples) * 100.0
            
        return distribution 