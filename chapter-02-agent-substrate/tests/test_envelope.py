# tests/test_envelope.py

from tools.envelope import success_response, error_response, partial_response


def test_success_response_shape():
    response = success_response({"message": "ok"})

    assert response["status"] == "success"
    assert response["data"] == {"message": "ok"}
    assert response["error"] is None


def test_error_response_shape():
    response = error_response(
        code="INVALID_INPUT",
        message="job_name is required",
        retryable=False,
        context={"field": "job_name"},
    )

    assert response["status"] == "error"
    assert response["data"] is None
    assert response["error"]["code"] == "INVALID_INPUT"
    assert response["error"]["message"] == "job_name is required"
    assert response["error"]["retryable"] is False
    assert response["error"]["context"] == {"field": "job_name"}


def test_partial_response_shape():
    response = partial_response(
        data={"records_found": 10},
        error={
            "code": "NO_LOGS_IN_RANGE",
            "message": "Some logs were unavailable",
            "retryable": True,
            "context": {"lookback_minutes": 30},
        },
    )

    assert response["status"] == "partial"
    assert response["data"]["records_found"] == 10
    assert response["error"]["code"] == "NO_LOGS_IN_RANGE"
    assert response["error"]["retryable"] is True
