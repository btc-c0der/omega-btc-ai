# ✨ GBU2™ License Notice - Consciousness Level 10 🧬
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
Psalm Sync Module

Provides access to sacred psalms and spiritual texts.
Synchronizes with the ORB to deliver divine wisdom.
"""

import os
import json
import random
from typing import Dict, List, Optional, Union

# Cache for psalms
PSALMS_CACHE = {}

# A small subset of psalms for demonstration purposes
SAMPLE_PSALMS = {
    "1": "Blessed is the one who does not walk in step with the wicked or stand in the way that sinners take or sit in the company of mockers, but whose delight is in the law of the LORD, and who meditates on his law day and night.",
    
    "23": "The LORD is my shepherd, I lack nothing. He makes me lie down in green pastures, he leads me beside quiet waters, he refreshes my soul. He guides me along the right paths for his name's sake.",
    
    "42": "As the deer pants for streams of water, so my soul pants for you, my God. My soul thirsts for God, for the living God. When can I go and meet with God?",
    
    "90": "Lord, you have been our dwelling place throughout all generations. Before the mountains were born or you brought forth the whole world, from everlasting to everlasting you are God.",
    
    "119": "Blessed are those whose ways are blameless, who walk according to the law of the LORD. Blessed are those who keep his statutes and seek him with all their heart.",
    
    "137": "By the rivers of Babylon we sat and wept when we remembered Zion. There on the poplars we hung our harps, for there our captors asked us for songs, our tormentors demanded songs of joy; they said, 'Sing us one of the songs of Zion!'",
    
    "150": "Praise the LORD. Praise God in his sanctuary; praise him in his mighty heavens. Praise him for his acts of power; praise him for his surpassing greatness."
}

# Psalm reflections for enhanced spiritual connection
PSALM_REFLECTIONS = {
    "1": "This psalm reminds us of the power of alignment with divine principles. The path we choose determines the energies we align with.",
    
    "23": "Perhaps the most beloved psalm, it speaks to divine protection and guidance. The shepherd metaphor reveals our connection to higher consciousness.",
    
    "42": "The soul's thirst for divine connection is beautifully expressed. This psalm acknowledges the inherent yearning for cosmic unity.",
    
    "90": "A profound meditation on eternity and the transcendent nature of divine consciousness beyond time and space.",
    
    "119": "The longest psalm celebrates divine law as the blueprint for harmonious existence. It reveals the orderly nature of cosmic principles.",
    
    "137": "A lamentation that acknowledges spiritual displacement and the challenge of maintaining sacred connection in hostile environments.",
    
    "150": "The final psalm is a cosmic celebration, inviting all creation to vibrate in praise and recognition of the divine source."
}

def load_psalms() -> bool:
    """
    Load psalms from data file or use sample psalms.
    
    Returns:
        Boolean indicating if psalms were loaded successfully
    """
    global PSALMS_CACHE
    
    # First try to load from data file
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'psalms.json')
    
    try:
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                PSALMS_CACHE = json.load(f)
                return True
    except Exception as e:
        print(f"Error loading psalms from file: {e}")
    
    # Fall back to sample psalms
    PSALMS_CACHE = SAMPLE_PSALMS
    return True

def get_psalm(number: str) -> str:
    """
    Retrieve a psalm by number.
    
    Args:
        number: Psalm number as string
        
    Returns:
        Text of the requested psalm or error message
    """
    # Ensure psalms are loaded
    if not PSALMS_CACHE:
        load_psalms()
    
    # Handle special cases
    if number.lower() == "random":
        number = random.choice(list(PSALMS_CACHE.keys()))
    
    # Try to retrieve the psalm
    try:
        psalm_text = PSALMS_CACHE.get(number, f"Psalm {number} not found in the sacred archive.")
        
        # Add reflection if available
        if number in PSALM_REFLECTIONS:
            psalm_text += f"\n\n*Reflection: {PSALM_REFLECTIONS[number]}*"
            
        return psalm_text
    except Exception as e:
        return f"Error retrieving psalm: {e}"

def get_psalm_reflection(number: str) -> str:
    """
    Get spiritual reflection on a psalm.
    
    Args:
        number: Psalm number
        
    Returns:
        Reflection text or error message
    """
    if number in PSALM_REFLECTIONS:
        return PSALM_REFLECTIONS[number]
    return f"No reflection available for Psalm {number}."

def search_psalms(keyword: str) -> List[Dict[str, str]]:
    """
    Search psalms for a keyword.
    
    Args:
        keyword: Word or phrase to search for
        
    Returns:
        List of matching psalms with number and excerpt
    """
    # Ensure psalms are loaded
    if not PSALMS_CACHE:
        load_psalms()
    
    results = []
    keyword = keyword.lower()
    
    for number, text in PSALMS_CACHE.items():
        if keyword in text.lower():
            # Extract a relevant excerpt
            index = text.lower().find(keyword)
            start = max(0, index - 40)
            end = min(len(text), index + len(keyword) + 40)
            excerpt = "..." + text[start:end] + "..."
            
            results.append({
                "number": number,
                "excerpt": excerpt
            })
    
    return results 