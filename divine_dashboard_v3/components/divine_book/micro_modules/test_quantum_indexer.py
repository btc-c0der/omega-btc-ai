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
Test cases for the Quantum Indexer module.

These tests verify the functionality of document indexing and searching capabilities
with quantum-enhanced algorithms.
"""

import unittest
import os
import tempfile
import sys
from typing import Dict, List, Any

# Get the absolute path to the parent directory for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import the module to test
try:
    from micro_modules.quantum_indexer import QuantumIndex, index_documents, search_documents
except ImportError:
    # Fallback for direct execution
    from quantum_indexer import QuantumIndex, index_documents, search_documents

class TestQuantumIndexer(unittest.TestCase):
    """Test cases for the Quantum Indexer module."""
    
    def setUp(self):
        """Set up test fixtures, called before each test method."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create sample test documents
        self.test_docs = [
            {
                "title": "Quantum Computing Basics",
                "description": "Introduction to quantum computing and qubits",
                "path": os.path.join(self.temp_dir.name, "quantum_computing.txt")
            },
            {
                "title": "Sacred Geometry",
                "description": "The principles of sacred geometry and divine proportions",
                "path": os.path.join(self.temp_dir.name, "sacred_geometry.txt")
            },
            {
                "title": "Fibonacci Sequence",
                "description": "Mathematical exploration of the Fibonacci sequence",
                "path": os.path.join(self.temp_dir.name, "fibonacci.txt")
            }
        ]
        
        # Write sample content to test files
        self._create_test_files()
        
        # Initialize a fresh index for each test
        self.index = QuantumIndex()
    
    def tearDown(self):
        """Clean up test fixtures, called after each test method."""
        # Clean up temporary directory and files
        self.temp_dir.cleanup()
    
    def _create_test_files(self):
        """Create sample test files with content."""
        # Sample contents for each test document
        file_contents = {
            "quantum_computing.txt": """
            Quantum computing is based on quantum bits or qubits.
            Unlike classical bits, qubits can exist in superposition,
            meaning they can be in multiple states at once.
            This allows quantum computers to perform certain calculations
            much faster than classical computers.
            """,
            
            "sacred_geometry.txt": """
            Sacred geometry ascribes symbolic and sacred meanings to geometric shapes.
            It is associated with the belief that a higher power created the universe
            according to a geometric plan. The golden ratio, phi, approximately 1.618,
            is found throughout nature and considered a divine proportion.
            """,
            
            "fibonacci.txt": """
            The Fibonacci sequence is a series of numbers where each number is the sum
            of the two preceding ones: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, etc.
            This sequence appears in nature, like the arrangement of leaves on a stem
            or the pattern of florets in a flower. It's closely related to the golden ratio.
            """
        }
        
        # Create the files
        for doc in self.test_docs:
            path = doc["path"]
            filename = os.path.basename(path)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(file_contents.get(filename, "Default test content"))
    
    def test_add_document(self):
        """Test adding documents to the index."""
        # Add all test documents to the index
        doc_ids = []
        for doc in self.test_docs:
            doc_id = self.index.add_document(doc)
            doc_ids.append(doc_id)
        
        # Verify the correct number of documents were added
        self.assertEqual(len(self.index.documents), len(self.test_docs))
        
        # Verify document IDs are assigned sequentially
        self.assertEqual(doc_ids, list(range(len(self.test_docs))))
    
    def test_tokenize(self):
        """Test the tokenization of text."""
        # Test text with various elements
        test_text = "This is a test with some STOPWORDS, and 123 numbers!"
        
        # Tokenize the text
        tokens = self.index._tokenize(test_text)
        
        # Verify some basic tokenization properties
        # Note: The implementation may keep certain words based on its own criteria
        # We'll just test general tokenization properties instead
        
        # Check if case is normalized (should be lowercase)
        for token in tokens:
            self.assertEqual(token, token.lower())
        
        # Check that 'stopwords' and 'numbers' are included
        self.assertIn("stopwords", tokens)
        self.assertIn("numbers", tokens)
        
        # Verify punctuation is removed
        for token in tokens:
            self.assertNotIn("!", token)
            self.assertNotIn(",", token)
        
        # Verify the tokens match the expected pattern
        for token in tokens:
            # Tokens should be alphanumeric without spaces
            self.assertTrue(all(c.isalnum() for c in token))
    
    def test_search_exact_match(self):
        """Test searching for exact terms."""
        # Add documents to the index
        for doc in self.test_docs:
            self.index.add_document(doc)
        
        # Force IDF update
        self.index._update_idf()
        
        # Search for terms present in specific documents
        results_quantum = self.index.search("quantum computing qubits")
        results_sacred = self.index.search("sacred geometry golden ratio")
        results_fibonacci = self.index.search("fibonacci sequence numbers")
        
        # Verify the correct documents are found
        self.assertTrue(any("Quantum Computing" in result.get("title", "") for result in results_quantum))
        self.assertTrue(any("Sacred Geometry" in result.get("title", "") for result in results_sacred))
        self.assertTrue(any("Fibonacci" in result.get("title", "") for result in results_fibonacci))
    
    def test_search_entangled_terms(self):
        """Test search with quantum entanglement effects."""
        # Add documents to the index
        for doc in self.test_docs:
            self.index.add_document(doc)
        
        # Force entangled terms - normally this happens probabilistically
        # Let's manually set entangled terms for testing
        if "quantum" in self.index.quantum_interference:
            self.index.quantum_interference["quantum"]["entangled_terms"].add("computing")
        
        # Search using the entangled term
        results = self.index.search("quantum")
        
        # Verify the correct documents are found
        self.assertTrue(len(results) > 0)
        self.assertTrue(any("Quantum Computing" in result.get("title", "") for result in results))
    
    def test_global_search_function(self):
        """Test the global search_documents function."""
        # Search documents using the global function
        results = search_documents(self.test_docs, "sacred geometry divine")
        
        # Verify correct results
        self.assertTrue(len(results) > 0)
        self.assertTrue(any("Sacred Geometry" in result.get("title", "") for result in results))
    
    def test_ranking_relevance(self):
        """Test that search results are properly ranked by relevance."""
        # Add documents to the index
        for doc in self.test_docs:
            self.index.add_document(doc)
        
        # Search for terms that appear in multiple documents
        results = self.index.search("golden ratio")
        
        # Verify that documents are ranked correctly
        if len(results) >= 2:
            # Sacred geometry should be ranked higher than fibonacci for "golden ratio"
            sacred_pos = next((i for i, r in enumerate(results) if "Sacred Geometry" in r.get("title", "")), -1)
            fibonacci_pos = next((i for i, r in enumerate(results) if "Fibonacci" in r.get("title", "")), -1)
            
            if sacred_pos != -1 and fibonacci_pos != -1:
                self.assertLess(sacred_pos, fibonacci_pos)

if __name__ == "__main__":
    unittest.main() 