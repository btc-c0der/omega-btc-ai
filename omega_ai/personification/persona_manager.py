"""
Persona Manager for OMEGA BTC AI Bot Personification

This module provides functionality to manage different bot personas 
and integrate them into the OMEGA BTC AI trading dashboard.
"""

import os
import json
import importlib
import inspect
from typing import Dict, List, Any, Optional, Type, Union
import logging

from omega_ai.personification.persona_base import BasePersona

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PersonaManager:
    """
    Manages bot personas and their interactions with the OMEGA BTC AI system.
    
    This class is responsible for loading, registering, and accessing different
    personas, as well as handling persona-specific data storage and retrieval.
    """
    
    def __init__(self, personas_dir: str = "omega_ai/personification/personas", 
                 data_dir: str = "omega_ai/personification/data"):
        """
        Initialize the persona manager.
        
        Args:
            personas_dir: Directory containing persona modules
            data_dir: Directory for storing persona-specific data
        """
        self.personas_dir = personas_dir
        self.data_dir = data_dir
        self.personas: Dict[str, BasePersona] = {}
        self.active_persona: Optional[BasePersona] = None
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Load available personas
        self._discover_personas()
    
    def _discover_personas(self) -> None:
        """Discover available personas in the persona directory."""
        try:
            # Ensure personas directory exists
            if not os.path.exists(self.personas_dir):
                os.makedirs(self.personas_dir)
                logger.warning(f"Created missing personas directory: {self.personas_dir}")

            # Get all Python files in the personas directory
            persona_files = [
                f for f in os.listdir(self.personas_dir)
                if f.endswith('.py') and f != '__init__.py'
            ]
            
            logger.info(f"Found {len(persona_files)} potential persona files")
            
            # Import each potential persona module
            for persona_file in persona_files:
                module_name = persona_file[:-3]  # Remove .py extension
                module_path = f"omega_ai.personification.personas.{module_name}"
                
                try:
                    # Import the module
                    module = importlib.import_module(module_path)
                    
                    # Find all classes in the module that inherit from BasePersona
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if (issubclass(obj, BasePersona) and 
                            obj is not BasePersona and 
                            obj.__module__ == module.__name__):
                                
                            # Create an instance of the persona and register it
                            persona = obj()
                            self.register_persona(persona)
                            logger.info(f"Registered persona: {persona.name}")
                except Exception as e:
                    logger.error(f"Error importing persona from {module_path}: {e}")
            
            # Explicitly register our core personas to ensure they're always available
            # This is a fallback in case the auto-discovery fails
            from omega_ai.personification.personas.rasta_oracle import RastaOraclePersona
            from omega_ai.personification.personas.tech_analyst import TechnicalAnalystPersona
            from omega_ai.personification.personas.fib_strategist import FibStrategistPersona
            from omega_ai.personification.personas.strategic_trader_persona import StrategicTraderPersona
            from omega_ai.personification.personas.scalper_trader_persona import ScalperTraderPersona
            from omega_ai.personification.personas.elite_exit_persona import EliteExitPersona
            
            if not any(p.name == "Rasta Oracle" for p in self.personas.values()):
                self.register_persona(RastaOraclePersona())
            
            if not any(p.name == "Technical Analyst" for p in self.personas.values()):
                self.register_persona(TechnicalAnalystPersona())
                
            if not any(p.name == "Fibonacci Strategist" for p in self.personas.values()):
                self.register_persona(FibStrategistPersona())
                
            if not any(p.name == "Strategic Trader" for p in self.personas.values()):
                self.register_persona(StrategicTraderPersona())
                
            if not any(p.name == "Scalper Trader" for p in self.personas.values()):
                self.register_persona(ScalperTraderPersona())
                
            if not any(p.name == "Elite Exit Specialist" for p in self.personas.values()):
                self.register_persona(EliteExitPersona())
                
        except Exception as e:
            logger.error(f"Error discovering personas: {e}")
            
            # Ensure we have at least a fallback persona
            if not self.personas:
                from omega_ai.personification.personas.tech_analyst import TechnicalAnalystPersona
                self.register_persona(TechnicalAnalystPersona())
    
    def register_persona(self, persona: BasePersona) -> None:
        """
        Register a new persona with the manager.
        
        Args:
            persona: BasePersona instance to register
        """
        self.personas[persona.name] = persona
        
        # Set as active persona if none is active
        if not self.active_persona:
            self.set_active_persona(persona.name)
    
    def get_persona(self, name: str) -> Optional[BasePersona]:
        """
        Get a persona by name.
        
        Args:
            name: Name of the persona to retrieve
            
        Returns:
            The persona instance, or None if not found
        """
        return self.personas.get(name)
    
    def set_active_persona(self, name: str) -> bool:
        """
        Set the active persona by name.
        
        Args:
            name: Name of the persona to set as active
            
        Returns:
            True if successful, False if persona not found
        """
        if name in self.personas:
            self.active_persona = self.personas[name]
            logger.info(f"Active persona set to: {name}")
            return True
        
        logger.warning(f"Persona not found: {name}")
        return False
    
    def get_active_persona(self) -> Optional[BasePersona]:
        """
        Get the currently active persona.
        
        Returns:
            The active persona instance, or None if none is active
        """
        return self.active_persona
    
    def get_all_personas(self) -> Dict[str, BasePersona]:
        """
        Get all registered personas.
        
        Returns:
            Dictionary of persona names to persona instances
        """
        return self.personas
    
    def get_persona_names(self) -> List[str]:
        """
        Get names of all registered personas.
        
        Returns:
            List of persona names
        """
        return list(self.personas.keys())
    
    def get_persona_details(self) -> List[Dict[str, Any]]:
        """
        Get details of all registered personas.
        
        Returns:
            List of dictionaries containing persona details
        """
        return [
            {
                "name": persona.name,
                "description": persona.description,
                "style": persona.style.to_dict(),
                "is_active": persona == self.active_persona
            }
            for persona in self.personas.values()
        ]
    
    def analyze_position(self, position_data: Dict[str, Any], 
                        persona_name: Optional[str] = None) -> str:
        """
        Analyze a trading position using a specified or active persona.
        
        Args:
            position_data: Dictionary containing position information
            persona_name: Optional name of the persona to use
            
        Returns:
            Styled analysis text in the persona's voice
        """
        persona = self._get_target_persona(persona_name)
        if not persona:
            return "No active persona to analyze position."
        
        return persona.analyze_position(position_data)
    
    def analyze_market(self, market_data: Dict[str, Any],
                       persona_name: Optional[str] = None) -> str:
        """
        Analyze market conditions using a specified or active persona.
        
        Args:
            market_data: Dictionary containing market information
            persona_name: Optional name of the persona to use
            
        Returns:
            Styled market analysis text in the persona's voice
        """
        persona = self._get_target_persona(persona_name)
        if not persona:
            return "No active persona to analyze market."
        
        return persona.analyze_market(market_data)
    
    def generate_recommendation(self, data: Dict[str, Any],
                               persona_name: Optional[str] = None) -> str:
        """
        Generate trading recommendations using a specified or active persona.
        
        Args:
            data: Dictionary containing relevant trading data
            persona_name: Optional name of the persona to use
            
        Returns:
            Styled recommendation text in the persona's voice
        """
        persona = self._get_target_persona(persona_name)
        if not persona:
            return "No active persona to generate recommendation."
        
        return persona.generate_recommendation(data)
    
    def summarize_performance(self, performance_data: Dict[str, Any],
                             persona_name: Optional[str] = None) -> str:
        """
        Summarize trading performance using a specified or active persona.
        
        Args:
            performance_data: Dictionary containing performance metrics
            persona_name: Optional name of the persona to use
            
        Returns:
            Styled performance summary in the persona's voice
        """
        persona = self._get_target_persona(persona_name)
        if not persona:
            return "No active persona to summarize performance."
        
        return persona.summarize_performance(performance_data)
    
    def get_greeting(self, persona_name: Optional[str] = None) -> str:
        """
        Get a greeting message from a specified or active persona.
        
        Args:
            persona_name: Optional name of the persona to use
            
        Returns:
            Greeting message in the persona's style
        """
        persona = self._get_target_persona(persona_name)
        if not persona:
            return "No active persona to provide greeting."
        
        return persona.get_greeting()
    
    def get_css_variables(self, persona_name: Optional[str] = None) -> str:
        """
        Get CSS variables for styling based on a specified or active persona.
        
        Args:
            persona_name: Optional name of the persona to use
            
        Returns:
            CSS variable definitions as a string
        """
        persona = self._get_target_persona(persona_name)
        if not persona:
            return "/* No active persona styles */\n"
        
        return persona.style.to_css()
    
    def _get_target_persona(self, persona_name: Optional[str] = None) -> Optional[BasePersona]:
        """
        Get the target persona based on the provided name or active persona.
        
        Args:
            persona_name: Optional name of the persona to retrieve
            
        Returns:
            The target persona instance, or None if not found
        """
        if persona_name:
            return self.get_persona(persona_name)
        
        return self.active_persona
    
    def save_persona_data(self, persona_name: str, data: Dict[str, Any]) -> bool:
        """
        Save persona-specific data to disk.
        
        Args:
            persona_name: Name of the persona to save data for
            data: Dictionary of data to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create a safe filename
            filename = f"{persona_name.lower().replace(' ', '_')}_data.json"
            filepath = os.path.join(self.data_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Saved data for persona: {persona_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving data for persona {persona_name}: {str(e)}")
            return False
    
    def load_persona_data(self, persona_name: str) -> Dict[str, Any]:
        """
        Load persona-specific data from disk.
        
        Args:
            persona_name: Name of the persona to load data for
            
        Returns:
            Dictionary of data, or empty dictionary if file not found
        """
        try:
            # Create a safe filename
            filename = f"{persona_name.lower().replace(' ', '_')}_data.json"
            filepath = os.path.join(self.data_dir, filename)
            
            if not os.path.exists(filepath):
                return {}
                
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            logger.info(f"Loaded data for persona: {persona_name}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading data for persona {persona_name}: {str(e)}")
            return {} 