# Cogni

# UPDATE

I'm still feeding the repo

# IMPORTANT NOTE 1
If your reading this, I'm currently refactoring my code and feeding the repo.

It's not usable yet, and I'm actively working on the doc (and this README.md).

You can still read it though, it will give you an idea of what it's all about. Just be aware that it will take a few days (probably a week) to be a usable/well documented project.

If you want to chat, come to my [Discord](https://discord.gg/eXtysN5HAH) :) !

I'm super glad for your interest in my stuff.

# IMPORTANT NOTE 2

My initial plan was to feed this README as I feed the repo, but I'm not sure yet how to structure it properly.

For that reason I'll leave it as it is and work on:

## Quick Start

[How Cogni works (If you're in a hurry)](doc/quickstart/how-cogni-works.md)

[Installation](doc/quickstart/install.md)

[Prompting primitives](doc/quickstart/prompting.md)

[Your first Cogni project](doc/quickstart/project_init.md)

[Your first tool](doc/quickstart/first_tool.md)

[Your first agent: ShellAgent](doc/quickstart/first_agent.md)

[Your first swarm: DiscordAgent](doc/quickstart/first_swarm.md)

[Handling states](doc/quickstart/states.md)

[Handling Endpoint](doc/quickstart/states.md)



## What is Cogni?

Cogni is a framework focusing on low code/low boilerplate implementation of LLM agents.

### Yeah but, why not LangChain though?

I wouldn't go that far as saying `LangChain==Cancer`.

LangChain/LangGraph allow for creating agents and orchestrating flow and communication.
One key assumption of Cogni is that agentic execution flow has the same requirements and complexity as code; and therefore Agents should be created, managed, and orchestrated as code and by code.

Which, as a side effect, allows for borrowing ideas from domains like web dev, where best practices are mature.

## How it works

Cogni is built on the principle of "Agents as Functions," allowing for a modular and composable approach to AI agent development.

### Hide complexity

Do Large Language Models have any amount of complexity?

If your answer includes "Matrix multiplication" or "Attention map caching", I would have a simple objection: **I don't care**

When you implement agents, for all you care, LLMs are magic black boxes that take text as input and return text.

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

We'll define *Agent* as a black box that takes any number of inputs of any type, and returns either nothing, or anything of any type, and potentially has *side effects*.

In other terms, agents can be thought as **functions**. This allows for powerful control flows:

(\*Note: `function` as in "a Python function"; as opposed to more rigorous definition, like in functional programming)

```python
from cogni import Agent

# Process tasks in a loop
def do_complex_stuff(task_description:str):
    for sub_task in Agent['task_splitter'](task_description):
        Agent['worker'](sub_task)
    
```

### Magic Imports


Cogni uses automatic discovery to make components available globally:

**With Cogni, we're free from the burden of imports**

Anywhere in your project:

```python
# project/it/can/be/any/path/fliddleblooksh.py
from cogni import tool

@tool
def add_two_ints(a:int, b:int)->int:
    return int(a) + int(b)
```

Anywhere else:

```python
# project/some/other/file/anywhere.py
from cogni import Tool

print(
    Tool['add_two_ints'](2, 3)
)#> 5
```

### Tools System

Tools are standalone functions that can be used by coder and agents:

```python
# agents/SomeAgents/tools/someagent_tools.py
from cogni import tool

@tool
def fetch_weather(city: str) -> dict:
    """Get weather data for a city"""
    return weather_api.get(city)

```

```python
# somefile.py
from cogni import Tool

print(Tool['fetch_weather']('Paris'))
```



### Install

````bash
git clone https://github.com/BrutLogic/cogni.git&&cd cogni
python3 -m pip install
### Creating an Agent
Agents are created by combining a prompt template (.conv file) with middleware:

```bash
cd myproject
cogni create_agent
````

### Middleware Flow

Middlewares form a processing chain, each receiving and returning a conversation:

```python
@mw
def myagent_loop(ctx, conv):
    # Access conversation history
    last_msg = conv[-1].content
    
    # Use tools
    result = Tool['some_tool'](user_msg)
    
    # Continue conversation with rehop
    return conv.rehop(
        f"I found this: {result}",
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

2. Prompt Template (my\_agent.conv):

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

