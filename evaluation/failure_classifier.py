from typing import Dict


def classify_failure(
    message: str,
    response: str,
    passed: bool,
) -> Dict:

    if passed:
        return {
            "failure_type": "None"
        }

    message = message.lower()
    response = response.lower()

    if "book" in message:
        if "date" not in response or "time" not in response:
            return {
                "failure_type": "Missing Info"
            }

    if "cancel" in message:
        if "booking" not in response and "id" not in response:
            return {
                "failure_type": "Missing Info"
            }

    if "reschedule" in message:
        if "appointment" not in response:
            return {
                "failure_type": "Missing Info"
            }

    if "service" in message:
        if "consultation" not in response:
            return {
                "failure_type": "Incomplete Answer"
            }

    return {
        "failure_type": "Unknown"
    }