import uuid
from .schema import AgentState


def start_agent_run(job_failures: list[str]) -> AgentState:
    return {
        "run_id": str(uuid.uuid4()),
        "job_failures": job_failures,
        "messages": [],
        "diagnoses": {},
        "confidence": {},
        "synthesis": None,
        "completed_agents": [],
        "escalate": False,
        "iteration_count": 0,
        "total_tokens": 0,
        "terminal_reason": None,
    }
