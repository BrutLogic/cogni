import os
import random
from openai import OpenAI
from agentix import tool, Conversation, Tool, Log, Event, SocketManager
from rich import print
import requests
import ollama

''' 
import ollama
zouzou = ''

stream = ollama.chat(
    model='qwen2.5-coder:32b',
    messages=[{'role': 'user', 'content': f"""
Can you code a chess board with movable pieces using chess unicode emojis ?
It should not
Comment your code thoroughly using emoji and in Jamaican patois"""},
              {"role":"assistant", "content":"""Should dat be in JS my brada ?
""",
               },{"role":"user","content":"""Yes plz:)"""}
              ],
    stream=True,
)

for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)

'''


@tool
def llm(conversation: Conversation, model='gpt-4') -> Conversation:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    # Event['beforeInfer'](conversation)

    if '{tool' in conversation[1].content:
        conversation.__content = conversation[1].content
    if hasattr(conversation, '__content'):
        conversation[1].content = Tool['tpl_tool'](conversation.__content)

    if '{tool' in conversation[1].content:
        raise Exception('Wrong parsing')

    msg_id = ''.join([random.choice('abcdefghijklmno5896321470')
                     for _ in range(10)])
    base_message_id = conversation.discord.get('base')
    reply_id = (
        requests.get(
            f"http://localhost:5000/reply/{base_message_id}/Thinking").json().get('message_id')
    )
    base_message_id = conversation.discord['current'] = reply_id
    conversation.discord['buffer'] = '.'
    last_call = 0

    def emit_msg(content=None):
        nonlocal last_call
        from time import time
        now = time()
        if content:
            conversation.discord['buffer'] = content
        if now - last_call < 1.:
            return False
        last_call = now
        # print(f'[red on green b]{content}')

        SocketManager.emit('streamMsg',
                           payload={
                               "conv": conversation.openai(),
                               # getattr(conversation, "discord_message_id", "-1"),
                               "discord_message_id": reply_id,
                               "msg_id": msg_id,
                               "content": conversation.discord['buffer'],
                           },
                           broadcast=True
                           )
        return True

    stream = conversation._flags.get('stream', False)
    llm = conversation.llm
    if conversation.llm == 'gpt-4':
        llm = 'gpt-4o'
    # '''
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=conversation.openai(),
        max_tokens=4000,
        temperature=.2,
        stream=True
    )
    '''
    response = ollama.chat(
        model='qwq',
        messages=conversation.openai(),
        stream=True,
    )
    #'''

    msg = ''
    emit_msg('___')
    last_edit_success = True
    for message in response:
        mm = message.choices[0].delta.content
        # mm = message['message']['content']
        if mm:
            msg += mm
            last_edit_success = emit_msg(msg)
            if not stream:
                continue

    while not last_edit_success:
        last_edit_success = emit_msg(content=msg)

    return msg


@tool
def llm_no_stream(conversation: Conversation, model='o1-mini') -> Conversation:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model=model,
        messages=conversation.openai(),
    )

    return response.choices[0].message.content
