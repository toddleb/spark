from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

class ModelConfig(BaseModel):
    '''AI model configuration'''
    model_id: str
    provider: str
    model_name: str
    version: str
    capabilities: list[str]
    parameters: Dict[str, Any]
    status: str = "active"

class AIModelRegistry:
    '''Registry for AI models'''
    
    def __init__(self):
        self._models = {}
        self._metrics = {}
    
    async def get_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        '''Get model by ID'''
        return self._models.get(model_id)
    
    async def register_model(self, config: ModelConfig):
        '''Register new model'''
        self._models[config.model_id] = {
            "config": config,
            "registered_at": datetime.now()
        }
    
    async def find_best_model(self, requirements: Dict[str, Any]) -> str:
        '''Find best model for requirements'''
        best_match = None
        best_score = 0
        
        for model_id, data in self._models.items():
            if data["config"].status != "active":
                continue
                
            score = self._calculate_match_score(data["config"], requirements)
            if score > best_score:
                best_score = score
                best_match = model_id
        
        return best_match
    
    def _calculate_match_score(self, config: ModelConfig, requirements: Dict[str, Any]) -> float:
        '''Calculate how well model matches requirements'''
        score = 0.0
        
        # Check capabilities
        req_capabilities = set(requirements.get("capabilities", []))
        model_capabilities = set(config.capabilities)
        if req_capabilities:
            score += len(req_capabilities & model_capabilities) / len(req_capabilities)
        
        return score