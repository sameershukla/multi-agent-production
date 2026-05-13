def make_ai_message(content: str, tool_calls: list[dict] | None = None) -> dict:
    return {'role': 'assistant', 'content': content, 'tool_calls': tool_calls or []}

def make_tool_message(tool_name: str, content: dict, tool_call_id: str) -> dict:
    return {'role': 'tool', 'name': tool_name, 'content': content, 'tool_call_id': tool_call_id}

def has_tool_calls(message: dict | None) -> bool:
    return bool(message and message.get('tool_calls'))
