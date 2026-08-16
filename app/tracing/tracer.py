from datetime import datetime
from uuid import uuid4


def create_trace():

    return {
        "trace_id": str(uuid4()),
        "started_at": datetime.utcnow().isoformat(),
        "steps": [],
    }


def add_step(
    trace: dict,
    step: str,
    data: dict,
):

    trace["steps"].append(
        {
            "time": datetime.utcnow().isoformat(),
            "step": step,
            "data": data,
        }
    )