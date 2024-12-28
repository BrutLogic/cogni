# Creating Your First Swarm: DiscordAgent

A swarm consists of multiple specialized agents working together. We'll create a Discord bot using multiple coordinated agents.

## Project Structure

```
agents/
└── DiscordAgent/
    ├── agents/
    │   ├── message_handler.py    # Processes incoming messages
    │   ├── command_parser.py     # Parses commands
    │   └── response_formatter.py # Formats responses
    ├── prompts/
    │   ├── message_handler.conv
    │   ├── command_parser.conv
    │   └── response_formatter.conv
    └── tools/
        └── discord_tools.py
```

## 1. Create the Agents

### Message Handler
```python
from cogni import Agent

Agent('MessageHandler', 'prompt|gpt4|message_handler_loop')
```

### Command Parser
```python
from cogni import Agent

Agent('CommandParser', 'prompt|gpt3|command_parser_loop')
```

### Response Formatter
```python
from cogni import Agent

Agent('ResponseFormatter', 'prompt|gpt3|response_formatter_loop')
```

## 2. Define Communication Flow

```python
from cogni import tool, Agent

@tool
def process_message(message: str) -> str:
    # 1. Message Handler processes raw input
    context = Agent['MessageHandler'](message)
    
    # 2. Command Parser extracts intent
    command = Agent['CommandParser'](context)
    
    # 3. Response Formatter creates reply
    response = Agent['ResponseFormatter'](command)
    
    return response
```

## 3. Implement Discord Integration

```python
import discord
from cogni import Tool

class DiscordBot(discord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            return
            
        response = Tool['process_message'](message.content)
        await message.channel.send(response)
```

## 4. State Management

```python
from cogni import State

# Store conversation history
@tool
def save_conversation(msg: dict):
    if 'conversations' not in State:
        State['conversations'] = []
    State['conversations'].append(msg)

# Track user preferences
@tool
def get_user_preferences(user_id: str) -> dict:
    return State['preferences'].get(user_id, {})
```

## 5. Running the Swarm

```python
# Initialize all agents
Agent['MessageHandler']
Agent['CommandParser']
Agent['ResponseFormatter']

# Start Discord bot
client = DiscordBot()
client.run('your-token-here')
```

## Benefits of Swarm Architecture

1. Specialization
   - Each agent has a specific role
   - Optimized for different tasks
   - Can use different models

2. Scalability
   - Easy to add new agents
   - Horizontal scaling
   - Independent updates

3. Reliability
   - Fault isolation
   - Easy to debug
   - Simple to test

## Next Steps

- Add [HTTP endpoints](endpoints.md)
- Implement [state persistence](states.md)
- Add monitoring and logging
