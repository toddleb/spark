import pytest
from core.database import DatabaseManager

@pytest.mark.asyncio
async def test_database_connection():
    # Test query execution
    query = "SELECT 1"
    try:
        result = await DatabaseManager.execute_query(query)
        assert result is not None
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")