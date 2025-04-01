"""
Quantum Proof-of-Work (qPoW) stylometric validator module.

This module provides stylometric analysis capabilities for the qPoW testnet,
inspired by the Doxer stylometric analysis library (https://github.com/goldmonkey21/doxer).
It helps identify authorship patterns in blockchain contributions for enhanced authentication.
"""

import os
import re
import math
import hashlib
import logging
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Set, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StylometricProfile:
    """
    Represents a stylometric profile of a node or author in the network.
    
    Inspired by the work of goldmonkey21 and the Doxer project, this class
    captures unique writing patterns and coding styles that can be used
    to authenticate contributions to the blockchain.
    """
    
    def __init__(self, name: str):
        """
        Initialize a stylometric profile.
        
        Args:
            name: Identifier for this profile
        """
        self.name = name
        self.function_lengths = []
        self.average_line_length = 0.0
        self.whitespace_ratio = 0.0
        self.indentation_style = ""
        self.comment_ratio = 0.0
        self.function_name_patterns = Counter()
        self.variable_name_patterns = Counter()
        self.common_bigrams = Counter()
        self.common_trigrams = Counter()
        self.linguistic_markers = {}
        
        # Markers specifically identified in the Doxer stylometric analysis
        self.back_of_envelope_usage = 0
        self.in_20_years_usage = 0
        self.sentence_structures = Counter()
        
    def to_dict(self) -> Dict:
        """Convert profile to dictionary format for serialization."""
        return {
            "name": self.name,
            "function_lengths": self.function_lengths,
            "average_line_length": self.average_line_length,
            "whitespace_ratio": self.whitespace_ratio,
            "indentation_style": self.indentation_style,
            "comment_ratio": self.comment_ratio,
            "function_name_patterns": dict(self.function_name_patterns),
            "variable_name_patterns": dict(self.variable_name_patterns),
            "common_bigrams": dict(self.common_bigrams),
            "common_trigrams": dict(self.common_trigrams),
            "linguistic_markers": self.linguistic_markers,
            "back_of_envelope_usage": self.back_of_envelope_usage,
            "in_20_years_usage": self.in_20_years_usage,
            "sentence_structures": dict(self.sentence_structures)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StylometricProfile':
        """Create profile from dictionary format."""
        profile = cls(data["name"])
        profile.function_lengths = data["function_lengths"]
        profile.average_line_length = data["average_line_length"]
        profile.whitespace_ratio = data["whitespace_ratio"]
        profile.indentation_style = data["indentation_style"]
        profile.comment_ratio = data["comment_ratio"]
        profile.function_name_patterns = Counter(data["function_name_patterns"])
        profile.variable_name_patterns = Counter(data["variable_name_patterns"])
        profile.common_bigrams = Counter(data["common_bigrams"])
        profile.common_trigrams = Counter(data["common_trigrams"])
        profile.linguistic_markers = data["linguistic_markers"]
        profile.back_of_envelope_usage = data["back_of_envelope_usage"]
        profile.in_20_years_usage = data["in_20_years_usage"]
        profile.sentence_structures = Counter(data["sentence_structures"])
        return profile
    
    def compute_fingerprint(self) -> str:
        """
        Compute a fingerprint hash that represents this stylometric profile.
        This can be used as a quick comparison method.
        """
        # Convert key elements of the profile to a string
        profile_str = (
            f"{self.name}|"
            f"{self.average_line_length}|"
            f"{self.whitespace_ratio}|"
            f"{self.indentation_style}|"
            f"{self.comment_ratio}|"
            f"{';'.join(str(x) for x in self.function_lengths[:10])}|"
            f"{';'.join(f'{k}:{v}' for k, v in self.function_name_patterns.most_common(10))}|"
            f"{';'.join(f'{k}:{v}' for k, v in self.variable_name_patterns.most_common(10))}|"
            f"{';'.join(f'{k}:{v}' for k, v in self.common_bigrams.most_common(10))}|"
            f"{';'.join(f'{k}:{v}' for k, v in self.common_trigrams.most_common(10))}|"
            f"{self.back_of_envelope_usage}|{self.in_20_years_usage}"
        )
        
        # Create a quantum-resistant hash of the profile string
        return hashlib.sha256(profile_str.encode()).hexdigest()


class StylometricAnalyzer:
    """
    Analyzes code or text samples to extract stylometric features.
    
    This class applies techniques similar to those used in the Doxer project
    to identify unique patterns in writing or coding style.
    """
    
    def __init__(self):
        """Initialize the stylometric analyzer."""
        self.known_profiles = {}
        
    def analyze_code(self, code_text: str, author_name: str = "unknown") -> StylometricProfile:
        """
        Analyze code text to extract stylometric features.
        
        Args:
            code_text: The code text to analyze
            author_name: Name to associate with this profile
            
        Returns:
            StylometricProfile containing the extracted features
        """
        profile = StylometricProfile(author_name)
        
        # Skip empty or very short code samples
        if not code_text or len(code_text) < 50:
            logger.warning(f"Code sample too small for stylometric analysis: {len(code_text)} chars")
            return profile
        
        lines = code_text.split('\n')
        
        # Basic metrics
        line_lengths = [len(line) for line in lines if line.strip()]
        profile.average_line_length = sum(line_lengths) / max(1, len(line_lengths))
        
        # Whitespace analysis
        total_chars = len(code_text)
        whitespace_chars = sum(1 for c in code_text if c.isspace())
        profile.whitespace_ratio = whitespace_chars / total_chars if total_chars > 0 else 0
        
        # Determine indentation style (spaces or tabs)
        space_indents = sum(1 for line in lines if line.startswith(' '))
        tab_indents = sum(1 for line in lines if line.startswith('\t'))
        profile.indentation_style = "spaces" if space_indents > tab_indents else "tabs"
        
        # Extract function/method definitions and their lengths
        function_pattern = re.compile(r'def\s+([a-zA-Z0-9_]+)\s*\(')
        functions = function_pattern.finditer(code_text)
        
        for match in functions:
            func_name = match.group(1)
            profile.function_name_patterns[self._extract_naming_pattern(func_name)] += 1
            
            # Find function end and calculate length
            start_pos = match.start()
            
            # Simple heuristic to find function end - this could be improved
            # by proper parsing, but works for basic analysis
            next_def = code_text.find('\ndef ', start_pos + 1)
            if next_def == -1:
                next_def = len(code_text)
                
            function_body = code_text[start_pos:next_def]
            function_lines = function_body.count('\n')
            profile.function_lengths.append(function_lines)
        
        # Variable naming patterns
        variable_pattern = re.compile(r'([a-zA-Z][a-zA-Z0-9_]*)\s*=')
        variables = variable_pattern.finditer(code_text)
        
        for match in variables:
            var_name = match.group(1)
            if var_name not in ('if', 'while', 'for'):  # Skip keywords
                profile.variable_name_patterns[self._extract_naming_pattern(var_name)] += 1
        
        # Comment analysis
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        profile.comment_ratio = comment_lines / len(lines) if lines else 0
        
        # N-gram analysis (character level)
        self._analyze_character_ngrams(code_text, profile)
        
        # Special pattern analysis (inspired by Doxer Satoshi analysis)
        self._analyze_special_patterns(code_text, profile)
        
        return profile
    
    def analyze_text(self, text: str, author_name: str = "unknown") -> StylometricProfile:
        """
        Analyze natural language text to extract stylometric features.
        
        Args:
            text: The text to analyze
            author_name: Name to associate with this profile
            
        Returns:
            StylometricProfile containing the extracted features
        """
        profile = StylometricProfile(author_name)
        
        # Skip empty or very short text samples
        if not text or len(text) < 50:
            logger.warning(f"Text sample too small for stylometric analysis: {len(text)} chars")
            return profile
        
        lines = text.split('\n')
        sentences = self._extract_sentences(text)
        
        # Basic metrics
        line_lengths = [len(line) for line in lines if line.strip()]
        profile.average_line_length = sum(line_lengths) / max(1, len(line_lengths))
        
        # Whitespace analysis
        total_chars = len(text)
        whitespace_chars = sum(1 for c in text if c.isspace())
        profile.whitespace_ratio = whitespace_chars / total_chars if total_chars > 0 else 0
        
        # Linguistic markers - sentence length
        sentence_lengths = [len(s) for s in sentences]
        avg_sentence_length = sum(sentence_lengths) / max(1, len(sentence_lengths))
        profile.linguistic_markers["avg_sentence_length"] = avg_sentence_length
        
        # Sentence structure analysis
        for sentence in sentences:
            # Simple classification of sentence structure
            words = sentence.split()
            if not words:
                continue
                
            # Classify by sentence length
            if len(words) < 5:
                structure = "very_short"
            elif len(words) < 10:
                structure = "short"
            elif len(words) < 20:
                structure = "medium"
            else:
                structure = "long"
                
            # Add beginning word pattern
            if words[0].lower() in ("the", "a", "an", "this", "that", "these", "those"):
                structure += "_determiner_start"
            elif words[0].lower() in ("i", "we", "you", "they", "he", "she", "it"):
                structure += "_pronoun_start"
                
            profile.sentence_structures[structure] += 1
        
        # N-gram analysis (character level)
        self._analyze_character_ngrams(text, profile)
        
        # Special pattern analysis (inspired by Doxer Satoshi analysis)
        self._analyze_special_patterns(text, profile)
        
        return profile
    
    def add_known_profile(self, profile: StylometricProfile):
        """Add a profile to the set of known profiles."""
        self.known_profiles[profile.name] = profile
        
    def compare_profiles(self, profile1: StylometricProfile, profile2: StylometricProfile) -> float:
        """
        Compare two stylometric profiles and return a similarity score.
        
        Args:
            profile1: First profile to compare
            profile2: Second profile to compare
            
        Returns:
            Similarity score between 0 and 1, where 1 is identical
        """
        # Compare using Burrows's Delta method (simplified)
        scores = []
        
        # Compare average line length
        line_length_diff = abs(profile1.average_line_length - profile2.average_line_length)
        line_length_score = 1.0 / (1.0 + line_length_diff)
        scores.append(line_length_score)
        
        # Compare whitespace ratio
        whitespace_diff = abs(profile1.whitespace_ratio - profile2.whitespace_ratio)
        whitespace_score = 1.0 - whitespace_diff
        scores.append(whitespace_score)
        
        # Compare indentation style
        indentation_score = 1.0 if profile1.indentation_style == profile2.indentation_style else 0.0
        scores.append(indentation_score)
        
        # Compare comment ratio
        comment_diff = abs(profile1.comment_ratio - profile2.comment_ratio)
        comment_score = 1.0 - comment_diff
        scores.append(comment_score)
        
        # Compare function length distributions
        if profile1.function_lengths and profile2.function_lengths:
            avg_func_len1 = sum(profile1.function_lengths) / len(profile1.function_lengths)
            avg_func_len2 = sum(profile2.function_lengths) / len(profile2.function_lengths)
            func_len_diff = abs(avg_func_len1 - avg_func_len2)
            func_len_score = 1.0 / (1.0 + func_len_diff / 10.0)  # Normalize
            scores.append(func_len_score)
        
        # Compare naming patterns using cosine similarity
        func_name_sim = self._cosine_similarity_counters(
            profile1.function_name_patterns, profile2.function_name_patterns)
        scores.append(func_name_sim)
        
        var_name_sim = self._cosine_similarity_counters(
            profile1.variable_name_patterns, profile2.variable_name_patterns)
        scores.append(var_name_sim)
        
        # Compare n-grams using cosine similarity
        bigram_sim = self._cosine_similarity_counters(
            profile1.common_bigrams, profile2.common_bigrams)
        scores.append(bigram_sim)
        
        trigram_sim = self._cosine_similarity_counters(
            profile1.common_trigrams, profile2.common_trigrams)
        scores.append(trigram_sim)
        
        # Special pattern markers from Doxer
        envelope_diff = abs(profile1.back_of_envelope_usage - profile2.back_of_envelope_usage)
        envelope_score = 1.0 / (1.0 + envelope_diff)
        scores.append(envelope_score)
        
        years_diff = abs(profile1.in_20_years_usage - profile2.in_20_years_usage)
        years_score = 1.0 / (1.0 + years_diff)
        scores.append(years_score)
        
        # Calculate overall score as weighted average
        # Give more weight to the more discriminative features
        weights = [0.5, 0.5, 1.0, 0.5, 1.0, 2.0, 2.0, 1.5, 1.5, 3.0, 3.0]
        
        # Normalize weights
        weight_sum = sum(weights[:len(scores)])
        norm_weights = [w / weight_sum for w in weights[:len(scores)]]
        
        # Calculate weighted average
        final_score = sum(s * w for s, w in zip(scores, norm_weights))
        
        return final_score
    
    def find_closest_profile(self, profile: StylometricProfile) -> Tuple[Optional[str], float]:
        """
        Find the closest matching profile from the known profiles.
        
        Args:
            profile: Profile to match
            
        Returns:
            Tuple of (profile_name, similarity_score)
        """
        if not self.known_profiles:
            return (None, 0.0)
            
        best_match = None
        best_score = -1.0
        
        for name, known_profile in self.known_profiles.items():
            score = self.compare_profiles(profile, known_profile)
            if score > best_score:
                best_score = score
                best_match = name
                
        return (best_match, best_score)
    
    def _extract_naming_pattern(self, name: str) -> str:
        """
        Extract a pattern from a name, focusing on style rather than the name itself.
        For example, camelCase vs snake_case.
        """
        pattern = ""
        for i, char in enumerate(name):
            if char.isupper():
                pattern += "U"
            elif char.islower():
                pattern += "l"
            elif char.isdigit():
                pattern += "d"
            elif char == '_':
                pattern += "_"
            else:
                pattern += "x"
                
        return pattern
    
    def _analyze_character_ngrams(self, text: str, profile: StylometricProfile):
        """Analyze character n-grams in the text."""
        # Extract bigrams
        for i in range(len(text) - 1):
            bigram = text[i:i+2]
            profile.common_bigrams[bigram] += 1
            
        # Extract trigrams
        for i in range(len(text) - 2):
            trigram = text[i:i+3]
            profile.common_trigrams[trigram] += 1
    
    def _extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text."""
        # Basic sentence splitting - could be improved with NLP libraries
        sentence_endings = re.compile(r'[.!?]')
        sentences = []
        last_end = 0
        
        for match in sentence_endings.finditer(text):
            end_pos = match.end()
            # Check if this is really a sentence end (not an abbreviation, etc.)
            if end_pos < len(text) and text[end_pos:end_pos+1].isspace():
                sentences.append(text[last_end:end_pos].strip())
                last_end = end_pos
                
        # Add the last sentence if any
        if last_end < len(text):
            sentences.append(text[last_end:].strip())
            
        return sentences
    
    def _analyze_special_patterns(self, text: str, profile: StylometricProfile):
        """
        Analyze special patterns identified in the Doxer project.
        
        These patterns were particularly useful in the Satoshi Nakamoto analysis.
        """
        # "back-of-the-envelope" pattern
        envelope_matches = re.findall(r'back.of.the.envelope', text.lower())
        profile.back_of_envelope_usage = len(envelope_matches)
        
        # "in 20 years" pattern
        years_matches = re.findall(r'in 20 years', text.lower())
        profile.in_20_years_usage = len(years_matches)
    
    def _cosine_similarity_counters(self, counter1: Counter, counter2: Counter) -> float:
        """
        Calculate cosine similarity between two Counter objects.
        
        This is used to compare frequency distributions of features.
        """
        # Get all keys
        all_keys = set(counter1.keys()) | set(counter2.keys())
        
        # Empty counters have zero similarity
        if not all_keys:
            return 0.0
            
        # Calculate dot product
        dot_product = sum(counter1.get(k, 0) * counter2.get(k, 0) for k in all_keys)
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(counter1.get(k, 0) ** 2 for k in all_keys))
        magnitude2 = math.sqrt(sum(counter2.get(k, 0) ** 2 for k in all_keys))
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
            
        return dot_product / (magnitude1 * magnitude2)


class StylometricBlockValidator:
    """
    Validates blockchain contributions based on stylometric analysis.
    
    This class integrates stylometric analysis into the blockchain validation process,
    providing an additional layer of authentication beyond traditional cryptographic methods.
    """
    
    def __init__(self):
        """Initialize the stylometric block validator."""
        self.analyzer = StylometricAnalyzer()
        self.node_profiles = {}  # Maps node IDs to their stylometric profiles
        self.trusted_fingerprints = set()  # Set of trusted stylometric fingerprints
        
    def register_node_profile(self, node_id: str, profile: StylometricProfile):
        """
        Register a stylometric profile for a node.
        
        Args:
            node_id: ID of the node
            profile: Stylometric profile to register
        """
        self.node_profiles[node_id] = profile
        
    def add_trusted_fingerprint(self, fingerprint: str):
        """
        Add a trusted stylometric fingerprint.
        
        Args:
            fingerprint: The fingerprint hash to add to trusted set
        """
        self.trusted_fingerprints.add(fingerprint)
        
    def validate_block_style(self, block_data: str, claimed_node_id: str) -> Tuple[bool, float]:
        """
        Validate that a block's style matches the claimed author's profile.
        
        Args:
            block_data: The data from the block to validate
            claimed_node_id: The node ID claiming to have created this block
            
        Returns:
            Tuple of (is_valid, confidence_score)
        """
        if claimed_node_id not in self.node_profiles:
            logger.warning(f"No known profile for node {claimed_node_id}")
            return (False, 0.0)
            
        # Get the claimed node's profile
        claimed_profile = self.node_profiles[claimed_node_id]
        
        # Analyze the block data
        block_profile = self.analyzer.analyze_text(block_data, "block")
        
        # Compare profiles
        similarity = self.analyzer.compare_profiles(block_profile, claimed_profile)
        
        # Determine if it's valid based on a threshold
        # This threshold could be adjusted based on security requirements
        threshold = 0.7
        is_valid = similarity >= threshold
        
        if not is_valid:
            logger.warning(f"Stylometric validation failed for block from {claimed_node_id} "
                           f"(similarity: {similarity:.4f})")
        
        return (is_valid, similarity)
    
    def fingerprint_block(self, block_data: str) -> str:
        """
        Generate a stylometric fingerprint for a block.
        
        Args:
            block_data: The data from the block
            
        Returns:
            A fingerprint hash representing the stylometric profile
        """
        block_profile = self.analyzer.analyze_text(block_data, "block")
        return block_profile.compute_fingerprint()
    
    def is_trusted_fingerprint(self, fingerprint: str) -> bool:
        """
        Check if a fingerprint is in the trusted set.
        
        Args:
            fingerprint: The fingerprint to check
            
        Returns:
            True if the fingerprint is trusted, False otherwise
        """
        return fingerprint in self.trusted_fingerprints


# ========================================================================
# Tribute to goldmonkey21 and the Doxer project
# ========================================================================

def print_doxer_tribute():
    """
    Print a tribute to goldmonkey21 and the Doxer project.
    
    This function acknowledges the inspiration for the stylometric analysis
    techniques used in this module.
    """
    tribute = """
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                                                                        ║
    ║               TRIBUTE TO GOLDMONKEY21 AND THE DOXER PROJECT           ║
    ║                                                                        ║
    ╠════════════════════════════════════════════════════════════════════════╣
    ║                                                                        ║
    ║  This stylometric analysis module is inspired by the pioneering work   ║
    ║  of goldmonkey21's Doxer project (https://github.com/goldmonkey21/    ║
    ║  doxer), which demonstrated the power of linguistic analysis for       ║
    ║  authorship attribution in the context of Bitcoin and beyond.          ║
    ║                                                                        ║
    ║  The Doxer project showed how "back-of-the-envelope" calculations,     ║
    ║  phrases like "in 20 years", and other linguistic patterns can reveal  ║
    ║  connections between texts written by the same author, even when they  ║
    ║  attempt to obscure their identity.                                    ║
    ║                                                                        ║
    ║  By integrating these techniques into our quantum-resistant blockchain, ║
    ║  we add an additional layer of validation that goes beyond traditional  ║
    ║  cryptographic methods, potentially providing protection against both   ║
    ║  quantum attacks and social engineering.                               ║
    ║                                                                        ║
    ║  JAH BLESS SATOSHI, and tip of the hat to goldmonkey21 for their       ║
    ║  fascinating work on authorship analysis!                              ║
    ║                                                                        ║
    ╚════════════════════════════════════════════════════════════════════════╝
    """
    print(tribute)


if __name__ == "__main__":
    print_doxer_tribute()
    
    # Example of using the stylometric validation
    analyzer = StylometricAnalyzer()
    
    # Example text samples
    satoshi_text = """
    The root problem with conventional currency is all the trust that's required to make it work. 
    The central bank must be trusted not to debase the currency, but the history of fiat currencies 
    is full of breaches of that trust. Banks must be trusted to hold our money and transfer it 
    electronically, but they lend it out in waves of credit bubbles with barely a fraction in reserve. 
    We have to trust them with our privacy, trust them not to let identity thieves drain our accounts. 
    Their massive overhead costs make micropayments impossible.
    
    A generation ago, multi-user time-sharing computer systems had a similar problem. Before strong 
    encryption, users had to rely on password protection to secure their files, placing trust in the 
    system administrator to keep their information private. Privacy could always be overridden by the 
    admin based on his judgment call weighing the principle of privacy against other concerns, or at 
    the behest of his superiors. Then strong encryption became available to the masses, and trust was 
    no longer required. Data could be secured in a way that was physically impossible for others to access, 
    no matter for what reason, no matter how good the excuse, no matter what.
    
    I'm sure that in 20 years there will either be very large transaction volume or no volume.
    """
    
    gavin_text = """
    I think it is very unlikely that in 20 years we will need to support more Bitcoin transactions 
    than all of the cash, credit card and international wire transactions that happen in the world today 
    (and that is the scale of transactions that a pretty-good year-2035 home computer and network 
    connection should be able to support).
    
    So I did a back-of-the-envelope calculation to see how much sprawl it might cause, worst case. 
    Take the 10,000 or so households in Amherst, count each as a "dwelling unit", multiple by 1,000 
    square feet, and you get: about 230 acres. Which is just a little over 1% of the total acreage in Amherst.
    """
    
    # Create profiles
    satoshi_profile = analyzer.analyze_text(satoshi_text, "satoshi")
    gavin_profile = analyzer.analyze_text(gavin_text, "gavin")
    
    # Add profiles to known set
    analyzer.add_known_profile(satoshi_profile)
    analyzer.add_known_profile(gavin_profile)
    
    # Test with a new text
    test_text = """
    I'm sure that in 20 years there will either be very large transaction volume or no volume.
    My back-of-the-envelope calculation suggests that we'll need to significantly increase
    the block size to handle all of the transactions that will occur if Bitcoin becomes widely used.
    """
    
    test_profile = analyzer.analyze_text(test_text, "unknown")
    
    # Find the closest match
    match_name, similarity = analyzer.find_closest_profile(test_profile)
    
    print(f"Test text most closely matches: {match_name} (similarity: {similarity:.4f})")
    
    # Run validator example
    validator = StylometricBlockValidator()
    validator.register_node_profile("satoshi_node", satoshi_profile)
    validator.register_node_profile("gavin_node", gavin_profile)
    
    # Validate a block
    is_valid, confidence = validator.validate_block_style(test_text, "satoshi_node")
    
    print(f"Block validation for 'satoshi_node': valid={is_valid}, confidence={confidence:.4f}")
    
    # Generate and check fingerprint
    fingerprint = validator.fingerprint_block(test_text)
    validator.add_trusted_fingerprint(fingerprint)
    
    print(f"Block fingerprint: {fingerprint}")
    print(f"Is trusted fingerprint: {validator.is_trusted_fingerprint(fingerprint)}") 