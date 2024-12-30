# Conversation and Message Guide

The `Conversation` and `Message` classes are core components for handling dialogue in Cogni.

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

# From a file
conv = Conversation.from_file('my_conversation.conv')
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

4. Persistence:
```python
# Save to string
conv_text = conv.to_str()

# Save to file
conv.to_file('saved_conversation.conv')

# Convert to OpenAI format
openai_messages = conv.openai()
```

5. Rehop for inference:
```python
# Create new conversation for next inference step
new_conv = conv.rehop("Let me think about that", role='system')
```

## File Format

Conversations use a simple text format with `__-__` as message separator:

```
system:You are a helpful assistant.
__-__
user:Hi there!
__-__
assistant:Hello! How can I help you today?
```

This format makes it easy to:
- Store conversations in version control
- Edit them in any text editor
- Share them between different parts of your application
