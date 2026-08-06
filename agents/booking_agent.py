def respond(message: str) -> str:
    message = message.lower()

    if "book" in message:
        return "Sure. What date and time would you prefer?"

    elif "cancel" in message:
        return "I can help cancel your appointment. What is your booking ID?"

    elif "reschedule" in message:
        return "No problem. Which appointment would you like to reschedule?"

    elif "service" in message:
        return "We currently offer consultation, follow-up, and dental services."

    else:
        return "Could you please clarify your request?"