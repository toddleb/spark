from typing import Dict, Any
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
            raise Exception(f"Project execution failed: {str(e)}")