#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OMEGA FEATURE FILE MANAGER
Divine manager for Gherkin feature files.

GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple
from ..models.quantum_collaboration import FeatureFile, Scenario

class FeatureFileManager:
    """Divine manager for Gherkin feature files."""
    
    def __init__(self):
        self.feature_files: Dict[str, FeatureFile] = {}
        self.tag_index: Dict[str, Set[str]] = {}
        self.scenario_index: Dict[str, List[str]] = {}
        self.divine_tags = {
            '@smoke': 'Basic functionality verification',
            '@regression': 'Comprehensive test coverage',
            '@critical': 'Business-critical features',
            '@divine': 'Sacred core functionality',
            '@quantum': 'Quantum-enhanced features',
            '@cosmic': 'Universal system features'
        }
    
    def load_feature_file(self, file_path: str) -> FeatureFile:
        """Load and analyze a feature file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Divine feature file not found: {file_path}")
        
        with open(path, 'r') as f:
            content = f.read()
        
        # Extract tags and scenarios
        tags = self._extract_tags(content)
        scenarios = self._extract_scenarios(content)
        
        feature_file = FeatureFile(
            path=str(path),
            title=self._extract_title(content),
            tags=tags,
            scenarios=scenarios,
            last_modified=datetime.fromtimestamp(path.stat().st_mtime),
            divine_organization=self._calculate_divine_organization(content),
            version=self._extract_version(content)
        )
        
        self._index_feature_file(feature_file)
        return feature_file
    
    def _extract_tags(self, content: str) -> Set[str]:
        """Extract divine tags from feature file content."""
        tags = set()
        tag_pattern = r'@\w+'
        for match in re.finditer(tag_pattern, content):
            tag = match.group(0)
            if tag in self.divine_tags:
                tags.add(tag)
        return tags
    
    def _extract_scenarios(self, content: str) -> List[Scenario]:
        """Extract scenarios from feature file content."""
        scenarios = []
        scenario_pattern = r'Scenario:(.*?)(?=Scenario:|$)'
        for match in re.finditer(scenario_pattern, content, re.DOTALL):
            scenario_text = match.group(1).strip()
            scenarios.append(self._parse_scenario(scenario_text))
        return scenarios
    
    def _parse_scenario(self, scenario_text: str) -> Scenario:
        """Parse a scenario text into a Scenario object."""
        given_steps = []
        when_steps = []
        then_steps = []
        
        for line in scenario_text.split('\n'):
            line = line.strip()
            if line.startswith('Given'):
                given_steps.append(line)
            elif line.startswith('When'):
                when_steps.append(line)
            elif line.startswith('Then'):
                then_steps.append(line)
        
        return Scenario(
            title=scenario_text.split('\n')[0].strip(),
            given_steps=given_steps,
            when_steps=when_steps,
            then_steps=then_steps,
            divine_clarity=0.0,
            abstraction_level=0.0,
            business_focus=0.0
        )
    
    def _extract_title(self, content: str) -> str:
        """Extract feature title from content."""
        title_match = re.search(r'Feature:(.*?)(?=\n|$)', content)
        return title_match.group(1).strip() if title_match else "Untitled Feature"
    
    def _extract_version(self, content: str) -> str:
        """Extract version from content or return default."""
        version_match = re.search(r'@version\s+(\d+\.\d+\.\d+)', content)
        return version_match.group(1) if version_match else "1.0.0"
    
    def _calculate_divine_organization(self, content: str) -> float:
        """Calculate divine organization score for the feature file."""
        # Mock implementation - in reality would analyze structure, duplication, etc.
        return 0.95
    
    def _index_feature_file(self, feature_file: FeatureFile) -> None:
        """Index a feature file for quick retrieval."""
        self.feature_files[feature_file.path] = feature_file
        
        # Index by tags
        for tag in feature_file.tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = set()
            self.tag_index[tag].add(feature_file.path)
        
        # Index by scenario
        for scenario in feature_file.scenarios:
            scenario_key = scenario.title
            if scenario_key not in self.scenario_index:
                self.scenario_index[scenario_key] = []
            self.scenario_index[scenario_key].append(feature_file.path)
    
    def find_by_tag(self, tag: str) -> List[FeatureFile]:
        """Find feature files by divine tag."""
        if tag not in self.tag_index:
            return []
        return [self.feature_files[path] for path in self.tag_index[tag]]
    
    def find_duplicate_scenarios(self) -> List[Tuple[str, List[str]]]:
        """Find duplicate scenarios across feature files."""
        duplicates = []
        for scenario_title, file_paths in self.scenario_index.items():
            if len(file_paths) > 1:
                duplicates.append((scenario_title, file_paths))
        return duplicates
    
    def refactor_feature_file(self, file_path: str) -> FeatureFile:
        """Refactor a feature file to improve divine organization."""
        feature_file = self.load_feature_file(file_path)
        
        # Remove duplicate scenarios
        unique_scenarios = []
        seen_titles = set()
        for scenario in feature_file.scenarios:
            if scenario.title not in seen_titles:
                unique_scenarios.append(scenario)
                seen_titles.add(scenario.title)
        
        # Update feature file
        feature_file.scenarios = unique_scenarios
        feature_file.divine_organization = self._calculate_divine_organization(
            self._generate_feature_content(feature_file)
        )
        
        # Save refactored content
        self._save_feature_file(feature_file)
        
        return feature_file
    
    def _generate_feature_content(self, feature_file: FeatureFile) -> str:
        """Generate feature file content from FeatureFile object."""
        content = []
        
        # Add tags
        content.extend(feature_file.tags)
        
        # Add feature title
        content.append(f"Feature: {feature_file.title}")
        
        # Add scenarios
        for scenario in feature_file.scenarios:
            content.append(f"\nScenario: {scenario.title}")
            content.extend(scenario.given_steps)
            content.extend(scenario.when_steps)
            content.extend(scenario.then_steps)
        
        return "\n".join(content)
    
    def _save_feature_file(self, feature_file: FeatureFile) -> None:
        """Save feature file content to disk."""
        content = self._generate_feature_content(feature_file)
        with open(feature_file.path, 'w') as f:
            f.write(content) 