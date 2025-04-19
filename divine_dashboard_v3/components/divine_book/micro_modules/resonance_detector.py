#!/usr/bin/env python3
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
Resonance Detector Module

Tools for analyzing sacred and mathematical patterns in text.
Detects alignments with universal constants and sacred geometry principles.
"""

import re
import math
import hashlib
from typing import Dict, List, Union, Tuple, Any

# Universal constants
GOLDEN_RATIO = 1.618033988749895
SCHUMANN_FREQUENCY = 7.83  # Hz
LUNAR_CYCLE = 29.53  # days
SOLAR_CYCLE = 365.24  # days
FIBONACCI_SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
PI = 3.14159265358979323846
E = 2.71828182845904523536

# Sacred number patterns to detect
SACRED_NUMBERS = [
    3, 7, 9, 12, 13, 18, 19, 21, 22, 24, 33, 36, 40, 
    42, 54, 60, 72, 108, 144, 216, 432, 666, 888, 1080, 1440
]

# Sacred words and symbols to detect
SACRED_WORDS = [
    "divine", "sacred", "holy", "eternal", "infinite", "cosmos", 
    "universe", "creation", "spirit", "soul", "consciousness",
    "enlightenment", "awakening", "truth", "wisdom", "light",
    "heaven", "god", "goddess", "source", "oneness", "unity",
    "harmony", "balance", "peace", "love", "compassion", "mercy"
]

SACRED_SYMBOLS = ["✨", "☀️", "🌙", "🌟", "🔮", "⚡", "🧬", "🕉️", "☯️", "✝️", "☪️", "✡️"]

def calculate_resonance(
    text: str, 
    golden_ratio_weight: float = 0.5,
    fibonacci_weight: float = 0.5,
    schumann_weight: float = 0.5,
    lunar_weight: float = 0.5,
    solar_weight: float = 0.5
) -> float:
    """
    Calculate the overall quantum resonance score of a text.
    
    Args:
        text: The text to analyze
        golden_ratio_weight: Weight for golden ratio alignment (0-1)
        fibonacci_weight: Weight for fibonacci alignment (0-1)
        schumann_weight: Weight for Schumann resonance alignment (0-1)
        lunar_weight: Weight for lunar cycle alignment (0-1)
        solar_weight: Weight for solar cycle alignment (0-1)
    
    Returns:
        A resonance score between 0 and 1
    """
    if not text or not text.strip():
        return 0.0
    
    # Calculate individual resonances
    golden_alignment = calculate_golden_ratio_alignment(text)
    fibonacci_alignment = calculate_fibonacci_alignment(text)
    
    # Calculate frequency resonances
    letter_frequencies = analyze_letter_frequencies(text)
    schumann_resonance = calculate_frequency_resonance(letter_frequencies, SCHUMANN_FREQUENCY)
    lunar_resonance = calculate_frequency_resonance(letter_frequencies, LUNAR_CYCLE)
    solar_resonance = calculate_frequency_resonance(letter_frequencies, SOLAR_CYCLE)
    
    # Calculate weighted average
    total_weight = (golden_ratio_weight + fibonacci_weight + 
                   schumann_weight + lunar_weight + solar_weight)
    
    if total_weight == 0:
        return 0.0
    
    weighted_sum = (
        golden_ratio_weight * golden_alignment +
        fibonacci_weight * fibonacci_alignment +
        schumann_weight * schumann_resonance +
        lunar_weight * lunar_resonance +
        solar_weight * solar_resonance
    )
    
    return weighted_sum / total_weight

def analyze_letter_frequencies(text: str) -> Dict[str, float]:
    """
    Analyze letter frequencies in the text.
    
    Args:
        text: The text to analyze
    
    Returns:
        Dictionary mapping each letter to its frequency
    """
    # Remove non-alphabetic characters and convert to lowercase
    clean_text = ''.join(c for c in text.lower() if c.isalpha())
    
    if not clean_text:
        return {}
    
    # Count occurrences of each letter
    letter_counts = {}
    for char in clean_text:
        letter_counts[char] = letter_counts.get(char, 0) + 1
    
    # Calculate frequencies
    total_chars = len(clean_text)
    letter_frequencies = {char: count / total_chars for char, count in letter_counts.items()}
    
    return letter_frequencies

def calculate_frequency_resonance(letter_frequencies: Dict[str, float], target_frequency: float) -> float:
    """
    Calculate resonance between letter frequencies and a target frequency.
    
    Args:
        letter_frequencies: Dictionary of letter frequencies
        target_frequency: Target frequency to compare against
    
    Returns:
        Resonance score between 0 and 1
    """
    if not letter_frequencies:
        return 0.0
    
    # Convert letter frequencies to numerical values (a=1, b=2, etc.)
    numerical_values = []
    for char, freq in letter_frequencies.items():
        # Convert character to numerical value (a=1, b=2, etc.)
        numerical_value = ord(char) - ord('a') + 1
        # Weight by frequency
        numerical_values.append(numerical_value * freq)
    
    # Calculate average
    avg_value = sum(numerical_values) / len(numerical_values)
    
    # Calculate resonance as proximity to target frequency (scaled to 0-1)
    max_diff = max(target_frequency, 26)  # Maximum possible difference
    diff = abs(avg_value - (target_frequency % 26))
    
    # Normalize to 0-1 range (1 is perfect resonance)
    resonance = 1 - (diff / max_diff)
    
    return resonance

def calculate_golden_ratio_alignment(text: str) -> float:
    """
    Calculate how closely the text aligns with the golden ratio.
    
    Args:
        text: The text to analyze
    
    Returns:
        Alignment score between 0 and 1
    """
    if not text or not text.strip():
        return 0.0
    
    # Clean text
    clean_text = ''.join(c for c in text if c.isalnum() or c.isspace())
    
    # Count words, sentences, and characters
    words = clean_text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]
    
    char_count = len(clean_text)
    word_count = len(words)
    sentence_count = len(sentences)
    
    # Prevent division by zero
    if word_count == 0 or sentence_count == 0:
        return 0.0
    
    # Calculate ratios
    chars_per_word = char_count / word_count
    words_per_sentence = word_count / sentence_count
    
    # Calculate alignment with golden ratio
    char_word_alignment = 1 - min(abs(chars_per_word / GOLDEN_RATIO - 1), 
                                 abs(GOLDEN_RATIO / chars_per_word - 1), 1)
    
    word_sentence_alignment = 1 - min(abs(words_per_sentence / GOLDEN_RATIO - 1),
                                     abs(GOLDEN_RATIO / words_per_sentence - 1), 1)
    
    # Average the alignments
    return (char_word_alignment + word_sentence_alignment) / 2

def calculate_fibonacci_alignment(text: str) -> float:
    """
    Calculate how closely the text structure aligns with the Fibonacci sequence.
    
    Args:
        text: The text to analyze
    
    Returns:
        Alignment score between 0 and 1
    """
    if not text or not text.strip():
        return 0.0
    
    # Split text into paragraphs, sentences, and words
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    words = text.split()
    
    # Count elements
    paragraph_count = len(paragraphs)
    sentence_count = len(sentences)
    word_count = len(words)
    
    # Find closest Fibonacci numbers
    closest_paragraph_fib = closest_fibonacci(paragraph_count)
    closest_sentence_fib = closest_fibonacci(sentence_count)
    closest_word_fib = closest_fibonacci(word_count)
    
    # Calculate alignment scores (proximity to Fibonacci numbers)
    paragraph_alignment = 1 - min(abs(paragraph_count - closest_paragraph_fib) / max(paragraph_count, 1), 1)
    sentence_alignment = 1 - min(abs(sentence_count - closest_sentence_fib) / max(sentence_count, 1), 1)
    word_alignment = 1 - min(abs(word_count - closest_word_fib) / max(word_count, 1), 1)
    
    # Average the alignments
    return (paragraph_alignment + sentence_alignment + word_alignment) / 3

def closest_fibonacci(n: int) -> int:
    """
    Find the closest Fibonacci number to the given number.
    
    Args:
        n: The number to find the closest Fibonacci number for
    
    Returns:
        The closest Fibonacci number
    """
    if n <= 0:
        return 1
    
    # Extend Fibonacci sequence if necessary
    fib_seq = FIBONACCI_SEQUENCE.copy()
    while fib_seq[-1] < n * 2:
        fib_seq.append(fib_seq[-1] + fib_seq[-2])
    
    # Find closest
    closest = fib_seq[0]
    min_diff = abs(n - closest)
    
    for fib in fib_seq:
        diff = abs(n - fib)
        if diff < min_diff:
            min_diff = diff
            closest = fib
    
    return closest

def detect_numeric_patterns(text: str) -> float:
    """
    Detect numeric patterns in the text and return a resonance score.
    
    Args:
        text: The text to analyze
        
    Returns:
        Resonance score for numeric patterns (0.0-1.0)
    """
    # Extract all numbers from text
    numbers = re.findall(r'\d+', text)
    
    # Check for sacred numbers (3, 7, 12, etc.)
    sacred_numbers = [3, 7, 12, 108, 144, 1008]
    sacred_count = sum(1 for num in numbers if int(num) in sacred_numbers)
    
    # Calculate pattern score based on frequency and distribution
    base_score = min(1.0, len(numbers) / 100)  # Base score from frequency
    sacred_bonus = min(0.5, sacred_count / 10)  # Bonus for sacred numbers
    
    return min(1.0, base_score + sacred_bonus)

def detect_geometric_patterns(text: str) -> float:
    """
    Detect references to geometric patterns in the text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Resonance score for geometric patterns (0.0-1.0)
    """
    # Keywords related to sacred geometry
    geometric_terms = [
        'circle', 'triangle', 'square', 'pentagon', 'hexagon', 
        'sacred geometry', 'vesica piscis', 'flower of life',
        'merkaba', 'metatron', 'cube', 'platonic solid'
    ]
    
    # Count occurrences
    text_lower = text.lower()
    occurrence_count = sum(text_lower.count(term) for term in geometric_terms)
    
    # Calculate score based on occurrence density
    return min(1.0, occurrence_count / 10)

def detect_symbolic_patterns(text: str) -> float:
    """
    Detect symbolic patterns and archetypes in the text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Resonance score for symbolic patterns (0.0-1.0)
    """
    # Keywords related to sacred symbols and archetypes
    symbolic_terms = [
        'light', 'dark', 'sun', 'moon', 'star', 'water', 'fire',
        'earth', 'air', 'spirit', 'divine', 'sacred', 'holy',
        'tree', 'serpent', 'dragon', 'phoenix', 'eagle', 'lion'
    ]
    
    # Count occurrences
    text_lower = text.lower()
    occurrence_count = sum(text_lower.count(term) for term in symbolic_terms)
    
    # Calculate score based on occurrence density and text length
    text_length_factor = min(1.0, len(text) / 5000)
    return min(1.0, (occurrence_count / 20) * text_length_factor)

def detect_linguistic_patterns(text: str) -> float:
    """
    Detect linguistic patterns like alliteration, repetition, etc.
    
    Args:
        text: The text to analyze
        
    Returns:
        Resonance score for linguistic patterns (0.0-1.0)
    """
    # Check for repetitions
    words = re.findall(r'\b\w+\b', text.lower())
    unique_words = set(words)
    repetition_factor = 1 - (len(unique_words) / len(words)) if words else 0
    
    # Check for alliteration
    alliteration_count = 0
    for i in range(len(words) - 1):
        if words[i] and words[i+1] and words[i][0] == words[i+1][0]:
            alliteration_count += 1
    alliteration_factor = min(1.0, alliteration_count / (len(words) / 5)) if words else 0
    
    # Combined score
    return min(1.0, (repetition_factor * 0.5) + (alliteration_factor * 0.5))

def calculate_quantum_entanglement(text: str) -> float:
    """
    Analyze the text for quantum-like entanglement patterns between concepts.
    
    Args:
        text: The text to analyze
        
    Returns:
        Quantum entanglement score (0.0-1.0)
    """
    # Keywords representing paired concepts
    concept_pairs = [
        ('light', 'dark'), ('above', 'below'), ('inner', 'outer'),
        ('heaven', 'earth'), ('mind', 'body'), ('spirit', 'matter'),
        ('male', 'female'), ('sun', 'moon'), ('life', 'death')
    ]
    
    text_lower = text.lower()
    entanglement = 0.0
    
    # Check for paired concepts appearing in proximity
    for concept1, concept2 in concept_pairs:
        if concept1 in text_lower and concept2 in text_lower:
            # Give higher score if both concepts are present
            # and even higher if they appear close to each other
            positions1 = [m.start() for m in re.finditer(r'\b' + concept1 + r'\b', text_lower)]
            positions2 = [m.start() for m in re.finditer(r'\b' + concept2 + r'\b', text_lower)]
            
            if positions1 and positions2:
                min_distance = min(abs(p1 - p2) for p1 in positions1 for p2 in positions2)
                proximity_score = math.exp(-min_distance / 1000)  # Higher score for closer concepts
                entanglement += proximity_score / len(concept_pairs)
    
    return min(1.0, entanglement)

def find_sacred_patterns(text: str) -> dict:
    """
    Find and score various sacred patterns in the provided text.
    
    Args:
        text: Text to analyze for sacred patterns
        
    Returns:
        Dictionary containing scores for different types of patterns
    """
    # Calculate individual pattern scores
    numeric_score = detect_numeric_patterns(text)
    geometric_score = detect_geometric_patterns(text)
    symbolic_score = detect_symbolic_patterns(text)
    linguistic_score = detect_linguistic_patterns(text)
    golden_ratio_score = calculate_golden_ratio_alignment(text)
    fibonacci_score = calculate_fibonacci_alignment(text)
    quantum_score = calculate_quantum_entanglement(text)
    
    # Return a dictionary of all pattern scores
    return {
        "numeric_patterns": numeric_score,
        "geometric_patterns": geometric_score,
        "symbolic_patterns": symbolic_score,
        "linguistic_patterns": linguistic_score,
        "golden_ratio_alignment": golden_ratio_score,
        "fibonacci_alignment": fibonacci_score,
        "quantum_entanglement": quantum_score
    } 