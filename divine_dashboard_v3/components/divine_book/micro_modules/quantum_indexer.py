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
Quantum Indexer Module

Provides quantum-enhanced document indexing and search capabilities
using advanced text analysis and TF-IDF principles.
"""

import re
import math
import time
import random
from collections import Counter
from typing import Dict, List, Any, Optional, Tuple, Set

class QuantumIndex:
    """Quantum-enhanced document indexing system."""
    
    def __init__(self):
        self.documents = []
        self.document_term_freq = []  # Term frequency for each document
        self.inverse_doc_freq = {}    # Inverse document frequency for terms
        self.term_index = {}          # Inverted index: term -> document IDs
        self.quantum_interference = {}  # Simulates quantum interference effects
        self.last_update = 0
    
    def add_document(self, doc_info: Dict[str, Any]) -> int:
        """Add a document to the index."""
        doc_id = len(self.documents)
        self.documents.append(doc_info)
        
        # Extract text from document
        content = ""
        try:
            with open(doc_info["path"], 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            content = doc_info.get("title", "") + " " + doc_info.get("description", "")
        
        # Process document text
        terms = self._tokenize(content)
        
        # Calculate term frequency
        term_freq = Counter(terms)
        self.document_term_freq.append(term_freq)
        
        # Update inverted index
        for term in term_freq:
            if term not in self.term_index:
                self.term_index[term] = []
            self.term_index[term].append(doc_id)
            
            # Apply quantum interference effects
            self._apply_quantum_interference(term, doc_id)
        
        # Mark for IDF update
        self.last_update = time.time()
        
        return doc_id
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into terms, removing stopwords."""
        # Remove non-alphanumeric characters
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        
        # Split into words
        words = text.split()
        
        # Remove stopwords (common words that don't help with search)
        stopwords = {
            "a", "an", "the", "and", "or", "but", "if", "then", "else", "when",
            "at", "by", "for", "with", "about", "against", "between", "into",
            "through", "during", "before", "after", "above", "below", "to", "from",
            "up", "down", "in", "out", "on", "off", "over", "under", "again",
            "further", "then", "once", "here", "there", "when", "where", "why",
            "how", "all", "any", "both", "each", "few", "more", "most", "other",
            "some", "such", "no", "nor", "not", "only", "own", "same", "so",
            "than", "too", "very", "can", "will", "just", "should", "now"
        }
        
        # Keep only non-stopwords with length > 2
        terms = [word for word in words if word not in stopwords and len(word) > 2]
        
        return terms
    
    def _update_idf(self):
        """Update inverse document frequency values."""
        num_docs = len(self.documents)
        
        for term, doc_ids in self.term_index.items():
            # Number of documents containing the term
            doc_freq = len(set(doc_ids))
            
            # Calculate IDF: log(N / df)
            self.inverse_doc_freq[term] = math.log(num_docs / max(1, doc_freq))
    
    def _apply_quantum_interference(self, term: str, doc_id: int):
        """
        Apply simulated quantum interference effects to enhance search.
        
        This is a simplified simulation of quantum concepts for enhanced ranking.
        """
        # Generate "superposition" values based on term
        if term not in self.quantum_interference:
            # Initialize with a phase value between -1 and 1
            phase = math.sin(hash(term) % 100 / 50 * math.pi)
            self.quantum_interference[term] = {
                "phase": phase,
                "amplitude": random.uniform(0.5, 1.0),
                "entangled_terms": set()
            }
            
            # Find "entangled" terms (terms that often appear together)
            for other_term in self.term_index:
                if other_term != term and random.random() < 0.05:  # 5% chance of entanglement
                    self.quantum_interference[term]["entangled_terms"].add(other_term)
                    if other_term in self.quantum_interference:
                        self.quantum_interference[other_term]["entangled_terms"].add(term)
    
    def search(self, query: str, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Search documents using quantum-enhanced TF-IDF.
        
        Args:
            query: The search query string
            top_n: Maximum number of results to return
            
        Returns:
            List of document dictionaries with scores
        """
        # Check if we need to update IDF values
        if time.time() - self.last_update > 60:  # Update if older than 60 seconds
            self._update_idf()
            self.last_update = time.time()
        
        # Tokenize query
        query_terms = self._tokenize(query)
        
        # Get unique terms
        unique_query_terms = set(query_terms)
        
        # Add entangled terms (quantum effect)
        expanded_terms = unique_query_terms.copy()
        for term in unique_query_terms:
            if term in self.quantum_interference:
                expanded_terms.update(self.quantum_interference[term]["entangled_terms"])
        
        # Calculate scores for each document
        scores = [0.0] * len(self.documents)
        
        for term in expanded_terms:
            if term not in self.term_index:
                continue
                
            # Get IDF value (or default if not calculated yet)
            idf = self.inverse_doc_freq.get(term, 1.0)
            
            # Get quantum interference effects
            quantum_factor = 1.0
            if term in self.quantum_interference:
                qi = self.quantum_interference[term]
                # Apply quantum amplitude boost
                quantum_factor = qi["amplitude"]
                
                # Apply phase effect: terms in original query get positive phase
                if term in unique_query_terms:
                    quantum_factor *= (1.0 + qi["phase"])
                else:
                    # Entangled terms might get negative phase (interference)
                    quantum_factor *= (1.0 - qi["phase"] * 0.5)
            
            # Score documents containing this term
            for doc_id in self.term_index[term]:
                # Get term frequency in document
                tf = self.document_term_freq[doc_id].get(term, 0)
                
                # Apply quantum-boosted TF-IDF score
                scores[doc_id] += tf * idf * quantum_factor
        
        # Sort documents by score
        doc_scores = [(i, score) for i, score in enumerate(scores) if score > 0]
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N documents with scores
        results = []
        for doc_id, score in doc_scores[:top_n]:
            doc = self.documents[doc_id].copy()
            doc["score"] = score
            results.append(doc)
        
        return results

# Global quantum index instance
_quantum_index = None

def index_documents(documents: List[Dict[str, Any]]) -> None:
    """
    Index documents for quantum search.
    
    Args:
        documents: List of document dictionaries
    """
    global _quantum_index
    _quantum_index = QuantumIndex()
    
    for doc in documents:
        _quantum_index.add_document(doc)

def search_documents(documents: List[Dict[str, Any]], query: str, top_n: int = 10) -> List[Dict[str, Any]]:
    """
    Search documents using quantum indexing.
    
    Args:
        documents: List of document dictionaries
        query: Search query string
        top_n: Maximum number of results to return
        
    Returns:
        List of matching documents
    """
    global _quantum_index
    
    # Create index if it doesn't exist
    if _quantum_index is None:
        index_documents(documents)
    
    # Search using the index
    return _quantum_index.search(query, top_n) 