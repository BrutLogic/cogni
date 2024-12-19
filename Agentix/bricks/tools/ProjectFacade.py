import uuid
import time
from agentix import Tool
from agentix import tool, State
from typing import Optional, List, Dict, Union


@tool
def PF_get_project(project_name: str) -> Dict:
    """Get all information about a specific project"""
    if not 'projects' in State:
        return {}

    projects = State['projects'].get('projects', {})
    return projects.get(project_name, {})


@tool
def PF_all_projects_summary() -> str:
    """Get a markdown summary of all projects"""
    if not 'projects' in State:
        return "No projects found"

    projects = State['projects'].get('projects', {}).to_dict()
    if not projects:
        return "No projects found"

    summary = "# Projects Summary\n\n"
    for name, info in projects.items():
        summary += f"## {name}\n"
        summary += "```json\n"
        summary += "{\n"
        summary += f'    "base_dir": "{info.get("base_dir", "Not set")}",\n'
        summary += f'    "description": "{info.get("description", "No description")}",\n'

        files = info.get('files_to_include', [])
        if files:
            summary += '    "files": [\n'
            for f in files:
                summary += f'        "{f}",\n'
            summary = summary.rstrip(',\n') + '\n    ]\n'
        summary += "}\n```\n\n"

    return summary


@tool
def PF_set_current_project(project_name: str) -> bool:
    """Set the active project"""
    if not 'projects' in State:
        return False

    if project_name not in State['projects'].get('projects', {}):
        return False

    State['projects']['current_project'] = project_name
    return True


@tool
def set_current_project(project_name: str):
    State['projects']['current'] = project_name

    if not project_name in State['projects']['projects'] or not (State['projects']['projects'][project_name].to_dict()):
        init_project(project_name)

    State['projects']['current'] = project_name

    return f"Project {project_name} selected and inited"

    return Tool['project_as_md']()


@tool
def init_project(project_name: str) -> dict:
    if not "projects" in State or (State['projects'].to_dict() == {}):
        State['projects'] = {
            "current": project_name,
            'projects': {}
        }
    State['projects']['current'] = project_name

    def iter_input(msg):
        values = []
        while True:
            val = Tool['Human'](
                f"# {msg}"
                "\n"
                f"I'm setting up `{project_name}`\ngive me {msg}  for aider omni plz.\n One per line or one per message. \nJust send '.' and nothing else to continue")
            if val.strip() == '.':
                break
            for v in val.split('\n'):
                values += [v.strip()]
        return values

    if not project_name in State['projects']['projects'] or \
            State['projects']['projects'][project_name].to_dict() == {}:

        State['projects']['projects'][project_name] = {
            'name': project_name,
            'base_dir': Tool[f"Human"](
                "# Base dir\n"
                f"Hey can you give me the base dir for the project {project_name}?\nNote it's not passed through an agent so reply with the path as a string and nothing else"),
            'files_to_add': iter_input('path to add'),
            'files_to_drop': iter_input('path to drop'),
            'current_task': None,
            'tasks': {}
        }

    Tool['insure_omni']()

    return f"project {project_name} inited"
    return Tool['project_as_md']()


@tool
def set_project_task(name: str, title: str, description: str) -> str:
    project = Tool['current_project']()
    project['current_task'] = name
    if not name in project['tasks']:

        project['tasks'][name] = {
            'name': name,
            'title': title,
            "description": description,
        }

        Tool['set_task_specs_and_aiders']()

    return f"Task {name} selected"
    return Tool['project_as_md']()


@tool
def set_current_project_task(task_name):
    proj = Tool['current_project']()
    if not task_name in proj['tasks']:
        return f"""
    <error>{task_name} doesn't exist in {proj.name}
- You should either create it with the tool `add_project_task`
- Maybe the project selected is not the right one. In general you can use tool `project_as_md` to get informations about the current proj.
- Don't use it this time though, because I'm about to give you the output of this tool
</error>
<project>
{Tool['project_as_md']()}
</project>
"""


@tool
def remove_task_checklist(task_id: str) -> str:
    """Remove a checklist item from the current task

    Args:
        task_id: The ID of the checklist item to remove
    """
    current_project_name = State['projects']['current']
    project = State['projects']['projects'][current_project_name]

    if not project['current_task']:
        return "No current task selected"

    task = project['tasks'][project['current_task']]

    if 'checklist' not in task or task_id not in task['checklist']:
        return f"Error: Item with ID {task_id} not found"

    del task['checklist'][task_id]
    task['checklist_order'].remove(task_id)

    return Tool['project_as_md']()


