from fraud_agent.messages import make_ai_message

class MockFraudModel:
    def invoke(self, state: dict) -> dict:
        iteration = state.get('iteration_count', 0)
        if iteration == 0:
            return make_ai_message(
                'Thought: A $4,200 charge in Miami needs travel context. I should check transaction history first.',
                [{'id':'call-1','name':'get_transaction_history','args':{'account_id':state['account_id'],'days':30,'category':'travel'}}]
            )
        if iteration == 1:
            return make_ai_message(
                'Thought: Travel explains Miami, but I need to verify whether the device is known.',
                [{'id':'call-2','name':'get_device_fingerprint','args':{'account_id':state['account_id'],'transaction_id':state['transaction_id']}}]
            )
        if iteration == 2:
            return make_ai_message(
                'Thought: The device is unknown. I need to check active risk rules for this merchant and amount.',
                [{'id':'call-3','name':'get_risk_rules','args':{'merchant':state['merchant'],'amount':state['amount']}}]
            )
        return make_ai_message(
            'Thought: Travel context explains Miami, but unknown device, novel merchant, amount outlier, and RR-441 indicate elevated risk. Final verdict is escalate with confidence 0.72.',
            []
        )
