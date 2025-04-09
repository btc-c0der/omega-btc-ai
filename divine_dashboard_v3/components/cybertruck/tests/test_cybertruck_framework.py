#!/usr/bin/env python3
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
    CybertruckComponent,
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
    assert ComponentCategory.EXOSKELETON.value == "exoskeleton"
    assert ComponentCategory.POWERTRAIN.value == "powertrain"
    assert ComponentCategory.SUSPENSION.value == "suspension"
    assert ComponentCategory.AUTOPILOT.value == "autopilot"

def test_test_stage():
    """Test the TestStage enum."""
    assert TestStage.DEFINE.value == "define"
    assert TestStage.IMPLEMENT.value == "implement"
    assert TestStage.RUN.value == "run"
    assert TestStage.PASS.value == "pass"
    assert TestStage.FAIL.value == "fail"

def test_test_priority():
    """Test the TestPriority enum."""
    assert TestPriority.P0.value == "p0"
    assert TestPriority.P1.value == "p1"
    assert TestPriority.P2.value == "p2"

# Test the TestCase class
class TestTestCase:
    """Tests for the TestCase class."""
    
    def test_initialization(self):
        """Test the initialization of a TestCase."""
        test_case = TestCase(
            id="test-case-id",
            module_id="module-id",
            name="Test Case",
            description="Test case description",
            priority=TestPriority.P0,
            expected_results=["Expected result 1", "Expected result 2"],
            author="Test Author",
            stage=TestStage.DEFINE
        )
        
        assert test_case.id == "test-case-id"
        assert test_case.module_id == "module-id"
        assert test_case.name == "Test Case"
        assert test_case.description == "Test case description"
        assert test_case.priority == TestPriority.P0
        assert len(test_case.expected_results) == 2
        assert test_case.author == "Test Author"
        assert test_case.stage == TestStage.DEFINE
    
    def test_to_dict(self):
        """Test converting a TestCase to a dictionary."""
        test_case = TestCase(
            id="test-case-id",
            module_id="module-id",
            name="Test Case",
            description="Test case description",
            priority=TestPriority.P0,
            expected_results=["Expected result 1", "Expected result 2"],
            author="Test Author",
            stage=TestStage.DEFINE
        )
        
        test_dict = test_case.to_dict()
        
        assert test_dict["id"] == "test-case-id"
        assert test_dict["module_id"] == "module-id"
        assert test_dict["name"] == "Test Case"
        assert test_dict["description"] == "Test case description"
        assert test_dict["priority"] == "p0"
        assert len(test_dict["expected_results"]) == 2
        assert test_dict["author"] == "Test Author"
        assert test_dict["stage"] == "define"

# Test the CybertruckComponent class
class TestCybertruckComponent:
    """Tests for the CybertruckComponent class."""
    
    def test_initialization(self):
        """Test the initialization of a CybertruckComponent."""
        component = CybertruckComponent(
            id="component-id",
            name="Component Name",
            category=ComponentCategory.EXOSKELETON,
            description="Component description",
            author="Component Author"
        )
        
        assert component.id == "component-id"
        assert component.name == "Component Name"
        assert component.category == ComponentCategory.EXOSKELETON
        assert component.description == "Component description"
        assert component.author == "Component Author"
    
    def test_to_dict(self):
        """Test converting a CybertruckComponent to a dictionary."""
        component = CybertruckComponent(
            id="component-id",
            name="Component Name",
            category=ComponentCategory.EXOSKELETON,
            description="Component description",
            author="Component Author"
        )
        
        component_dict = component.to_dict()
        
        assert component_dict["id"] == "component-id"
        assert component_dict["name"] == "Component Name"
        assert component_dict["category"] == "exoskeleton"
        assert component_dict["description"] == "Component description"
        assert component_dict["author"] == "Component Author"

