from tools.envelope import success_response
from observability.logging import log_event


def handler(event: dict, context=None) -> dict:
    log_event(
        "tool_invoked",
        event,
        agent=event.get("agent", "glue_specialist"),
        tool_name="list_glue_jobs",
    )

    prefix = event.get("prefix", "")

    jobs = [
        "customer-etl",
        "loan-etl",
        "account-etl",
    ]

    if prefix:
        jobs = [job for job in jobs if job.startswith(prefix)]

    return success_response({
        "jobs": jobs,
    })
