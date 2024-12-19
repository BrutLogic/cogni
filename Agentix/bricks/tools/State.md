# State Management in Agentix

## State Architecture

- **_State**: Manages state entries, loading, saving, callbacks.
- **StateDict**: Dict wrapper, attribute access, persistence.
- **StateList**: List wrapper, persistence.

## Projects Handling

Projects are stored as:

```json
{
  "projects": {
    "current_project": "ProjectAlpha",
    "projects": {
      "ProjectAlpha": {
        "base_dir": "/path/to/project",
        "files_to_add": ["src/main.py", "src/utils.py"],
        "files_to_drop": ["src/old_module.py"],
        "aider_session": {
          "omni": "ProjectAlpha_omni_session"
        }
      }
    }
  },
  "current_task": {
    "description": "Implement authentication",
    "acceptance_criteria": ["User can register", "User can login"]
  },
  "discord": {
    "message_map": {},
    "callbacks": {
      "general": "general_channel_handler"
    }
  }
}
```

- **Pointers**: `current_project`, `current_task` reference specific states.

## Using State

### Setting State

```python
from agentix import State

State['new_state'] = {'key1': 'value1'}
State['current_project'].description = "Updated Project Description"
```

### Getting State

```python
"NonexistentState" in State  # > False

current_project = State['current_project'].to_dict()
base_dir = State['projects']['ProjectAlpha'].base_dir
```

### Deleting State

```python
del State['obsolete_state']
```

## State Persistence

- Auto-saved to `./.states/*.json`.
- Callbacks triggered on changes.

## Accessing State as JSON

```python
import json

state_json = json.dumps(State['projects'].to_dict(), indent=2)
print(state_json)
```

## Example Usage

### Initialize Project

```python
from agentix import State

State['projects'] = {
    "current_project": "ProjectAlpha",
    "projects": {}
}

State['projects']['projects']['ProjectAlpha'] = {
    "base_dir": "/path/to/project",
    "files_to_add": ["src/main.py", "src/utils.py"],
    "files_to_drop": ["src/old_module.py"],
    "aider_session": {
        "omni": "ProjectAlpha_omni_session"
    }
}
```

### Manage Tasks

```python
State['current_task'] = {
    "description": "Implement authentication",
    "acceptance_criteria": ["User can register", "User can login"]
}

State['current_task'].status = "In Progress"
```

### Register Callbacks

```python
def on_project_change(state_id, state):
    print(f"Project {state_id} updated.")

State.onChange(on_project_change)
```

## Best Practices

- **Consistent Naming**: Clear, consistent state names.
- **Avoid Deep Nesting**: Keep state structure flat.
- **Use Callbacks Wisely**: Prevent complex dependencies.
- **Regular Backups**: Protect against data loss.
- **Validation**: Ensure data integrity.

## Conclusion

`State` efficiently manages application state. Follow strategies and best practices for effective project and task handling.
