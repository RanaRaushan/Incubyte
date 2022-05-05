from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from word_app.exception import WordNotFoundException
from word_app.models import WordTable
from word_app.schemas import WordSchema, WordCreate


class WordDbAdapter:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, _id) -> [WordSchema, None]:
        row = await self.session.get(WordTable, _id)
        if row is None:
            return None
        return WordSchema(word_id=row.word_id, word=row.word)

    async def create(self, word_create: WordCreate) -> WordSchema:
        word_table = WordTable(word=word_create.word)
        self.session.add(word_table)
        await self.session.commit()
        await self.session.refresh(word_table)
        return WordSchema(word_id=word_table.word_id, word=word_table.word)

    async def delete(self, word_id: int):
        row = await self.session.get(WordTable, word_id)
        if not row:
            raise WordNotFoundException
        await self.session.delete(row)
        await self.session.commit()

    async def update(self, _id: int, word_update: WordCreate) -> WordSchema:
        row = await self.session.get(WordTable, _id)
        if not row:
            raise WordNotFoundException
        row.word = word_update.word
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return WordSchema(word_id=row.word_id, word=row.word)

    async def get_all_word(self) -> List[WordSchema]:
        statement = 'SELECT w.word_id, w.word FROM word as w;'
        results = await self.session.execute(statement)
        list_of_word = []
        results = list(map(lambda res: res, results.all()))
        for result in results:
            if result:
                list_of_word.append(
                    WordSchema(word_id=result.word_id, word=result.word)
                )
        return list_of_word


class WordManager:
    def __init__(self, word_db_adapter: WordDbAdapter):
        self.db_adapter = word_db_adapter

    async def get_by_id(self, _id: int) -> WordSchema:
        word = await self.db_adapter.get(_id)
        if word is None:
            raise WordNotFoundException
        else:
            return word

    async def create(self, word_create: WordCreate) -> WordSchema:
        return await self.db_adapter.create(word_create)

    async def delete(self, word_id: int):
        await self.db_adapter.delete(word_id)

    async def update(self, _id: int, word_update: WordCreate):
        updated_word = await self.db_adapter.update(_id, word_update)
        return updated_word

    async def get_all_word(self):
        return await self.db_adapter.get_all_word()


async def get_word_adapter(session: AsyncSession = Depends(get_async_session)):
    yield WordDbAdapter(session)


async def get_word_manager(word_db: WordDbAdapter = Depends(get_word_adapter)):
    yield WordManager(word_db)
