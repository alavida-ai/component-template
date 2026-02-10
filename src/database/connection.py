import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL", "")

# Convert postgres:// to postgresql+asyncpg://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, echo=False) if DATABASE_URL else None

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) if engine else None


async def get_session() -> AsyncSession:
    if async_session is None:
        raise RuntimeError("DATABASE_URL not configured")
    async with async_session() as session:
        yield session
