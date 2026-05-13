# Same ReAct graph shape as fraud_agent. Only state, prompt, and tools differ.
"""
glue_agent/graph.py

Glue RCA ReAct graph.

This file intentionally mirrors the fraud_agent graph shape:

    agent -> tools -> agent
    agent -> END when no tool call is emitted

Only the domain state, prompt, and tools differ.
"""

from __future__ import annotations

import json
from typing import Any

from chapter-02-agent-substrate.observability.logging import log_event
from glue_agent.config import GLUE_SYSTEM_PROMPT
from glue_agent.state import GlueAgentState


MAX_ITERATIONS = 8
MAX_TOKENS = 8000


class InMemoryDynamoDBCheckpointer:
    """
    Demo checkpointer used in the companion repo.

    In production, replace this with a DynamoDB-backed checkpointer.
    The important idea is that state is persisted after every node execution.
    """

    def __init__(self) -> None:
        self.store: dict[str, list[dict[str, Any]]] = {}

    def save(self, thread_id: str, state: dict[str, Any]) -> None:
        self.store.setdefault(thread_id, []).append(dict(state))

    def history(self, thread_id: str) -> list[dict[str, Any]]:
        return self.store.get(thread_id, [])


def make_ai_message(content: str, tool_calls: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "role": "assistant",
        "content": content,
        "tool_calls": tool_calls or [],
    }


def make_tool_message(tool_name: str, content: dict[str, Any], tool_call_id: str) -> dict[str, Any]:
    return {
        "role": "tool",
        "name": tool_name,
        "content": content,
        "tool_call_id": tool_call_id,
    }


def success_response(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "success",
        "data": data,
        "error": None,
    }


def error_response(code: str, message: str, retryable: bool) -> dict[str, Any]:
    return {
        "status": "error",
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "retryable": retryable,
            "context": {},
        },
    }


# ---------------------------------------------------------------------
# Mock Glue tools
# ---------------------------------------------------------------------

def read_cloudwatch_logs(args: dict[str, Any], run_id: str) -> dict[str, Any]:
    job_name = args.get("job_name")
    if not job_name:
        return error_response("INVALID_INPUT", "job_name is required", False)

    return success_response(
        {
            "job_name": job_name,
            "error_type": "OutOfMemoryError",
            "executor_memory_gb": 4,
            "records_processed": 48200000,
            "message": "Container killed by YARN for exceeding memory limits.",
        }
    )


def check_glue_job_config(args: dict[str, Any], run_id: str) -> dict[str, Any]:
    job_name = args.get("job_name")
    if not job_name:
        return error_response("INVALID_INPUT", "job_name is required", False)

    return success_response(
        {
            "job_name": job_name,
            "worker_type": "G.1X",
            "number_of_workers": 2,
            "executor_memory_gb": 4,
            "max_capacity": 2,
        }
    )


def query_incident_history(args: dict[str, Any], run_id: str) -> dict[str, Any]:
    job_name = args.get("job_name")
    error_type = args.get("error_type")

    if not job_name or not error_type:
        return error_response("INVALID_INPUT", "job_name and error_type are required", False)

    return success_response(
        {
            "job_name": job_name,
            "error_type": error_type,
            "prior_incidents": 3,
            "pattern": "OOM failures occurred when input partitions exceeded 40 million records.",
        }
    )


def write_rca_report(args: dict[str, Any], run_id: str) -> dict[str, Any]:
    required = ["job_name", "root_cause", "recommendation"]
    missing = [field for field in required if not args.get(field)]

    if missing:
        return error_response("INVALID_INPUT", f"Missing fields: {missing}", False)

    report_key = f"rca-reports/{args['job_name']}/{run_id}/report.json"

    return success_response(
        {
            "report_key": report_key,
            "idempotency_key": run_id,
        }
    )


GLUE_TOOLS = {
    "read_cloudwatch_logs": read_cloudwatch_logs,
    "check_glue_job_config": check_glue_job_config,
    "query_incident_history": query_incident_history,
    "write_rca_report": write_rca_report,
}


