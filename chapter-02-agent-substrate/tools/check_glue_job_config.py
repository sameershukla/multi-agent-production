from tools.envelope import success_response, error_response
from observability.logging import log_event


def handler(event: dict, context=None) -> dict:
    log_event(
        "tool_invoked",
        event,
        agent=event.get("agent", "glue_specialist"),
        tool_name="check_glue_job_config",
    )

    job_name = event.get("job_name")

    if not job_name:
        return error_response(
            code="INVALID_INPUT",
            message="job_name is required",
            retryable=False,
        )

    return success_response({
        "job_name": job_name,
        "worker_type": "G.1X",
        "number_of_workers": 2,
        "executor_memory_gb": 4,
    })
