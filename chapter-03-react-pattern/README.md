# Chapter 03 — The ReAct Pattern

This companion repository implements the ReAct pattern using a fraud investigation agent.

ReAct means Reason + Act. The agent alternates between Thought, Action, and Observation until it reaches a verdict and emits no further tool call.

This chapter builds on the Chapter 02 substrate:

- shared state
- standard tool response envelope
- structured logs
- run_id correlation
- loop guards
- checkpointing

## Graph Shape

```text
START -> agent -> tools -> agent
              \-> END
```

The `agent` node reasons and may request a tool call. The `tools` node executes the requested tool and returns the observation. The conditional edge exits when the model produces no tool call.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Test

```bash
pytest tests/
```
