import asyncio
from app.core.security import get_password_hash
from app.repositories.user_repository import UserRepository
from app.db.session import AsyncSessionLocal
from app.models.user_model import User

async def test():
    async with AsyncSessionLocal() as session:
        repo = UserRepository(session)
        user = User(email='test@ex.com', hashed_password=get_password_hash('pass'[:72]))
        await repo.create(user)
        print('Created successfully')

if __name__ == '__main__':
    asyncio.run(test())
