import pytest
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
    assert isinstance(result["response"], str)