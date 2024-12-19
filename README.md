# Cogni

## What is Cogni?
Cogni is a micro-framework allowing low code/low boilerplate implementation of LLM agents.

### Yeah but, why not LangChain though?
LangChain/LangGraph allow for creating agents and orchestrating flow and communication.
One key assumption of Cogni is that agentic execution flow has the same requirements and complexity as code; and therefore Agents should be created, managed, and orchestrated by code.
Which, as a side effect, allows for borrowing architecture from domains like web dev, where best practices are mature.

## How it works
Cogni is built on the principle of "Agents as Functions," allowing for a modular and composable approach to AI agent development.

### Hide complexity
Do Large Language Models have any amount of complexity?

If your answer includes "Matrix multiplication" or "Attention map caching", I would object that I don't care.

LLMs are magic black boxes that take text as input and return text.

For all we care, from our coder point of view, LLMs are as simple as:
```python
def chat_completion(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()
```

### Going further
Our goal as coders should be that, from any given scope, all dependencies are magic black boxes with clear specifications.

### Everything is a function
We'll define *Agent* as a blackbox that takes any number of inputs of any type, and returns either nothing, or anything of any type, and potentially has *side effects*.

In other terms, agents can be thought as **functions**.

Here's a toy example of an execution flow this approach allows for:
```python
from cogni import Agent

for task in Agent['task_lister'](user_input):
    Agent['task_executor'](task)
```

### Cogni's approach

#### Separation of concerns
In web development, it's common to have a conventional directory structure containing:
- Presentation/integration (templates)
- Application logic (TypeScript)
- Styling (CSS)

Adopting a similar approach, we can break down our agents into:
- Conversation templates
- Application Logic
- Tools/utilities/dependencies

Because some processes will be common across agents, we'll further break down *Application Logic* into middlewares.

#### Global containers and magic imports
Taking inspiration from web frameworks like Nuxt and aiming for **Low Code**, all components of our agentic stack will be automatically imported and accessible via global containers:

```python
# Inside any file within our project
from cogni import tool

@tool
def add_ints(a: int, b: int) -> int:
    return a + b

# Automatically available anywhere
from cogni import Tool
print("4 + 3 =", Tool['add_ints'](4, 3))
```

### Building an agent with Cogni

#### Tools vs Middleware
- **Tools** (@tool): Standalone functions for discrete operations
```python
@tool
def validate_json(data: str) -> bool:
    return is_valid_json(data)
```

- **Middleware** (@mw): Functions that process agent conversations
```python
@mw
def add_context(ctx, conv):
    conv.add_message("system", get_context())
    return conv
```

#### Agent Flow with Rehop
Agents can trigger multiple LLM calls in a conversation:

```python
@mw
def smart_reply(ctx, conv):
    # First inference
    conv = conv.rehop(llm(conv))
    
    # Check if we need clarification
    if needs_clarification(conv[-1].content):
        # Second inference with updated context
        conv = conv.rehop(
            "Please clarify your previous response",
            role="system"
        )
    return conv

# Create agent with middleware chain
agent = Agent("smart_agent", "prompt|gpt4|smart_reply")
```

The rehop mechanism allows:
- Multiple LLM calls per conversation
- Dynamic conversation flow
- Context preservation between calls

#### Getting Started

1. Install:
```bash
pip install cogni
```

2. Create an agent:
```python
from cogni import Agent, mw, tool

@tool
def fetch_data(query: str) -> dict:
    """Tool for data retrieval"""
    return database.query(query)

@mw
def process_response(ctx, conv):
    """Middleware for response processing"""
    return enhance(conv)

# Chain middlewares with pipes
agent = Agent("my_agent", "prompt|gpt4|process_response")
```

3. Use the agent:
```python
result = agent("Hello!")
```

### Key Features

- **Magic Imports**: Automatic component discovery
- **Tool System**: Easy function registration and access
- **Flexible Middleware**: Chainable conversation processors
- **Rehop Mechanism**: Multi-step LLM interactions
- **Built-in Conversation Management**: Ready-to-use utilities

### Testing

Run the test suite:
```bash
pytest tests/
```

### License

MIT License
