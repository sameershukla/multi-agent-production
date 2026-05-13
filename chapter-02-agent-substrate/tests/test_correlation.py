# tests/test_correlation.py

import logging

from tools.read_cloudwatch_logs import handler as read_cloudwatch_logs


def test_run_id_appears_in_logs(caplog):
    caplog.set_level(logging.INFO)

    run_id = "correlation-test-run"

    read_cloudwatch_logs({
        "run_id": run_id,
        "job_name": "customer-etl",
        "agent": "glue_specialist",
    })

    assert run_id in caplog.text
    assert "tool_invoked" in caplog.text
    assert "tool_completed" in caplog.text
