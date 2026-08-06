from typing import Dict, List


def evaluate_response(message: str, response: str) -> Dict:
    normalized_message = message.lower().strip()
    normalized_response = response.lower().strip()

    expected_keywords: List[str]

    if "book" in normalized_message:
        expected_keywords = ["date", "time"]

    elif "cancel" in normalized_message:
        expected_keywords = ["booking", "id"]

    elif "reschedule" in normalized_message:
        expected_keywords = ["appointment", "reschedule"]

    elif "service" in normalized_message:
        expected_keywords = [
            "consultation",
            "follow-up",
            "dental",
        ]

    else:
        expected_keywords = ["clarify"]

    matched_keywords = [
        keyword
        for keyword in expected_keywords
        if keyword in normalized_response
    ]

    score = round(
        len(matched_keywords) / len(expected_keywords) * 100
    )

    passed = score == 100

    if passed:
        reason = "The response contains the expected information."
    elif score > 0:
        reason = "The response contains only part of the expected information."
    else:
        reason = "The response does not contain the expected information."

    return {
        "passed": passed,
        "score": score,
        "reason": reason,
    }