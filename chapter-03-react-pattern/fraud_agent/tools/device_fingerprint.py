from chapter-02-agent-substrate.tools.envelope import success_response, error_response

def get_device_fingerprint(event: dict) -> dict:
    if not event.get('account_id') or not event.get('transaction_id'):
        return error_response('INVALID_INPUT', 'account_id and transaction_id are required', False)
    return success_response({
        'device_id': 'DVCF-44821',
        'known_device': False,
        'device_type': 'Windows laptop',
        'known_devices': ['iPhone', 'iPhone', 'MacBook'],
        'ip_location': 'Miami hotel network',
    })
