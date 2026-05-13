from state.initialise import start_agent_run
from tools.read_cloudwatch_logs import handler as read_logs
from tools.check_glue_job_config import handler as check_config
from tools.query_incident_history import handler as query_history
from tools.write_rca_report import handler as write_report
from observability.logging import log_event


def run_demo():
    state = start_agent_run(["customer-etl"])

    log_event("agent_run_started", state, agent="glue_specialist")

    job_name = state["job_failures"][0]

    logs = read_logs({
        "run_id": state["run_id"],
        "job_name": job_name,
        "agent": "glue_specialist",
    })

    config = check_config({
        "run_id": state["run_id"],
        "job_name": job_name,
        "agent": "glue_specialist",
    })

    history = query_history({
        "run_id": state["run_id"],
        "job_name": job_name,
        "error_type": logs["data"]["error_type"],
        "agent": "glue_specialist",
    })

    state["diagnoses"][job_name] = "Insufficient executor memory for large partition size"
    state["confidence"][job_name] = 0.91
    state["iteration_count"] = 4
    state["terminal_reason"] = "GOAL_ACHIEVED"

    report = write_report({
        "run_id": state["run_id"],
        "job_name": job_name,
        "root_cause": state["diagnoses"][job_name],
        "recommendation": "Increase worker size or repartition input data before Glue processing.",
        "agent": "glue_specialist",
    })

    log_event(
        "agent_run_complete",
        state,
        agent="glue_specialist",
        terminal_reason=state["terminal_reason"],
    )

    return {
        "state": state,
        "logs": logs,
        "config": config,
        "history": history,
        "report": report,
    }


if __name__ == "__main__":
    result = run_demo()
    print(result)
