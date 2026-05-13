from chapter-02-agent-substrate.tools.envelope import success_response, error_response

def get_transaction_history(event: dict) -> dict:
    if not event.get('account_id'):
        return error_response('INVALID_INPUT', 'account_id is required', False)
    return success_response({
        'transactions': [{'date':'today 09:15','merchant':'United Airlines','amount':380,'city':'San Francisco','category':'travel'}],
        'average_30_day_amount': 87,
        'current_amount_multiplier': 48,
        'prior_luxury_merchant_use': False,
    })
