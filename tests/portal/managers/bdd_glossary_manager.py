#!/usr/bin/env python3

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

# -*- coding: utf-8 -*-

"""
OMEGA BDD GLOSSARY MANAGER
Divine manager for BDD domain terminology.

GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Set, Optional
from pathlib import Path
import json

@dataclass
class DomainTerm:
    """Sacred representation of a domain-specific term."""
    term: str
    definition: str
    examples: List[str]
    related_terms: Set[str]
    team_owner: str
    last_updated: datetime
    divine_clarity: float

class BDDGlossaryManager:
    """Divine manager for BDD domain terminology."""
    
    def __init__(self, glossary_path: str = "bdd_glossary.json"):
        self.glossary_path = Path(glossary_path)
        self.terms: Dict[str, DomainTerm] = {}
        self.team_terms: Dict[str, Set[str]] = {}
        self._load_glossary()
    
    def _load_glossary(self) -> None:
        """Load the divine glossary from disk."""
        if self.glossary_path.exists():
            with open(self.glossary_path, 'r') as f:
                data = json.load(f)
                for term_data in data:
                    term = DomainTerm(
                        term=term_data['term'],
                        definition=term_data['definition'],
                        examples=term_data['examples'],
                        related_terms=set(term_data['related_terms']),
                        team_owner=term_data['team_owner'],
                        last_updated=datetime.fromisoformat(term_data['last_updated']),
                        divine_clarity=term_data['divine_clarity']
                    )
                    self.terms[term.term] = term
                    if term.team_owner not in self.team_terms:
                        self.team_terms[term.team_owner] = set()
                    self.team_terms[term.team_owner].add(term.term)
    
    def _save_glossary(self) -> None:
        """Save the divine glossary to disk."""
        data = []
        for term in self.terms.values():
            term_data = {
                'term': term.term,
                'definition': term.definition,
                'examples': term.examples,
                'related_terms': list(term.related_terms),
                'team_owner': term.team_owner,
                'last_updated': term.last_updated.isoformat(),
                'divine_clarity': term.divine_clarity
            }
            data.append(term_data)
        
        with open(self.glossary_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_term(self, term: str, definition: str, examples: List[str],
                related_terms: Set[str], team_owner: str) -> DomainTerm:
        """Add a divine term to the glossary."""
        if term in self.terms:
            raise ValueError(f"Divine term already exists: {term}")
        
        new_term = DomainTerm(
            term=term,
            definition=definition,
            examples=examples,
            related_terms=related_terms,
            team_owner=team_owner,
            last_updated=datetime.now(),
            divine_clarity=0.95  # Initial divine clarity
        )
        
        self.terms[term] = new_term
        if team_owner not in self.team_terms:
            self.team_terms[team_owner] = set()
        self.team_terms[team_owner].add(term)
        
        self._save_glossary()
        return new_term
    
    def update_term(self, term: str, definition: Optional[str] = None,
                   examples: Optional[List[str]] = None,
                   related_terms: Optional[Set[str]] = None,
                   team_owner: Optional[str] = None) -> DomainTerm:
        """Update a divine term in the glossary."""
        if term not in self.terms:
            raise ValueError(f"Divine term not found: {term}")
        
        current_term = self.terms[term]
        
        if definition is not None:
            current_term.definition = definition
        if examples is not None:
            current_term.examples = examples
        if related_terms is not None:
            current_term.related_terms = related_terms
        if team_owner is not None:
            # Update team ownership
            old_team = current_term.team_owner
            self.team_terms[old_team].remove(term)
            if team_owner not in self.team_terms:
                self.team_terms[team_owner] = set()
            self.team_terms[team_owner].add(term)
            current_term.team_owner = team_owner
        
        current_term.last_updated = datetime.now()
        current_term.divine_clarity = self._calculate_divine_clarity(current_term)
        
        self._save_glossary()
        return current_term
    
    def get_term(self, term: str) -> Optional[DomainTerm]:
        """Retrieve a divine term from the glossary."""
        return self.terms.get(term)
    
    def get_team_terms(self, team: str) -> Set[str]:
        """Get all divine terms owned by a team."""
        return self.team_terms.get(team, set())
    
    def search_terms(self, query: str) -> List[DomainTerm]:
        """Search for divine terms matching the query."""
        query = query.lower()
        matches = []
        
        for term in self.terms.values():
            if (query in term.term.lower() or
                query in term.definition.lower() or
                any(query in example.lower() for example in term.examples)):
                matches.append(term)
        
        return matches
    
    def _calculate_divine_clarity(self, term: DomainTerm) -> float:
        """Calculate divine clarity score for a term."""
        # Mock implementation - in reality would analyze definition quality, examples, etc.
        return 0.95 