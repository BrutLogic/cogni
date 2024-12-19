import requests
from functools import wraps
import os
import inspect
from .func_wrapper import FuncWrapper
from .instances_store import InstancesStore


class Tool(FuncWrapper, metaclass=InstancesStore):
    ...


tool = Tool.register


def get_function_info(func, include_body=False):
    """
    Retrieves information about a given function, including its prototype,
    docstring, file path, and optionally its body.

    Args:
        func (function): The function to inspect.
        include_body (bool): Whether to include the function's body in the output.

    Returns:
        str: A formatted string containing the function's information.
    """
    if hasattr(func, '_func'):
        func = func._func
    elif hasattr(func, '__wrapped__'):
        func = func.__wrapped__
    signature = inspect.signature(func)
    docstring = inspect.getdoc(func)
    file_path = inspect.getfile(func)
    prototype = f"{func.__name__}{signature}"

    # Initialize the result with file path, prototype, and docstring
    result = f"""# {file_path}

{prototype}
    '''{docstring}'''
    """

    # Optionally include the function's body
    if include_body:
        source_lines, _ = inspect.getsourcelines(func)
        body = ''.join(source_lines)
        result += f"\n\n{body}"

    return result


@tool
def process_tool_commands(last_msg_content):
    from agentix import State
    if not "DBG" in State:
        State['DBG'] = {}
    if last_msg_content == "REPLAY":
        last_msg_content = State['DBG']['last_msg_content']
        print(last_msg_content)
        print('x\n'*5)
    else:
        State['DBG']['last_msg_content'] = last_msg_content
    parser = Tool['xml_parser']('tool')
    tool_commands = parser(last_msg_content)

    output = {'errors': []}

    def propagate_error(err):
        output['errors'].append(err)

    for name, cmd in tool_commands.items():
        bichon = ''

        if not name in Tool:
            propagate_error(
                f"ERROR: using: \n```\n{cmd['raw']}\n```\nthe tool {name} doesn't seem to exist"
            )
            continue
        tool = Tool[name]
        tool_result = ''

        if cmd.get('format') == 'json':
            try:
                import json
                args = json.loads(cmd['content'])
                if not isinstance(args, dict):

                    propagate_error(
                        f"ERROR: using: \n```\n{cmd['raw']}\n```\nthe JSON appears not an object"
                    )
                    continue
            except json.JSONDecodeError as e:
                error_msg = f"ERROR: Failed to parse JSON in:\n```\n{cmd['raw']}\n```\nJSON Error: {str(e)}"
                propagate_error(error_msg)
                continue
            except ValueError as e:
                error_msg = f"ERROR: Invalid JSON content in:\n```\n{cmd['raw']}\n```\nError: {str(e)}"
                propagate_error(error_msg)
                continue

            try:
                tool_result = tool(**args, **cmd['kwargs'])
                bichon = str(args)
                output[name] = {
                    'name': name,
                    'result': tool_result,
                    'args': args
                }

            except TypeError as e:
                error_msg = f"ERROR: Invalid arguments for tool {name}:\n```\n{cmd['raw']}\n```\n\nFunction info:\n{get_function_info(tool)}\n\nError: {str(e)}"
                propagate_error(error_msg)
                continue
            except Exception as e:
                error_msg = f"ERROR: Tool execution failed for {name}:\n```\n{cmd['raw']}\n```\n\nFunction info:\n{get_function_info(tool, include_body=True)}\n\nError: {str(e)}"
                propagate_error(error_msg)
                continue
        else:
            try:
                if cmd['content'] == "":
                    tool_result = tool(**cmd['kwargs'])
                else:
                    tool_result = tool(cmd['content'], **cmd['kwargs'])
                output[name] = {
                    'name': name,
                    'result': tool_result,
                    'args': cmd['content']
                }
                bichon = str(cmd['content'])
            except TypeError as e:
                error_msg = f"ERROR: Invalid arguments for tool {name}:\n```\n{cmd['raw']}\n```\n\nFunction info:\n{get_function_info(tool)}\n\nError: {str(e)}"
                propagate_error(error_msg)
                continue
            except Exception as e:
                error_msg = f"ERROR: Tool execution failed for {name}:\n```\n{cmd['raw']}\n```\n\nFunction info:\n{get_function_info(tool, include_body=True)}\n\nError: {str(e)}"
                propagate_error(error_msg)
                continue
    return output


def update_bot_message(id, content):
    if not content:
        content = "I'm working on it"

    url = f"http://localhost:5000/edit/{id}"
    payload = {"content": content}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def use_tools(*tools, **kwargs):
    tool_prefix = kwargs.get('prefix', '')
    from agentix import Conversation, Tool, SocketManager, State, Agent
    import requests

    def _mw_wrapper(mw):
        @wraps(mw)
        def _mw_wrapper_inner(ctx, conv):
            last_system_msg = ''
            for msg in conv:
                if msg.role == "system":
                    last_system_msg = msg.content
            conv[-1].content = conv[-1].content.replace('$$LAST_SYSTEM_REPLY',
                                                        f"""
{last_system_msg}
""")
            ctx['tools'] = {}

            def send_tool_result(content):
                if not hasattr(conv, 'discord'):
                    return
                if not "current" in conv.discord:
                    return
                thread_msg_id = (
                    requests.get(
                        f'http://localhost:5000/reply/thread/{conv.discord["current"]}/tool')
                ).json().get('message_id')
                update_bot_message(thread_msg_id, content)
                SocketManager.emit('streamMsg',
                                   payload={
                                       "conv": conv.openai(),
                                       # getattr(conversation, "discord_message_id", "-1"),
                                       "discord_message_id": thread_msg_id,
                                       "msg_id": thread_msg_id,
                                       "content": content,
                                   },
                                   broadcast=True
                                   )

            agent_name = ctx['agent'].name

            if not isinstance(conv, Conversation) \
                    or conv[-1].role != "assistant" \
            or "!!NOTOOL" in conv[-1].content:
                return mw(ctx, conv)
            ctx['tools'] = {}
            ctx['tools'] = process_tool_commands(conv[-1].content)
            br = '\n\n'
            for tn, tr in ctx['tools'].items():
                if tn == "errors":
                    if len(tr):
                        send_tool_result(f"##Errors:{br}{br.join(tr)}")

                    continue
                send_tool_result(f"## Tool {tn}{br}{tr['result']}")
            return mw(ctx, conv)
        return _mw_wrapper_inner
    return _mw_wrapper
