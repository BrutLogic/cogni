# Cogni

## What is Cogni?
Cogni is a micro-framework for building conversational AI systems with minimal boilerplate code. It provides a functional approach to agent development, treating agents as composable functions.

### Core Concepts

#### Magic Imports
Cogni uses automatic discovery and registration of components:
```python
# Any file in tools/ directory is automatically imported
@tool  # Registers function in global Tool container
def process_data(input: str) -> str:
    return transform(input)

# Access from anywhere
from cogni import Tool
result = Tool['process_data']("hello")
```

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

agent = Agent("smart_agent", "prompt|smart_reply")
```

The rehop mechanism allows:
- Multiple LLM calls per conversation
- Dynamic conversation flow
- Context preservation between calls

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

2. Create tools and middleware:
```python
from cogni import tool, mw, Agent

@tool
def fetch_data(query: str) -> dict:
    """Tool for data retrieval"""
    return database.query(query)

@mw
def process_response(ctx, conv):
    """Middleware for response processing"""
    return enhance(conv)

agent = Agent("my_agent", "prompt|process_response")
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

### Architecture

The framework follows these key principles:
- Automatic component registration
- Separation of tools and middleware
- Flexible conversation flow with rehop
- Convention over configuration

### Testing

Run the test suite:
```bash
pytest tests/
```

### License

MIT License
