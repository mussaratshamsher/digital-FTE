import asyncio
from app.repositories.customer_repository import CustomerRepository
from app.db.session import AsyncSessionLocal

async def get_ids():
    async with AsyncSessionLocal() as session:
        repo = CustomerRepository(session)
        custs = await repo.get_all()
        print(f"Customer IDs: {[c.id for c in custs]}")

if __name__ == '__main__':
    asyncio.run(get_ids())
