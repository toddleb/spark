import asyncpg
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
            await conn.close()