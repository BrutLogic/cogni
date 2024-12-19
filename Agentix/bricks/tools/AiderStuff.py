from agentix import tool, Tool, State, Agent
from typing import Optional, List, Dict, Union


@tool
def reset_project(project_name: str):
    State['projects']['projects'][project_name] = {}
    State['Aiders'] = {}

    return "Poject reset, you can proceed"


@tool
def register_aider(
    session_name,
        files: list[str],
    mode: 'ask|code',

) -> str:
    if not "Aiders" in State:
        State['Aiders'] = {}

    if session_name in State['Aiders']:
        raise Exception(f"aider session {session_name} exists")
    State['Aiders'][session_name] = {
        "name": session_name,
        "files": files,
        "mode": mode,
    }

    insure_aider(session_name)


@tool
def insure_aider(session_name: str):
    if session_name.endswith('_omni'):
        raise Exception(
            f"TODO: refacto omni/aider init for dry (passed {session_name} in insure_aider)")
    is_aider = Tool['is_aider']
    if Tool['is_aider'](session_name):
        return True
    if not session_name in State['Aiders']:
        raise Exception(f"aider {session_name} should be registered first")
    session = State['Aiders'][session_name].to_dict()
    mode = session['mode']
    files = session['files']
    run_with_tmux = Tool['run_with_tmux']
    Tool['run_with_tmux'](f"cd {Tool['cwd']()}", session_name)

    run_with_tmux('aider --sonnet --no-pretty', session_name)
    # run_with_tmux('aider --model ollama_chat/qwq --no-pretty', session_name)
    print(f"setting up aider session: [green b]{session_name}[/]", end="")
    while not is_aider(session_name):
        print('.', end='')
    run_with_tmux(f"/chat-mode {mode}", session_name)
    run_with_tmux('/add ' + ' '.join(files), session_name)
    return False


@tool
def talk_to_omni(message):
    # return 'oiu'
    is_aider = Tool['is_aider']
    run_with_tmux = Tool['run_with_tmux']
    insure_omni = Tool['insure_omni']
    project = State['projects']['current']

    o_sess = f"{project}_omni"
    insure_omni()

    reply_name = Tool['random_id']()
    assert is_aider(o_sess), f"{o_sess} doesn't seem like an aider session"

    full_msg = f"""
## **Output Format**
You'll think about the problem using <thought ttl="n">your thought</thought>
The reply should be inside <reply></reply>.

Your base ttl is given at the start, you're allowed that many thoughts.
- If you're asked for a list of files, you reply should consist in file paths and nothing else, one per line.
- If you're ask for a list of file, be greedy and add, if possible, extra files where stuff looks like what we want to do for inspiration/convention

In your thinking you should consider all the files involved and all the place it will be affected in code
Here's an example of output:
```
user: Can you give me the list of relevant files to add a module ?
assistant:<thought ttl="25">I should find the doc for modules</thought>
<thought ttl="24">I should also include some already implemented module for inspiration</thought>
...
<thought ttl="2">User asked for a list of files, my reply should be easily parsable, I'll answer with file paths, one per line and nothing else</thought>

<reply name="GloriousPimple">
modules/doc.md
modules/SomeModule/manifest.yml
...
</reply>

The thing we'll work on today
<project>
{Tool['project_as_md']()}
</project>

## **User question**

{message}

## **Settings**

- Your thought TTL is 27
- The `name` attr of your reply opening tag should be '{reply_name}'
    """
    with open('/tmp/zouzou', "w") as f:
        f.write(full_msg)

    run_with_tmux('wl-copy < /tmp/zouzou', 'zoubida')

    reply = '\n'.join(run_with_tmux('/paste', o_sess))
    print(len(reply))
    reply_content = Tool['xml_parser']('reply')(
        reply).get(reply_name, {}).get('content', '')

    return reply_content


@tool
def set_task_specs_and_aiders():
    o_sess = Tool['current_project']()['aider_session']['omni']
    task_name = Tool['current_project']().current_task

    def ask_omni(msg) -> str:
        return Tool['talk_to_aider'](msg.strip(), o_sess)

    specs = ask_omni(
        """Give me an as concise and as thorough as possible list of all specs for current task""")

    def HITL_validate(spcs) -> str:
        return Tool['Human'](f"""Hey bro,
I'm setting the specs for:
### `{Tool['current_task']().name}` {Tool['current_task']().name} (proj:**{Tool['current_project']().name}**)
#### Specs
{spcs}

Reply "OK" and nothing else once it's OK.""").strip()

    human_response = HITL_validate(specs)

    while human_response.lower() != 'ok':
        specs = ask_omni(f"""
You gave me those specs:
<specs>
{specs}
</specs>
Can you update them based on this feedback from human ?
<feedback>
{human_response}
</feedback>
""")
        human_response = HITL_validate(specs)

    Tool['current_task']()['specs'] = specs

    files = ask_omni("""
OK, now, given the current task, I want you to give me a list of all relevant files.
Think thoroughly about all affected files, including the imports and stuff.
Also, think about the relevant files with similar stuff to know what code style and conventions to use
                     """).split('\n')

    Tool['Human']("I'm about to create the omni sessions")
    register_aider(f'{task_name}_ask', files, 'ask')

    register_aider(f'{task_name}_code', files, 'code')

    return Tool['project_as_md']()


