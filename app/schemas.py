from typing import List
from pydantic import BaseModel, Field

class AgentRunRequest(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
        description="Name of the AI agent.",
    )

    prompt: str = Field(
        min_length=10,
        max_length=5000,
        description="Instructions that define the agent's behavior.",
    )

    conversation_count: int = Field(
        default=5,
        ge=1,
        le=100,
        description="Number of conversations to simulate.",
    )


class TestCreatedResponse(BaseModel):
    test_id: str
    status: str
    name: str
    conversation_count: int


class TestDetailsResponse(BaseModel):
    test_id: str
    status: str
    name: str
    prompt: str
    conversation_count: int


class AgentMessageRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=1000,
        description="Message sent to the booking agent.",
    )
class AgentMessageResponse(BaseModel):
    agent: str
    response: str


class SimulationResult(BaseModel):
    user: str
    personality: str
    message: str
    response: str
    passed: bool
    score: int
    reason: str
    recommendation: str
    failure_type: str
class SimulationResponse(BaseModel):
    total_users: int
    passed_tests: int
    failed_tests: int
    average_score: float
    results: List[SimulationResult]