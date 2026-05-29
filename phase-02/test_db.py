import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import sys
import os

# Add the current directory to sys.path so it can find the 'app' package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config.settings import settings

async def test_connection():
    # Convert settings URL to async, remove sslmode=require if it's causing issues with asyncpg
    url = settings.DATABASE_URL.replace("postgresql+psycopg2", "postgresql+asyncpg")
    # asyncpg doesn't take sslmode as a query param in the same way, usually handled by options
    if "?sslmode=require" in url:
        url = url.replace("?sslmode=require", "")
    
    print(f"Connecting to: {url}")
    engine = create_async_engine(url)
    
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("Successfully connected to Supabase!")
            print(f"Result: {result.scalar()}")
    except Exception as e:
        print(f"Failed to connect: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())
