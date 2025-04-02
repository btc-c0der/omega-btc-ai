from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class TestCase:
    name: str
    description: str
    steps: List[str]
    expected_results: List[str]
    priority: int
    category: str

class QAPersona(ABC):
    """Base class for QA AI personas"""
    
    def __init__(self, name: str, expertise: List[str]):
        self.name = name
        self.expertise = expertise
        self.test_cases: List[TestCase] = []
    
    @abstractmethod
    def analyze_requirements(self, requirements: Dict) -> List[TestCase]:
        """Analyze requirements and generate test cases"""
        pass
    
    @abstractmethod
    def generate_test_script(self, test_case: TestCase, framework: str = "playwright") -> str:
        """Generate test script for a given test case"""
        pass
    
    @abstractmethod
    def review_test_results(self, results: Dict) -> Dict:
        """Review test results and provide insights"""
        pass
    
    def save_test_cases(self, output_dir: Path) -> None:
        """Save generated test cases to files"""
        for test_case in self.test_cases:
            test_file = output_dir / f"{test_case.name.lower().replace(' ', '_')}.py"
            test_script = self.generate_test_script(test_case)
            test_file.write_text(test_script)
    
    def get_metrics(self) -> Dict:
        """Get persona-specific metrics"""
        return {
            "name": self.name,
            "expertise": self.expertise,
            "test_cases_generated": len(self.test_cases),
            "categories": list(set(tc.category for tc in self.test_cases))
        }
    
    def __str__(self) -> str:
        return f"{self.name} (Expertise: {', '.join(self.expertise)})" 