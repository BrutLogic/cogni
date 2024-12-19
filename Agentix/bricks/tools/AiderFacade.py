from agentix import tool, Tool
from typing import Optional, List, Dict, Union


@tool
def validate_with_human(msg: str):
    return Tool['Human'](msg)


@tool
def AF_ensure_session(name: str, mode: str = "ask") -> str:
    """Ensure an Aider session exists and is in the correct mode"""
    ...


@tool
def AF_ensure_omni(project_name: str) -> str:
    """Ensure the omniscient Aider session exists for a project"""


@tool
def AF_set_context_files(files: List[str], session_name: Optional[str] = None) -> bool:
    """Set the files that Aider should work with"""
    ...


@tool
def AF_ask(
    prompt: str,
    session_name: Optional[str] = None,
    context_files: Optional[List[str]] = None
) -> str:
    """Ask Aider a question about the codebase"""
    ...


@tool
def AF_set_current_task(
    task_description: str,
    acceptance_criteria: Optional[List[str]] = None
) -> str:
    """Set the current task for Aider to work on"""
    ...


@tool
def AF_validate_step(step_description: str, files_changed: List[str]) -> bool:
    """Validate that a step meets its acceptance criteria"""
    ...


@tool
def AF_propose_changes(
    task: str,
    files: List[str],
    constraints: Optional[Dict] = None
) -> Dict[str, str]:
    """Get Aider to propose specific changes to files"""
    ...


@tool
def AF_review_changes(
    files_changed: List[str],
    review_criteria: Optional[List[str]] = None
) -> Dict[str, List[str]]:
    """Get Aider to review changes against criteria"""
    ...


@tool
def _talk_to_omni(message):
    # return 'oiu'
    project = State['projects']['current']

    if input(f"Current project is {project}, continue ? (Y)/n: ").strip().startswith('n'):
        print('bye then')
        return
    all_sessions = all_aider_sessions(project)

    assert 'omni' in all_sessions, f'init project with \nTool["_aider_project"]("{project}")\n'
    o_sess = all_sessions['omni']
    reply_name = random_id()
    assert is_aider(o_sess), f"{o_sess} doesn't seem like an aider session"
    run_with_tmux('/chat-mode ask', o_sess)
    full_msg = f"""
## **Output Format**
You'll think about the problem using <thought ttl="n">your thought</thought>
The reply should be inside <reply></reply>.

Your base ttl is given at the start, you're allowed that many thoughts.
- If you're asked for a list of files, you reply should consist in file paths and nothing else, one per line.
- If you're ask for a list of file, be greedy and add, if possible, extra files where stuff looks like what we want to do for inspiration/convention

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
    reply_content = Tool['xml_parser']('reply')(
        reply).get(reply_name, {}).get('content', '')

    return reply_content
