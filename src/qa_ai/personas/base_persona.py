"""
Base class for all QA AI personas.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

class BasePersona(ABC):
    """Abstract base class for QA personas."""

    def __init__(self, name: str, description: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize a persona with its characteristics.
        
        Args:
            name: The name of the persona
            description: A description of the persona's focus
            config: Optional configuration dictionary
        """
        self.name = name
        self.description = description
        self.config = config or {}
        self.active_scenarios = []
        logger.info(f"Initialized {name} persona")
    
    @abstractmethod
    def generate_test_cases(self, target: str, test_type: str, output_dir: Path) -> List[Path]:
        """
        Generate test cases specific to this persona.
        
        Args:
            target: The target system or URL to test
            test_type: The type of test (e.g., e2e, unit, integration)
            output_dir: Directory to save the generated tests
            
        Returns:
            List of paths to the generated test files
        """
        pass
    
    @abstractmethod
    def analyze_results(self, results_path: Path) -> Dict[str, Any]:
        """
        Analyze test results based on persona's expertise.
        
        Args:
            results_path: Path to the test results file/directory
            
        Returns:
            Dictionary containing analysis results
        """
        pass
    
    def load_heuristics(self, heuristics_file: Optional[Path] = None) -> Dict[str, Any]:
        """
        Load testing heuristics for this persona.
        
        Args:
            heuristics_file: Optional path to a JSON file containing heuristics
        
        Returns:
            Dictionary of testing heuristics
        """
        if heuristics_file is None:
            # Default heuristics file location
            heuristics_file = Path(__file__).parent / "data" / f"{self.name.lower()}_heuristics.json"
        
        try:
            if heuristics_file.exists():
                with open(heuristics_file, 'r') as f:
                    return json.load(f)
            else:
                logger.warning(f"Heuristics file not found: {heuristics_file}")
                return {}
        except Exception as e:
            logger.error(f"Error loading heuristics: {str(e)}")
            return {}
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the persona.
        
        Returns:
            Dictionary containing persona status information
        """
        return {
            "name": self.name,
            "description": self.description,
            "active_scenarios": len(self.active_scenarios),
            "config": self.config
        }