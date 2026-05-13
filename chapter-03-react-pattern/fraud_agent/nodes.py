from chapter_02.observability.logging import log_event
from fraud_agent.config import MAX_ITERATIONS, MAX_TOKENS
from fraud_agent.messages import make_tool_message
from fraud_agent.model import MockFraudModel
from fraud_agent.tools.registry import invoke_tool

model = MockFraudModel()

def is_repeated_call(name: str, args: dict, history: list[dict]) -> bool:
    return any(item['name'] == name and item['args'] == args for item in history)

def agent_node(state: dict) -> dict:
    if state['iteration_count'] >= MAX_ITERATIONS:
        log_event('guard_triggered', state, agent='fraud_investigator', guard='MAX_ITERATIONS')
        return {'terminal_reason':'MAX_ITERATIONS_EXCEEDED','verdict':'escalate','justification':'Investigation exceeded step limit.'}
    if state['total_tokens'] >= MAX_TOKENS:
        log_event('guard_triggered', state, agent='fraud_investigator', guard='MAX_TOKENS')
        return {'terminal_reason':'TOKEN_BUDGET_EXCEEDED','verdict':'escalate','justification':'Investigation exceeded token budget.'}

    response = model.invoke(state)
    log_event('agent_thought', state, agent='fraud_investigator', thought=response['content'])

    updated = {'messages': state.get('messages', []) + [response], 'iteration_count': state['iteration_count'] + 1, 'total_tokens': state['total_tokens'] + 700}
    if not response.get('tool_calls'):
        updated.update({
            'verdict': 'escalate',
            'confidence': 0.72,
            'justification': 'Travel context explains Miami location, but unknown device, novel merchant, amount outlier, and active risk rule require human review.',
            'risk_signals': ['unknown_device','novel_merchant','amount_outlier','rule_RR441_triggered'],
            'terminal_reason': 'VERDICT_REACHED',
        })
    return updated

def tools_node(state: dict) -> dict:
    last_msg = state['messages'][-1]
    results = []
    history = list(state.get('tool_call_history', []))
    observations = list(state.get('observations', []))
    for tool_call in last_msg.get('tool_calls', []):
        name, args = tool_call['name'], tool_call['args']
        if is_repeated_call(name, args, history):
            log_event('loop_detected', state, agent='fraud_investigator', tool_name=name, repeated_args=args)
            return {'terminal_reason':'LOOP_DETECTED','verdict':'escalate','justification':'Repeated identical tool call detected.'}
        log_event('tool_invoked', state, agent='fraud_investigator', tool_name=name, args=args)
        result = invoke_tool(name, args, state['run_id'])
        log_event('tool_completed', state, agent='fraud_investigator', tool_name=name, status=result['status'])
        results.append(make_tool_message(name, result, tool_call['id']))
        history.append({'name': name, 'args': args})
        observations.append({'tool_name': name, 'result': result})
    return {'messages': state.get('messages', []) + results, 'tool_call_history': history, 'observations': observations}
