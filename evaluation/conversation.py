from agents.booking_agent import respond


def simulate_conversation(user):
    message = user.goal

    agent_response = respond(message)

    return {
        "user": user.name,
        "personality": user.personality,
        "message": message,
        "response": agent_response,
    }