from sqlalchemy import Column, Integer, String
from db.database import Base


class WordTable(Base):
    __tablename__ = "word"

    word_id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(500), nullable=False)
