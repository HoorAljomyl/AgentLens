from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
)

from database.connection import Base


class TestRecord(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, nullable=False, default="created")
    name = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    conversation_count = Column(Integer, nullable=False)


class EvaluationReport(Base):
    __tablename__ = "evaluation_reports"

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    total_tests = Column(
        Integer,
        nullable=False,
    )

    passed_tests = Column(
        Integer,
        nullable=False,
    )

    failed_tests = Column(
        Integer,
        nullable=False,
    )

    average_score = Column(
        Float,
        nullable=False,
    )