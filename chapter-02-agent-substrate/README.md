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
