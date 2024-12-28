# Creating Your First Agent: ShellAgent

This guide walks through creating a shell command assistant agent.

## 1. Create Agent Structure

```bash
cogni create-agent ShellAgent
```

This creates:
```
agents/
└── ShellAgent/
    ├── prompts/
    │   └── shell_agent.conv
    ├── middlewares/
    │   └── shell_loop.py
    └── agent.py
```

## 2. Define the Prompt

Edit `prompts/shell_agent.conv`:

```
system: You are ShellAgent, a CLI assistant.
You help users with shell commands.

Instructions:
1. Understand the user's request
2. Suggest appropriate commands
3. Explain what each command does
4. Use safe commands only

Tools available:
<tool name="run_command">command</tool>
<tool name="check_permissions">path</tool>

user: {user_input}
```

## 3. Implement Middleware

Edit `middlewares/shell_loop.py`:

```python
from cogni import mw, Tool

@mw
def shell_loop(ctx, conv):
    """Process shell commands safely."""
    # Get user's last message
    user_msg = conv[-1].content
    
    # Process through LLM
    response = conv.rehop(
        f"I'll help you with: {user_msg}",
        role="assistant"
    )
    
    return response
```

## 4. Create Required Tools

Create `tools/shell_tools.py`:

```python
from cogni import tool
import subprocess

@tool
def run_command(cmd: str) -> str:
    """Run a shell command safely."""
    # Add safety checks here
    result = subprocess.run(
        cmd, 
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout

@tool
def check_permissions(path: str) -> bool:
    """Check if we have permission to access path."""
    return os.access(path, os.R_OK | os.W_OK)
```

## 5. Register the Agent

In `agent.py`:

```python
from cogni import Agent

Agent('ShellAgent', 'prompt|gpt4|shell_loop')
```

## Using the Agent

```python
from cogni import Agent

# Create agent instance
shell = Agent['ShellAgent']

# Ask for help
response = shell("How do I list files in the current directory?")
print(response)
```

## Safety Considerations

1. Input Validation
   - Sanitize all commands
   - Check permissions
   - Limit allowed commands

2. Error Handling
   - Catch and handle exceptions
   - Provide clear error messages
   - Prevent dangerous operations

3. Monitoring
   - Log all commands
   - Track usage patterns
   - Set up alerts

## Next Steps

- Create a [swarm of agents](first_swarm.md)
- Add [state management](states.md)
- Create [HTTP endpoints](endpoints.md)
