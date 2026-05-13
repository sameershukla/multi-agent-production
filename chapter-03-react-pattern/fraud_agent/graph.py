from fraud_agent.edges import should_continue
from fraud_agent.nodes import agent_node, tools_node

class InMemoryDynamoDBCheckpointer:
    def __init__(self):
        self.store: dict[str, list[dict]] = {}
    def save(self, thread_id: str, state: dict) -> None:
        self.store.setdefault(thread_id, []).append(dict(state))
    def history(self, thread_id: str) -> list[dict]:
        return self.store.get(thread_id, [])

class SimpleReActGraph:
    def __init__(self, checkpointer: InMemoryDynamoDBCheckpointer | None = None):
        self.checkpointer = checkpointer or InMemoryDynamoDBCheckpointer()
    def invoke(self, initial_state: dict, config: dict | None = None) -> dict:
        thread_id = (config and config.get('configurable', {}).get('thread_id')) or initial_state['run_id']
        state = dict(initial_state)
        self.checkpointer.save(thread_id, state)
        while True:
            state.update(agent_node(state))
            self.checkpointer.save(thread_id, state)
            route = should_continue(state)
            if route == 'end':
                return state
            state.update(tools_node(state))
            self.checkpointer.save(thread_id, state)
            if state.get('terminal_reason'):
                return state

checkpointer = InMemoryDynamoDBCheckpointer()
fraud_agent = SimpleReActGraph(checkpointer=checkpointer)
