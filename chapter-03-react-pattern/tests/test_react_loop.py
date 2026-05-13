from fraud_agent.nodes import tools_node

def test_loop_detection_fires_on_repeated_tool_call():
    args = {'account_id':'ACC-8821','days':30,'category':'travel'}
    state = {'run_id':'run-loop-test','messages':[{'role':'assistant','content':'Thought','tool_calls':[{'id':'call-2','name':'get_transaction_history','args':args}]}], 'tool_call_history':[{'name':'get_transaction_history','args':args}], 'observations':[], 'iteration_count':2, 'total_tokens':1400}
    result = tools_node(state)
    assert result['terminal_reason'] == 'LOOP_DETECTED'
    assert result['verdict'] == 'escalate'
