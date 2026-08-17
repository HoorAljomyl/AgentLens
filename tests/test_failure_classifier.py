from evaluation.failure_classifier import classify_failure


def test_no_failure():
    result = classify_failure(
        message="Book Appointment",
        response="What date and time would you prefer?",
        passed=True,
    )

    assert result["failure_type"] == "None"


def test_unsupported_pricing():
    result = classify_failure(
        message="Ask About Pricing",
        response="Could you please clarify your request?",
        passed=False,
    )

    assert result["failure_type"] == "Unsupported Intent"