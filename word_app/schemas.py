from pydantic import BaseModel


class WordSchema(BaseModel):
    word_id: int
    word: str


class WordCreate(BaseModel):
    word: str
