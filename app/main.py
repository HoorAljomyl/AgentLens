from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from evaluation.recommendations import generate_recommendation
from evaluation.failure_classifier import classify_failure
from app.schemas import (
    AgentMessageRequest,
    AgentMessageResponse,
    AgentRunRequest,
    SimulationResponse,
    TestCreatedResponse,
    TestDetailsResponse,
)

from database.connection import Base, engine, get_db
from database.models import TestRecord, EvaluationReport
from synthetic_users.generator import generate_user
from evaluation.conversation import simulate_conversation
from evaluation.evaluator import evaluate_response

from reports.report_generator import (
    generate_report,
    generate_text_report,
    save_text_report,
)

from agents.booking_agent import respond

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AgentLens API",
    description="API for testing and evaluating AI agents.",
    version="0.7.0",
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
    response = respond(request.message)

    return {
        "agent": "Booking Assistant",
        "response": response,
    }
@app.get("/simulate", response_model=SimulationResponse)
def simulate():
    results = []

    for _ in range(5):
        user = generate_user()

        conversation = simulate_conversation(user)

        evaluation = evaluate_response(
            message=conversation["message"],
            response=conversation["response"],
        )

        conversation.update(evaluation)

        failure = classify_failure(
            message=conversation["message"],
            response=conversation["response"],
            passed=conversation["passed"],
        )

        conversation.update(failure)

        recommendation = generate_recommendation(
            message=conversation["message"],
            response=conversation["response"],
            passed=conversation["passed"],
        )

        conversation.update(recommendation)

        results.append(conversation)

    report = generate_report(results)

    return {
        "total_users": report["total_conversations"],
        "passed_tests": report["passed"],
        "failed_tests": report["failed"],
        "average_score": report["average_score"],
        "results": results,
    }
@app.get("/report", response_class=PlainTextResponse)
def create_report():
    results = []

    for _ in range(5):
        user = generate_user()

        conversation = simulate_conversation(user)

        evaluation = evaluate_response(
            message=conversation["message"],
            response=conversation["response"],
        )

        conversation.update(evaluation)
        results.append(conversation)

    report_summary = generate_report(results)

    report_data = {
        "total_users": report_summary["total_conversations"],
        "passed_tests": report_summary["passed"],
        "failed_tests": report_summary["failed"],
        "average_score": report_summary["average_score"],
        "results": results,
    }

    text_report = generate_text_report(report_data)

    return text_report
@app.get("/report/save")
def save_report(
    database: Session = Depends(get_db),
):
    results = []

    for _ in range(5):
        user = generate_user()

        conversation = simulate_conversation(user)

        evaluation = evaluate_response(
            message=conversation["message"],
            response=conversation["response"],
        )

        conversation.update(evaluation)
        results.append(conversation)

    report_summary = generate_report(results)

    report_data = {
        "total_users": report_summary["total_conversations"],
        "passed_tests": report_summary["passed"],
        "failed_tests": report_summary["failed"],
        "average_score": report_summary["average_score"],
        "results": results,
    }

    database_report = EvaluationReport(
        total_tests=report_data["total_users"],
        passed_tests=report_data["passed_tests"],
        failed_tests=report_data["failed_tests"],
        average_score=report_data["average_score"],
    )

    database.add(database_report)
    database.commit()
    database.refresh(database_report)

    text_report = generate_text_report(report_data)

    file_path = "reports/evaluation_report.txt"

    save_text_report(
        text=text_report,
        file_path=file_path,
    )

    return {
        "message": "Report saved successfully",
        "file_path": file_path,
        "report_id": database_report.id,
    }
@app.get("/reports/history")
def get_report_history(
    database: Session = Depends(get_db),
):
    reports = (
        database.query(EvaluationReport)
        .order_by(EvaluationReport.id.desc())
        .all()
    )

    return [
        {
            "id": report.id,
            "created_at": report.created_at,
            "total_tests": report.total_tests,
            "passed_tests": report.passed_tests,
            "failed_tests": report.failed_tests,
            "average_score": report.average_score,
        }
        for report in reports
    ]