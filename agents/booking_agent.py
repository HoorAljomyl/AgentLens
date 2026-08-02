def generate_agent_response(message: str) -> str:
    """
    Generate a simple response based on the user's message.

    This is a rule-based agent. It does not use an LLM yet.
    """

    normalized_message = message.lower().strip()

    if not normalized_message:
        return "Please enter a message."

    if "book" in normalized_message:
        return "Sure. What date and time would you prefer?"

    if "cancel" in normalized_message:
        return "I can help you cancel. Please provide your booking number."

    if "reschedule" in normalized_message or "change" in normalized_message:
        return "I can help you reschedule. What is your booking number?"

    if "service" in normalized_message:
        return (
            "We currently support booking, cancellation, "
            "and appointment rescheduling."
        )

    if "hello" in normalized_message or "hi" in normalized_message:
        return "Hello! How can I help you with your appointment?"

    return (
        "I did not fully understand your request. "
        "Would you like to book, cancel, or reschedule an appointment?"
    )