import asyncio
import sqlalchemy
from sqlalchemy import text
from app.config.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine

async def fix_schema():
    # Replace psycopg2 with asyncpg in the URL, and remove sslmode if present
    url = settings.DATABASE_URL.replace("postgresql+psycopg2", "postgresql+asyncpg")
    if "?sslmode=require" in url:
        url = url.replace("?sslmode=require", "")
    elif "&sslmode=require" in url:
        url = url.replace("&sslmode=require", "")

    engine = create_async_engine(url)

    async with engine.begin() as conn:
        print("Ensuring schema is up to date...")
        
        # Table: messages
        for col in [('sentiment', 'VARCHAR(50)'), ('sentiment_score', 'INTEGER')]:
            col_name, col_type = col
            result = await conn.execute(text(
                f"SELECT column_name FROM information_schema.columns WHERE table_name='messages' AND column_name='{col_name}';"
            ))
            if not result.first():
                print(f"Adding '{col_name}' to 'messages'...")
                await conn.execute(text(f"ALTER TABLE messages ADD COLUMN {col_name} {col_type}"))

        # Table: execution_logs
        for col in [('reasoning', 'TEXT'), ('step_number', 'INTEGER')]:
            col_name, col_type = col
            result = await conn.execute(text(
                f"SELECT column_name FROM information_schema.columns WHERE table_name='execution_logs' AND column_name='{col_name}';"
            ))
            if not result.first():
                print(f"Adding '{col_name}' to 'execution_logs'...")
                await conn.execute(text(f"ALTER TABLE execution_logs ADD COLUMN {col_name} {col_type}"))

        # Table: customers
        for col in [('lead_score', 'INTEGER'), ('lead_status', 'VARCHAR(50)')]:
            col_name, col_type = col
            result = await conn.execute(text(
                f"SELECT column_name FROM information_schema.columns WHERE table_name='customers' AND column_name='{col_name}';"
            ))
            if not result.first():
                print(f"Adding '{col_name}' to 'customers'...")
                await conn.execute(text(f"ALTER TABLE customers ADD COLUMN {col_name} {col_type}"))

    print("Schema fix completed.")

if __name__ == "__main__":
    asyncio.run(fix_schema())
