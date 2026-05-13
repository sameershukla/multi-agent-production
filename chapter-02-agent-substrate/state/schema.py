from typing import TypedDict, Annotated, List, Dict, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    run_id: str
    job_failures: List[str]

    messages: Annotated[List[BaseMessage], add_messages]

    diagnoses: Dict[str, str]
    confidence: Dict[str, float]
    synthesis: Optional[str]

    completed_agents: List[str]
    escalate: bool

    iteration_count: int
    total_tokens: int
    terminal_reason: Optional[str]
