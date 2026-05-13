from tools.envelope import success_response, error_response
from observability.logging import log_event


IN_MEMORY_S3 = {}


def handler(event: dict, context=None) -> dict:
    log_event(
        "tool_invoked",
        event,
        agent=event.get("agent", "glue_specialist"),
        tool_name="write_rca_report",
    )

    required = ["job_name", "run_id", "root_cause", "recommendation"]

    missing = [field for field in required if not event.get(field)]

    if missing:
        return error_response(
            code="INVALID_INPUT",
            message=f"Missing required fields: {missing}",
            retryable=False,
        )

    key = f"rca-reports/{event['job_name']}/{event['run_id']}/report.json"

    IN_MEMORY_S3[key] = {
        "job_name": event["job_name"],
        "root_cause": event["root_cause"],
        "recommendation": event["recommendation"],
    }

    return success_response({
        "report_key": key,
        "idempotency_key": event["run_id"],
    })