@tool
def check_checklist_task(task_id: str) -> str:
    """Mark a checklist item as checked

    Args:
        task_id: The ID of the checklist item to check
    """
    current_project_name = State['projects']['current']
    project = State['projects']['projects'][current_project_name]

    if not project['current_task']:
        return "No current task selected"

    task = project['tasks'][project['current_task']]

    if 'checklist' not in task or task_id not in task['checklist']:
        return f"Error: Item with ID {task_id} not found"

    task['checklist'][task_id]['checked'] = True

    return Tool['project_as_md']()


@tool
def uncheck_checklist_task(task_id: str) -> str:
    """Mark a checklist item as unchecked

    Args:
        task_id: The ID of the checklist item to uncheck
    """
    current_project_name = State['projects']['current']
    project = State['projects']['projects'][current_project_name]

    if not project['current_task']:
        return "No current task selected"

    task = project['tasks'][project['current_task']]

    if 'checklist' not in task or task_id not in task['checklist']:
        return f"Error: Item with ID {task_id} not found"

    task['checklist'][task_id]['checked'] = False

    return Tool['project_as_md']()


@tool
def set_checklist_task_status(status: str, task_id: str) -> str:
    """Set the status text for a checklist item

    Args:
        status: The status text to set
        task_id: The ID of the checklist item
    """
    current_project_name = State['projects']['current']
    project = State['projects']['projects'][current_project_name]

    if not project['current_task']:
        return "No current task selected"

    task = project['tasks'][project['current_task']]

    if 'checklist' not in task or task_id not in task['checklist']:
        return f"Error: Item with ID {task_id} not found"

    task['checklist'][task_id]['status'] = status

    return Tool['project_as_md']()


@tool
def set_task_checklist_unitary(is_unitary: str, task_id: str) -> str:
    """Set whether a checklist item is unitary or not

    Args:
        is_unitary: "True" or "False" string indicating if task is unitary
        task_id: The ID of the checklist item
    """
    current_project_name = State['projects']['current']
    project = State['projects']['projects'][current_project_name]

    if not project['current_task']:
        return "No current task selected"

    task = project['tasks'][project['current_task']]

    if 'checklist' not in task or task_id not in task['checklist']:
        return f"Error: Item with ID {task_id} not found"

    task['checklist'][task_id]['unitary'] = is_unitary.lower() == "true"

    return Tool['project_as_md']()


@tool
def add_checklist_task_devlog(devlog: str, task_id: str) -> str:
    """Add a devlog entry to a checklist item

    Args:
        devlog: The devlog text to add
        task_id: The ID of the checklist item
    """
    current_project_name = State['projects']['current']
    project = State['projects']['projects'][current_project_name]

    if not project['current_task']:
        return "No current task selected"

    task = project['tasks'][project['current_task']]

    if 'checklist' not in task or task_id not in task['checklist']:
        return f"Error: Item with ID {task_id} not found"

    if 'devlog' not in task['checklist'][task_id]:
        task['checklist'][task_id]['devlog'] = []

    task['checklist'][task_id]['devlog'].append(devlog)

    return Tool['project_as_md']()


@tool
def add_task_checklist_item(caption: str, after: Optional[str] = None) -> str:
    """Add a checklist item to the current task

    Args:
        caption: The text description of the checklist item
        after: Optional ID of item to insert after. If None, appends to end
    """
    current_project_name = State['projects']['current']
    project = State['projects']['projects'][current_project_name]

    if not project['current_task']:
        return "No current task selected"

    task = project['tasks'][project['current_task']]

    # Initialize checklist structures if they don't exist
    if 'checklist' not in task:
        task['checklist'] = {}
    if 'checklist_order' not in task:
        task['checklist_order'] = []

    # Generate unique ID (first 8 chars of UUID)
    item_id = str(uuid.uuid4())[:8]

    new_item = {
        "name": caption,
        "status": "",
        "checked": False
    }

    task['checklist'][item_id] = new_item

    # Handle insertion position
    if after is None:
        # Append to end
        task['checklist_order'].append(item_id)
    else:
        if after not in task['checklist']:
            return f"Error: Item with ID {after} not found"
        # Insert after the specified item
        insert_idx = task['checklist_order'].index(after) + 1
        task['checklist_order'].insert(insert_idx, item_id)

    return f"task {caption} with id {item_id} added toe the checklist"
    return Tool['project_as_md']()


