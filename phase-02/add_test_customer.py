import asyncio
from app.repositories.customer_repository import CustomerRepository
from app.db.session import AsyncSessionLocal
from app.models.customer_model import Customer

async def add_cust():
    async with AsyncSessionLocal() as session:
        repo = CustomerRepository(session)
        await repo.create(Customer(name='Test Customer', email='cust@test.com'))
        print('Customer added')

if __name__ == '__main__':
    asyncio.run(add_cust())
