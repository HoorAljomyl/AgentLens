def judge_response(message: str, response: str) -> str:
    response_lower = response.lower()

    if len(response.strip()) < 10:
        return "The response is too short and needs more useful information."

    if "book" in message.lower():
        if "date" in response_lower or "time" in response_lower:
            return "The response appropriately asks for booking details."
        return "The response should ask for the preferred date and time."

    if "cancel" in message.lower():
        if "booking" in response_lower or "id" in response_lower:
            return "The response appropriately asks for booking information."
        return "The response should ask which booking should be cancelled."

    if "reschedule" in message.lower():
        if "appointment" in response_lower:
            return "The response appropriately asks which appointment should be rescheduled."
        return "The response needs more information to handle the rescheduling request."

    if "service" in message.lower():
        if "consultation" in response_lower or "service" in response_lower:
            return "The response provides relevant service information."
        return "The response should provide more information about available services."

    return "The response appears relevant but may require further evaluation."