@tool
def add_checklist_tasks(tasks):
    response = []
    for task in tasks.split('\n'):
        if task.strip().startswith('##') or len(task.strip()) < 10:
            continue
        if task.strip().startswith('-'):
            task = task[1:]
        response.append(add_task_checklist_item(task.strip()))

    return '\n'.join(response)


@tool
def __project_as_md():
    """Convert the current project state to a markdown formatted string."""
    # Get current project data
    current_project_name = State['projects']['current']
    project = State['projects']['projects'][current_project_name]

    all_proj = State['projects']['projects'].to_dict()

    # Start building the markdown string
    md = ["# All Projects\n"]

    for pname in all_proj.keys():
        md.append(f"- `{pname}`")
    md.append('\n')

    # Project header
    md.append(f"# Project: {project['name']}\n")

    # Base directory
    md.append(f"**Base Directory:** `{project['base_dir']}`\n")

    # Aider Sessions
    md.append("\n## Aider Sessions")

    # Files to add
    md.append("\n## Files to Add")
    if project['files_to_add']:
        for file in project['files_to_add']:
            md.append(f"- `{file}`")
    else:
        md.append("- *No files to add*")

    # Files to drop
    md.append("\n## Files to Drop")
    if project['files_to_drop']:
        for file in project['files_to_drop']:
            md.append(f"- `{file}`")
    else:
        md.append("- *No files to drop*")

    aider_sessions = {
        'omni': project['aider_session']['omni']
    }
    md.append("\n## Tasks")
    if project['tasks']:
        for task_name, task_data in project['tasks'].items():
            # Add task header with current task indicator
            is_current = task_name == project['current_task']
            current_marker = " (Current)" if is_current else ""
            md.append(
                f"\n### {task_data.get('title', task_name)}{current_marker}")

            # Show checklist only for current task
            if is_current and 'checklist' in task_data:
                if 'aider_session' in task_data:
                    for name, sess_name in task_data['aider_session'].item():
                        aider_sessions[name] = sess_name
                md.append("\n#### Checklist:")
                # Use checklist_order to display items in correct order
                for item_id in task_data.get('checklist_order', []):
                    item = task_data['checklist'][item_id]
                    checkbox = "[x]" if item['checked'] else "[ ]"
                    md.append(f"- {checkbox} {item['name']} `{item_id}`")
                    if item['status']:
                        md.append(f"  - Status: {item['status']}")
    else:
        md.append("\n*No tasks defined*")

    md.append('\n')
    md.append('#### aider sessions')
    for name, sess_name in aider_sessions:
        md.append(f"- **{name}**: {sess_name}")

    # Join all lines with newlines
    return "\n".join(md)


@tool
def insure_omni() -> bool:
    # input('cacacaca')
    project_name = Tool['current_project']().name
    state_dict = State['projects']['projects'][project_name].to_dict()
    base_dir = state_dict['base_dir']
    files_to_add = state_dict['files_to_add']
    files_to_drop = state_dict['files_to_drop']
    project_name = State['projects']['current']
    run_with_tmux = Tool['run_with_tmux']

    o_sess_name = f"{project_name}_omni"
    if Tool['is_aider'](o_sess_name):
        return True

    print('init omni aider')
    run_with_tmux(f"cd {base_dir}", o_sess_name)

    time.sleep(.05)
    run_with_tmux(f"aider --sonnet --no-pretty", o_sess_name)
    # run_with_tmux('aider --model ollama_chat/qwq --no-pretty', o_sess_name)
    # time.sleep(1)
    print('sending <Enter> a bunch of times')
    for i in range(5):
        run_with_tmux('', o_sess_name)
        # time.sleep(0.02)

    run_with_tmux('/chat-mode ask', o_sess_name)

    for path in files_to_add:
        print(f"/add {path}")
        run_with_tmux(f"/add {path}", o_sess_name)
        # time.sleep(0.5)

    for path in files_to_drop:
        print(f"/drop {path}")
        run_with_tmux(f"/drop {path}", o_sess_name)
        # time.sleep(0.5)
    is_aider = Tool['is_aider']
    assert is_aider(
        o_sess_name), f"something went wrong wrapping aider in tmux session `{o_sess_name}`"
    State['projects']['projects'][project_name]['aider_session']['omni'] = o_sess_name

    return State['projects']['projects'][project_name]


@tool
def add_tasks_to_checklist(tasks):
    if not "checklist" in Tool['current_task']():
        Tool['current_task']()['checklist_order'] = []

    Tool['current_task']()['checklist'] = {}
