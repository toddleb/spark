"""
~/prizym/spark/scripts/2_code_setup.py
Populates project structure with code
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(os.path.expanduser("~/prizym/spark"))

# Code templates
CODE_CONTENT = {
    "ai/models/base.py": """from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseModel(ABC):
    '''Base class for all AI models'''
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        '''Process input data and return results'''
        pass""",

    "ai/models/gpt.py": """from typing import Dict, Any
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
        return {"response": response.content if hasattr(response, "content") else response}""",

    "core/registries/model_registry.py": """from typing import Dict, Any, Optional
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
        
        return score""",

    "core/registries/phase_registry.py": """from typing import Dict, Any, Type
from pydantic import BaseModel

class PhaseConfig(BaseModel):
    '''Phase configuration'''
    phase_number: int
    phase_name: str
    description: str
    required_capabilities: list[str]
    prompt_template: str

class BasePhase:
    '''Base class for workflow phases'''
    
    def __init__(self, config: PhaseConfig):
        self.config = config
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        '''Execute phase'''
        raise NotImplementedError

class PhaseRegistry:
    '''Registry for workflow phases'''
    
    _phases: Dict[str, Type[BasePhase]] = {}
    
    @classmethod
    def register(cls, phase_name: str, phase_class: Type[BasePhase]):
        '''Register new phase type'''
        cls._phases[phase_name] = phase_class
    
    @classmethod
    def get_phase(cls, config: PhaseConfig) -> BasePhase:
        '''Get phase implementation'''
        phase_class = cls._phases.get(config.phase_name)
        if not phase_class:
            raise ValueError(f"Unknown phase type: {config.phase_name}")
        return phase_class(config)""",

    "core/registries/workflow_registry.py": """from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel
from .phase_registry import PhaseConfig

class WorkflowType(BaseModel):
    '''Workflow type configuration'''
    type_code: str
    name: str
    description: str
    phases: List[PhaseConfig]

class WorkflowRegistry:
    '''Registry for workflow types'''
    
    def __init__(self):
        self._workflows: Dict[str, WorkflowType] = {}
    
    async def get_workflow(self, type_code: str) -> Optional[WorkflowType]:
        '''Get workflow by type code'''
        return self._workflows.get(type_code)
    
    async def register_workflow(self, workflow: WorkflowType):
        '''Register new workflow type'''
        self._workflows[workflow.type_code] = workflow
    
    async def identify_workflow_type(self, description: str) -> str:
        '''Identify appropriate workflow type'''
        # TODO: Implement AI-based matching
        return list(self._workflows.keys())[0] if self._workflows else None""",

    "core/database.py": """import asyncpg
import os
from typing import Dict, Any, List

async def get_db_connection():
    '''Get database connection'''
    return await asyncpg.connect(
        database=os.getenv("DB_NAME", "spark_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "your_password"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )

class DatabaseManager:
    '''Database operations manager'''
    
    @staticmethod
    async def execute_query(query: str, *args) -> Any:
        '''Execute database query'''
        conn = await get_db_connection()
        try:
            return await conn.execute(query, *args)
        finally:
            await conn.close()""",

    "core/timeline/tracker.py": """from typing import Dict, Any
from datetime import datetime
from enum import Enum

class PhaseStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ProjectTimeline:
    '''Tracks project execution timeline'''
    
    def __init__(self):
        self.phases: Dict[str, Dict[str, Any]] = {}
        self.start_time = datetime.now()
    
    async def start_phase(self, phase_name: str):
        '''Start a phase'''
        self.phases[phase_name] = {
            "status": PhaseStatus.IN_PROGRESS,
            "start_time": datetime.now()
        }
    
    async def complete_phase(self, phase_name: str, result: Dict[str, Any] = None):
        '''Complete a phase'''
        if phase_name in self.phases:
            self.phases[phase_name].update({
                "status": PhaseStatus.COMPLETED,
                "end_time": datetime.now(),
                "result": result
            })
    
    async def fail_phase(self, phase_name: str, error: str):
        '''Mark phase as failed'''
        if phase_name in self.phases:
            self.phases[phase_name].update({
                "status": PhaseStatus.FAILED,
                "end_time": datetime.now(),
                "error": error
            })""",

    "ai/workflow_engine.py": """from typing import Dict, Any
from core.registries import WorkflowRegistry, PhaseRegistry, AIModelRegistry
from core.timeline.tracker import ProjectTimeline

class DetailedAIWorkflowEngine:
    '''Main workflow engine'''
    
    def __init__(self):
        self.workflow_registry = WorkflowRegistry()
        self.phase_registry = PhaseRegistry()
        self.model_registry = AIModelRegistry()
        self.timeline = ProjectTimeline()
    
    async def execute_project(self, project_spec: Dict[str, Any]) -> Dict[str, Any]:
        '''Execute complete project workflow'''
        try:
            # Identify workflow type
            workflow_type = await self.workflow_registry.identify_workflow_type(
                project_spec.get("description", "")
            )
            
            # Get workflow
            workflow = await self.workflow_registry.get_workflow(workflow_type)
            if not workflow:
                raise ValueError(f"Unknown workflow type: {workflow_type}")
            
            results = {}
            
            # Execute phases
            for phase_config in workflow.phases:
                await self.timeline.start_phase(phase_config.phase_name)
                
                try:
                    # Get phase implementation
                    phase = self.phase_registry.get_phase(phase_config)
                    
                    # Execute phase
                    result = await phase.execute(project_spec)
                    
                    # Store result
                    results[phase_config.phase_name] = result
                    await self.timeline.complete_phase(phase_config.phase_name, result)
                    
                except Exception as e:
                    await self.timeline.fail_phase(phase_config.phase_name, str(e))
                    raise
            
            return {
                "workflow_type": workflow_type,
                "results": results,
                "timeline": self.timeline.phases
            }
            
        except Exception as e:
            raise Exception(f"Project execution failed: {str(e)}")"""
}

def create_project_structure():
    """Create project directory structure and populate with code templates"""
    for file_path, content in CODE_CONTENT.items():
        # Construct full path
        full_path = PROJECT_ROOT / file_path
        
        # Create directory if it doesn't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content to file
        with open(full_path, 'w') as f:
            f.write(content)
        
        print(f"Created: {full_path}")

def main():
    """Main function to execute code setup"""
    create_project_structure()
    print("Project structure populated successfully!")

if __name__ == "__main__":
    main()