@tool
def run(cmd):

    import time

    sess_name = f"{Tool['current_project']().name}_shell"

    def r(c):
        return '\n'.join(Tool['run_with_tmux'](c, sess_name))
    rid = Tool['random_id']()
    r('')
    r(f"cd {Tool['cwd']()}")
    time.sleep(0.5)
    r(f"echo {rid}")
    time.sleep(0.5)
    return r(cmd).split(rid)[-1].strip()


@tool
def talk_to_aider(message, session_name):
    # return 'oiu'
    is_aider = Tool['is_aider']
    run_with_tmux = Tool['run_with_tmux']
    insure_aider = Tool['insure_aider']
    if session_name.endswith('_omni'):
        Tool['insure_omni']()
    else:
        insure_aider(session_name)

    reply_name = Tool['random_id']()
    assert is_aider(
        session_name), f"{session_name} doesn't seem like an aider session"

    full_msg_ask = f"""
## **Output Format**
You'll think about the problem using <thought ttl="n">your thought</thought>
The reply should be inside <reply></reply>.

Your base ttl is given at the start, you're allowed that many thoughts.
- If you're asked for a list of files, you reply should consist in file paths and nothing else, one per line.
- If you're asked for a list of file, be greedy and add, if possible, extra files where stuff looks like what we want to do for inspiration/convention
- If asked for a list of file, ONLY GIVE FILE THAT EXIST !!!
- I insist; If asked for a list of file, ONLY GIVE FILE THAT EXIST, not the file to be created.
- If you're asked for steps/specs, respect the instructions in <replyFormat>
In your thinking you should consider all the files involved and all the place it will be affected in code

## **Reply format**
<replyFormat>
When asked for specifications or list of unitary task, you have to be thorough but also, as concise as possible.
Do not include things that were not explicitely asked (eg: if I don't ask for logging and error management, don't put it in the specs).

Your goal is to have a list of specs that has the least possible amount of items while being comprehensive for the task at end.
Also, each item must be formulated with the shortest (while thorough) formulation.
eg:
- Create `some/path/template.html` based on `some/path/template2.html`
- Update `some_function` in `some/file/file.py` to add `some behavior
</replyFormat>

Here's an example of output:
<example1>
user: Can you give me the list of relevant files to add a module ?
assistant:<thought ttl="25">I should find the doc for modules</thought>
<thought ttl="24">I should also include some already implemented module for inspiration</thought>
...
<thought ttl="2">User asked for a list of files, my reply should be easily parsable, I'll answer with file paths, one per line and nothing else</thought>

<reply name="GloriousPimple">
modules/doc.md
modules/SomeModule/manifest.yml
...
</reply>
</example1>

____

<example2>
user: Can you tell me how to implement a new endpoint that return stuff ?

assistant:<thought ttl="25">I should identify all the affected code</thought>
<thought ttl="24">I should make a list with unitary steps, in a concise manner, making the list as short as possible while being as comprehensive as possible</thought>
...
<thought ttl="5">I thought of task related to error management and one for future improvements. User didn't ask for that explicitely so I won't include it in my final list</thought>

<reply name="GloriousPimple">
## **Steps**
- Create `some/file/template.html` based on `some/other/file/template2.html`
...
## **Validation**
- `some_file` should exist
- `some behavior` should happen when hitting `GET /some/endpoint`
</reply>
<example2>


The thing we'll work on today

## **Current project state**
<currentTask>
{Tool['project_as_md']()}
</currentTask>

## **User query**
<userQuery>
{message}
<userQuery>

## **Settings**

- Your thought TTL is 27
- The `name` attr of your reply opening tag should be '{reply_name}'
    """

    full_msg_code = f"""
## **Output Format**
You'll think about the problem using <thought ttl="n">your thought</thought>
Your final answer after having implemented what's asked <reply></reply>.

Your base ttl is given at the start, you're allowed that many thoughts.

## **Reply format**
<replyFormat>
<thought ttl="24">I should create a new file `some_dir/some_file.html` taking inspiration from `some_dir/some_other_file.html`</thought>
...
</replyFormat>

Here's an example of output:
<example1>
user: Can you update `some_function` to add "some behavior" >
assistant:<thought ttl="25">I should identify all the files to be changed</thought>
<thought ttl="24">OK so, `some_path/some_file.py` contains the function to update</thought>
<thought ttl="23">I should create a new function `some_function` in `some/file.py`</thought>
<thought ttl="22">I should not forget to add the correct import in `some_dire/yet/another/file.py`</thought>
...
<thought ttl="2">Once it's done I should report the changes made to user</thought>

(Here you'll use your diff tools to write all the code)

<reply name="GloriousPimple">
I created the file ... and updated the function ...
</reply>
</example1>

The thing we'll work on today

## **Current project state**
<currentTask>
{Tool['project_as_md']()}
</currentTask>

## **User query**
<userQuery>
{message}
<userQuery>

## **Settings**

- Your thought TTL is 27
- The `name` attr of your reply opening tag should be '{reply_name}'
    """

    full_msg = full_msg_code if session_name.endswith(
        '_code') else full_msg_ask

    with open('/tmp/zouzou', "w") as f:
        f.write(full_msg)

    run_with_tmux('wl-copy < /tmp/zouzou', 'zoubida')

    reply = '\n'.join(run_with_tmux('/paste', session_name))
    reply_content = Tool['xml_parser']('reply')(
        reply).get(reply_name, {}).get('content', '')

    return reply_content
