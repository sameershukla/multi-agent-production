# tests/test_idempotency.py

from tools.write_rca_report import handler as write_rca_report
from tools.write_rca_report import IN_MEMORY_S3


def test_write_rca_report_is_idempotent():
    IN_MEMORY_S3.clear()

    event = {
        "run_id": "same-run-id",
        "job_name": "customer-etl",
        "root_cause": "Insufficient executor memory",
        "recommendation": "Increase worker size",
        "agent": "glue_specialist",
    }

    first_response = write_rca_report(event)
    second_response = write_rca_report(event)

    assert first_response["status"] == "success"
    assert second_response["status"] == "success"

    assert first_response["data"]["report_key"] == second_response["data"]["report_key"]

    assert len(IN_MEMORY_S3) == 1
