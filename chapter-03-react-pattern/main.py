from fraud_agent.handler import investigate_transaction

if __name__ == '__main__':
    tx = {
        'id': 'TX-9001',
        'account_id': 'ACC-8821',
        'amount': 4200.00,
        'merchant': 'Luxury Retail Miami',
        'city': 'Miami',
    }
    result = investigate_transaction(tx)
    print('\n=== Fraud Investigation Result ===')
    print('Verdict:', result['verdict'])
    print('Confidence:', result['confidence'])
    print('Justification:', result['justification'])
    print('Risk signals:', result['risk_signals'])
    print('Terminal reason:', result['terminal_reason'])
    print('Iterations:', result['iteration_count'])
