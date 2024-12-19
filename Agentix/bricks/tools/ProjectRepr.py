from agentix import tool, Tool, State


@tool
def current_project():
    """Get the current project data."""
    current_project_name = State['projects']['current']
    return State['projects']['projects'][current_project_name]


@tool
def current_task():
    """Get the current task data."""
    project = current_project()
    current_task_name = project['current_task']
    if current_task_name and project['tasks']:
        return project['tasks'][current_task_name]
    return None


def all_projects_as_md():
    """Generate markdown for all projects list."""
    all_proj = State['projects']['projects'].to_dict()
    md = ["# All Projects\n"]
    for pname in all_proj.keys():
        md.append(f"- `{pname}`")
    return '\n'.join(md)


def project_files_as_md(project):
    """Generate markdown for project files sections."""
    md = []

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

    return md


@tool
def task_as_md():
    """Generate markdown for a single task."""
    task_data = Tool['current_task']()
    if not task_data:
        return "\n**No current task yet**\n"
    md = [
        f'''## Current Task (`{task_data['name']}`) **{task_data['title']}**'''
    ]
    md.append('### Description')
    md.append(task_data['description'])

    md.append('\n### Specs')

    if not 'specs' in task_data:
        md.append('*No specs yet*')
    else:
        md.append(task_data['specs'])

    md.append("\n### Checklist:")

    if not 'checklist' in task_data:
        md.append('*No checklist items yet*')

    for item_id in task_data.get('checklist_order', []):
        md.append('\n')
        item = task_data['checklist'][item_id]
        checkbox = "[x]" if item['checked'] else "[ ]"
        md.append(f"- {checkbox} (`{item_id}`) {item['name']} ")
        if item['status']:
            md.append(f"  - Status: {item['status']}")

    return "\n".join(md)


def aider_sessions_as_md(project, current_task_data):
    """Generate markdown for aider sessions."""
    aider_sessions = {
        'omni': project['aider_session']['omni']
    }
    task = current_task()
    if task:
        tname = task.name
        if f"{tname}_ask" in State['Aiders']:
            aider_sessions['ask'] = f"{tname}_ask"

        if f"{tname}_code" in State['Aiders']:
            aider_sessions['code'] = f"{tname}_code"

    md = ['\n#### aider sessions']
    for name, sess_name in aider_sessions.items():
        md.append(f"- **{name}**: {sess_name}")
    return "\n".join(md)


@tool
def cwd():
    return Tool['current_project']()['base_dir']


@tool
def project_as_md():
    """Convert the current project state to a markdown formatted string."""
    project = current_project()
    current_task_data = current_task()

    md = []

    # Add all projects section
    md.append(all_projects_as_md())

    # Project header and base directory
    md.extend([
        f"\n# Current Project: {project['name']}\n",
        f"**Base Directory:** `{project['base_dir']}`\n",
    ])

    # Add files sections
    # md.extend(project_files_as_md(project))

    # Add tasks section
    md.append("\n## Tasks")

    if project['tasks']:
        for task_name, task_data in project['tasks'].items():
            is_current = task_name == project['current_task']
            if not is_current:
                md.append(f"### (`{task_name}`) {task_data['title']}")

        md.append(task_as_md())
    else:
        md.append("\n*No tasks defined*")

    # Add aider sessions
    md.append(aider_sessions_as_md(project, current_task_data))

    # Add checklist with devlogs

    md.append("\n### Checklist")

    md.append(Tool['current_checklist_as_md']())
    md.append('\n\n# Next step (the action to perform)')
    if 'next_step' in project:

        md.append(project.next_step)
    else:
        md.append('**No next step yet**')

    return "\n".join(md)


@tool
def set_next_step(caption: str):
    Tool['current_project']()['next_step'] = caption

    return f"Next step set to `{caption}`"


@tool
def current_checklist():
    return Tool['current_task']().checklist


@tool
def current_checklist_as_md():
    md = ["#### current checklist item"]
    current_task = Tool['current_task']()

    if not 'checklist' in current_task:
        md.append('no checklist yet')
        return '\n'.join(md)

    # del current_task['checklist']
    # del current_task['checklist_order']
    # del current_task['current_cl_item']

    cl = current_task.checklist

    for task_id, task in cl.to_dict().items():
        if not task['checked']:
            current_task['current_cl_item'] = task_id
            break

#    cur_cl_id = 'oui'
    if not 'current_cl_item' in current_task \
        or not "checklist" in current_task \
            or not len(current_task['checklist']) \
        or not current_task['current_cl_item']\
            or not isinstance(current_task.current_cl_item, str):
        md.append('**No checklistitem selected**')
        return '\n'.join(md)
    else:
        cur_cl_id = current_task.current_cl_item
        print(cur_cl_id)
        md.append(current_task.current_cl_item +
                  ' \t' +
                  cl[cur_cl_id].name)

    md.append('\n#### All Checklist Items')
    for item_id in current_task.get('checklist_order', []):
        item = current_task['checklist'][item_id]
        if not len(item['name'].strip()):
            continue

        check_mark = "x" if item.get('checked', False) else " "
        status = f" ({item['status']})" if item.get('status') else ""
        md.append(
            f"- 【{check_mark}】(id=`{item_id}`) {item['name']}{status}. The id is `{item_id}`")

        # Add devlog entries if they exist
        if 'devlog' in item and item['devlog']:
            for log_entry in item['devlog']:
                md.append(f"    > {log_entry}")
    return '\n'.join(md)


@tool
def current_checklist():
    return Tool['current_task']().checklist

    return str(Tool['current_task']().checklist)


@tool
def set_current_checklist_item(cl_item_id):
    Tool['current_task']().current_cl_item = cl_item_id
    return f"{cl_item_id} set as current"
