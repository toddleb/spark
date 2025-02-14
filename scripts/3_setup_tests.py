"""
~/prizym/spark/scripts/3_setup_tests.py
Creates comprehensive test suite for the project
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(os.path.expanduser("~/prizym/spark"))

# Test content templates
TEST_CONTENT = {
    "tests/test_models/test_gpt_model.py": """import pytest
from ai.models.gpt import GPTModel

@pytest.fixture
def gpt_model():
    config = {
        "model_name": "gpt-4-turbo",
        "temperature": 0.7
    }
    return GPTModel(config)

@pytest.mark.asyncio
async def test_gpt_process(gpt_model):
    input_data = {"prompt": "Test prompt"}
    result = await gpt_model.process(input_data)
    assert "response" in result
    assert isinstance(result["response"], str)""",

    "tests/test_models/test_model_registry.py": """import pytest
from core.registries.model_registry import AIModelRegistry, ModelConfig

@pytest.fixture
def model_registry():
    return AIModelRegistry()

@pytest.mark.asyncio
async def test_register_model(model_registry):
    config = ModelConfig(
        model_id="test-model",
        provider="openai",
        model_name="gpt-4",
        version="1.0",
        capabilities=["text-generation"],
        parameters={"temperature": 0.7}
    )
    
    await model_registry.register_model(config)
    model = await model_registry.get_model("test-model")
    assert model is not None
    assert model["config"].model_id == "test-model"

@pytest.mark.asyncio
async def test_find_best_model(model_registry):
    config1 = ModelConfig(
        model_id="model1",
        provider="openai",
        model_name="gpt-4",
        version="1.0",
        capabilities=["text-generation", "code"],
        parameters={}
    )
    
    config2 = ModelConfig(
        model_id="model2",
        provider="anthropic",
        model_name="claude-3",
        version="1.0",
        capabilities=["text-generation"],
        parameters={}
    )
    
    await model_registry.register_model(config1)
    await model_registry.register_model(config2)
    
    best_model = await model_registry.find_best_model({
        "capabilities": ["text-generation", "code"]
    })
    
    assert best_model == "model1"  # Should match model with more capabilities""",

    "tests/test_router/test_workflow_engine.py": """import pytest
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
        pytest.fail(f"Project execution failed: {str(e)}")""",

    "tests/test_generators/test_phase_generator.py": """import pytest
from core.registries import PhaseRegistry, PhaseConfig

@pytest.fixture
def phase_registry():
    return PhaseRegistry()

def test_phase_registration(phase_registry):
    class TestPhase:
        def __init__(self, config):
            self.config = config
    
    PhaseRegistry.register("test-phase", TestPhase)
    
    config = PhaseConfig(
        phase_number=1,
        phase_name="test-phase",
        description="Test phase",
        required_capabilities=["test"],
        prompt_template="Test"
    )
    
    phase = PhaseRegistry.get_phase(config)
    assert isinstance(phase, TestPhase)
    assert phase.config == config""",

    "tests/conftest.py": """import pytest
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure pytest
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )

@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()""",

    "tests/test_core/__init__.py": "",
    
    "tests/test_core/test_timeline.py": """import pytest
from datetime import datetime
from core.timeline.tracker import ProjectTimeline, PhaseStatus

@pytest.fixture
def timeline():
    return ProjectTimeline()

@pytest.mark.asyncio
async def test_phase_tracking(timeline):
    # Start phase
    phase_name = "test-phase"
    await timeline.start_phase(phase_name)
    assert timeline.phases[phase_name]["status"] == PhaseStatus.IN_PROGRESS
    
    # Complete phase
    result = {"output": "test"}
    await timeline.complete_phase(phase_name, result)
    assert timeline.phases[phase_name]["status"] == PhaseStatus.COMPLETED
    assert timeline.phases[phase_name]["result"] == result
    
    # Verify timing
    assert isinstance(timeline.phases[phase_name]["start_time"], datetime)
    assert isinstance(timeline.phases[phase_name]["end_time"], datetime)""",

    "tests/test_core/test_database.py": """import pytest
from core.database import DatabaseManager

@pytest.mark.asyncio
async def test_database_connection():
    # Test query execution
    query = "SELECT 1"
    try:
        result = await DatabaseManager.execute_query(query)
        assert result is not None
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")"""
}

def create_test_files():
    """Create test files with content"""
    for file_path, content in TEST_CONTENT.items():
        full_path = PROJECT_ROOT / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        print(f"Created test file: {full_path}")

def create_pytest_config():
    """Create pytest configuration file"""
    pytest_ini = PROJECT_ROOT / "pytest.ini"
    content = """[pytest]
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    asyncio: mark test as asynchronous
testpaths = tests"""
    
    pytest_ini.write_text(content)
    print("Created pytest.ini")

def main():
    """Main test setup function"""
    print("🚀 Setting up test suite...")
    
    # Create test files
    print("\nCreating test files...")
    create_test_files()
    
    # Create pytest config
    print("\nCreating pytest configuration...")
    create_pytest_config()
    
    print("\n✅ Test setup complete!")
    print("\nTo run tests:")
    print("1. Activate virtual environment")
    print("2. Run: pytest")
    print("3. For specific tests: pytest tests/test_models/")

if __name__ == "__main__":
    main()
