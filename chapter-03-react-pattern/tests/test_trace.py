import logging
from fraud_agent.nodes import agent_node

def test_agent_thought_is_logged(caplog):
    caplog.set_level(logging.INFO)
    state = {'run_id':'trace-test','messages':[],'iteration_count':0,'total_tokens':0,'account_id':'ACC-8821','transaction_id':'TX-9001','amount':4200,'merchant':'Luxury Retail Miami','merchant_city':'Miami'}
    agent_node(state)
    assert 'agent_thought' in caplog.text
    assert 'trace-test' in caplog.text
    assert 'Thought:' in caplog.text
