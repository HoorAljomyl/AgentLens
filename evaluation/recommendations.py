from typing import Dict


def generate_recommendation(
    message: str,
    response: str,
    passed: bool,
) -> Dict:

    if passed:
        return {
            "recommendation":
                "No improvement needed."
        }

    message = message.lower()
    response = response.lower()

    if "book" in message:
        return {
            "recommendation":
                "Ask the user for the preferred appointment date and time."
        }

    if "cancel" in message:
        return {
            "recommendation":
                "Ask the user which appointment they want to cancel."
        }

    if "reschedule" in message:
        return {
            "recommendation":
                "Ask which appointment should be rescheduled."
        }

    if "services" in message:
        return {
            "recommendation":
                "Provide a complete list of available services."
        }

    return {
        "recommendation":
            "Provide a more detailed response."
    }