def should_continue(state: dict) -> str:
    if state.get('terminal_reason'):
        return 'end'
    if not state.get('messages'):
        return 'end'
    last_msg = state['messages'][-1]
    if last_msg.get('role') == 'assistant' and last_msg.get('tool_calls'):
        return 'tools'
    return 'end'
