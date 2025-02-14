"""
Phase Registry for Workflow Management
"""

from typing import Dict, Any, Type
from pydantic import BaseModel

class PhaseConfig(BaseModel):
    """Phase configuration"""
    phase_number: int
    phase_name: str
    description: str
    required_capabilities: list[str]
    prompt_template: str

class BasePhase:
    """Base class for workflow phases"""
    
    def __init__(self, config: PhaseConfig):
        """Initialize phase with configuration"""
        self.config = config
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute phase"""
        raise NotImplementedError("Subclasses must implement execute method")

class PhaseRegistry:
    """Registry for workflow phases"""
    
    # Use a class-level dictionary to store phase classes
    _phases: Dict[str, Type[BasePhase]] = {}
    
    @classmethod
    def register(cls, phase_name: str, phase_class: Type[BasePhase]):
        """
        Register a new phase type
        
        :param phase_name: Name of the phase
        :param phase_class: Phase implementation class
        """
        cls._phases[phase_name] = phase_class
        print(f"Registered phase: {phase_name}")  # Add debug print
    
    @classmethod
    def get_phase(cls, config: PhaseConfig) -> BasePhase:
        """
        Get phase implementation
        
        :param config: Phase configuration
        :return: Instantiated phase
        :raises ValueError: If phase type is unknown
        """
        # Print registered phases for debugging
        print(f"Registered phases: {list(cls._phases.keys())}")
        
        phase_class = cls._phases.get(config.phase_name)
        if not phase_class:
            raise ValueError(f"Unknown phase type: {config.phase_name}")
        
        return phase_class(config)
