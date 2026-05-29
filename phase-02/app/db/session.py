from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

# Replace psycopg2 with asyncpg in the URL, and remove sslmode if present
url = settings.DATABASE_URL.replace("postgresql+psycopg2", "postgresql+asyncpg")
if "?sslmode=require" in url:
    url = url.replace("?sslmode=require", "")
elif "&sslmode=require" in url:
    url = url.replace("&sslmode=require", "")

engine = create_async_engine(url, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
