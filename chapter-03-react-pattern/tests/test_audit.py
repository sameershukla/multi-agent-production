from fraud_agent.graph import InMemoryDynamoDBCheckpointer, SimpleReActGraph

def test_checkpoint_history_is_created():
    checkpointer = InMemoryDynamoDBCheckpointer()
    graph = SimpleReActGraph(checkpointer=checkpointer)
    initial_state = {'run_id':'audit-test','job_failures':[],'messages':[],'diagnoses':{},'confidence':None,'synthesis':None,'completed_agents':[],'escalate':False,'iteration_count':0,'total_tokens':0,'terminal_reason':None,'transaction_id':'TX-9001','account_id':'ACC-8821','amount':4200,'merchant':'Luxury Retail Miami','merchant_city':'Miami','verdict':None,'justification':None,'risk_signals':[],'tool_call_history':[],'observations':[]}
    result = graph.invoke(initial_state, {'configurable': {'thread_id':'audit-test'}})
    history = checkpointer.history('audit-test')
    assert result['verdict'] == 'escalate'
    assert len(history) >= 4
    assert history[0]['run_id'] == 'audit-test'
