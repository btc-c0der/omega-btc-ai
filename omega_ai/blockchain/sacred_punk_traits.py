"""Sacred Punk Traits Module for OMEGA NFT Creator."""

from dataclasses import dataclass
from typing import Dict, List, Optional
import math

@dataclass
class SacredPunkTrait:
    """A sacred punk trait with divine properties."""
    name: str
    category: str
    rarity: float  # 0 to 1, where 1 is most rare
    divine_resonance: float  # 0 to 1, measuring divine energy
    description: str
    geometry_pattern: str  # Type of sacred geometry to incorporate

class SacredPunkTraits:
    """Collection of sacred punk traits with divine geometry."""
    
    # Sacred geometry patterns
    SACRED_PATTERNS = {
        "flower_of_life": "The fundamental pattern of creation",
        "metatrons_cube": "The blueprint of the universe",
        "sri_yantra": "The mother of all geometric patterns",
        "seed_of_life": "The origin pattern of creation",
        "tree_of_life": "The cosmic structure of existence",
        "vesica_piscis": "The womb of sacred geometry",
        "torus": "The fundamental energy pattern",
        "golden_spiral": "The divine proportion in motion"
    }
    
    # Punk-style trait categories with sacred twists
    TRAITS = {
        "divine_headwear": [
            SacredPunkTrait("Golden Crown", "headwear", 0.95, 0.9, 
                           "A crown imbued with sacred proportions", "flower_of_life"),
            SacredPunkTrait("Third Eye Band", "headwear", 0.8, 0.85, 
                           "A band marking the third eye chakra", "sri_yantra"),
            SacredPunkTrait("Cosmic Beanie", "headwear", 0.5, 0.7, 
                           "A beanie with cosmic patterns", "seed_of_life"),
            SacredPunkTrait("Merkaba Cap", "headwear", 0.9, 0.95, 
                           "A cap with the star tetrahedron", "metatrons_cube")
        ],
        "sacred_eyes": [
            SacredPunkTrait("All-Seeing", "eyes", 0.9, 0.95, 
                           "Eyes that perceive divine truth", "vesica_piscis"),
            SacredPunkTrait("Golden Ratio", "eyes", 0.85, 0.9, 
                           "Eyes aligned to phi", "golden_spiral"),
            SacredPunkTrait("Cosmic Shades", "eyes", 0.7, 0.8, 
                           "Sunglasses with universal patterns", "flower_of_life"),
            SacredPunkTrait("Third Eye Open", "eyes", 0.95, 1.0, 
                           "The awakened third eye", "sri_yantra")
        ],
        "divine_mouth": [
            SacredPunkTrait("Om Speaker", "mouth", 0.9, 0.95, 
                           "Speaking sacred vibrations", "seed_of_life"),
            SacredPunkTrait("Sacred Smile", "mouth", 0.7, 0.8, 
                           "A smile of divine joy", "vesica_piscis"),
            SacredPunkTrait("Cosmic Pipe", "mouth", 0.8, 0.85, 
                           "A pipe emanating sacred geometry", "torus")
        ],
        "sacred_accessories": [
            SacredPunkTrait("Phi Chain", "accessories", 0.9, 0.95, 
                           "A chain with golden ratio links", "golden_spiral"),
            SacredPunkTrait("Sacred Earring", "accessories", 0.8, 0.85, 
                           "An earring with divine symbols", "flower_of_life"),
            SacredPunkTrait("Cosmic Watch", "accessories", 0.85, 0.9, 
                           "A watch showing sacred time", "metatrons_cube")
        ]
    }
    
    @classmethod
    def get_trait(cls, category: str, rarity_threshold: float) -> Optional[SacredPunkTrait]:
        """Get a trait from a category based on rarity threshold."""
        if category not in cls.TRAITS:
            return None
            
        # Filter traits by rarity threshold (higher rarity = more rare)
        possible_traits = [
            trait for trait in cls.TRAITS[category]
            if trait.rarity >= rarity_threshold
        ]
        
        # Return the trait with highest divine resonance if any match
        return max(possible_traits, key=lambda t: t.divine_resonance) if possible_traits else None
    
    @classmethod
    def get_sacred_pattern(cls, pattern_name: str) -> str:
        """Get description of a sacred pattern."""
        return cls.SACRED_PATTERNS.get(pattern_name, "Unknown sacred pattern")
    
    @classmethod
    def calculate_divine_rarity(cls, traits: List[SacredPunkTrait]) -> float:
        """Calculate the divine rarity score for a combination of traits."""
        if not traits:
            return 0.0
            
        # Combine rarity and divine resonance
        rarity_score = sum(trait.rarity for trait in traits) / len(traits)
        resonance_score = sum(trait.divine_resonance for trait in traits) / len(traits)
        
        # Use golden ratio to weight the scores
        phi = (1 + math.sqrt(5)) / 2
        divine_rarity = (rarity_score * phi + resonance_score) / (phi + 1)
        
        return divine_rarity 