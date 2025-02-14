import pytest
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
    assert phase.config == config