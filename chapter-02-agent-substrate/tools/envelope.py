from typing import Any, Optional


def success_response(data: dict[str, Any]) -> dict:
    return {
        "status": "success",
        "data": data,
        "error": None,
    }


def error_response(
    code: str,
    message: str,
    retryable: bool,
    context: Optional[dict[str, Any]] = None,
) -> dict:
    return {
        "status": "error",
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "retryable": retryable,
            "context": context or {},
        },
    }


def partial_response(data: dict[str, Any], error: dict[str, Any]) -> dict:
    return {
        "status": "partial",
        "data": data,
        "error": error,
    }
