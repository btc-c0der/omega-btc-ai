"""
QA AI Personas module - AI-powered test personas with specialized focuses.
"""

import logging
from typing import Dict, Any

from qa_ai.personas.factory import PersonaFactory
from qa_ai.personas.base_persona import BasePersona
from qa_ai.personas.architect import Architect
from qa_ai.personas.explorer import Explorer
from qa_ai.personas.guardian import Guardian

__all__ = [
    'PersonaFactory',
    'BasePersona',
    'Architect',
    'Explorer',
    'Guardian',
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)