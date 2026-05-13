from tools.envelope import success_response, error_response
from observability.logging import log_event


def handler(event: dict, context=None) -> dict:
    log_event(
        "tool_invoked",
        event,
        agent=event.get("agent", "glue_specialist"),
        tool_name="read_cloudwatch_logs",
    )

    job_name = event.get("job_name")

    if not job_name:
        log_event(
            "tool_failed",
            event,
            agent=event.get("agent", "glue_specialist"),
            tool_name="read_cloudwatch_logs",
            error_code="INVALID_INPUT",
            retryable=False,
        )
        return error_response(
            code="INVALID_INPUT",
            message="job_name is required",
            retryable=False,
        )

    data = {
        "job_name": job_name,
        "error_type": "OutOfMemoryError",
        "executor_memory_gb": 4,
        "records_processed": 48200000,
    }

    log_event(
        "tool_completed",
        event,
        agent=event.get("agent", "glue_specialist"),
        tool_name="read_cloudwatch_logs",
        status="success",
    )

    return success_response(data)
