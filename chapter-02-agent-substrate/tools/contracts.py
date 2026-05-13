TOOLS = {
    "read_cloudwatch_logs": {
        "when_to_call": "First step. Always read logs before other RCA tools.",
        "required": ["job_name"],
        "optional": ["lookback_minutes", "filter_pattern"],
        "errors": [
            "LOG_GROUP_NOT_FOUND",
            "API_THROTTLED",
            "NO_LOGS_IN_RANGE",
            "EXECUTION_TIMEOUT",
            "INVALID_INPUT",
        ],
    },
    "check_glue_job_config": {
        "required": ["job_name"],
        "errors": ["INVALID_INPUT", "PERMISSION_DENIED"],
    },
    "query_incident_history": {
        "required": ["job_name", "error_type"],
        "errors": ["INVALID_INPUT"],
    },
    "list_glue_jobs": {
        "required": [],
        "optional": ["prefix"],
        "errors": [],
    },
    "write_rca_report": {
        "when_to_call": "Last step only. Use after root cause is confirmed.",
        "required": ["job_name", "run_id", "root_cause", "recommendation"],
        "errors": ["INVALID_INPUT", "PERMISSION_DENIED"],
    },
}
