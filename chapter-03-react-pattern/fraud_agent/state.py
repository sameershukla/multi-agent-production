from typing import List, Optional
from chapter_02.state.schema import AgentState

class FraudAgentState(AgentState, total=False):
    transaction_id: str
    account_id: str
    amount: float
    merchant: str
    merchant_city: str
    verdict: Optional[str]
    justification: Optional[str]
    risk_signals: List[str]
    tool_call_history: List[dict]
    observations: List[dict]
