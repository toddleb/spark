import pytest
from ai.workflow_engine import DetailedAIWorkflowEngine
from core.registries import WorkflowRegistry, WorkflowType, PhaseConfig

@pytest.fixture
async def workflow_engine():
    engine = DetailedAIWorkflowEngine()
    
    # Register test workflow
    workflow = WorkflowType(
        type_code="test-workflow",
        name="Test Workflow",
        description="A test workflow",
        phases=[
            PhaseConfig(
                phase_number=1,
                phase_name="test-phase",
                description="Test phase",
                required_capabilities=["text-generation"],
                prompt_template="Test template"
            )
        ]
    )
    
    await engine.workflow_registry.register_workflow(workflow)
    return engine

@pytest.mark.asyncio
async def test_execute_project(workflow_engine):
    project_spec = {
        "name": "Test Project",
        "description": "A test project",
        "requirements": ["req1", "req2"]
    }
    
    try:
        result = await workflow_engine.execute_project(project_spec)
        assert result["workflow_type"] == "test-workflow"
        assert "results" in result
        assert "timeline" in result
    except Exception as e:
        pytest.fail(f"Project execution failed: {str(e)}")