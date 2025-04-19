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

"""
Tests for cybertruck_test_framework.py
-------------------------------------

These tests cover the key components of the Cybertruck Test Framework
to ensure proper functionality and maintain high test coverage.
"""

import os
import sys
import json
import pytest
import unittest.mock as mock
from pathlib import Path
from enum import Enum

# Add the parent directory to the path so we can import the module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import from the cybertruck_test_framework
from cybertruck_test_framework import (
    Colors,
    ComponentCategory,
    TestStage,
    TestPriority,
    TestCase,
    MicroModule,
    TestFirstFramework
)

# Test fixtures
@pytest.fixture
def test_framework():
    """Create a TestFirstFramework instance for testing."""
    with mock.patch('cybertruck_test_framework.os.makedirs'):
        return TestFirstFramework(
            project_root="/tmp/cybertruck_test",
            report_dir="/tmp/cybertruck_test/reports"
        )

@pytest.fixture
def test_module(test_framework):
    """Create a test module for testing."""
    with mock.patch('cybertruck_test_framework.json.dump'):
        module = test_framework.create_module(
            name="Test Exoskeleton",
            category=ComponentCategory.EXOSKELETON,
            description="Test module for the exoskeleton"
        )
        return module

@pytest.fixture
def test_case(test_framework, test_module):
    """Create a test case for testing."""
    with mock.patch('cybertruck_test_framework.json.dump'):
        test_case = test_framework.define_test_case(
            module_id=test_module.id,
            name="Impact Resistance",
            description="Test exoskeleton resistance to impact",
            priority=TestPriority.P0,
            expected_results=["Should withstand impact of 15,000 joules"],
            author="Tesla QA Team"
        )
        return test_case

# Test the Colors class
def test_colors():
    """Test the Colors class."""
    assert Colors.RED.startswith('\033[')
    assert Colors.GREEN.startswith('\033[')
    assert Colors.YELLOW.startswith('\033[')
    assert Colors.ENDC.startswith('\033[')

# Test the Enums
def test_component_category():
    """Test the ComponentCategory enum."""
    assert ComponentCategory.EXOSKELETON is not None
    assert ComponentCategory.POWERTRAIN is not None
    assert ComponentCategory.SUSPENSION is not None
    assert ComponentCategory.AUTOPILOT is not None

def test_test_stage():
    """Test the TestStage enum."""
    assert TestStage.DEFINED.value == "DEFINED"
    assert TestStage.IMPLEMENTED.value == "IMPLEMENTED"
    assert TestStage.RUNNING.value == "RUNNING"
    assert TestStage.PASSED.value == "PASSED"
    assert TestStage.FAILED.value == "FAILED"

def test_test_priority():
    """Test the TestPriority enum."""
    assert TestPriority.P0.value == 0
    assert TestPriority.P1.value == 1
    assert TestPriority.P2.value == 2
    assert TestPriority.P3.value == 3

# Test the TestCase class
class TestTestCase:
    """Tests for the TestCase class."""
    
    def test_initialization(self):
        """Test the initialization of a TestCase."""
        test_case = TestCase(
            id="test-case-id",
            name="Test Case",
            description="Test case description",
            category=ComponentCategory.EXOSKELETON,
            priority=TestPriority.P0,
            expected_results=["Expected result 1", "Expected result 2"],
            author="Test Author",
            stage=TestStage.DEFINED
        )
        
        assert test_case.id == "test-case-id"
        assert test_case.name == "Test Case"
        assert test_case.description == "Test case description"
        assert test_case.category == ComponentCategory.EXOSKELETON
        assert test_case.priority == TestPriority.P0
        assert len(test_case.expected_results) == 2
        assert test_case.author == "Test Author"
        assert test_case.stage == TestStage.DEFINED
    
    def test_to_dict(self):
        """Test converting a TestCase to a dictionary."""
        test_case = TestCase(
            id="test-case-id",
            name="Test Case",
            description="Test case description",
            category=ComponentCategory.EXOSKELETON,
            priority=TestPriority.P0,
            expected_results=["Expected result 1", "Expected result 2"],
            author="Test Author",
            stage=TestStage.DEFINED
        )
        
        test_dict = test_case.to_dict()
        
        assert test_dict["id"] == "test-case-id"
        assert test_dict["name"] == "Test Case"
        assert test_dict["description"] == "Test case description"
        assert test_dict["author"] == "Test Author"
        # The enum values would be serialized differently now

# Test the MicroModule class (previously CybertruckComponent)
class TestMicroModule:
    """Tests for the MicroModule class."""
    
    def test_initialization(self):
        """Test the initialization of a MicroModule."""
        module = MicroModule(
            id="module-id",
            name="Module Name",
            category=ComponentCategory.EXOSKELETON,
            description="Module description"
        )
        
        assert module.id == "module-id"
        assert module.name == "Module Name"
        assert module.category == ComponentCategory.EXOSKELETON
        assert module.description == "Module description"
    
    def test_to_dict(self):
        """Test converting a MicroModule to a dictionary."""
        module = MicroModule(
            id="module-id",
            name="Module Name",
            category=ComponentCategory.EXOSKELETON,
            description="Module description"
        )
        
        module_dict = module.to_dict()
        
        assert module_dict["id"] == "module-id"
        assert module_dict["name"] == "Module Name"
        assert module_dict["description"] == "Module description"
        # Category would be serialized differently

# Test the TestFirstFramework class
class TestTestFirstFramework:
    """Tests for the TestFirstFramework class."""
    
    def test_initialization(self, test_framework):
        """Test the initialization of TestFirstFramework."""
        assert test_framework.project_root == "/tmp/cybertruck_test"
        assert test_framework.report_dir == "/tmp/cybertruck_test/reports"
        assert isinstance(test_framework.modules, dict)
    
    def test_create_module(self, test_framework):
        """Test creating a module."""
        with mock.patch('cybertruck_test_framework.json.dump'):
            module = test_framework.create_module(
                name="Test Module",
                category=ComponentCategory.EXOSKELETON,
                description="Test module description"
            )
            
            assert module.name == "Test Module"
            assert module.category == ComponentCategory.EXOSKELETON
            assert module.description == "Test module description"
            assert module.id in test_framework.modules
    
    def test_define_test_case(self, test_framework, test_module):
        """Test defining a test case."""
        with mock.patch('cybertruck_test_framework.json.dump'):
            test_case = test_framework.define_test_case(
                module_id=test_module.id,
                name="Test Case",
                description="Test case description",
                priority=TestPriority.P0,
                expected_results=["Expected result"],
                author="Test Author"
            )
            
            assert test_case.name == "Test Case"
            assert test_case.description == "Test case description"
            assert test_case.priority == TestPriority.P0
            assert test_case.author == "Test Author"
            assert test_module.test_cases[test_case.id] == test_case 