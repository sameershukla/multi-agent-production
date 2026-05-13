import json
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def log_event(event: str, state_or_event: dict[str, Any], **extra: Any) -> None:
    entry = {
        "event": event,
        "run_id": state_or_event.get("run_id"),
        "agent": extra.pop("agent", "unknown"),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "iteration": state_or_event.get("iteration_count", 0),
        "tokens": state_or_event.get("total_tokens", 0),
        **extra,
    }

    logger.info(json.dumps(entry))
