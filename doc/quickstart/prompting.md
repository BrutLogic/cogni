# Conversation and Message Guide

The `Conversation` and `Message` classes are core components for handling dialogue in Cogni.

## Note about Few Shot Prompting

Few Shot Prompting is great, and you should be using it.

For all of this doc, I'll call "**Prompt**" the base conversation of an agent; a short conversation starting with a system prompt

## File

By convention, the prompt of an agent will be in a file with the same name as the agent with `.conv` extension.

So, for the example agent `ShellAgent`
```
agents/
└─ ShellAgent/
    ├─ agents/
    │   └─ ShellAgent.py 
    ├─ middlewares/
    │   └─ shellagent_loop.py
    ├─ prompts/
    │   └─ ShellAgent.conv # 👈 IT'S HERE
    └─ tools/
        └─ shellagent_tools.py 
```

## File Format

A message is formated `{role}:{content}` and message are separated with `__-__`

```
system: Your are an agent blabla

__-__

user: can you to stuff

__-__

assistant: sure :)
```

## Message Class

A `Message` represents a single message in a conversation with:

- A `role` (e.g., 'user', 'system', 'assistant')
- `content` (the actual text)

```python
from cogni import Message

# Create a message
msg = Message('user', 'What is the current directory?')

# Access properties
print(msg.role)      # 'user'
print(msg.content)   # 'What is the current directory?'

# Convert to dict format
msg_dict = msg.to_dict()  # {'role': 'user', 'content': '...'}
```

## Conversation Class

A `Conversation` manages a sequence of messages with features for:

1. Creation from strings or files:
```python
from cogni import Conversation

# From a string
conv_str = """
system:You are a helpful assistant.
__-__

user:Hi!
__-__
assistant:Hello! How can I help you?
"""
conv = Conversation.from_str(conv_str)
```

2. Adding messages:
```python
# Add a single message
conv = conv + Message('user', 'What time is it?')

# Combine conversations
conv2 = Conversation.from_str("user:Another question")
combined = conv + conv2
```

3. Accessing messages:
```python
# Get specific message
first_msg = conv[0]
last_msg = conv[-1]

# Get a slice
recent = conv[-3:]  # Last 3 messages
```

## Flags

Conversations can have flags that control their behavior:

```python
conv = Conversation.from_str("user: hello")

# Check flags
print(conv.llm)           # None - LLM model to use
print(conv.should_infer)  # False - Whether to run inference
print(conv.hops)         # 0 - Number of inference steps

# Set flags
conv.llm = "gpt-4"
conv.should_infer = True
```

## Templating

Messages can be parsed using custom parsers to replace placeholders or apply formatting:

```python
from cogni import Message, parser

# Create a parser for <var> tags
var_parser = parser("<var>", "</var>")

msg = Message("user", "My name is <var>Alice</var>")
msg.parse(var_parser)  # Will process the <var> tags

# Create custom parsers for any tags
custom_parser = parser("{{", "}}")
msg.parse(custom_parser)  # Will process {{tags}}
```

The parser function helps create reusable parsers for different tag formats. Common uses include:

- Replacing variables in prompts
- Formatting code blocks
- Processing custom markup in messages
