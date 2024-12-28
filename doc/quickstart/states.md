# Managing State in Cogni

State management is crucial for maintaining context and persistence in your agent applications.

## Basic State Usage

```python
from cogni import State

# Set state
State['my_state'] = {'key': 'value'}

# Get state
value = State['my_state'].key

# Check if state exists
if 'my_state' in State:
    print("State exists!")

# Delete state
del State['my_state']
```

## State Types

### Dictionary State
```python
# Attribute-style access
State['config'].debug = True
State['config'].api_key = "sk-..."

# Dictionary-style access
State['config']['timeout'] = 30
```

### List State
```python
# Initialize list
State['history'] = []

# Append items
State['history'].append("event")

# Access items
latest = State['history'][-1]
```

## Persistence

State is automatically persisted to disk:

```python
# State is saved in .states directory
State['user_preferences'] = {
    'theme': 'dark',
    'language': 'en'
}  # Automatically persisted

# Load persisted state
preferences = State['user_preferences']
```

## State Patterns

### Conversation History
```python
@tool
def save_message(msg: dict):
    if 'conversation' not in State:
        State['conversation'] = []
    State['conversation'].append({
        'content': msg['content'],
        'timestamp': time.time(),
        'role': msg['role']
    })
```

### User Preferences
```python
@tool
def get_user_settings(user_id: str) -> dict:
    if 'users' not in State:
        State['users'] = {}
    if user_id not in State['users']:
        State['users'][user_id] = {
            'language': 'en',
            'timezone': 'UTC'
        }
    return State['users'][user_id]
```

### Caching
```python
@tool
def cached_api_call(url: str) -> dict:
    if 'api_cache' not in State:
        State['api_cache'] = {}
    
    if url in State['api_cache']:
        if time.time() - State['api_cache'][url]['timestamp'] < 3600:
            return State['api_cache'][url]['data']
    
    data = requests.get(url).json()
    State['api_cache'][url] = {
        'data': data,
        'timestamp': time.time()
    }
    return data
```

## Best Practices

1. State Organization
   - Use clear naming conventions
   - Group related data
   - Document state structure

2. Error Handling
   - Check for existence
   - Provide defaults
   - Handle race conditions

3. Performance
   - Cache frequently accessed data
   - Clean up old state
   - Use appropriate data structures

## Next Steps

- Create [HTTP endpoints](endpoints.md)
- Build a [swarm of agents](first_swarm.md)
- Implement monitoring
