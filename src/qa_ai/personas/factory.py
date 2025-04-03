"""
Factory for creating and managing persona instances.
"""

import logging
from typing import Dict, Any, Optional

from qa_ai.personas.base_persona import BasePersona
from qa_ai.personas.architect import Architect
from qa_ai.personas.explorer import Explorer
from qa_ai.personas.guardian import Guardian

logger = logging.getLogger(__name__)

class PersonaFactory:
    """Factory class for creating and managing QA personas."""
    
    @staticmethod
    def create_persona(persona_type: str, config: Optional[Dict[str, Any]] = None) -> BasePersona:
        """
        Create a persona instance based on the specified type.
        
        Args:
            persona_type: The type of persona to create (architect, explorer, guardian)
            config: Optional configuration dictionary for the persona
            
        Returns:
            An instance of the requested persona
            
        Raises:
            ValueError: If the persona type is not supported
        """
        persona_type = persona_type.lower()
        
        if persona_type == "architect":
            return Architect(config)
        elif persona_type == "explorer":
            return Explorer(config)
        elif persona_type == "guardian":
            return Guardian(config)
        else:
            logger.error(f"Unsupported persona type: {persona_type}")
            raise ValueError(f"Unsupported persona type: {persona_type}")