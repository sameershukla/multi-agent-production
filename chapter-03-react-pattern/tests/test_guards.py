from fraud_agent.config import MAX_ITERATIONS, MAX_TOKENS
from fraud_agent.nodes import agent_node

def base_state():
    return {'run_id':'guard-test','messages':[],'iteration_count':0,'total_tokens':0,'account_id':'ACC-8821','transaction_id':'TX-9001','amount':4200,'merchant':'Luxury Retail Miami','merchant_city':'Miami'}

def test_max_iterations_guard_escalates():
    state = base_state(); state['iteration_count'] = MAX_ITERATIONS
    result = agent_node(state)
    assert result['terminal_reason'] == 'MAX_ITERATIONS_EXCEEDED'
    assert result['verdict'] == 'escalate'

def test_token_budget_guard_escalates():
    state = base_state(); state['total_tokens'] = MAX_TOKENS
    result = agent_node(state)
    assert result['terminal_reason'] == 'TOKEN_BUDGET_EXCEEDED'
    assert result['verdict'] == 'escalate'
