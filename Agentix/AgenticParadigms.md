# Agentic paradigms 
## There is a paradigm

If you're writting code, the language you're using, the way you'll conceive your code, all of that, regardless of you knowing it, will be done under [A Paradigm](https://en.wikipedia.org/wiki/Programming_paradigm).

A paradigm can be viewed as a set of statements
about what conceptual objects to consider, their properties, and in what way they should interact. 

## Agentic has paradigms too

We can postulate that agentic, as code writting, is done under a paradigm (that is yet to be defined).

Agentic's Moving parts the way they're defined, the way they interact. that will also fit into a paradigm. So defining them is usefull

## My best try at defining paradigms

### Monolithic Agent
ChatGPT, (though debatable if an agent as it has no feedback loop) would be a Monolithic Agent.
```
You're an helpful assistant.
# Instructions
{instructions}
# Context
{context}
# Tools
{tools}
``` 
### Swarm
#### Swarm of clone
Very useful for prompting strategy.
Three of thoughts would be an example
#### Swarm of specialists
CrewAI.
A bunch of agents with a role, a context, tools and some kind of shared space to communicate.
#### Tree of specialists
Or **Agents as code**
Agents interact in a fixed way.
##### Functionnal agentic
(what **Agentix** is all about).
> Agents are functions

_______________

Broad intuitions:

A LLM, configured as a chatbot works by being fed user inputs, conversation history, and it's own output until a STOP token is hit.

What's presented to the LLM can be dynamic and evolve according to the LLM outputs.

That's the "LLM as a computer" intuition.

Another approach would be to consider hyper-specialised agents, that would be part of an algorithm. 

I'm not sure where this can lead but a lot of cursor can be identified and some of the responsibility could shift from the LLM to the cognitive architecture.