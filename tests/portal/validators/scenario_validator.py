#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OMEGA SCENARIO VALIDATOR
Divine validator for Gherkin scenarios.

GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void
"""

import re
from typing import List, Tuple
from ..models.quantum_collaboration import Scenario

class ScenarioValidator:
    """Divine validator for Gherkin scenarios."""
    
    def __init__(self):
        self.technical_patterns = [
            r'click',
            r'type',
            r'select',
            r'press',
            r'enter',
            r'input'
        ]
        self.business_outcomes = [
            r'achieve',
            r'complete',
            r'verify',
            r'confirm',
            r'ensure',
            r'validate'
        ]
    
    def validate_scenario(self, scenario: Scenario) -> Tuple[bool, List[str]]:
        """Validate a scenario against divine principles."""
        issues = []
        
        # Check Given-When-Then structure
        if not scenario.given_steps:
            issues.append("Scenario lacks Given steps")
        if not scenario.when_steps:
            issues.append("Scenario lacks When steps")
        if not scenario.then_steps:
            issues.append("Scenario lacks Then steps")
        
        # Check for technical implementation details
        for step in scenario.given_steps + scenario.when_steps + scenario.then_steps:
            if any(re.search(pattern, step.lower()) for pattern in self.technical_patterns):
                issues.append(f"Step contains technical implementation: {step}")
        
        # Check for business outcomes
        has_business_outcome = any(
            re.search(pattern, step.lower())
            for step in scenario.then_steps
            for pattern in self.business_outcomes
        )
        if not has_business_outcome:
            issues.append("Scenario lacks clear business outcome")
        
        return len(issues) == 0, issues
    
    def enhance_scenario(self, scenario: Scenario) -> Scenario:
        """Enhance a scenario through divine principles."""
        # Convert technical steps to business-focused steps
        enhanced_steps = []
        for step in scenario.given_steps + scenario.when_steps + scenario.then_steps:
            enhanced_step = step
            for pattern in self.technical_patterns:
                if re.search(pattern, step.lower()):
                    enhanced_step = self._convert_to_business_step(step)
            enhanced_steps.append(enhanced_step)
        
        # Calculate divine metrics
        scenario.divine_clarity = self._calculate_divine_clarity(enhanced_steps)
        scenario.abstraction_level = self._calculate_abstraction_level(enhanced_steps)
        scenario.business_focus = self._calculate_business_focus(enhanced_steps)
        
        return scenario
    
    def _convert_to_business_step(self, step: str) -> str:
        """Convert technical step to business-focused step."""
        # Example conversions
        conversions = {
            r'click': 'select',
            r'type': 'enter',
            r'press': 'activate',
            r'input': 'provide'
        }
        
        for tech, business in conversions.items():
            if re.search(tech, step.lower()):
                return re.sub(tech, business, step, flags=re.IGNORECASE)
        return step
    
    def _calculate_divine_clarity(self, steps: List[str]) -> float:
        """Calculate divine clarity score for steps."""
        # Mock implementation
        return 0.95
    
    def _calculate_abstraction_level(self, steps: List[str]) -> float:
        """Calculate abstraction level score for steps."""
        # Mock implementation
        return 0.92
    
    def _calculate_business_focus(self, steps: List[str]) -> float:
        """Calculate business focus score for steps."""
        # Mock implementation
        return 0.98 