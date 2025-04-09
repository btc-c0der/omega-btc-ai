#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OMEGA FEATURE FILE MANAGER TESTS
Divine tests for feature file management.

GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void
"""

import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from ..managers.feature_file_manager import FeatureFileManager

class TestFeatureFileManager(unittest.TestCase):
    """Divine tests for FeatureFileManager."""
    
    def setUp(self):
        """Set up divine test environment."""
        self.manager = FeatureFileManager()
        self.temp_dir = tempfile.mkdtemp()
        self.feature_file_path = os.path.join(self.temp_dir, "test.feature")
        self._create_test_feature_file()
    
    def tearDown(self):
        """Clean up divine test environment."""
        if os.path.exists(self.feature_file_path):
            os.remove(self.feature_file_path)
        os.rmdir(self.temp_dir)
    
    def _create_test_feature_file(self):
        """Create a divine test feature file."""
        content = """
@smoke @divine
Feature: Divine Test Feature
  As a divine being
  I want to test the feature file manager
  So that I can ensure its divine functionality

Scenario: Loading a feature file
  Given I have a valid feature file
  When I load the feature file
  Then I should get a FeatureFile object
  And the object should contain all the divine information

Scenario: Finding by tag
  Given I have loaded multiple feature files
  When I search for files with @divine tag
  Then I should get all divine feature files
"""
        with open(self.feature_file_path, 'w') as f:
            f.write(content)
    
    def test_load_feature_file(self):
        """Test divine feature file loading."""
        feature_file = self.manager.load_feature_file(self.feature_file_path)
        
        self.assertEqual(feature_file.title, "Divine Test Feature")
        self.assertEqual(feature_file.path, self.feature_file_path)
        self.assertEqual(len(feature_file.tags), 2)
        self.assertEqual(len(feature_file.scenarios), 2)
        self.assertTrue(isinstance(feature_file.last_modified, datetime))
        self.assertTrue(0 <= feature_file.divine_organization <= 1)
        self.assertEqual(feature_file.version, "1.0.0")
    
    def test_find_by_tag(self):
        """Test divine tag-based search."""
        self.manager.load_feature_file(self.feature_file_path)
        divine_files = self.manager.find_by_tag('@divine')
        
        self.assertEqual(len(divine_files), 1)
        self.assertEqual(divine_files[0].path, self.feature_file_path)
    
    def test_find_duplicate_scenarios(self):
        """Test divine duplicate scenario detection."""
        # Create a duplicate scenario in another file
        duplicate_file_path = os.path.join(self.temp_dir, "duplicate.feature")
        with open(duplicate_file_path, 'w') as f:
            f.write("""
@smoke
Feature: Duplicate Feature

Scenario: Loading a feature file
  Given I have a valid feature file
  When I load the feature file
  Then I should get a FeatureFile object
""")
        
        self.manager.load_feature_file(self.feature_file_path)
        self.manager.load_feature_file(duplicate_file_path)
        
        duplicates = self.manager.find_duplicate_scenarios()
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0][0], "Loading a feature file")
        self.assertEqual(len(duplicates[0][1]), 2)
        
        os.remove(duplicate_file_path)
    
    def test_refactor_feature_file(self):
        """Test divine feature file refactoring."""
        # Create a file with duplicate scenarios
        duplicate_scenario_file = os.path.join(self.temp_dir, "duplicates.feature")
        with open(duplicate_scenario_file, 'w') as f:
            f.write("""
@smoke
Feature: Duplicate Scenarios

Scenario: First Scenario
  Given some setup
  When something happens
  Then something should be true

Scenario: First Scenario
  Given some setup
  When something happens
  Then something should be true
""")
        
        refactored = self.manager.refactor_feature_file(duplicate_scenario_file)
        self.assertEqual(len(refactored.scenarios), 1)
        
        os.remove(duplicate_scenario_file)
    
    def test_invalid_file_path(self):
        """Test divine error handling for invalid paths."""
        with self.assertRaises(FileNotFoundError):
            self.manager.load_feature_file("nonexistent.feature")

if __name__ == '__main__':
    unittest.main() 