# Test the TestFirstFramework class
class TestTestFirstFramework:
    """Tests for the TestFirstFramework class."""
    
    def test_initialization(self, test_framework):
        """Test the initialization of TestFirstFramework."""
        assert test_framework.project_root == "/tmp/cybertruck_test"
        assert test_framework.report_dir == "/tmp/cybertruck_test/reports"
        assert isinstance(test_framework.modules, dict)
        assert isinstance(test_framework.test_cases, dict)
    
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
            assert module.id.startswith("CT-EXOSKELETON-TEST_MODULE-")
    
    def test_define_test_case(self, test_framework, test_module):
        """Test defining a test case."""
        with mock.patch('cybertruck_test_framework.json.dump'):
            test_case = test_framework.define_test_case(
                module_id=test_module.id,
                name="Test Case",
                description="Test case description",
                priority=TestPriority.P0,
                expected_results=["Expected result 1", "Expected result 2"],
                author="Test Author"
            )
            
            assert test_case.name == "Test Case"
            assert test_case.description == "Test case description"
            assert test_case.priority == TestPriority.P0
            assert len(test_case.expected_results) == 2
            assert test_case.author == "Test Author"
            assert test_case.stage == TestStage.DEFINE
    
    def test_get_module_by_id(self, test_framework, test_module):
        """Test getting a module by ID."""
        module = test_framework.get_module_by_id(test_module.id)
        assert module.id == test_module.id
        assert module.name == test_module.name
    
    def test_get_test_cases_for_module(self, test_framework, test_module, test_case):
        """Test getting test cases for a module."""
        test_cases = test_framework.get_test_cases_for_module(test_module.id)
        assert len(test_cases) == 1
        assert test_cases[0].id == test_case.id
    
    def test_implement_test_case(self, test_framework, test_case):
        """Test implementing a test case."""
        with mock.patch('cybertruck_test_framework.json.dump'):
            with mock.patch('cybertruck_test_framework.os.path.exists', return_value=True):
                test_framework.implement_test_case(
                    test_case_id=test_case.id,
                    implementation_path="/tmp/cybertruck_test/tests/test_exoskeleton.py"
                )
                
                implemented_case = test_framework.get_test_case_by_id(test_case.id)
                assert implemented_case.stage == TestStage.IMPLEMENT
                assert implemented_case.implementation_path == "/tmp/cybertruck_test/tests/test_exoskeleton.py"
    
    def test_mark_test_pass(self, test_framework, test_case):
        """Test marking a test as passed."""
        with mock.patch('cybertruck_test_framework.json.dump'):
            with mock.patch('cybertruck_test_framework.os.path.exists', return_value=True):
                # First implement the test case
                test_framework.implement_test_case(
                    test_case_id=test_case.id,
                    implementation_path="/tmp/cybertruck_test/tests/test_exoskeleton.py"
                )
                
                # Then mark it as passed
                test_framework.mark_test_pass(test_case.id)
                
                passed_case = test_framework.get_test_case_by_id(test_case.id)
                assert passed_case.stage == TestStage.PASS
    
    def test_mark_test_fail(self, test_framework, test_case):
        """Test marking a test as failed."""
        with mock.patch('cybertruck_test_framework.json.dump'):
            with mock.patch('cybertruck_test_framework.os.path.exists', return_value=True):
                # First implement the test case
                test_framework.implement_test_case(
                    test_case_id=test_case.id,
                    implementation_path="/tmp/cybertruck_test/tests/test_exoskeleton.py"
                )
                
                # Then mark it as failed
                test_framework.mark_test_fail(test_case.id, "Test failure reason")
                
                failed_case = test_framework.get_test_case_by_id(test_case.id)
                assert failed_case.stage == TestStage.FAIL
                assert failed_case.failure_reason == "Test failure reason"
    
    def test_save_load_modules(self, test_framework, test_module):
        """Test saving and loading modules."""
        # Mock the file operations
        mock_data = {}
        
        def mock_dump(data, file):
            nonlocal mock_data
            mock_data = data
        
        def mock_load(file):
            return mock_data
        
        with mock.patch('cybertruck_test_framework.json.dump', side_effect=mock_dump):
            with mock.patch('cybertruck_test_framework.json.load', side_effect=mock_load):
                with mock.patch('cybertruck_test_framework.os.path.exists', return_value=True):
                    with mock.patch('builtins.open', mock.mock_open()):
                        # Save modules
                        test_framework._save_modules()
                        
                        # Clear modules
                        test_framework.modules = {}
                        
                        # Load modules
                        test_framework._load_modules()
                        
                        # Check if modules were loaded
                        assert len(test_framework.modules) == 1
                        assert test_module.id in test_framework.modules
    
    def test_calculate_coverage(self, test_framework, test_module, test_case):
        """Test calculating coverage."""
        with mock.patch('cybertruck_test_framework.json.dump'):
            with mock.patch('cybertruck_test_framework.os.path.exists', return_value=True):
                # First implement the test case
                test_framework.implement_test_case(
                    test_case_id=test_case.id,
                    implementation_path="/tmp/cybertruck_test/tests/test_exoskeleton.py"
                )
                
                # Then mark it as passed
                test_framework.mark_test_pass(test_case.id)
                
                # Calculate coverage
                with mock.patch('cybertruck_test_framework.subprocess.run', return_value=mock.MagicMock(
                    stdout=json.dumps({
                        "totals": {
                            "percent_covered": 85.0
                        }
                    })
                )):
                    coverage = test_framework.calculate_coverage(test_module.id)
                    assert coverage == 85.0
    
    def test_generate_report(self, test_framework, test_module, test_case):
        """Test generating a report."""
        with mock.patch('cybertruck_test_framework.json.dump'):
            with mock.patch('cybertruck_test_framework.os.path.exists', return_value=True):
                # First implement the test case
                test_framework.implement_test_case(
                    test_case_id=test_case.id,
                    implementation_path="/tmp/cybertruck_test/tests/test_exoskeleton.py"
                )
                
                # Then mark it as passed
                test_framework.mark_test_pass(test_case.id)
                
                # Generate report
                with mock.patch('builtins.open', mock.mock_open()):
                    report_path = test_framework.generate_report(test_module.id)
                    assert report_path is not None 