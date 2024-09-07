from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from passlib.context import CryptContext

from auth.user_model import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register_user(id: int, email: str, password: str, async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:
        statement = select(User).filter(User.email == email)

        result = await session.execute(statement)

        if result.first():
            raise ValueError("User with this email already exists!")

        else:
            new_user = User(
                id = id,
                email = email,
                password = password
            )
            session.add(new_user)
            await session.commit()

        return 0

async def authenticate_user(id: int, email: str, password: str, async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:
        statement = select(User).filter(User.id == id and User.email == email and User.password == password)

        result = await session.execute(statement)

        if not result:
            raise ValueError("User doesn't exist!")
        else:
            return 0
