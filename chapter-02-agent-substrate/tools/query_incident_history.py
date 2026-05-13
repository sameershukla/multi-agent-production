from tools.envelope import success_response, error_response
from observability.logging import log_event


def handler(event: dict, context=None) -> dict:
    log_event(
        "tool_invoked",
        event,
        agent=event.get("agent", "glue_specialist"),
        tool_name="query_incident_history",
    )

    job_name = event.get("job_name")
    error_type = event.get("error_type")

    if not job_name or not error_type:
        return error_response(
            code="INVALID_INPUT",
            message="job_name and error_type are required",
            retryable=False,
        )

    return success_response({
        "job_name": job_name,
        "error_type": error_type,
        "prior_incidents": 3,
        "pattern": "OOM occurred when partition size exceeded 40 million records",
    })
