from agentix import mw, Tool, tool, Event, use_tools, Agent
from time import sleep

@mw
@use_tools('caca')
def changedescriptor_loop(ctx, conv):
    if "REHOP" in conv[-1].content:
        return conv.rehop('rehoped :) it works, you can say something. Do not include "REHOP" in your next message or you will be rehopped in an endless loop :p')
    tool_output = ''
    for name, tool_result in ctx['tools'].items():
        if False and name == 'error' and len(tool_result):
            return conv.rehop(f"We add an error:\n\n{tool_result}\n\n Inform user we're working on it and to try later")
        if len(tool_result):
            tool_output += f'''
## Result of tool {name}
{tool_result}
'''
    if len(tool_output):
        return conv.rehop(tool_output)

    return conv[-1].content
