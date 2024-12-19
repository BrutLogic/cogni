# Agentix

## What is Agentix?
Agentix is a micro-framework allowing low code/low boilerplate implementation of LLM agents.

### Yeah but, why not LangChain though ?
LangChain/LangGraph allow for creating agents and orchestrating flow and communication.
One key assumption of Agentix is that agentic execution flow has the same requirements and complexity as code; and therefore Agents should created, managed, and orchestrated by code.
Which, as a side effect, allows for borrowing architecture from domains as web dev, where best practices are mature.

## How it works
Agentix is built on the principle of "Agents as Functions," allowing for a modular and composable approach to AI agent development.

### Hide complexity
Do Large Language Models have any amount of complexity ?

If your answer includes "Matrix multiplication" or "Attention map caching", I would object that I don't care.

LLMs are magic black boxes that take text as input and return text.

For all we care, from our coder point of view, LLMs are as simple as
```python
mport openai
import os

# Set up the OpenAI API client
openai.api_key = os.environ.get("OPENAI_API_KEY")

def chat_completion(prompt, model="gpt-3.5-turbo", max_tokens=150):
    try:
        # Create the API request
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )

        # Extract and return the generated message
        return response.choices[0].message['content'].strip()

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    user_prompt = "What is the capital of Paris ?"
    result = chat_completion(user_prompt)
    
    if result:
        print("Assistant:", result)
    else:
        print("Failed to get a response.")
```

### Going further

Our goal as coders should be that, from any given scope, all dependencies are magic black boxes with clear specifications.

### Everything is a function

We'll define *Agent* as a blackbox that takes any number of inputs of any type, and return, either nothing, or anything of any type, and potentially have *side effects*.

In other terms, agents can be thought as **functions**

*NOTE: the term **Function** is used in the programmatic sense (i.e.: a Python function), as opposed to the stricter sense it carries in **Functional Programming***

Here's a toy example of an execution flow this approach allows for:
```python
from agentix import Agent

for task in Agent['task_lister'](user_input):
    Agent['task_executor'](task)
```

*NOTE: the why and how of global containers as **agentix.Agent** will be explained further down*

### Agentix's approach

#### Separation of concerns
In web development, it's common to have a conventional directory structure containing:
- Presentation/integration (aka templates)
- Application logic (say, TypeScript files)
- Styling (CSS)

Adopting a similar approach, we can break down our agents into:
- Conversation templates
- Application Logic
- Tools/utilities/dependencies

Because some processed will be common accross agents, we'll further break down *Application Logic* into middlewares.

#### Global containers and magic imports

Taking inspiration from the web framework **Nuxt**, aiming as much as possible at **Low Code**, all components of our agentic stack will be automatically imported and accessible via a set of global containers.

example:
```python
# Inside any file within our arboresence
from agentix import func

@func
def add_ints(a:int, b:int) -> int:
    return a + b
```

without any additionnal code, in any other file
```python
from agentix import Func

print("4 + 3=", Func['add_ints'](4, 3))
```

### Building an agent with Agentix

#### Agentix CLI tool

```bash
agentix create ShellGPT
```

will result in this boilerplate being created

```
📁agents
└─📁ShellGPT
   ├─📁agents
   │  └─📄ShellGPT.py
   ├─📁middlewares
   │  └─📄ShellGPT_loop.py
   ├─📁prompts
   │  └─📄ShellGPT.conv
   ├─📁tests
   │  └─📄test_ShellGPT.py
   └─📁tools
```


TODO: Write this TODO