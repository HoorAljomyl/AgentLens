from dataclasses import dataclass
import random
from synthetic_users.personas import (
    ANGRY_CUSTOMER,
    RUSHED_CUSTOMER,
    CONFUSED_CUSTOMER,
)

@dataclass
class SyntheticUser:
    name: str
    personality: str
    goal: str


PERSONAS = [
    ANGRY_CUSTOMER,
    RUSHED_CUSTOMER,
    CONFUSED_CUSTOMER,
]


def generate_user():
    persona = random.choice(PERSONAS)

    return SyntheticUser(
        name=persona["name"],
        personality=persona["personality"],
        goal=persona["goal"],
    )
