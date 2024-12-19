# Cogni

## What is Cogni?
Cogni is a micro-framework for building conversational AI systems with minimal boilerplate code. It provides a functional approach to agent development, treating agents as composable functions.

### Core Concepts

#### Agents as Functions
In Cogni, agents are treated as black-box functions that:
- Take any number/type of inputs
- Return any type of output
- Can have side effects
- Can be composed and chained

Example:
```python
from cogni import Agent

# Process user input through multiple agents
result = Agent['summarizer'](
    Agent['fact_checker'](user_input)
)
```

#### Middleware Chain
Agents use a middleware chain pattern for processing:
- Each middleware is a function that processes input
- Middlewares can be chained together
- Common operations (LLM calls, validation, etc.) are middleware
- Easy to add custom middleware

Example:
```python
@MW.register
def validate_input(ctx, conv):
    # Validation logic
    return conv

agent = Agent("validator", "validate_input|llm_chain")
```

#### Conversation Management
Built-in classes for managing conversations:
- `Message`: Single message with role and content
- `Conversation`: Sequence of messages with utilities
- Serialization/deserialization support
- OpenAI API format compatibility

### Getting Started

1. Install:
```bash
pip install cogni
```

2. Create an agent:
```python
from cogni import Agent, MW

@MW.register
def my_middleware(ctx, conv):
    return process(conv)

agent = Agent("my_agent", "my_middleware|llm_chain")
```

3. Use the agent:
```python
result = agent("Hello!")
```

### Key Features

- **Minimal Boilerplate**: Focus on agent logic, not infrastructure
- **Functional Design**: Agents as composable functions
- **Flexible Middleware**: Easy to extend and customize
- **Built-in Conversation Management**: Ready-to-use message handling
- **LLM Integration**: Pre-built middleware for LLM interactions

### Architecture

The framework follows these key principles:
- Separation of concerns via middleware
- Functional composition of agents
- Convention over configuration
- Extensible by design

### Testing

Run the test suite:
```bash
pytest tests/
```

### License

MIT License
