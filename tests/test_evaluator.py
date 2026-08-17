from evaluation.evaluator import evaluate_response


def test_booking_response_passes():
    result = evaluate_response(
        message="Book Appointment",
        response="Sure. What date and time would you prefer?",
    )

    assert result["passed"] is True
    assert result["score"] == 100


def test_pricing_response_fails():
    result = evaluate_response(
        message="Ask About Pricing",
        response="Could you please clarify your request?",
    )

    assert result["passed"] is False
    assert result["score"] == 0