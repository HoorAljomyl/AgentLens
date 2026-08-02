from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.schemas import (
    AgentMessageRequest,
    AgentMessageResponse,
    AgentRunRequest,
    TestCreatedResponse,
    TestDetailsResponse,
)
from database.connection import Base, engine, get_db
from database.models import TestRecord
from agents.booking_agent import generate_agent_response
from synthetic_users.generator import generate_user

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AgentLens API",
    description="API for testing and evaluating AI agents.",
    version="0.6.0",
)



@app.get("/")
def root():
    return {
        "project": "AgentLens",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.post("/tests", response_model=TestCreatedResponse)
def create_test(
    request: AgentRunRequest,
    database: Session = Depends(get_db),
):
    test_id = str(uuid4())

    new_test = TestRecord(
        test_id=test_id,
        status="created",
        name=request.name,
        prompt=request.prompt,
        conversation_count=request.conversation_count,
    )

    database.add(new_test)
    database.commit()
    database.refresh(new_test)

    return {
        "test_id": new_test.test_id,
        "status": new_test.status,
        "name": new_test.name,
        "conversation_count": new_test.conversation_count,
    }


@app.get("/tests/{test_id}", response_model=TestDetailsResponse)
def get_test(
    test_id: str,
    database: Session = Depends(get_db),
):
    test = (
        database.query(TestRecord)
        .filter(TestRecord.test_id == test_id)
        .first()
    )

    if test is None:
        raise HTTPException(
            status_code=404,
            detail="Test not found",
        )

    return {
        "test_id": test.test_id,
        "status": test.status,
        "name": test.name,
        "prompt": test.prompt,
        "conversation_count": test.conversation_count,
    }
@app.get("/synthetic-user")
def create_synthetic_user():
    user = generate_user()

    return {
        "name": user.name,
        "personality": user.personality,
        "goal": user.goal,
    }
@app.post("/agent/respond", response_model=AgentMessageResponse)
def respond_to_message(request: AgentMessageRequest):
    response = generate_agent_response(request.message)

    return {
        "agent": "Booking Assistant",
        "response": response,
    }