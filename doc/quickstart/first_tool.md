# Creating Your First Tool

Tools are standalone functions that can be used by both developers and agents. They provide reusable functionality that can be accessed globally throughout your project.

## Basic Tool Example

Create `tools/calculator.py`:

```python
from cogni import tool

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of the two numbers
    """
    return a + b
```

## Using Tools

Tools can be accessed anywhere in your project:

```python
from cogni import Tool

# Use the tool directly
result = Tool['add_numbers'](5, 3)
print(result)  # Output: 8

# Tools are also available to agents
@tool
def complex_math(x: int) -> int:
    """Perform complex math using other tools."""
    result = Tool['add_numbers'](x, 10)
    return result * 2
```

## Tool Best Practices

1. Clear Documentation
   - Always include docstrings
   - Document parameters and return types
   - Provide usage examples

2. Error Handling
   - Validate inputs
   - Return meaningful error messages
   - Handle edge cases

3. Naming Conventions
   - Use descriptive names
   - Follow verb_noun pattern for actions
   - Be consistent across project

## Advanced Features

### Tool with State

```python
from cogni import tool, State

@tool 
def save_result(calculation: str, result: float):
    """Save a calculation result to state."""
    if 'calculations' not in State:
        State['calculations'] = []
    State['calculations'].append({
        'calculation': calculation,
        'result': result,
        'timestamp': time.time()
    })
```

### Async Tools

```python
from cogni import tool

@tool
async def fetch_data(url: str) -> dict:
    """Fetch JSON data from URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

## Next Steps

- Learn how to [create an agent](first_agent.md) that uses your tools
- Explore [state management](states.md) for persistent data
- See how to create [HTTP endpoints](endpoints.md)
