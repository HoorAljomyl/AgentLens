from dataclasses import dataclass
import random


@dataclass
class SyntheticUser:
    name: str
    personality: str
    goal: str


PERSONALITIES = [
    "Calm",
    "Angry",
    "Confused",
    "Impatient",
]

GOALS = [
    "Book Appointment",
    "Cancel Appointment",
    "Reschedule Appointment",
    "Ask About Services",
]


def generate_user():
    return SyntheticUser(
        name=f"User-{random.randint(1000,9999)}",
        personality=random.choice(PERSONALITIES),
        goal=random.choice(GOALS),
    )