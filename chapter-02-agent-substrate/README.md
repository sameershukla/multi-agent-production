# Chapter 02 — Building the Agent Substrate

This chapter builds the foundation every future agent in this book depends on.

Before implementing ReAct loops, supervisors, routing logic, reflection, or multi-agent orchestration, we first establish the substrate:

- Shared state
- Tool contracts
- Observability baseline

Without these three pillars, agents work in development but become impossible to debug in production.

This chapter intentionally does NOT build sophisticated agent patterns yet.

Instead, it builds the invisible infrastructure that allows those patterns to scale safely.

---

# Why This Chapter Matters

Most engineers start building agents by jumping directly into:

- supervisor patterns
- routing logic
- tool calling
- multi-agent coordination

The result is usually:

- inconsistent tool responses
- missing correlation IDs
- untraceable logs
- broken retries
- silent failures
- impossible debugging

This chapter prevents that.

The substrate created here becomes the permanent foundation for every remaining chapter in the book.

---

# The Three Pillars

## 1. Shared State

Every agent reads from and writes to the same shared state object.

The state acts like the radar screen in air traffic control.

Every agent sees the same execution context.

The shared state contains:

- run_id
- messages
- diagnoses
- confidence scores
- execution metadata
- coordination signals

The schema lives in:

```bash
state/schema.py
```

---

## 2. Tool Contracts

Every tool returns the exact same response envelope.

```python
{
    "status": "success" | "error" | "partial",
    "data": {...},
    "error": {...}
}
```

This removes ambiguity from agent reasoning.

The model learns one shape and applies it to every tool.

The envelope helpers live in:

```bash
tools/envelope.py
```

---

## 3. Observability Baseline

Every tool invocation and every agent step emits structured JSON logs.

Every log line contains:

- run_id
- timestamp
- agent name
- iteration count
- token count
- event name

This makes executions reconstructable from CloudWatch or OpenSearch.

The logging standard lives in:

```bash
observability/logging.py
```

---

# Repository Structure

```bash
chapter-02-agent-substrate/
│
├── state/
│   ├── schema.py
│   └── initialise.py
│
├── tools/
│   ├── envelope.py
│   ├── contracts.py
│   ├── read_cloudwatch_logs.py
│   ├── check_glue_job_config.py
│   ├── query_incident_history.py
│   ├── list_glue_jobs.py
│   └── write_rca_report.py
│
├── observability/
│   └── logging.py
│
├── tests/
│   ├── test_envelope.py
│   ├── test_correlation.py
│   └── test_idempotency.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Running the Demo

```bash
python main.py
```

Execution flow:

1. Create shared AgentState
2. Generate correlation ID
3. Invoke tools
4. Emit structured logs
5. Update shared state
6. Produce RCA report

---

# Example Execution Flow

```text
Agent Run Started
        │
        ▼
read_cloudwatch_logs
        │
        ▼
check_glue_job_config
        │
        ▼
query_incident_history
        │
        ▼
write_rca_report
        │
        ▼
Agent Run Complete
```

---

# Example Structured Log

```json
{
  "event": "tool_invoked",
  "run_id": "4df6c3e9",
  "agent": "glue_specialist",
  "timestamp": "2026-05-13T12:00:00Z",
  "iteration": 1,
  "tokens": 0,
  "tool_name": "read_cloudwatch_logs"
}
```

---

# Why add_messages Matters

The `messages` field uses:

```python
Annotated[List[BaseMessage], add_messages]
```

Without this annotation:

- each node replaces the message history

With this annotation:

- messages are appended

Without it, the agent forgets previous tool results and repeatedly redoes work.

---

# Idempotency

The write tool uses deterministic keys:

```python
rca-reports/{job_name}/{run_id}/report.json
```

Retrying the same execution:

- overwrites the same report
- creates no duplicates
- produces safe retries

---

# Tests

Run all tests:

```bash
pytest tests/
```

### test_envelope.py

Verifies every tool returns the standard response envelope.

### test_correlation.py

Verifies `run_id` appears in all logs.

### test_idempotency.py

Verifies retries do not create duplicate side effects.

---

# Important Design Philosophy

This chapter focuses on engineering discipline before agent intelligence.

The substrate determines whether your agent system:

- scales
- debugs cleanly
- survives production incidents
- supports future patterns safely

Every later chapter imports from this chapter.

The substrate never changes.

Only the reasoning patterns evolve.

---

# What Comes Next

Chapter 03 introduces the first reasoning pattern:

## ReAct Agent

The ReAct agent will:

- read shared state
- call tools
- reason over observations
- update diagnoses
- emit structured logs

Because the substrate already exists, Chapter 03 can focus entirely on reasoning.
