from typing import Optional
from chapter_02.state.schema import AgentState

class GlueAgentState(AgentState, total=False):
    job_name: str
    root_cause: Optional[str]
    report_key: Optional[str]
