import pytest
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
    
    assert best_model == "model1"  # Should match model with more capabilities