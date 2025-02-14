from typing import Dict, Any
from .base import BaseModel
from langchain_openai import ChatOpenAI

class GPTModel(BaseModel):
    '''GPT model implementation'''
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model = ChatOpenAI(
            model_name=config.get("model_name", "gpt-4-turbo"),
            temperature=config.get("temperature", 0.7)
        )
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        '''Process input with GPT model'''
        response = await self.model.invoke(input_data["prompt"])
        return {"response": response.content if hasattr(response, "content") else response}