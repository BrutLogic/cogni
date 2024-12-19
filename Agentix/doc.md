# Message and Conversation Documentation

## Message
The `Message` class encapsulates a single message, identifying the sender (`role`) and the message text (`content`).

- `role`: Sender's role (e.g., 'user', 'system', 'assistant').
- `content`: Text of the message.

Messages are fundamental for tracking and managing dialogues.

## Conversation
The `Conversation` class models a sequence of messages, with methods to manage and persist conversations.

Useful methods:

- `from_file(path: str)`: Loads a conversation from a file.
- `from_str(conv_str: str)`: Creates a conversation from a string.
- `to_str()`: Serializes the conversation to a string.
- `to_file(path: str)`: Persists the conversation to a file.
- `openai()`: Formats the conversation for OpenAI API.
- `to_dict()`: Converts the conversation to a list of dictionaries, each representing a message.
Example output of `to_dict()` with three messages:
```python
[{'role': 'system', 'content': "You're an AGI"},
 {'role': 'user', 'content': 'How do I start?'},
 {'role': 'assistant', 'content': 'Just tell me what you need help with!'}]
```


Conversations support dynamic interactions, including adding messages or merging conversations.