def invoke_tool(name: str, args: dict[str, Any], run_id: str) -> dict[str, Any]:
    tool = GLUE_TOOLS.get(name)

    if tool is None:
        return error_response("UNKNOWN_TOOL", f"Unknown tool: {name}", False)

    return tool(args, run_id)


# ---------------------------------------------------------------------
# Mock model
# ---------------------------------------------------------------------

class MockGlueModel:
    """
    Deterministic model for local execution.

    In production, this class would be replaced with a Bedrock, Anthropic,
    OpenAI, or LangChain model call.
    """

    def invoke(self, state: GlueAgentState) -> dict[str, Any]:
        iteration = state.get("iteration_count", 0)
        job_name = state["job_name"]

        if iteration == 0:
            return make_ai_message(
                content=(
                    "Thought: I need to inspect CloudWatch logs first to identify "
                    "the failure signature for this Glue job."
                ),
                tool_calls=[
                    {
                        "id": "glue-call-1",
                        "name": "read_cloudwatch_logs",
                        "args": {"job_name": job_name, "lookback_minutes": 60},
                    }
                ],
            )

        if iteration == 1:
            return make_ai_message(
                content=(
                    "Thought: The logs show OutOfMemoryError. I need to check "
                    "the Glue job configuration to confirm executor memory."
                ),
                tool_calls=[
                    {
                        "id": "glue-call-2",
                        "name": "check_glue_job_config",
                        "args": {"job_name": job_name},
                    }
                ],
            )

        if iteration == 2:
            return make_ai_message(
                content=(
                    "Thought: Executor memory is low for this data volume. I should "
                    "query incident history to see whether this pattern has occurred before."
                ),
                tool_calls=[
                    {
                        "id": "glue-call-3",
                        "name": "query_incident_history",
                        "args": {"job_name": job_name, "error_type": "OutOfMemoryError"},
                    }
                ],
            )

        if iteration == 3:
            return make_ai_message(
                content=(
                    "Thought: Prior incidents confirm the same OOM pattern. I should "
                    "write the RCA report now that the root cause is confirmed."
                ),
                tool_calls=[
                    {
                        "id": "glue-call-4",
                        "name": "write_rca_report",
                        "args": {
                            "job_name": job_name,
                            "root_cause": "Insufficient executor memory for large partition size.",
                            "recommendation": (
                                "Increase worker size or repartition input data before Glue processing."
                            ),
                        },
                    }
                ],
            )

        return make_ai_message(
            content=(
                "Thought: The RCA report has been written. No more tools are needed. "
                "Final diagnosis: insufficient executor memory for large input partitions."
            ),
            tool_calls=[],
        )


model = MockGlueModel()


# ---------------------------------------------------------------------
# ReAct nodes and edges
# ---------------------------------------------------------------------

def is_repeated_call(name: str, args: dict[str, Any], history: list[dict[str, Any]]) -> bool:
    return any(item["name"] == name and item["args"] == args for item in history)


def agent_node(state: GlueAgentState) -> dict[str, Any]:
    if state["iteration_count"] >= MAX_ITERATIONS:
        log_event("guard_triggered", state, agent="glue_diagnostic_agent", guard="MAX_ITERATIONS")
        return {
            "terminal_reason": "MAX_ITERATIONS_EXCEEDED",
            "root_cause": None,
            "confidence": 0.0,
        }

    if state["total_tokens"] >= MAX_TOKENS:
        log_event("guard_triggered", state, agent="glue_diagnostic_agent", guard="MAX_TOKENS")
        return {
            "terminal_reason": "TOKEN_BUDGET_EXCEEDED",
            "root_cause": None,
            "confidence": 0.0,
        }

    response = model.invoke(state)

    log_event(
        "agent_thought",
        state,
        agent="glue_diagnostic_agent",
        thought=response["content"],
    )

    update = {
        "messages": state.get("messages", []) + [response],
        "iteration_count": state["iteration_count"] + 1,
        "total_tokens": state["total_tokens"] + 650,
    }

    if not response.get("tool_calls"):
        update.update(
            {
                "terminal_reason": "GOAL_ACHIEVED",
                "root_cause": "Insufficient executor memory for large input partitions.",
                "confidence": 0.91,
            }
        )

    return update


