from typing import AsyncGenerator
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load our .env file to environment
load_dotenv()
print(os.environ.get("SQL_TEST_DB_URL"))

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg"+os.environ.get('DATABASE_URL')[8:]

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

async_session_maker = sessionmaker(autocommit=False, class_=AsyncSession, autoflush=False, bind=engine)

Base = declarative_base()


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
