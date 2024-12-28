# Creating Your First Cogni Project

## Project Structure

A typical Cogni project has this structure:

```
my_project/
├── agents/          # Agent definitions and logic
├── tools/          # Reusable tool functions
├── middlewares/    # Processing middleware
└── prompts/        # Agent conversation templates
```

## Initialize Project

1. Create and enter project directory:
```bash
mkdir my_project
cd my_project
cogni init
```

2. This creates a basic project structure and configuration file.

## Configuration

The `cogni.yaml` file controls your project settings:

```yaml
name: my_project
version: 0.1.0
description: "My first Cogni project"

# Configure default LLM settings
llm:
  provider: openai
  model: gpt-4
  temperature: 0.7

# Add any project-specific settings
settings:
  debug: false
  log_level: info
```

## Next Steps

- Create your first [tool](first_tool.md)
- Set up your first [agent](first_agent.md)
- Learn about [state management](states.md)