def tools_node(state: GlueAgentState) -> dict[str, Any]:
    last_msg = state["messages"][-1]
    history = list(state.get("tool_call_history", []))
    observations = list(state.get("observations", []))
    tool_messages = []

    for tool_call in last_msg.get("tool_calls", []):
        name = tool_call["name"]
        args = tool_call["args"]

        if is_repeated_call(name, args, history):
            log_event(
                "loop_detected",
                state,
                agent="glue_diagnostic_agent",
                tool_name=name,
                repeated_args=args,
            )
            return {
                "terminal_reason": "LOOP_DETECTED",
                "root_cause": None,
                "confidence": 0.0,
            }

        log_event(
            "tool_invoked",
            state,
            agent="glue_diagnostic_agent",
            tool_name=name,
            args=args,
        )

        result = invoke_tool(name, args, state["run_id"])

        log_event(
            "tool_completed",
            state,
            agent="glue_diagnostic_agent",
            tool_name=name,
            status=result["status"],
        )

        if name == "write_rca_report" and result["status"] == "success":
            state["report_key"] = result["data"]["report_key"]

        history.append({"name": name, "args": args})
        observations.append({"tool_name": name, "result": result})
        tool_messages.append(make_tool_message(name, result, tool_call["id"]))

    return {
        "messages": state.get("messages", []) + tool_messages,
        "tool_call_history": history,
        "observations": observations,
        "report_key": state.get("report_key"),
    }


def should_continue(state: GlueAgentState) -> str:
    if state.get("terminal_reason"):
        return "end"

    if not state.get("messages"):
        return "end"

    last_msg = state["messages"][-1]

    if last_msg.get("role") == "assistant" and last_msg.get("tool_calls"):
        return "tools"

    return "end"


# ---------------------------------------------------------------------
# Graph assembly
# ---------------------------------------------------------------------

class GlueReActGraph:
    """
    Small local graph runner that mirrors LangGraph flow:

        agent -> tools -> agent
        agent -> END
    """

    def __init__(self, checkpointer: InMemoryDynamoDBCheckpointer | None = None) -> None:
        self.checkpointer = checkpointer or InMemoryDynamoDBCheckpointer()

    def invoke(self, initial_state: GlueAgentState, config: dict[str, Any] | None = None) -> GlueAgentState:
        thread_id = (
            config
            and config.get("configurable", {}).get("thread_id")
            or initial_state["run_id"]
        )

        state = dict(initial_state)
        self.checkpointer.save(thread_id, state)

        while True:
            state.update(agent_node(state))
            self.checkpointer.save(thread_id, state)

            route = should_continue(state)

            if route == "end":
                return state

            state.update(tools_node(state))
            self.checkpointer.save(thread_id, state)

            if state.get("terminal_reason"):
                return state


checkpointer = InMemoryDynamoDBCheckpointer()
glue_agent = GlueReActGraph(checkpointer=checkpointer)


def diagnose_glue_job(job_name: str, run_id: str = "demo-glue-run") -> GlueAgentState:
    initial_state: GlueAgentState = {
        "run_id": run_id,
        "job_failures": [job_name],
        "messages": [],
        "diagnoses": {},
        "synthesis": None,
        "completed_agents": [],
        "escalate": False,
        "iteration_count": 0,
        "total_tokens": 0,
        "terminal_reason": None,
        "job_name": job_name,
        "root_cause": None,
        "confidence": None,
        "report_key": None,
        "tool_call_history": [],
        "observations": [],
    }

    config = {"configurable": {"thread_id": run_id}}
    return glue_agent.invoke(initial_state, config)


if __name__ == "__main__":
    result = diagnose_glue_job("customer-etl")
    print(json.dumps(result, indent=2))
