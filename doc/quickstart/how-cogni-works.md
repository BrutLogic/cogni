# How Cogni works
*Condensed version*

## Foreword

I'll be feeding the repo for the coming week. As of right now, it's a mess. So I decided to write this markdown that explains briefly all the ideas Cogni is based on.

## Philosophy

A trend in computer science is to be able to implement anything with higher and higher abstractions.

We went from binary code on punch cards, to assembly, to C (not the first language historically, but that's beside the point), to eventually Python, and even further: Frameworks.

What happens is that, as time goes on and technology progress, implementing a given software behavior is done by manipulating higher and higher abstraction, therefore write less and less code.

Cogni aims at providing the highest possible abstractions to implement agents.

Said otherwise, any framework should aim at allowing for implementing absolutely anything by writing only the parts that change.

## Starting point: What IS an agent anyway ?

*Thinking about implementing a framework should start by specifying the behaviors of the highest level abstractions at use time. And ONLY then, think about implementation details*


### Agent: At use time/From the outside

I'll illustrate

```python
# Agents are functions that take any input and return any output
result = Agent['ShellAgent']("what's in the current directory?")
print(result) # Lists directory contents

# Agents can be chained
summary = Agent['ChangeDescriptor'](
    Agent['Gitor']("analyze https://github.com/openai/whisper")
)

# Agents can maintain state
Agent['ChatAgent'].memory['last_topic'] = "AI safety"

# Agents can emit and handle events
@Event.on('user_message') 
def handle_message(event):
    Agent['ChatAgent'](event.data['message'])

# Agents can use tools
@tool
def get_weather(city: str) -> str:
    return weather_api.get(city)

Agent['WeatherBot']("What's the weather in Paris?")
```

