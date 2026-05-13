from fraud_agent.tools.transaction_history import get_transaction_history
from fraud_agent.tools.device_fingerprint import get_device_fingerprint
from fraud_agent.tools.peer_account_behavior import get_peer_account_behavior
from fraud_agent.tools.risk_rules import get_risk_rules

TOOL_REGISTRY = {
    'get_transaction_history': get_transaction_history,
    'get_device_fingerprint': get_device_fingerprint,
    'get_peer_account_behavior': get_peer_account_behavior,
    'get_risk_rules': get_risk_rules,
}

def invoke_tool(name: str, args: dict, run_id: str) -> dict:
    if name not in TOOL_REGISTRY:
        return {'status':'error','data':None,'error':{'code':'UNKNOWN_TOOL','message':f'Unknown tool: {name}','retryable':False,'context':{'tool_name':name}}}
    return TOOL_REGISTRY[name]({**args, 'run_id': run_id})
