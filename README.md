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

In other terms, agents can be thought as **functions**. This allows for powerful control flows:

```python
# Sequential processing
result = Agent['processor'](Agent['parser'](user_input))

# Parallel tasks
tasks = Agent['task_splitter'](complex_job)
results = [Agent['worker'](task) for task in tasks]
final = Agent['aggregator'](results)

# Recursive handling
def process_with_feedback(input_data):
    result = Agent['processor'](input_data)
    if Agent['quality_check'](result):
        return result
    return process_with_feedback(Agent['refiner'](result))
```

### Magic Imports
Cogni uses automatic discovery to make components available globally:

```python
# Components are automatically discovered in your project structure
from cogni import Tool, Agent, MW

# No need to manually import individual tools/agents
result = Tool['my_tool'](data)
response = Agent['my_agent'](query)
```

### Tools System
Tools are standalone functions that can be used by any agent:

```python
from cogni import tool, Tool

@tool
def fetch_weather(city: str) -> dict:
    """Get weather data for a city"""
    return weather_api.get(city)

# Use anywhere in your code
Tool['fetch_weather']('Paris')
```

### Creating an Agent
Agents are created by combining a prompt template (.conv file) with middleware:

1. Create the prompt template (my_agent.conv):
```
system: You are MyAgent, designed to process user requests.
Your goal is to {goal}.

user: {user_input}
```

2. Create the agent:
```python
from cogni import Agent, mw

@mw
def process_response(ctx, conv):
    # Use tools if needed
    weather = Tool['fetch_weather'](conv[-1].content)
    # Return modified conversation
    return conv.rehop(f"The weather is {weather}")

# Chain middlewares with pipes
Agent('my_agent', 'prompt|gpt4|process_response')
```

### Middleware Flow
Middlewares form a processing chain, each receiving and returning a conversation:

```python
@mw
def smart_middleware(ctx, conv):
    # Access conversation history
    user_msg = conv[-1].content
    
    # Use tools
    result = Tool['some_tool'](user_msg)
    
    # Continue conversation with rehop
    return conv.rehop(
        f"I found this: {result}",
        role="assistant"
    )
```

### Creating a Complete Agent

1. Project Structure:
```
agents/
  my_agent/
    prompts/
      my_agent.conv    # Prompt template
    middlewares/
      process.py       # Custom middleware
    tools/
      helpers.py       # Agent-specific tools
```

2. Prompt Template (my_agent.conv):
```
system: You are MyAgent, specialized in {domain}.
Your capabilities include: {capabilities}

user: {user_input}
```

3. Middleware (process.py):
```python
from cogni import mw, Tool

@mw
def process(ctx, conv):
    # Process user input
    data = Tool['helper'](conv[-1].content)
    
    # Continue conversation
    return conv.rehop(f"Processed: {data}")
```

4. Tools (helpers.py):
```python
from cogni import tool

@tool
def helper(input: str) -> str:
    return f"Processed {input}"
```

5. Agent Registration:
```python
from cogni import Agent

Agent('my_agent', 'prompt|gpt4|process')
```

6. Usage:
```python
from cogni import Agent

response = Agent['my_agent']("Hello!")
```

### Testing

Run the test suite:
```bash
pytest tests/
```

### License

MIT License
