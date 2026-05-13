from chapter-02-agent-substrate.tools.envelope import success_response, error_response

def get_risk_rules(event: dict) -> dict:
    if not event.get('merchant') or event.get('amount') is None:
        return error_response('INVALID_INPUT', 'merchant and amount are required', False)
    return success_response({
        'matched_rules': [{
            'rule_id': 'RR-441',
            'description': 'Escalate luxury retail transactions over $1,000 when device is unknown and merchant is novel.',
            'recommended_action': 'escalate',
        }]
    })
