from copy import deepcopy
import random
import re
import string
from agentix import tool, Conversation, Message


@tool
def tpl_s(tpl_str: str, **kwargs) -> str:
    for key, value in kwargs.items():
        if not isinstance(value, (str, int, float)):
            continue
        tpl_str = tpl_str.replace('{'+key+'}', str(value))

    return tpl_str


@tool
def tpl_c(conv: Conversation, **kwargs) -> Conversation:
    new_conv = deepcopy(conv)

    for m in new_conv.msgs:
        m.content = tpl_s(m.content, **kwargs)

    return new_conv


@tool
def tpl(conv, **kwargs):
    if isinstance(conv, str):
        return tpl_s(conv, **kwargs)
    if isinstance(conv, Conversation):
        return tpl_c(conv, **kwargs)

    raise ValueError("Input must be a string or an instance of Conversation.")


def generate_random_id():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(3)) + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


@tool
def tpl_tool(conv):
    from agentix import Tool
    tool_uses = {}
    modified_content = conv

    # Find all {tool:xxx} patterns
    tool_pattern = r'\{tool:([^\}]+)\}'

    if isinstance(conv, str):
        matches = re.finditer(tool_pattern, conv)
        for match in matches:
            tool_to_use = match.group(1)
            random_id = generate_random_id()
            tool_uses[random_id] = Tool[tool_to_use]()
            modified_content = modified_content.replace(
                match.group(0), f'{{{random_id}}}')

    elif isinstance(conv, Conversation):
        new_conv = deepcopy(conv)
        for msg in new_conv.msgs:
            matches = re.finditer(tool_pattern, msg.content)
            for match in matches:
                tool_to_use = match.group(1)
                random_id = generate_random_id()
                tool_uses[random_id] = Tool[tool_to_use]()
                msg.content = msg.content.replace(
                    match.group(0), f'{{{random_id}}}')
        modified_content = new_conv

    return tpl(modified_content, **tool_uses)
