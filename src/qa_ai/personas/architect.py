"""
The Architect: System design and integration testing persona.
"""

import logging
from typing import Dict, List, Any
from pathlib import Path
import json
import time

from qa_ai.personas.base_persona import BasePersona

logger = logging.getLogger(__name__)

class Architect(BasePersona):
    """
    The Architect focuses on system design and integration testing,
    ensuring components work together as expected.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the Architect persona"""
        super().__init__(
            name="The Architect",
            description="Focuses on system design and integration testing",
            config=config
        )
        self.integration_patterns = [
            "API Gateway", "Service Mesh", "Event-Driven", 
            "Microservices", "Database Integration", "Third-Party Services"
        ]
    
    def generate_test_cases(self, target: str, test_type: str, output_dir: Path) -> List[Path]:
        """
        Generate integration-focused test cases.
        
        Args:
            target: The target system or URL to test
            test_type: The type of test (e.g., e2e, integration)
            output_dir: Directory to save the generated tests
            
        Returns:
            List of paths to the generated test files
        """
        logger.info(f"Architect generating {test_type} tests for {target}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        generated_files = []
        
        # Create integration test scenarios based on patterns
        for pattern in self.integration_patterns:
            if pattern.lower() in target.lower() or test_type == "integration":
                test_file = output_dir / f"test_integration_{pattern.lower().replace('-', '_')}.py"
                
                # Create a test file with integration testing best practices
                with open(test_file, 'w') as f:
                    f.write(self._generate_integration_test_template(target, pattern))
                
                generated_files.append(test_file)
                self.active_scenarios.append(f"Integration test for {pattern}")
        
        # Create system design validation tests
        if test_type == "e2e":
            system_test_file = output_dir / "test_system_architecture.py"
            with open(system_test_file, 'w') as f:
                f.write(self._generate_system_test_template(target))
            
            generated_files.append(system_test_file)
            self.active_scenarios.append("System architecture validation")
        
        logger.info(f"Architect generated {len(generated_files)} test files")
        return generated_files
    
    def analyze_results(self, results_path: Path) -> Dict[str, Any]:
        """
        Analyze test results with focus on system integration issues.
        
        Args:
            results_path: Path to the test results file/directory
            
        Returns:
            Dictionary containing architectural analysis
        """
        logger.info(f"Architect analyzing results from {results_path}")
        
        # In a real implementation, this would parse the test results
        # and provide insights on system design and integration issues
        
        # Simulated analysis for demonstration
        analysis = {
            "integration_issues": [
                {"component": "API Gateway", "issue": "Timeout during high load", "severity": "High"},
                {"component": "Database Integration", "issue": "Connection pooling inefficient", "severity": "Medium"}
            ],
            "architectural_recommendations": [
                "Consider implementing circuit breaker pattern for API calls",
                "Database connection pooling needs optimization"
            ],
            "system_health_score": 85,
            "bottlenecks": ["Authentication service", "Report generation"]
        }
        
        return analysis
    
    def _generate_integration_test_template(self, target: str, pattern: str) -> str:
        """Generate code for an integration test based on the pattern"""
        return f"""
# Integration test for {pattern} with {target}
import pytest
import requests

def test_{pattern.lower().replace('-', '_')}_integration():
    \"\"\"
    Test the integration with {pattern} component
    \"\"\"
    # Setup test environment
    base_url = "{target}"
    
    # Execute integration test
    response = requests.get(f"{{base_url}}/api/{pattern.lower().replace(' ', '-')}")
    
    # Verify integration is working
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "operational"

def test_{pattern.lower().replace('-', '_')}_error_handling():
    \"\"\"
    Test error handling in {pattern} integration
    \"\"\"
    # Implementation here
    pass
"""
    
    def _generate_system_test_template(self, target: str) -> str:
        """Generate code for a system architecture test"""
        return f"""
# System architecture validation test for {target}
import pytest
import requests

def test_system_components_availability():
    \"\"\"
    Verify all system components are available
    \"\"\"
    base_url = "{target}"
    components = ["auth", "api", "database", "cache", "storage"]
    
    for component in components:
        response = requests.get(f"{{base_url}}/health/{{component}}")
        assert response.status_code == 200, f"{{component}} is not available"
        assert response.json()["status"] == "up", f"{{component}} is not up"

def test_system_latency():
    \"\"\"
    Verify system response times are within acceptable limits
    \"\"\"
    base_url = "{target}"
    response = requests.get(f"{{base_url}}/api/status")
    
    # Verify response time is acceptable
    assert response.elapsed.total_seconds() < 1.0, "System response time exceeds threshold"
"""