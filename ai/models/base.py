from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseModel(ABC):
    '''Base class for all AI models'''
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        '''Process input data and return results'''
        pass