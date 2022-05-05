import asyncio
from typing import Generator

import pytest
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from db.database import Base
import os

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.environ.get("SQL_TEST_DB_URL")
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)
TestingSessionLocal = sessionmaker(autocommit=False, class_=AsyncSession, autoflush=False, bind=engine)


async def override_get_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        await db.close()


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

