from sqlalchemy import Column, Integer, String, Text

from database.connection import Base


class TestRecord(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, nullable=False, default="created")
    name = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    conversation_count = Column(Integer, nullable=False)