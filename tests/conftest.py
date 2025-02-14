import pytest
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
    loop.close()