from agentix import Agent

def test_prompt(): 
    Agent('prompt_test_agent','prompt')
    
    assert 'ok'==Agent['prompt_test_agent']('aa')[1].content

def test_prompt_histo():
    agent_name = 'prompt_test_histo_agent'
    middleware_name = 'prompt_histo'
    Agent(agent_name, middleware_name)
    conv = Agent[agent_name]('Hi')

    assert conv[-1].content == 'Hi'
     
    