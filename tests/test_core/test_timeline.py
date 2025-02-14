import pytest
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
    assert isinstance(timeline.phases[phase_name]["end_time"], datetime)