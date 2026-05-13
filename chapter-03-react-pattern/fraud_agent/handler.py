import uuid
from chapter_02.state.initialise import start_agent_run
from chapter_02.observability.logging import log_event
from fraud_agent.graph import fraud_agent

def investigate_transaction(tx: dict) -> dict:
    run_id = str(uuid.uuid4())
    initial_state = {
        **start_agent_run([]),
        'run_id': run_id,
        'transaction_id': tx['id'],
        'account_id': tx['account_id'],
        'amount': tx['amount'],
        'merchant': tx['merchant'],
        'merchant_city': tx['city'],
        'verdict': None,
        'confidence': None,
        'justification': None,
        'risk_signals': [],
        'tool_call_history': [],
        'observations': [],
    }
    log_event('agent_run_started', initial_state, agent='fraud_investigator')
    result = fraud_agent.invoke(initial_state, {'configurable': {'thread_id': run_id}})
    log_event('agent_run_complete', result, agent='fraud_investigator')
    return result
