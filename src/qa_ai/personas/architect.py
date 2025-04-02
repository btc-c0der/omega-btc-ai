from typing import Dict, List
from pathlib import Path
from .base import QAPersona, TestCase

class ArchitectPersona(QAPersona):
    """The Architect persona focuses on system design and integration testing"""
    
    def __init__(self):
        super().__init__(
            name="The Architect",
            expertise=[
                "System Architecture",
                "Integration Testing",
                "API Testing",
                "Performance Testing",
                "Scalability Analysis"
            ]
        )
    
    def analyze_requirements(self, requirements: Dict) -> List[TestCase]:
        """Analyze requirements from an architectural perspective"""
        test_cases = []
        
        # Analyze system components
        for component in requirements.get("components", []):
            test_case = TestCase(
                name=f"Component Integration: {component['name']}",
                description=f"Verify integration of {component['name']} with other system components",
                steps=[
                    f"Initialize {component['name']} component",
                    "Verify component dependencies",
                    "Test component interfaces",
                    "Validate data flow between components"
                ],
                expected_results=[
                    "Component initializes successfully",
                    "All dependencies are properly resolved",
                    "Interfaces function as expected",
                    "Data flows correctly between components"
                ],
                priority=1,
                category="integration"
            )
            test_cases.append(test_case)
        
        # Analyze API endpoints
        for endpoint in requirements.get("apis", []):
            test_case = TestCase(
                name=f"API Endpoint: {endpoint['path']}",
                description=f"Verify {endpoint['method']} {endpoint['path']} endpoint functionality",
                steps=[
                    f"Prepare {endpoint['method']} request",
                    "Set appropriate headers and parameters",
                    "Send request to endpoint",
                    "Validate response format and content"
                ],
                expected_results=[
                    "Request is properly formatted",
                    "Response matches expected schema",
                    "Status code is appropriate",
                    "Error handling is correct"
                ],
                priority=2,
                category="api"
            )
            test_cases.append(test_case)
        
        self.test_cases.extend(test_cases)
        return test_cases
    
    def generate_test_script(self, test_case: TestCase, framework: str = "playwright") -> str:
        """Generate test script for the Architect's test cases"""
        if framework == "playwright":
            return self._generate_playwright_script(test_case)
        else:
            raise ValueError(f"Unsupported framework: {framework}")
    
    def _generate_playwright_script(self, test_case: TestCase) -> str:
        """Generate Playwright test script"""
        script = f'''import pytest
from playwright.sync_api import Page, expect

def test_{test_case.name.lower().replace(' ', '_')}(page: Page):
    """
    {test_case.description}
    """
    # Test steps
    {self._format_steps(test_case.steps)}
    
    # Verify expected results
    {self._format_expected_results(test_case.expected_results)}
'''
        return script
    
    def _format_steps(self, steps: List[str]) -> str:
        """Format test steps for the script"""
        formatted = []
        for i, step in enumerate(steps, 1):
            formatted.append(f"    # Step {i}: {step}")
        return "\n".join(formatted)
    
    def _format_expected_results(self, results: List[str]) -> str:
        """Format expected results for the script"""
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(f"    # Expected {i}: {result}")
        return "\n".join(formatted)
    
    def review_test_results(self, results: Dict) -> Dict:
        """Review test results and provide architectural insights"""
        insights = {
            "system_health": "good",
            "integration_points": [],
            "performance_metrics": {},
            "recommendations": []
        }
        
        # Analyze integration test results
        for test in results.get("integration_tests", []):
            if test["status"] == "failed":
                insights["integration_points"].append({
                    "component": test["component"],
                    "issue": test["error"],
                    "severity": "high"
                })
        
        # Analyze performance metrics
        if "performance_metrics" in results:
            insights["performance_metrics"] = {
                "response_time": results["performance_metrics"].get("avg_response_time"),
                "throughput": results["performance_metrics"].get("requests_per_second"),
                "error_rate": results["performance_metrics"].get("error_rate")
            }
        
        # Generate recommendations
        if insights["integration_points"]:
            insights["recommendations"].append(
                "Review and fix integration points with high severity issues"
            )
        
        return insights 