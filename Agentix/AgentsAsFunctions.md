[Back to README](README.md)
# Agents are functions

Here we'll decribe Agentix's Agents behaviors. What you should consider when **USING** them (as opposed to their implementation details)


Said otherwise, this is a **Black box description** of what Agents are in Agentix.

## Agents, Are, Functions.
From the outside, an **Agent is conceptually a function**. Oh, and also actually **a python function**. 

It ingests inputs. 

It return outputs of given types.

It mutates some states here and there.

It's a Function. 


While this principle is simple and doesn't look like much, it proved unsuspectedly powerful to implement complex control flow over LLM inferences.

**Note:** Agentix's Agents are function in the programmatical sense, not (yet) in a stricter sense.

Here's how "Agents are functions" works **Exemple of control flow with Agentix**
```python
for task in Agent['task_lister'](user_input):
    Agent['task_executor'](task)
```

Here's an actual piece of code I used to implement a long term memory:


```python
for fact in Agent['LTM_fact_extract'](user_input):
    Agent['LTM_fact_store'](
        Agent['LTM_compress_fact'](fact)
        )

context = Agent['LTM_fact_recall'](user_input)
```

(Bare in mind each Agent/function call resulted in one or several conversations, LLM contexts, and arbitrarely long feedback loops.)


It allows for strong algorithmic decoupling, which in turn makes easy to have very specialist agents.

Akin to a function, an agent can itself be an arbitrarly complexe set of agents. Resulting for a given task in many contexts/conversations.

**Note**: One thing I first thought as a tradeoff: my approach is heavy in LLM calls. In reality, it's balanced by the fact it requires overall less tokens generated than other approachs (when done correctly). Also, some Agents can run with `gpt-3.5-turbo`.

_______________



**experimental takeaway of this approach**
* Increase overall performance
* Multi-LLM architecture (some tasks can be handled by _gpt-3.5-turbo_, ) with gains in both speed and cost.


## Agentic Single Responsibility Principle
**Agentic Single Responsibility Principle** states (I should know, I made it up) that an Agent should do one thing.

(You should trust me on this one)

[Back to README](README.md)

